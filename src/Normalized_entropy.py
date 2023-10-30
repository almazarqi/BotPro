from pymongo import MongoClient
import pandas as pd
from bokeh.plotting import figure, show, output_file
import numpy as np

# MongoDB configuration
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["shannon_ports"]

# Define the minimum Entropy threshold and maximum target_port count for filtering
min_entropy_threshold = 0.1  # Adjust as needed
max_target_port_count = 45  # Adjust as needed

# Retrieve data from MongoDB
data = list(collection.find({"Entropy": {"$gt": min_entropy_threshold}}, {"_id": 0, "Entropy": 1, "target_port": 1}))

# Calculate the number of unique target_ports for each Entropy value
entropy_unique_ports = {}
for entry in data:
    entropy = entry["Entropy"]
    target_port = entry["target_port"]
    if entropy not in entropy_unique_ports:
        entropy_unique_ports[entropy] = set()
    entropy_unique_ports[entropy].add(target_port)

# Prepare data for plotting based on the maximum target_port count
entropy_values = sorted(list(entropy for entropy, ports in entropy_unique_ports.items() if len(ports) <= max_target_port_count))
unique_port_counts = [len(entropy_unique_ports[entropy]) for entropy in entropy_values]

# Set up Bokeh plot
output_file("Filtered_Sorted_Entropy_Unique_Ports_Step_Line_Chart.html")
p = figure(
    x_axis_label='Entropy',
    y_axis_label='Number of Unique Ports',
    background_fill_color="#fafafa",
    plot_height=400,  # Adjust the plot height as needed
    plot_width=750

    
)

# Plot the step line chart
p.step(
    x=entropy_values,
    y=unique_port_counts,
    line_color="darkblue",
    line_width=2,
    mode="before"  # Specify step mode
)

# Set labels and style
p.xaxis.axis_label_text_font_size = "18pt"
p.yaxis.axis_label_text_font_size = "18pt"
p.xaxis.major_label_text_font_size = "14pt"
p.yaxis.major_label_text_font_size = "14pt"

# Show the plot
show(p)
