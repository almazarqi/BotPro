from pymongo import MongoClient
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file

# MongoDB configuration
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["shannon"]

# Retrieve data from MongoDB
data = list(collection.find({}, {"_id": 0, "Entropy": 1}))

# Prepare data for plotting
entropy_values = [entry["Entropy"] for entry in data]

# Set up Bokeh plot
output_file("Entropy_Histogram_LogScale.html")
p = figure(
    x_axis_label='Normalised Entropy',
    y_axis_label='Unique IP addresses',
    background_fill_color="#fafafa",
    y_axis_type="log",  # Set y-axis to log scale
    plot_height=400  # Adjust the plot height as needed
)

# Plot the histogram
hist, edges = np.histogram(entropy_values, bins=5)
p.quad(
    top=hist,
    left=edges[:-1],
    right=edges[1:],
    fill_color="darkblue",
    line_color="grey",
    alpha=0.7,
    bottom=0.5,  # Adjust the bottom value for log scale
    fill_alpha=0.5
)

# Set labels and style
p.xaxis.axis_label_text_font_size = "18pt"
p.yaxis.axis_label_text_font_size = "18pt"
p.xaxis.major_label_text_font_size = "14pt"
p.yaxis.major_label_text_font_size = "14pt"

# Show the plot
show(p)
