from pymongo import MongoClient
import json
import os
import pika


# Set up MongoDB client
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27018")
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["data2"]

# Set up RabbitMQ connection
rabbitmq_uri = os.environ.get("RABBITMQ_URI", "amqp://localhost:5672/")
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_uri))
channel = connection.channel()

# Retrieve distinct source IP addresses from the collection
source_ips_cursor = collection.distinct("source_ip_address")
source_ips = list(source_ips_cursor)

# Publish IP addresses for AS queries to the AS_query_queue in RabbitMQ
for ip in source_ips:
    message = {
        "ip": ip
    }

    # Publish the message to the AS_query_queue in RabbitMQ
    channel.basic_publish(
        exchange="",
        routing_key="AS_query_queue",
        body=json.dumps(message)
    )

    print(f"Published IP: {ip}")

# Close the RabbitMQ connection
connection.close()
