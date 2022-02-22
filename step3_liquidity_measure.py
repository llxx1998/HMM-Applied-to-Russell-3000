import pandas as pd
import numpy as np


def CxCal(srs: pd.Series):
    """
    This function uses volatility, average trading volume, price
    to generate the price invariant measure of liquidity
    :param srs:
    :param sig: float, volatility (sigma)
    :param avg_Vol: float, volume
    :param p: float, average price
    :return: float, price invariant measure
    """
    sig, avg_Vol, p = srs['Vohlc'], srs['avgVolume'], srs['avgprice']
    # the following variables are parameters for calculating liquidity measure.
    XoverV = pow(10, -5.71)
    Vol_std = 0.02
    const1 = 8.21e-4
    const2 = 2.5e-4
    expt1 = - 1 / 3
    expt2 = 1 / 3
    W_std = 0.02 * 40 * 1000000     # W* in the paper, a scaler for W
    XV_std = 0.01
    try:
        value = (sig / Vol_std) * (const1 * pow(sig * p * avg_Vol / W_std, expt1) +
                              const2 * pow(sig * p * avg_Vol / W_std, expt2) * XoverV / XV_std)
        return value
    except Exception:
        return -1


data = pd.read_csv('./out2.csv')
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
data = data.sort_values(by=['date'], ascending=True)

result = None
comp_list = data['tic'].unique()
for comp in comp_list:
    try:
        temp = data.loc[data['tic'] == comp, :]
        if temp.shape[0] >= 20:
            temp.loc[:, 'avgprice'] = temp['prccd'].rolling(window=20).mean()
            temp.loc[:, 'avgVolume'] = temp['cshtrd'].rolling(window=20).mean()
            temp = temp.dropna()
        else:
            temp['avgprice'] = temp['prccd']
            temp['avgVolume'] = temp['cshtrd']
        temp.loc[:, 'INVL'] = temp.apply(CxCal, axis=1)
        temp = temp[temp.INVL != -1]
        temp = temp[['date', 'tic', 'INVL']]
        if result is None:
            result = temp
        else:
            result = result.append(temp)
    except Exception:
        temp = data.loc[data['tic'] == comp, :]
        # temp.to_csv('./error/'+str(comp)+'.csv')
        print('error occur')
        continue
result.to_csv('./out3.csv', index=False)