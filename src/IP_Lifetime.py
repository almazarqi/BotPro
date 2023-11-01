from pymongo import MongoClient
import pandas as pd

# MongoDB configuration
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["full_graph"]

# Retrieve data from MongoDB
pipeline = [
    {
        "$project": {
            "_id": 0,
            "source_ip_address": 1,
            "first_seen": 1,
            "last_seen": 1,
        }
    }
]

cursor = collection.aggregate(pipeline)
data = list(cursor)

# Convert the data to a DataFrame
data = pd.DataFrame(data)

# Convert 'first_seen' and 'last_seen' to datetime objects
data["first_seen"] = pd.to_datetime(data["first_seen"], infer_datetime_format=False)
data["last_seen"] = pd.to_datetime(data["last_seen"], infer_datetime_format=False)

# Calculate the duration (lifetime) as seconds (integer)
data["Duration"] = (data["last_seen"] - data["first_seen"]).dt.total_seconds().astype(int)

# Include the 'ip_address' field in the DataFrame
data = data[["source_ip_address","first_seen","last_seen" ,"Duration"]]

# Create a new collection 'lifetime' and insert the data
lifetime_collection = db["lifetime"]
lifetime_collection.insert_many(data.to_dict(orient="records"))

# Close the MongoDB connection
client.close()
