import matplotlib.pyplot as plt
import datetime as dt

from . import config as cfg
from . import trading212 as hstry
from . import useful_tools as ut

PORTFOLIO_STARTDATE=dt.datetime(2020,4,1)

def plot_historic_data(history_ticker):
    wb_ticker = ut.get_wb_ticker(history_ticker)
    data = cfg.web_df['Close',wb_ticker]
    plt.plot(data.keys(),data.values,c='blue')
    plt.title(history_ticker)
    plt.xticks(rotation=45)
    plt.grid(alpha=0.25)
    plt.show()

def plot_activity_on_history(history_ticker):
    wb_ticker = ut.get_wb_ticker(history_ticker)
    data = cfg.web_df['Close',wb_ticker]
    plt.plot(data.keys(),data.values,alpha=0.5)

    mask = (((hstry.history['Action']=='Market buy') | (hstry.history['Action']=='Limit buy')) &
            (hstry.history['Ticker']==history_ticker))
    times = hstry.history[mask]['Time'].values
    prices = hstry.history[mask]['Price / share'].values
    plt.scatter(times,prices,c='green')

    mask = (((hstry.history['Action']=='Market sell') | (hstry.history['Action']=='Limit sell')) &
            (hstry.history['Ticker']==history_ticker))
    times = hstry.history[mask]['Time'].values
    prices = hstry.history[mask]['Price / share'].values
    plt.scatter(times,prices,c='red')

    plt.title(history_ticker)
    plt.xticks(rotation=45)
    plt.grid(alpha=0.25)
    plt.show()

def plot_portfolio_returns():
    # portfolio start date
    startdate=PORTFOLIO_STARTDATE

    ndays = (dt.datetime.now()-startdate).days
    date_list = [startdate + dt.timedelta(days=x) for x in range(ndays)]
    returns = [ut.portfolio_returns(end_date=date) for date in date_list]
    plt.plot(date_list,returns)
    plt.xticks(rotation=90)
    plt.show()
