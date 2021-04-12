import sys, os
import pandas as pd

#module root directory
rdir = os.path.join(os.path.dirname(__file__),'..')

# historical trading212 data
history = pd.read_csv(os.path.join(rdir,'data/historical.csv'))

buys = history[(history['Action']=='Market buy') | (history['Action']=='Limit buy')].copy()
sells = history[(history['Action']=='Market sell') | (history['Action']=='Limit sell')].copy()
buysells = history[((history['Action']=='Market buy') | (history['Action']=='Limit buy') |
                     (history['Action']=='Market sell') | (history['Action']=='Limit sell'))].copy()
