from pymongo import MongoClient
import pandas as pd
import math

# MongoDB configuration
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["test22"]

# Define the aggregation pipeline
pipeline = [
    {
        "$group": {
            "_id": "$source_ip_address",
            "ASN_Number": {"$first": "$ASN_Number"},
            "Spamhaus": {"$first": "$Spamhaus"},
            "Spamhaus_XBL": {"$first": "$Spamhaus_XBL"},
            "Barracuda": {"$first": "$Barracuda"},
            "SORBS": {"$first": "$SORBS"},
            "CBL": {"$first": "$CBL"},
        }
    }
]

# Execute the aggregation pipeline
result = list(collection.aggregate(pipeline))

# Create a DataFrame from the aggregation result
df = pd.DataFrame(result)

# Add Blacklist_detection column based on conditions
df["Blacklist_detection"] = df[["Spamhaus", "Spamhaus_XBL", "Barracuda", "SORBS", "CBL"]].any(axis=1).astype(int)

# Group by 'ASN_Number' and calculate the number of unique 'source_ip_address'
unique_source_ips_per_asn = df.groupby('ASN_Number')['_id'].nunique().reset_index()

# Group by 'ASN_Number' and sum 'Blacklist_detection'
sum_blacklist_detection_per_asn = df.groupby('ASN_Number')['Blacklist_detection'].sum().reset_index()

# Merge the two DataFrames on 'ASN_Number' column
merged_df = pd.merge(unique_source_ips_per_asn, sum_blacklist_detection_per_asn, on='ASN_Number', how='outer')

# Rename columns for clarity
merged_df.rename(columns={'_id': 'Unique_Source_IPs', 'Blacklist_detection': 'Sum_Blacklist_Detection'}, inplace=True)

# Calculate CV for each row in the DataFrame
cv = []
for index, row in merged_df.iterrows():
    data = [row['Unique_Source_IPs'], row['Sum_Blacklist_Detection']]
    mean = sum(data) / 2
    SS = sum([(x - mean)**2 for x in data])  # Sum of Squares
    SD = math.sqrt(SS / 2)                   # Standard Deviation
    cv.append(SD / mean)                     # Coefficient Of Variation

# Add CV column to DataFrame
merged_df['CV'] = cv

# Store the result in a new collection 'ASes_statics'
result_collection = db["ASes_statics"]
result_collection.delete_many({})  # Clear existing data in the collection
result_collection.insert_many(merged_df.to_dict('records'))
