import pika
import json
import os
import geoip2.database
from pymongo import MongoClient

# Set up RabbitMQ connection
rabbitmq_uri = os.environ.get("RABBITMQ_URI", "amqp://localhost:5672/")
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_uri))
channel = connection.channel()

# Define the RabbitMQ exchange name (should match the exchange used by the publisher)
exchange_name = "Geolocation"  # Replace with your actual exchange name

# Declare the exchange
channel.exchange_declare(exchange=exchange_name, exchange_type="direct")

# Declare a queue to receive messages
queue_name = "your_queue_name"  # Replace with your desired queue name
channel.queue_declare(queue=queue_name, durable=True)

# Bind the queue to the exchange with a routing key (if needed)
routing_key = "Geolocation_route"  # Replace with your routing key
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

# Specify the relative path to the database file in the same folder as your script
database_file = 'GeoLite2-City.mmdb'

# Create a Reader object
with geoip2.database.Reader(database_file) as reader:
    # Set up MongoDB client
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27018")
    client = MongoClient(mongo_uri)
    db = client["botnet"]
    collection = db["Geolocation"]

    # Define a callback function to process messages
    def callback(ch, method, properties, body):
        try:
            # Parse the JSON message
            message = json.loads(body)

            # Process the message (customize as needed)
            ip_address = message.get("ip_address")

            # Perform geolocation lookup using MaxMind GeoIP2
            response = reader.city(ip_address)

            # Extract geolocation information
            city_name = response.city.name
            country_name = response.country.name
            latitude = response.location.latitude
            longitude = response.location.longitude

            # Print or process the geolocation data
            print(f"Received IP data for: {ip_address}")
            print(f"City: {city_name}, Country: {country_name}")
            print(f"Latitude: {latitude}, Longitude: {longitude}")

            # Save the geolocation data to MongoDB
            geolocation_data = {
                "ip_address": ip_address,
                "city_name": city_name,
                "country_name": country_name,
                "latitude": latitude,
                "longitude": longitude
            }
            collection.insert_one(geolocation_data)

            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(f"Error processing message: {str(e)}")

    # Set the number of concurrent messages to process (prefetch count)
    channel.basic_qos(prefetch_count=1)

    # Set up the consumer to receive messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    # Start consuming messages
    print("Waiting for messages. To exit, press CTRL+C")
    channel.start_consuming()
