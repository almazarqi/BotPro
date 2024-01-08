# working3_ full dataset, Latex
import networkx as nx
from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool, MultiLine, Plot, Range1d, ResetTool)
from bokeh.plotting import from_networkx
from pymongo import MongoClient

# Set up MongoDB client
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["full_graph"]

# Create an empty directed graph
G = nx.DiGraph()
# G = nx.Graph()

# Retrieve data from the MongoDB collection
data = collection.find({}, {"source_ip_address": 1, "IP_URL": 1})

# Add edges to the graph based on the source and target fields
for doc in data:
    source = doc["source_ip_address"]
    target = doc["IP_URL"]
    G.add_edge(source, target)

# Compute betweenness centrality
betweenness_centrality = nx.betweenness_centrality(G)
# Sort the nodes by their betweenness centrality scores
