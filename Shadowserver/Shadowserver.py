from pymongo import MongoClient
import json
import os
import pika


# Set up MongoDB client
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27018")
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["ASes"]

# Set up RabbitMQ connection
rabbitmq_uri = os.environ.get("RABBITMQ_URI", "amqp://localhost:5672/")
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_uri))
channel = connection.channel()

# Retrieve distinct source IP addresses from the collection
source_as_cursor = collection.distinct("ASN")
source_as = list(source_as_cursor)

# Publish IP addresses for AS queries to the AS_query_queue in RabbitMQ
for ASN in source_as:
    message = {
        "ASN": ASN
    }

    # Publish the message to the Shadow_Server_query_queue in RabbitMQ
    channel.basic_publish(
        exchange="",
        routing_key="Shadow_Server_query_queue",
        body=json.dumps(message)
    )

    print(f"Published AS: {ASN}")

# Close the RabbitMQ connection
connection.close()
