import pandas as pd
import re
import string
from sklearn.metrics import adjusted_rand_score
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

commands = data.payload.tolist()
len(commands)
commands[0]
tokenized_doc = data.payload.apply(lambda x: x.split())
tokenized_doc[0]
import spacy
nlp = spacy.load('en_core_web_sm')

prepocessedDocs_1 = []
for t in commands:
  regex_sub = re.sub(r"(?P<url>https?:/\\/[^\s]+)",'URL', t)
  regex_sub = re.sub(r"(?P<url>https?:/\/[^\s]+)",'URL', regex_sub)
  regex_sub = re.sub(r"(?P<url>https?://[^\s]+)",'URL', regex_sub)    
  prepocessedDocs_1.append(regex_sub.strip())
  
 from sklearn.feature_extraction.text import TfidfVectorizer
# tfidf vectorizer of scikit learn
vectorizer = TfidfVectorizer(max_features=None, use_idf = True, ngram_range=(1,3))
prepocessedDocs_1 = prepocessedDocs_2[:]
X = vectorizer.fit_transform(prepocessedDocs_1)
print(X.shape) # check shape of the document-term matrix
terms = vectorizer.get_feature_names()

num_clusters = 6
km = KMeans(n_clusters=num_clusters)
# , init='k-means++', max_iter=100, n_init=1

km.fit(X)
clusters = km.labels_.tolist()

# reduce the features to 2D
pca = PCA(n_components=2, random_state=random_state)
reduced_features = pca.fit_transform(X.toarray())

# reduce the cluster centers to 2D
reduced_cluster_centers = pca.transform(km.cluster_centers_)

plt.scatter(reduced_features[:,0], reduced_features[:,1], c=km.predict(X),s=35)
plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
plt.savefig('K-means.eps',  dpi=600, format='eps',bbox_inches='tight')
plt.legend()
plt.show()
