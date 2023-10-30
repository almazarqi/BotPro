# Top ASes 

from pymongo import MongoClient
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256

# MongoDB configuration
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["full_graph"]

# Retrieve data from MongoDB
pipeline = [
    {
        "$group": {
            "_id": "$ASN_Number",
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
data["_id"] = data["_id"].astype(str)
data = data.sort_values(by="unique_source_ips_count", ascending=False)  # Sort in descending order

# Set up color map
color_mapper = linear_cmap(field_name="unique_source_ips_count", palette=Viridis256, low=min(data["unique_source_ips_count"]), high=max(data["unique_source_ips_count"]))

# Set up Bokeh plot
output_file("ASes_top_vertical_color.html")
p = figure(
    x_range=data["_id"],
    x_axis_label='ASN Number',
    y_axis_label='Number of Unique Source IPs',
    background_fill_color="#fafafa",
    plot_height=330,  # Adjust the plot height as needed
    plot_width=520
)


source = ColumnDataSource(data)
hover = HoverTool(tooltips=[ ("", "@unique_source_ips_count")])
# hover = HoverTool(tooltips=[("ASN Number", "@_id"), ("Total IPs", "@unique_source_ips_count")])

p.add_tools(hover)
# Plot the vertical bars with color gradation
p.vbar(
    x="_id",
    top="unique_source_ips_count",
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
