from . import config
from . import trading212
from . import useful_tools
from . import plot

trading212.history['Time'] = useful_tools.str_to_datetime(trading212.history['Time'])
