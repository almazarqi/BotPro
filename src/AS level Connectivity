# Set up MongoDB client
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)

client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["graph"]

# Create an empty directed graph
G = nx.DiGraph()

# Retrieve data from the MongoDB collection
data = collection.find({}, {"ASN_Number": 1, "AS_URL_IP": 1})

# Add edges to the graph based on the source and target fields
for doc in data:
    source = doc["ASN_Number"]
    target = doc["AS_URL_IP"]
    G.add_edge(source, target)

# Determine source nodes and target nodes
source_nodes = [node for node in G.nodes if G.in_degree(node) == 0]
target_nodes = [node for node in G.nodes if G.out_degree(node) == 0]

# Determine nodes in ASN_Number connected to nodes in AS_URL_IP
connected_nodes = set()
for target in target_nodes:
    connected_nodes.update(G.predecessors(target))

# Show with Bokeh
plot = Plot(width=800, height=800,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
plot.title.text = "Botnet Graph"

node_hover_tool = HoverTool(tooltips=[("index", "@index")])
plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

# Adjust the layout algorithm parameters
layout = nx.spring_layout(G, scale=1, center=(0, 0), k=0.2, iterations=100)

graph_renderer = from_networkx(G, layout)
graph_renderer.node_renderer.data_source.data["colors"] = ["red" if node in connected_nodes else Blues8[2] for node in G.nodes]
graph_renderer.node_renderer.glyph = Circle(size=8, fill_color="colors")
graph_renderer.edge_renderer.glyph = MultiLine(line_color="black", line_alpha=0.8, line_width=1)
plot.renderers.append(graph_renderer)

output_file("interactive_graphs.html")
show(plot)
