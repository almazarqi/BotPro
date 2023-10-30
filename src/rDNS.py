
from pymongo import MongoClient
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256

# MongoDB configuration
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["Four_Blacklists"]

# Retrieve data from MongoDB
pipeline = [
    {
        "$group": {
            "_id": "$rDNS",
            "unique_source_ips": {"$addToSet": "$source_ip_address"}
        }
    },
    {
        "$project": {
            "_id": 1,
            "unique_source_ips_count": {"$size": "$unique_source_ips"}
        }
    },
    {"$sort": {"unique_source_ips_count": -1}},
    {"$limit": 10}
]

result = list(collection.aggregate(pipeline))

# Prepare data for plotting and sort
data = pd.DataFrame(result)
data = data.dropna()  # Drop rows with missing rDNS data
data["_id"] = data["_id"].astype(str)
data = data.sort_values(by="unique_source_ips_count", ascending=False)  # Sort in descending order

# Set up color map
color_mapper = linear_cmap(field_name="unique_source_ips_count", palette=Viridis256, low=min(data["unique_source_ips_count"]), high=max(data["unique_source_ips_count"]))

# Set up Bokeh plot
output_file("rDNS_Top_Bar_Chart.html")
p = figure(
    y_range=data["_id"],  # Use 'y_range' for vertical bars
    y_axis_label='rDNS',
    x_axis_label='Number of Unique Source IPs',  # Swap x and y axis labels
    background_fill_color="#fafafa",
    plot_width=1000,  # Adjust the plot width as needed
    plot_height=500  # Adjust the plot height as needed
)

# Plot the horizontal bars with color gradation and hover tooltips
source = ColumnDataSource(data)
hover = HoverTool(tooltips=[("rDNS", "@_id"), ("Unique Source IPs", "@unique_source_ips_count")])
p.add_tools(hover)

p.hbar(  # Use 'hbar' for horizontal bars
    y="_id",  # Use 'y' for vertical positioning
    left=0,  # Use 'left' for horizontal positioning
    right="unique_source_ips_count",  # Use 'right' for horizontal bar length
    source=source,
    height=0.5,  # Adjust the bar height as needed
    color=color_mapper,
    line_color="grey",
    alpha=0.7
)

# Set labels and style
p.xaxis.axis_label_text_font_size = "18pt"
p.yaxis.axis_label_text_font_size = "18pt"
p.xaxis.major_label_text_font_size = "14pt"
p.yaxis.major_label_text_font_size = "14pt"

# Rotate y-axis tick labels for better readability
p.yaxis.major_label_orientation = "horizontal"

# Show the plot
show(p)
