import pika
import json
import os
from pymongo import MongoClient

# Set up MongoDB client
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27018")
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["data2"]

# Set up RabbitMQ connection
rabbitmq_uri = os.environ.get("RABBITMQ_URI", "amqp://localhost:5672/")
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_uri))
channel = connection.channel()

# Declare the message queue for Entropy
entropy_queue = "entropy_queue"
channel.queue_declare(queue=entropy_queue)

# Retrieve source IP addresses and associated ports
source_ips = collection.aggregate([
    {
        "$group": {
            "_id": "$source_ip_address",
            "ports": {"$push": "$target_port"}
        }
    }
])

# Publish IP addresses and ports to the Entropy message queue in RabbitMQ
for ip in source_ips:
    message = {
        "ip": ip["_id"],
        "ports": ip["ports"]
    }

    # Publish the message to the Entropy message queue in RabbitMQ
    channel.basic_publish(
        exchange="",
        routing_key=entropy_queue,
        body=json.dumps(message)
    )

    print(f"Published IP: {ip['_id']} | Ports: {ip['ports']}")

# Close the RabbitMQ connection
connection.close()
