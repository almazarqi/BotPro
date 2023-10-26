import socket
import os
from pymongo import MongoClient
import pika
import json

def check_blacklist(ip):
    blacklists = [
        ("cbl.abuseat.org", ""),
        ("dnsbl.sorbs.net", ""),
        ("bl.spamcop.net", ""),
        ("zen.spamhaus.org", ""),
        ("b.barracudacentral.org", "")
    ]

    results = []
    for blacklist, _ in blacklists:
        lookup_address = ip + "." + blacklist
        try:
            socket.gethostbyname_ex(lookup_address)
            results.append({"blacklist": blacklist, "status": 1})
        except socket.gaierror:
            results.append({"blacklist": blacklist, "status": 0})

    return results

def process_blacklist_message(channel, method, properties, body):
    message = json.loads(body)
    ip_address = message.get("ip")

    # Set up MongoDB client
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27018")
    client = MongoClient(mongo_uri)
    db = client["botnet"]
    
    # Create a new collection called "Blacklists"
    blacklists_collection = db["Blacklists"]

    # Check blacklisting status for the IP
    blacklist_results = check_blacklist(ip_address)

    # Create a document for the IP in the "Blacklists" collection
    document = {
        "ip_address": ip_address,
        "blacklist_status": blacklist_results
    }

    # Insert the document into the "Blacklists" collection
    blacklists_collection.insert_one(document)

    print(f"Blacklisting status for IP {ip_address} stored in the 'Blacklists' collection.")

# Set up RabbitMQ connection
rabbitmq_uri = os.environ.get("RABBITMQ_URI", "amqp://localhost:5672/")
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_uri))
channel = connection.channel()

# Declare the message queue for Blacklists queries
blacklists_query_queue = "Blacklists_query_queue"
channel.queue_declare(queue=blacklists_query_queue)

# Set up a consumer to process incoming messages from the Blacklists_query_queue
channel.basic_consume(
    queue=blacklists_query_queue,
    on_message_callback=process_blacklist_message,
    auto_ack=True
)

print("Waiting for messages. To exit, press CTRL+C")
channel.start_consuming()
