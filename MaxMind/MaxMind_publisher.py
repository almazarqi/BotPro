import geoip2.database
import json
import os
import pika
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

# Specify the relative path to the database file in the same folder as your script
database_file = 'GeoLite2-City.mmdb'

# Create a Reader object
with geoip2.database.Reader(database_file) as reader:
    # Retrieve distinct source IP addresses from the collection
    source_ips_cursor = collection.distinct("source_ip_address")
    source_ips = list(source_ips_cursor)

    # Define the RabbitMQ exchange name
    exchange_name = "your_exchange_name"  # Replace with your actual exchange name

    # Loop through distinct source IP addresses and publish data
    for ip_address in source_ips:
        # Perform IP address lookup using MaxMind GeoIP2
        response = reader.city(ip_address)

        # Process the response (customize as needed)
        city_name = response.city.name
        country_name = response.country.name
        latitude = response.location.latitude
        longitude = response.location.longitude

        # Create a message with the data to publish
        message = {
            "ip_address": ip_address,
            "city_name": city_name,
            "country_name": country_name,
            "latitude": latitude,
            "longitude": longitude
        }

        # Publish the message to the RabbitMQ exchange
        channel.basic_publish(
            exchange=exchange_name,
            routing_key="",
            body=json.dumps(message)
        )

        print(f"Published IP data for: {ip_address}")

# Close the RabbitMQ connection
connection.close()
