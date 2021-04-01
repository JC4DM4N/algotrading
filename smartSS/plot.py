import matplotlib.pyplot as plt

from . import config as cfg
from . import trading212 as hstry
from . import useful_tools as ut

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
    plt.plot(data.keys(),data.values,alpha=0.5,c='blue')

    mask = (((hstry.history['Action']=='Market buy') | (hstry.history['Action']=='Limit buy')) &
            (hstry.history['Ticker']==history_ticker))
    times = hstry.history[mask]['Time'].values
    times = ut.str_to_datetime(times)
    prices = hstry.history[mask]['Price / share'].values
    plt.scatter(times,prices,c='green')

    mask = (((hstry.history['Action']=='Market sell') | (hstry.history['Action']=='Limit sell')) &
            (hstry.history['Ticker']==history_ticker))
    times = hstry.history[mask]['Time'].values
    times = ut.str_to_datetime(times)
    prices = hstry.history[mask]['Price / share'].values
    plt.scatter(times,prices,c='red')

    plt.title(history_ticker)
    plt.xticks(rotation=45)
    plt.grid(alpha=0.25)
    plt.show()
