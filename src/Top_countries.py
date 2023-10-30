# Top Countries
from pymongo import MongoClient
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Category20
from bokeh.models import ColumnDataSource, HoverTool


# MongoDB configuration
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["full_graph"]

# Retrieve data from MongoDB
pipeline = [
    {
        "$group": {
            "_id": "$country",
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

# Prepare data for plotting
data = pd.DataFrame(result)
data = data.dropna()  # Drop rows with missing country data

# Set up color map
color_map = factor_cmap(field_name="_id", palette=Category20[20], factors=data["_id"])

# Set up Bokeh plot
output_file("Top_Countries_Bar_Chart.html")
p = figure(
    x_range=data["_id"],
    x_axis_label='Country',
    y_axis_label='Number of Unique Source IPs',
    background_fill_color="#fafafa",
    plot_height=330 , # Adjust the plot height as needed
    plot_width=520
)
source = ColumnDataSource(data)
hover = HoverTool(tooltips=[ ("", "@unique_source_ips_count")])
# hover = HoverTool(tooltips=[("ASN Number", "@_id"), ("Total IPs", "@unique_source_ips_count")])

p.add_tools(hover)
# Plot the bars with color mapping
p.vbar(
    x="_id",
    top="unique_source_ips_count",
    source=ColumnDataSource(data),
    width=0.5,
    color=color_map,
#     legend_field="_id"
)

# Set labels and style
p.xaxis.axis_label_text_font_size = "13pt"
p.yaxis.axis_label_text_font_size = "13pt"
p.xaxis.major_label_text_font_size = "10pt"
p.yaxis.major_label_text_font_size = "10pt"
p.xaxis.major_label_orientation = 45   # Rotate x-axis tick labels
p.legend.title_text_font_size = "14pt"

# Show the plot
show(p)
