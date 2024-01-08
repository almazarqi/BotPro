import networkx as nx
import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, DataTable, TableColumn, HoverTool, CustomJS
from pymongo import MongoClient

# Set up MongoDB client
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["full_graph"]

# Create an empty directed graph
G = nx.DiGraph()

# Retrieve data from the MongoDB collection
data = collection.find({}, {"source_ip_address": 1, "IP_URL": 1})

# Add edges to the graph based on the source and target fields
for doc in data:
    source = doc["source_ip_address"]
    target = doc["IP_URL"]
    G.add_edge(source, target)

# Compute degree centrality
degree_centrality = nx.degree_centrality(G)

# Sort the nodes by their degree centrality scores
sorted_nodes = sorted(degree_centrality.keys(), key=lambda x: degree_centrality[x], reverse=True)

# Create a DataFrame to store the results
data = {"IP_URL": [], "Degree Centrality": []}

# Retrieve the top N nodes with the highest degree centrality
top_n = 10  # You can change this to the desired number of top nodes
for node in sorted_nodes[:top_n]:
    data["IP_URL"].append(node)
    data["Degree Centrality"].append(degree_centrality[node])

# Create a Bokeh DataTable
source = ColumnDataSource(data=data)
columns = [
    TableColumn(field="IP_URL", title="IP_URL"),
    TableColumn(field="Degree Centrality", title="Degree Centrality"),
]

# Define HoverTool tooltips
tooltips = [
    ("IP_URL", "@IP_URL"),
    ("Degree Centrality", "@{Degree Centrality}"),
]

hover = HoverTool(tooltips=tooltips, mode="mouse")

data_table = DataTable(source=source, columns=columns, width=400, height=280)

# Add HoverTool with JavaScript callback to the DataTable's view property
custom_js = CustomJS(
    code="""
    const table = document.getElementsByClassName("bk-data-table")[0];
    const rows = table.getElementsByTagName("tr");
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const ip_url = row.cells[0].textContent;
        const degree_centrality = row.cells[1].textContent;
        row.onmouseover = function() {
            const tooltip = document.createElement("div");
            tooltip.className = "bk-tooltip";
            tooltip.style.left = (event.pageX + 10) + "px";
            tooltip.style.top = (event.pageY - 20) + "px";
            tooltip.innerHTML = `IP_URL: ${ip_url}<br>Degree Centrality: ${degree_centrality}`;
            document.body.appendChild(tooltip);
        };
        row.onmouseout = function() {
            const tooltips = document.getElementsByClassName("bk-tooltip");
            for (let i = 0; i < tooltips.length; i++) {
                tooltips[i].parentNode.removeChild(tooltips[i]);
            }
        };
    }
    """
)

hover.callback = custom_js

# Show the Bokeh DataTable
output_file("top_IP_URLs_degree_centrality.html")
show(data_table)
