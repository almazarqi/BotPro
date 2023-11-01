# ASes lifetime

from pymongo import MongoClient
import pandas as pd

# MongoDB configuration
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]

# Define the source and target collections
source_collection = db["graph"]
target_collection = db["ASes_statics"]

# Aggregate the data per ASN_Number
pipeline = [
    {
        "$group": {
            "_id": "$ASN_Number",
            "first_seen": {"$min": "$first_seen"},
            "last_seen": {"$max": "$last_seen"}
        }
    },
    {
        "$project": {
            "_id": 0,
            "ASN_Number": "$_id",
            "first_seen": 1,
            "last_seen": 1
        }
    }
]

result = list(source_collection.aggregate(pipeline))

# Create a DataFrame from the aggregation result
data = pd.DataFrame(result)

# Convert date columns to datetime if needed
data["first_seen"] = pd.to_datetime(data["first_seen"])
data["last_seen"] = pd.to_datetime(data["last_seen"])

# Calculate the 'active_days' column
data["active_days"] = (data["last_seen"] - data["first_seen"]).dt.days

# Update the ASes_statics collection with the active_days data
for index, row in data.iterrows():
    asn_number = row["ASN_Number"]
    active_days = row["active_days"]
    
    target_collection.update_many(
        {"ASN_Number": asn_number},
        {"$set": {"Active_Days": active_days}}
    )

# Confirm the update
updated_entries = target_collection.find({}, {"_id": 0, "ASN_Number": 1, "Active_Days": 1})
for entry in updated_entries:
    print(entry)