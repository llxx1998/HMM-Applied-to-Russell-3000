import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('./liq_states.csv').set_index(keys=['date'])
data = data.loc['2004-09-24':, :]

# data_map = data.fillna(0)
# plt.figure(figsize=(20, 11))
# plt.pcolormesh(data_map.T, cmap='GnBu')
# plt.xticks(ticks=list(range(70, data.shape[0], 252)),
#            labels=list(range(2005, 2005 + data.shape[0] // 252)))
# plt.colorbar()
# plt.title('Ribbon Plot for Russell 3000 Constituents Liquidity Status',
#           loc='center', fontdict={'fontsize': 24}, y=1)
# plt.savefig('./summary_results/summary_ribbon_chart.png')


count0 = (data == 0).sum(axis=1)
count1 = (data == 1).sum(axis=1)
count2 = (data == 2).sum(axis=1)

count_data = pd.DataFrame({'State0': count0,
                           'State1': count1,
                           'State2': count2, })

count_data['Comp#'] = count_data.sum(axis=1)
count_data['AverageState'] = (1 * count_data['State1'] + 2 * count_data['State2']) / count_data['Comp#']
count_data['S0Percent'] = count_data['State0'] / count_data['Comp#']
count_data['S1Percent'] = count_data['State1'] / count_data['Comp#']
count_data['S2Percent'] = count_data['State2'] / count_data['Comp#']

plt.figure(figsize=(20, 11))
plt.plot(count_data['S0Percent'], color='g', linestyle='-', alpha=0.3, label='State0')
plt.plot(count_data['S1Percent'], color='b', linestyle='-', alpha=0.3, label='State1')
plt.plot(count_data['S2Percent'], color='r', linestyle='-', label='State2')
plt.legend(loc='upper right')
plt.ylabel('State Percentage')
plt.title('Each State\'s Percentage for Russell 3000 Constituents', fontdict={'fontsize': 24})
plt.xticks(ticks=list(range(70, data.shape[0], 252)),
           labels=list(range(2005, 2005 + data.shape[0] // 252)))
plt.savefig('./summary_results/summary_states_percentage.png')

plt.figure(figsize=(20, 11))
plt.plot(count_data['AverageState'], linestyle='-', label='Average State')
plt.ylabel('Average State')
plt.title('Average State for Russell 3000 Constituents', fontdict={'fontsize': 24})
plt.xticks(ticks=list(range(70, data.shape[0], 252)),
           labels=list(range(2005, 2005 + data.shape[0] // 252)))
plt.savefig('./summary_results/summary_average_state.png')

plt.figure(figsize=(20, 11))
plt.pcolormesh(count_data[['AverageState']].T, cmap='GnBu')
plt.xticks(ticks=list(range(70, data.shape[0], 252)),
           labels=list(range(2005, 2005 + data.shape[0] // 252)))
plt.colorbar()
plt.title('Ribbon Plot for Russell 3000 Constituents Average Liquidity Status',
          loc='center', fontdict={'fontsize': 24}, y=1)
plt.savefig('./summary_results/summary_ribbon_chart_avg.png')


print(count_data.head())
count_data.to_csv('./summary_results/summary_state_counts.csv', index=True)
