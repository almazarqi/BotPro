import os
import json
import pika
from pymongo import MongoClient
from ipwhois.experimental import get_bulk_asn_whois

def process_asn_message(channel, method, properties, body):
    message = json.loads(body)
    ip = message.get("ip")

    # Perform the ASN lookup using ipwhois library
    result = get_bulk_asn_whois(addresses=[ip])

    # Set up MongoDB client
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27018")
    client = MongoClient(mongo_uri)
    db = client["botnet"]

    # Store the ASN data in the "ASes" collection
    ases_collection = db["ASes"]

    for line in result.split('\n'):
        if line.strip():
            ases_data = line.strip().split('|')
            if len(ases_data) >= 7:
                ases_collection.insert_one({
                    "source_ip_address": ases_data[1].strip(),
                    "ASN": ases_data[0].strip(),
                    "prefix": ases_data[2].strip(),
                    "ISP": ases_data[4].strip(),
                    "data": ases_data[5].strip(),
                    "org": ases_data[6].strip()
                })

    print(f"Processed IP: {ip}")

# Set up RabbitMQ connection
rabbitmq_uri = os.environ.get("RABBITMQ_URI", "amqp://localhost:5672/")
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_uri))
channel = connection.channel()

# Declare the message queue for AS queries
as_query_queue = "AS_query_queue"
channel.queue_declare(queue=as_query_queue)

# Set up a consumer to process incoming messages from the AS_query_queue
channel.basic_consume(
    queue=as_query_queue,
    on_message_callback=process_asn_message,
    auto_ack=True
)

print("Waiting for messages. To exit, press CTRL+C")
channel.start_consuming()
