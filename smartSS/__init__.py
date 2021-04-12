from . import config
from . import trading212
from . import useful_tools
from . import plot

# convert trading212 data to datetime
trading212.history.loc[:,'Time'] = useful_tools.str_to_datetime(trading212.history['Time'].values).copy()
trading212.buys.loc[:,'Time'] = useful_tools.str_to_datetime(trading212.buys['Time'].values).copy()
trading212.sells.loc[:,'Time'] = useful_tools.str_to_datetime(trading212.sells['Time'].values).copy()
trading212.buysells.loc[:,'Time'] = useful_tools.str_to_datetime(trading212.buysells['Time'].values).copy()
