import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM
import math


def ModelHMM(df: pd.DataFrame):
    try:
        model = GaussianHMM(n_components=3, covariance_type='full', n_iter=1000)
        model.fit(df[['INVL']])
        # get the corresponding relationship between state and its observable mean
        trx = np.argsort(model.means_, axis=0)
        # get state number
        prdt = model.predict(df[['INVL']])
        # get SORTED state number, higher state represents higher observable level
        for i in range(len(prdt)):
            prdt[i] = trx[prdt[i]]
        return prdt
    except Exception:
        print('error occur in HMM')
        return None


data = pd.read_csv('./out3.csv')
data.loc[data['INVL'] == 'nan', :] = None
data = data.dropna(how='any')
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

data['INVL'] = data['INVL'].apply(lambda x: math.log(x))

data = data[data['INVL'] <= 1]
comp = data['tic'].unique()

states = None

for i, tic in enumerate(comp):
    if i % 100 == 0:
        print(i)
    temp = data[data['tic'] == tic].sort_values(by=['date']).set_index(keys=['date'])
    result = ModelHMM(temp)
    if result is not None:
        temp[tic] = result
        temp[tic] = temp[tic].astype(int)
        temp = temp[[tic]]
        if states is None:
            states = temp
        else:
            states = pd.merge(states, temp, how='outer', left_index=True, right_index=True)

states.to_csv('./liq_states.csv', index=True)



