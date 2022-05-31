from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

num_clusters = 6
km = KMeans(n_clusters=num_clusters)
km.fit(X)
clusters = km.labels_.tolist()

km.labels_

random_state=0

# reduce the features to 2D
pca = PCA(n_components=2, random_state=random_state)
reduced_features = pca.fit_transform(X.toarray())

# reduce the cluster centers to 2D
reduced_cluster_centers = pca.transform(km.cluster_centers_)

#Plot 2D figure
plt.scatter(reduced_features[:,0], reduced_features[:,1], c=km.predict(X),s=35)
plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
plt.savefig('K-means.eps',  dpi=600, format='eps',bbox_inches='tight')
plt.legend()
plt.show()

#visualize each clusters
reduced_features[:,0]
c=km.predict(X)
plt.figure(figsize = (6,4))
plt.scatter(reduced_features[c == 0, 0], reduced_features[c == 0, 1], marker='o',s=45)
plt.scatter(reduced_features[c == 1, 0], reduced_features[c == 1, 1], marker='x',s=45)
plt.scatter(reduced_features[c == 2, 0], reduced_features[c == 2, 1], marker='s',s=45)
plt.scatter(reduced_features[c == 3, 0], reduced_features[c == 3, 1], marker='v',s=45)
plt.scatter(reduced_features[c == 4, 0], reduced_features[c == 4, 1], marker='+',s=30)
plt.scatter(reduced_features[c == 5, 0], reduced_features[c == 5, 1], marker='p',s=45, color='black')
plt.legend(['Cluster 1','Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5', 'Cluster 6'])
#plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=180, c='b',linewidth=2.9)
plt.grid( linestyle='-', linewidth=1)
plt.ylabel('PC2',fontsize=16)
plt.xlabel('PC1',fontsize=16)
plt.xticks(fontsize=12)
plt.grid( linestyle='-', linewidth=1)
plt.yticks(fontsize=12)
plt.savefig('Cluster2.eps', format='eps',dpi=300,bbox_inches='tight')





