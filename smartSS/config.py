import datetime as dt
import pandas_datareader.data as wb

# now get historic price data
QUANDL_API_KEY = 'suGdyfH4RSYbTE5ExozP'
AV_API_KEY = 'K0U7WUJYXD4OY0TM'

# web_ticker : trading212 ticker
ticker_map = {  'GOOG' : 'GOOGL',
                'IUSA.UK' : 'IUSA',
                'BARC.UK' : 'BARC',
                'GME' : 'GME',
                'ECAR.UK': 'ECAR',
                'CNX1.UK': 'CNX1',
                'JDW.UK' : 'JDW',
                'VUKE.UK':'VUKE',
                'VAPX.UK':'VAPX',
                'MA.US':'MA',
                'INRG.UK':'INRG',
                'HSBA.UK':'HSBA',
                'MSFT.US':'MSFT',
                'BP.UK':'BP'}

old_tickers = { 'V.US':'V',
                'BB.US':'BB',
                'NAKD.US':'NAKD',
                'NOK.US':'NOK'}

startdate = dt.datetime(2019, 3, 1)
enddate = dt.datetime.now()

# dataframe of historic price data
web_df = wb.DataReader([key for key in ticker_map.keys()],
                      'stooq',
                      startdate,
                      enddate,
                      api_key=QUANDL_API_KEY)


# dictionary of current exchange rates
forex = {
        'GBP':1,
        'USD':float(wb.DataReader('USD/GBP','av-forex',api_key=AV_API_KEY).loc['Exchange Rate'].iloc[0]),
        'GBX':0.01
        }
