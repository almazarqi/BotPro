# power bi
from pymongo import MongoClient
from bokeh.io import show
from bokeh.models import Plot, Range1d, Circle, HoverTool, MultiLine, EdgesAndLinkedNodes, TapTool, OpenURL, CustomJS
from bokeh.models.graphs import from_networkx
import networkx as nx

# Set up MongoDB client
mongo_uri = "mongodb://localhost:27018"
client = MongoClient(mongo_uri)
db = client["botnet"]
collection = db["graph"]

# Create an empty directed graph
graph = nx.DiGraph()

# Retrieve data from the MongoDB collection
data = collection.find({}, {"ASN_Number": 1, "AS_URL_IP": 1})

# Add edges to the graph based on the ASN_Number and AS_URL_IP fields
for doc in data:
    source = doc["ASN_Number"]
    target = doc["AS_URL_IP"]
    graph.add_edge(source, target)

# Create a list of source nodes and target nodes
source_nodes = [node for node in graph.nodes if not list(graph.pred[node])]
target_nodes = [node for node in graph.nodes if not list(graph.succ[node])]

# Set the node colors
node_colors = {node: "#F44336" if node in source_nodes else "#2196F3" for node in graph}

# Create a Bokeh plot
plot = Plot(plot_width=800, plot_height=600,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))

plot.title.text = "Botnet Graph Visualization"
plot.title.text_font_size = "20px"

# Set up hover tools
hover = HoverTool(tooltips=[("Node", "@index")])
plot.add_tools(hover, TapTool())

# Create a renderer for the graph
graph_renderer = from_networkx(graph, nx.spring_layout, scale=1, center=(0, 0), k=0.4)
graph_renderer.node_renderer.data_source.data["colors"] = [node_colors[node] for node in graph]
graph_renderer.node_renderer.glyph = Circle(size=15, fill_color="colors")
graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=0.5)
graph_renderer.selection_policy = EdgesAndLinkedNodes()

# Add node click behavior
node_callback = CustomJS(code="""
    var node_indices = cb_obj.indices;
    var node_index = node_indices[node_indices.length - 1];
    var node_data = source.data;
    var node = node_data['index'][node_index];
    var node_type = node_data['colors'][node_index];
    if (node_type == '#F44336') {
        // Redirect to source node information page
        window.open('https://source-node-url/' + node);
    } else {
        // Redirect to target node information page
        window.open('https://target-node-url/' + node);
    }
""")
graph_renderer.node_renderer.data_source.selected.js_on_change("indices", node_callback)

# Add the graph renderer to the plot
plot.renderers.append(graph_renderer)

# Set plot styling
plot.toolbar.logo = None
plot.toolbar_location = None
plot.outline_line_color = None
plot.background_fill_color = "#FFFFFF"
plot.border_fill_color = "#FFFFFF"
plot.min_border_left = 40
plot.min_border_right = 40
plot.min_border_top = 40
plot.min_border_bottom = 40

# Display the plot
show(plot)
