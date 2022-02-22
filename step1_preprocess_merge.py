import pandas as pd


def treatComnam(srs):
    ls = srs.split(' ')
    if len(ls) >= 3:
        return ls[0] + ls[1]
    else:
        return ls[0]


comp = pd.read_csv('./step1_compustat.csv')
comp = comp[['datadate', 'tic', 'conm', 'cshtrd', 'prccd', 'prchd', 'prcld', 'prcod']]

comp.dropna(subset=['tic', 'cshtrd', 'prccd', 'prchd', 'prcld', 'prcod'], inplace=True)
comp['datadate'] = pd.to_datetime(comp['datadate'], format='%Y%m%d')
comp['year'] = comp['datadate'].apply(lambda x: int(x.year))
comp['conm'] = comp['conm'].apply(treatComnam)
comp['conm'] = comp['conm'].apply(lambda x: x.lower())

bbg = pd.read_csv('./step1_bbg.csv')
bbg['tic'] = bbg['tic'].apply(lambda x: x.split(' ')[0])
bbg['COMNAM'] = bbg['COMNAM'].apply(treatComnam)
bbg['COMNAM'] = bbg['COMNAM'].apply(lambda x: x.lower())
bbg['isBBG'] = 1

df1 = pd.merge(bbg, comp, how='right', left_on=['year', 'tic'], right_on=['year', 'tic'])

df2 = pd.merge(bbg, comp, how='right', left_on=['year', 'COMNAM'], right_on=['year', 'conm'])
print(df1, df1.info())
print(df2, df2.info())

df1 = df1.loc[df1['isBBG'] == 1, :]
df1 = df1[['tic', 'datadate', 'conm', 'cshtrd', 'prccd', 'prchd', 'prcld', 'prcod']]
print(df1, df1.shape)

df2 = df2.loc[df2['isBBG'] == 1, :]
df2['tic'] = df2['tic_y']
df2 = df2[['tic', 'datadate', 'conm', 'cshtrd', 'prccd', 'prchd', 'prcld', 'prcod']]
print(df2, df2.shape)

df = df1.append(df2)
print(df, df.shape)
df.drop_duplicates(subset=['datadate', 'conm'], keep='first', inplace=True)
df.drop_duplicates(subset=['datadate', 'tic'], keep='first', inplace=True)
print(df, df.shape)
df.to_csv('./out1.csv', index=False)