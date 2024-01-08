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
# Sort the nodes by their betweenness centrality scores
top_nodes = sorted(betweenness_centrality, key=betweenness_centrality.get, reverse=True)[:100]

# Assign weights to the edges
for u, v in G.edges():
    if u in top_nodes or v in top_nodes:
        G[u][v]["weight"] = 250 # Assign higher weight to edges connected to top nodes
    else:
        G[u][v]["weight"] = 0
        

# Extract the subgraph consisting of the top nodes and their connected nodes
subgraph_nodes = top_nodes.copy()  # Create a copy of top_nodes
for node in top_nodes:
    subgraph_nodes += list(G.successors(node))  # Add successors
    subgraph_nodes += list(G.predecessors(node))  # Add predecessors
subgraph_nodes = list(set(subgraph_nodes))  # Remove duplicates
subgraph = G.subgraph(subgraph_nodes)


# Adjust the layout algorithm parameters
layout = nx.spring_layout(subgraph, scale=1, center=(0, 0), k=1.3, iterations=120, seed=24, weight="weight", dim=2)
# layout = nx.spring_layout(subgraph, scale=1, center=(0, 0), k=1.3, iterations=120, seed=0, weight="weight", dim=2)

# k=1.3

# Calculate the extents of the layout
min_x = min(layout[node][0] for node in layout)
max_x = max(layout[node][0] for node in layout)
min_y = min(layout[node][1] for node in layout)
max_y = max(layout[node][1] for node in layout)

# Set plot range based on layout extents
# x_range = Range1d(min_x - 0.1, max_x + 0.1)
# y_range = Range1d(min_y - 0.1, max_y + 0.1)



# Adjust the padding values to control the space around the plot
padding_x = 0.05  # Adjust as needed
padding_y = 0.05  # Adjust as needed

# Set plot range based on layout extents with padding
x_range = Range1d(min_x - padding_x, max_x + padding_x)
y_range = Range1d(min_y - padding_y, max_y + padding_y)



# Show with Bokeh
plot = Plot(width=500, height=500,


node_hover_tool = HoverTool(tooltips=[("Node", "@index")])
plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())
plot.toolbar.logo = None


# Define node colors and sizes
node_colors = []
node_sizes = []
for node in subgraph.nodes:
    if node in top_nodes:
        node_colors.append("red")
        node_sizes.append(6)  # Larger size for top nodes
    else:
        node_colors.append("blue")
        node_sizes.append(3.5)   # Smaller size for connected nodes

# Create the graph renderer
graph_renderer = from_networkx(subgraph, layout)

# Set node colors and sizes
graph_renderer.node_renderer.data_source.data["colors"] = node_colors
graph_renderer.node_renderer.glyph = Circle(size="node_sizes", fill_color="colors")
graph_renderer.node_renderer.data_source.data["node_sizes"] = node_sizes

# Set edge renderer
graph_renderer.edge_renderer.glyph = MultiLine(line_color="grey", line_alpha=0.4, line_width=0.5)

# Add renderers to the plot
plot.renderers.append(graph_renderer)

# Save and show the plot
show(plot)
