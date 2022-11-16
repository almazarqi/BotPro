import pymongo
import pandas as pd
from pymongo import MongoClient

#Connect python to MongoDB
client = pymongo.MongoClient("mongodb+srv://user:<password>@cluster0.zp6kw.mongodb.net/?retryWrites=true&w=majority")
db = client.test

collection = db.data
data = pd.DataFrame(list(collection.find()))
