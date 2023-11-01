from pymongo import MongoClient

# MongoDB configuration
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]

# Define the source and target collections
source_collection = db["ASes_statics"]

# Aggregate the abuse_rate per ASN_Number
pipeline = [
    {
        "$project": {
            "ASN_Number": 1,
            "Infected_Prefix": 1,
            "Prefix_Count": 1
        }
    },
    {
        "$addFields": {
            "abuse_rate": {
                "$multiply": [
                    {
                        "$divide": ["$Infected_Prefix", "$Prefix_Count"]
                    },
                    100
                ]
            }
        }
    }
]

abuse_rates = list(source_collection.aggregate(pipeline))

# Update the ASes_statics collection with the abuse_rate data
for entry in abuse_rates:
    asn_number = entry["ASN_Number"]
    abuse_rate = entry["abuse_rate"]
    
    source_collection.update_many(
        {"ASN_Number": asn_number},
        {"$set": {"Abuse_Rate": abuse_rate}}
    )

# Confirm the update
updated_entries = source_collection.find({}, {"_id": 0, "ASN_Number": 1, "Abuse_Rate": 1})
for entry in updated_entries:
    print(entry)