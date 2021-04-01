import pandas as pd
import os

data_dir = '/Users/s1863104/Documents/algotrading'

# historical trading212 data
history = pd.read_csv(os.path.join(data_dir,'data/historical.csv'))

buys = history[(history['Action']=='Market buy') | (history['Action']=='Limit buy')]
sells = history[(history['Action']=='Market sell') | (history['Action']=='Limit sell')]
buysells = history[((history['Action']=='Market buy') | (history['Action']=='Limit buy') |
                     (history['Action']=='Market sell') | (history['Action']=='Limit sell'))]
