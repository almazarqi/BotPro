import os
import requests
import time
from pymongo import MongoClient
import pika
import json

def process_shadow_message(channel, method, properties, body):
    message = json.loads(body)
    asn_number = message.get("ASN")

    # Set up MongoDB client
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27018")
    client = MongoClient(mongo_uri)
    db = client["botnet"]
    ases_collection = db["ASes"]
    shadow_collection = db["shadow"]

    # Make API request to Shadowserver to get information about prefixes
    url = "https://api.shadowserver.org/net/asn?prefix=" + str(asn_number)
    response = requests.get(url=url)
    time.sleep(1.5)  # Add a delay to avoid rate limiting from the API
    response = response.json()

    # Count the number of prefixes
    prefix_count = len(response)

    # Create a list to store the prefixes
    prefixes = []
    for item in response:
        prefixes.append(item)

    # Create a document to store the prefix count and prefixes in the "shadow" collection
    document = {
        "ASN_Number": asn_number,
        "Prefix_Count": prefix_count,
        "Prefixes": prefixes
    }

    # Insert the document into the "shadow" collection
    shadow_collection.insert_one(document)

    print(f"Prefix count and prefixes for ASN {asn_number} stored in the 'shadow' collection.")

# Set up RabbitMQ connection
rabbitmq_uri = os.environ.get("RABBITMQ_URI", "amqp://localhost:5672/")
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_uri))
channel = connection.channel()

# Declare the message queue for Shadow Server queries
shadow_server_query_queue = "Shadow_Server_query_queue"
channel.queue_declare(queue=shadow_server_query_queue)

# Set up a consumer to process incoming messages from the Shadow_Server_query_queue
channel.basic_consume(
    queue=shadow_server_query_queue,
    on_message_callback=process_shadow_message,
    auto_ack=True
)

print("Waiting for messages. To exit, press CTRL+C")
channel.start_consuming()
