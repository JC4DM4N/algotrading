import pandas as pd
import numpy as np
import pandas_datareader.data as wb
import datetime as dt

from . import config as cfg
from . import trading212 as hstry

def get_history_ticker(wb_ticker):
    return cfg.ticker_map[wb_ticker]

def get_wb_ticker(history_ticker):
    return [ticker for ticker in cfg.ticker_map.keys() if cfg.ticker_map[ticker]==history_ticker][0]

def str_to_datetime(times):
    return [dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') for time in times]

def get_nearest_candle(history_ticker,action_time):
    wb_ticker = get_wb_ticker(history_ticker)
    data = cfg.web_df['Close',wb_ticker]
    dates = cfg.web_df['Close'][wb_ticker].keys()
    dates = dates[~np.isnan(data.values)]
    idx = (np.abs(dates-action_time).total_seconds()).argmin()
    return [data[idx], cfg.web_df['Close'][wb_ticker].iloc[idx]]

def get_asset_current(history_ticker):
    asset_buys = hstry.buys[hstry.buys['Ticker']==history_ticker]
    asset_sells = hstry.sells[hstry.sells['Ticker']==history_ticker]
    asset_total = np.sum(asset_buys['No. of shares']) - np.sum(asset_sells['No. of shares'])
    current_price = get_nearest_candle(history_ticker,dt.datetime.now())[1]
    asset_value = asset_total*current_price
    currency = hstry.buys[hstry.buys['Ticker']==history_ticker]['Currency (Price / share)'].values[0]
    asset = {'Ticker':history_ticker,
             'Holding':asset_total,
             'Value':asset_value,
             'Price':current_price,
             'Currency':currency}
    return asset

def get_portfolio_value():
    total_value = 0
    for ticker in cfg.ticker_map.values():
        asset = get_asset_current(ticker)
        total_value += asset['Value']*cfg.forex[asset['Currency']]
    return total_value

def get_asset_returns_since_buy(history_ticker,ibuy):
    asset = get_asset_current(history_ticker)
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
        returns += total_volume*get_asset_current(history_ticker)['Price']*cfg.forex[asset['Currency']]
    return returns

def get_asset_returns_total(history_ticker):
    asset = get_asset_current(history_ticker)
    asset_buysells = hstry.buysells[hstry.buysells['Ticker']==history_ticker]

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
        returns += total_volume*get_asset_current(history_ticker)['Price']*cfg.forex[asset['Currency']]
    return returns
