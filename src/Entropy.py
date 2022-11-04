import transform as transform
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
from math import log2
import matplotlib.pyplot as plt

g_sum = df.groupby('source_ip_address')['target_port'].transform('sum')
values = df['target_port']/g_sum
df['Entropy'] = -(values*np.log2(values))

df1 = df.groupby('source_ip_address',as_index=False,sort=False)['Entropy'].sum()

x = df1['Entropy'].values
normalized = (x-min(x))/(max(x)-min(x))
df1['Normalised_Entropy'] = normalized

df = df.sort_values(by=['Entropy'], ascending=True)




plt.figure(figsize=[14,7])
plt.plot(df['Entropy'], df['count'],drawstyle='steps-pre')
#plt.title('title name',fontsize=26)
plt.xlabel('Normalized Entropy',fontsize=26)
plt.xticks(fontsize=24)
plt.yticks(fontsize=24)

plt.ylabel('Port scans per IP address',fontsize=26)
plt.grid(True)
plt.savefig('Number of unique ports as per Entropy.eps', format='eps',dpi=300,bbox_inches='tight')


plt.show()
