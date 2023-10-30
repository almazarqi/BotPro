import pandas as pd
from pymongo import MongoClient
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256

# MongoDB connection settings
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["shannon_ports"]  # Change to the "shannon_ports" collection

# Aggregation pipeline to group by source_ip_address and calculate the sum of event_count
pipeline = [
    {
        "$group": {
            "_id": "$source_ip_address",
            "event_count_sum": {"$sum": "$event_count"}
        }
    },
    {"$sort": {"event_count_sum": -1}},
    {"$limit": 10}
]

result = list(collection.aggregate(pipeline))

# Prepare data for plotting and sort
data = pd.DataFrame(result)
data["_id"] = data["_id"].astype(str)
data = data.sort_values(by="event_count_sum", ascending=False)  # Sort in descending order

# Set up color map
color_mapper = linear_cmap(field_name="event_count_sum", palette=Viridis256, low=min(data["event_count_sum"]), high=max(data["event_count_sum"]))

# Set up Bokeh plot
output_file("Top_Source_IPs.html")
p = figure(
    x_range=data["_id"],
    x_axis_label='Source IP Address',
    y_axis_label='Number of scanning',
    background_fill_color="#fafafa",
    plot_height=330,  # Adjust the plot height as needed
    plot_width=520
)

source = ColumnDataSource(data)
hover = HoverTool(tooltips=[("Source IP", "@_id"), ("Sum of Event Count", "@event_count_sum")])

p.add_tools(hover)
# Plot the vertical bars with color gradation
p.vbar(
    x="_id",
    top="event_count_sum",
    source=ColumnDataSource(data),
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
