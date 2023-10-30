import pandas as pd
from pymongo import MongoClient
from collections import Counter
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256

# MongoDB connection settings
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["scanning"]

# Retrieve data from MongoDB and filter Num_Ports >= 2
data = list(collection.find({"count_ports": {"$gte": 2}}, {"_id": 0, "sum_ports": 1, "count_ports": 1}))

# Extract port sequences and count occurrences
all_port_sequences = []
for item in data:
    port_sequence = item["sum_ports"]
    all_port_sequences.append(port_sequence)

# Count port sequence occurrences
port_sequence_counts = Counter(all_port_sequences)

# Get the top 10 port sequences and their counts
top_port_sequences = port_sequence_counts.most_common(10)

# Prepare data for plotting
port_sequences, counts = zip(*top_port_sequences)

# Set up color map
color_mapper = linear_cmap(field_name="counts", palette=Viridis256, low=min(counts), high=max(counts))

# Set up Bokeh plot
output_file("Top_Port_Sequences.html")
p = figure(
    x_range=[str(seq) for seq in port_sequences],
    x_axis_label='Port Sequence',
    y_axis_label='Count',
    background_fill_color="#fafafa",
    plot_height=330,  # Adjust the plot height as needed
    plot_width=520
)

source = ColumnDataSource(data=dict(port_sequences=[str(seq) for seq in port_sequences], counts=counts))
hover = HoverTool(tooltips=[("Port Sequence", "@port_sequences"), ("Count", "@counts")])

p.add_tools(hover)
# Plot the vertical bars with color gradation
p.vbar(
    x="port_sequences",
    top="counts",
    source=source,
    width=0.5,
    color=color_mapper,
    line_color="grey",
    alpha=0.7
)

# Set labels and style
p.xaxis.axis_label_text_font_size = "13pt"
p.yaxis.axis_label_text_font_size = "13pt"
p.xaxis.major_label_text_font_size = "11pt"
p.yaxis.major_label_text_font_size = "11pt"
p.xaxis.major_label_orientation = 45

# Show the plot
show(p)
