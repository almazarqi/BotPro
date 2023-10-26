import os
import subprocess
from pymongo import MongoClient
import pika
import json

def process_dns_message(channel, method, properties, body):
    message = json.loads(body)
    ip_address = message.get("ip")

    try:
        cmd = ["nslookup", "-type=PTR", "-debug", ip_address]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout.strip()

        # Extract PTR record and TTL from the output
        ptr_record = ""
        ttl = ""
        nxdomain = False
        lines = output.split("\n")
        for line in lines:
            if "name =" in line:
                ptr_record = line.split("name = ")[-1].strip()
            elif "ttl =" in line:
                ttl = line.split("ttl = ")[-1].strip()

        # Check if NXDOMAIN is present in the output
        nxdomain = "NXDOMAIN" in output

        # Set up MongoDB client
        mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27018")
        client = MongoClient(mongo_uri)
        db = client["botnet"]
        dns_collection = db["DNS"]

        # Create a document for each IP in the DNS collection
        document = {
            "IP": ip_address,
            "PTR": ptr_record,
            "TTL": ttl,
            "NXDOMAIN": nxdomain
        }

        # Insert the document into the DNS collection
        dns_collection.insert_one(document)

        print(f"DNS information for IP {ip_address} saved in the 'DNS' collection.")
    except subprocess.CalledProcessError:
        print(f"Unable to resolve PTR record for {ip_address}")

# Set up RabbitMQ connection
rabbitmq_uri = os.environ.get("RABBITMQ_URI", "amqp://localhost:5672/")
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_uri))
channel = connection.channel()

# Declare the message queue for DNS queries
dns_query_queue = "DNS_query_queue"
channel.queue_declare(queue=dns_query_queue)

# Set up a consumer to process incoming messages from the DNS_query_queue
channel.basic_consume(
    queue=dns_query_queue,
    on_message_callback=process_dns_message,
    auto_ack=True
)

print("Waiting for messages. To exit, press CTRL+C")
channel.start_consuming()
