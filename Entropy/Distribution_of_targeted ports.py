# Import required libraries
import transform as transform
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing

#read csv file and sort ports
df = pd.read_csv("Dataset.csv")
df = df.sort_values(by=['target_port'], ascending=True)


from math import log2
g_sum = df.groupby('source_ip_address')['target_port'].transform('sum')
values = df['target_port']/g_sum
df['Entropy'] = -(values*np.log2(values))

df1 = df.groupby('source_ip_address',as_index=False,sort=False)['Entropy'].sum()

x = df1['Entropy'].values
normalized = (x-min(x))/(max(x)-min(x))
df1['Normalised_Entropy'] = normalized

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pyplot

df2= pd.read_csv('Dataset_Scan.csv')
df2 = df2.drop_duplicates(subset=['source_ip_address'], keep='first')
#df2 = df2[df2.Normalised_Entropy > 0]

# generate figure showing the distribution of destination ports scans from
unique IP addresses 
probs = df2['Normalised_Entropy']
plt.figure(figsize=[14,7],)
plt.hist(probs, histtype='bar',
         bins = 10,
         #stacked=True, 
         #edgecolor="blue",
         #color="skyblue" ,
         #rwidth=0.99)
        )
plt.title('')
plt.xlabel('Normalised Entropy',fontsize=26)
plt.ylabel('Unique IP addresses',fontsize=26)
plt.xticks(fontsize=24)
plt.grid( linestyle='-', linewidth=1)
plt.yticks(fontsize=24)
plt.yscale('log')
plt.show()
