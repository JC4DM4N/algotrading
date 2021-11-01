import pandas as pd
import numpy as np
import pandas_datareader.data as wb
import datetime as dt

from . import config as cfg
from . import trading212 as hstry

PORTFOLIO_STARTDATE=dt.datetime(2020,4,1)

def get_history_ticker(wb_ticker):
    return cfg.ticker_map[wb_ticker]

def get_wb_ticker(history_ticker):
    return [ticker for ticker in cfg.ticker_map.keys() if cfg.ticker_map[ticker]==history_ticker][0]

def str_to_datetime(times):
    return [dt.datetime.strptime(time, '%d/%m/%Y %H:%M') for time in times]

def get_nearest_candle(history_ticker,action_time):

    wb_ticker = get_wb_ticker(history_ticker)
    prices = cfg.web_df['Close',wb_ticker]
    dates = cfg.web_df['Close'][wb_ticker].keys()
    dates = dates[~np.isnan(prices.values)]
    prices = prices[~np.isnan(prices.values)]
    idx = (np.abs(dates-action_time).total_seconds()).argmin()
    return (dates[idx],prices[idx])

def get_asset_info(history_ticker,date=dt.datetime.now()):
    asset_buys = hstry.buys[(hstry.buys['Ticker']==history_ticker) & (hstry.buys['Time']<=date)]
    asset_sells = hstry.sells[(hstry.sells['Ticker']==history_ticker) & (hstry.sells['Time']<=date)]
    asset_total = np.sum(asset_buys['No. of shares']) - np.sum(asset_sells['No. of shares'])
    nearest_candle = get_nearest_candle(history_ticker,date)
    asset_value = asset_total*nearest_candle[1]
    currency = hstry.buys[hstry.buys['Ticker']==history_ticker]['Currency (Price / share)'].values[0]
    asset = {'Ticker':history_ticker,
             'Date':nearest_candle[0],
             'Holding':asset_total,
             'Value':asset_value,
             'Price':nearest_candle[1],
             'Currency':currency}
    return asset

def get_portfolio_value():
    total_value = 0
    for ticker in cfg.ticker_map.values():
        asset = get_asset_info(ticker)
        total_value += asset['Value']*cfg.forex[asset['Currency']]
    return total_value

def get_portfolio_value_on_date(end_date=dt.datetime.now()):
    total_value = 0
    for ticker in cfg.ticker_map.values():
        asset = get_asset_info(ticker)
        total_value += asset['Value']*cfg.forex[asset['Currency']]
    return total_value

def get_asset_returns_since_buy(history_ticker,ibuy):
    asset = get_asset_info(history_ticker)
    asset_buys = hstry.buys[hstry.buys['Ticker']==history_ticker]
    asset_sells = hstry.sells[hstry.sells['Ticker']==history_ticker]
    init_buy_price = asset_buys['Price / share'].iloc[ibuy]*cfg.forex[asset['Currency']]
    init_buy_volume = asset_buys['No. of shares'].iloc[ibuy]
    init_buy_date = asset_buys['Time'].iloc[ibuy]
    total_volume = init_buy_volume

    returns = -init_buy_price*init_buy_volume
    if len(asset_sells)>0:
        for i in range(len(asset_sells)):
            # only want to use sales after the initial buy date
            if asset_sells.iloc[i]['Time'] > init_buy_date:
                while total_volume>0:
                    sell_price = asset_sells.iloc[i]['Price / share']*cfg.forex[asset['Currency']]
                    sell_volume = asset_sells.iloc[i]['No. of shares']

                    if total_volume>=sell_volume:
                        returns += sell_volume*sell_price
                        total_volume -= sell_volume
                    else:
                        # only want to use the amount we have left from initial buy to calc this
                        sell_volume = total_volume
                        returns += sell_volume*sell_price
                        total_volume -= sell_volume

    # if still some left over, calc profit on remaining assets based on current value.
    if total_volume>0:
        returns += total_volume*get_asset_info(history_ticker)['Price']*cfg.forex[asset['Currency']]
    return returns

def get_asset_returns_total(history_ticker):
    asset = get_asset_info(history_ticker)
    asset_buysells = hstry.buysells[hstry.buysells['Ticker']==history_ticker]

    # get price and volume at initial purchase
    init_buy_price = asset_buysells['Price / share'].iloc[0]*cfg.forex[asset['Currency']]
    init_buy_volume = asset_buysells['No. of shares'].iloc[0]
    init_buy_date = asset_buysells['Time'].iloc[0]
    total_volume = init_buy_volume

    returns = -init_buy_price*init_buy_volume
    for i in range(1,len(asset_buysells)):
        if 'buy' in asset_buysells['Action'].iloc[i]:
            buy_price = asset_buysells.iloc[i]['Price / share']*cfg.forex[asset['Currency']]
            buy_volume = asset_buysells.iloc[i]['No. of shares']
            returns -= buy_volume*buy_price
            total_volume += buy_volume

        elif 'sell' in asset_buysells['Action'].iloc[i]:
            sell_price = asset_buysells.iloc[i]['Price / share']*cfg.forex[asset['Currency']]
            sell_volume = asset_buysells.iloc[i]['No. of shares']
            if total_volume>=sell_volume:
                returns += sell_volume*sell_price
                total_volume -= sell_volume
            else:
                # only want to use the amount we have left from initial buy to calc this
                sell_volume = total_volume
                returns += sell_volume*sell_price
                total_volume -= sell_volume

    # if still some left over, calc profit on remaining assets based on current value.
    if total_volume>0:
        returns += total_volume*get_asset_info(history_ticker)['Price']*cfg.forex[asset['Currency']]
    return returns

def asset_returns(ticker,start_date=PORTFOLIO_STARTDATE,end_date=dt.datetime.now()):
    #get asset value in portfolio at start date and current date
    value_start = get_asset_info(ticker,start_date)['Value']
    value_start*=cfg.forex[get_asset_info(ticker,start_date)['Currency']]
    value_now = get_asset_info(ticker,end_date)['Value']
    value_now*=cfg.forex[get_asset_info(ticker,end_date)['Currency']]

    # sum ticker buys and sells since date
    buys = hstry.buys.loc[(hstry.buys['Ticker']==ticker) &
                           (hstry.buys['Time']>start_date) &
                           (hstry.buys['Time']<=end_date)]
    sells = hstry.sells.loc[(hstry.sells['Ticker']==ticker) &
                             (hstry.sells['Time']>start_date) &
                             (hstry.sells['Time']<=end_date)]
    # return net profit/loss since date
    return value_now-value_start-buys['Total (GBP)'].sum()+sells['Total (GBP)'].sum()

def portfolio_returns(start_date=PORTFOLIO_STARTDATE,end_date=dt.datetime.now()):
    # sum returns for each asset between dates
    returns=0
    for ticker in cfg.ticker_map.values():
        returns+=asset_returns(ticker,start_date,end_date)
    return returns

def get_portolio_returns_total():
    #return get_portfolio_value() - hstry.buys['Total (GBP)'].sum() + hstry.sells['Total (GBP)'].sum()
    return sum([get_asset_returns_total(ticker) for ticker in cfg.ticker_map.values()])
