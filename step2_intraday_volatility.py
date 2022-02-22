import math
import pandas as pd
import numpy as np

df = pd.read_csv('./out1.csv')
# df.dropna(how='any', inplace=True)

df['date'] = pd.to_datetime(df['datadate'], format='%Y-%m-%d')
df = df[df['date'] >= '2004-08-27']
df = df[['date', 'tic', 'cshtrd', 'prccd', 'prchd', 'prcld', 'prcod']]
print('read in data for russell 3000', df.shape)

k = 50
comp_cnt = df[['date', 'tic']].groupby(['date']).count()
date_list = comp_cnt[comp_cnt['tic'] < k].index.tolist()
df = df[~df["date"].isin(date_list)]
(df.groupby(['date']).count()).to_csv('./data_number.csv')

df = df[df['prchd'] > 0]
df = df[df['prcld'] > 0]
df = df[df['prccd'] > 0]
df = df[df['prcod'] > 0]
print('begin calculation')
r1 = np.array(df['prchd'] / df['prcld'])
r2 = np.array(df['prccd'] / df['prcod'])
df['Vohlc'] = np.power(0.5 * np.power(np.log(r1), 2) - (2*math.log(2) - 1) * np.power(np.log(r2), 2), 0.5)
df = df[['tic', 'date', 'Vohlc', 'prccd', 'cshtrd']]
print('finish calculation', df.shape)
# data to use in our HMM model
df.to_csv('./out2.csv', index=False)



