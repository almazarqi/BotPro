import pandas as pd
import re
import string
import sklearn
from sklearn.metrics import adjusted_rand_score
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_csv('Paylodas.csv')
data  = data.drop_duplicates(subset='event_id', keep="first")


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
