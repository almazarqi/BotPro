import streamlit as st
import streamlit.components.v1 as components

# Set the page configuration to wide layout
st.set_page_config(layout="wide")

# Header and subheader with cyber security theme
st.title("BotPro")
st.markdown("Profiling IoT Botnet Activity")

# Add a line to separate the header and subheader
st.markdown("---")

# Sidebar with a dark background and cyber security theme
st.sidebar.title("BotPro")
st.sidebar.markdown("")

# Boolean flag to determine if home content should be displayed
display_home_content = False

# Function to reset to the home page
def home_button_click():
    global display_home_content
    display_home_content = True

# Create the "Home" button
if st.sidebar.button("Home"):
    home_button_click()

# Button to display the "Map" option with a cyber security label
if st.sidebar.button("Geographic Distribution"):
    st.header("")
    # Display the filtered map
    HtmlFile = open("Bot_Maps.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, width=800, height=600)

# Button to display the "Bot Loaders" option
if st.sidebar.button("Bot Loaders"):
    st.header("Bot Loaders")
    # Load the bot loaders HTML
    bot_loaders_html_file_path = "bot_loaders4.html"
    with open(bot_loaders_html_file_path, "r", encoding='utf-8') as bot_loaders_html_file:
        bot_loaders_html_content = bot_loaders_html_file.read()

    # Load the top nodes graph HTML
    top_nodes_graph_html_file_path = "top_nodes_graph2.html"
    with open(top_nodes_graph_html_file_path, "r", encoding='utf-8') as top_nodes_graph_html_file:
        top_nodes_graph_html_content = top_nodes_graph_html_file.read()

    # Adjust spacing between components
    col1, col2 = st.columns((2, 3.5))

    with col1:
        components.html(bot_loaders_html_content, width=500, height=500)

    with col2:
        components.html(top_nodes_graph_html_content, width=500, height=500)

    # Display the degree centrality table HTML underneath
    degree_centrality_table_html_file_path = "top_IP_URLs_degree_centrality.html"
    with open(degree_centrality_table_html_file_path, "r", encoding='utf-8') as degree_centrality_table_html_file:
        degree_centrality_table_html_content = degree_centrality_table_html_file.read()
    components.html(degree_centrality_table_html_content, width=850, height=600)

# Button to display the "ASes Analysis" option
if st.sidebar.button("ASes Analysis"):
    st.header("Top ASes Analysis")
    # Load the All ASes HTML content (replace with appropriate file path)
    all_ases_html_file_path = "All_ASes.html"
    with open(all_ases_html_file_path, "r", encoding="utf-8") as all_ases_html_file:
        all_ases_html_content = all_ases_html_file.read()

    # Load the top ASes HTML content (replace with appropriate file path)
    top_ases_html_file_path = "top_ASes.html"
    with open(top_ases_html_file_path, "r", encoding="utf-8") as top_ases_html_file:
        top_ases_html_content = top_ases_html_file.read()

    # Load the Top Countries Bar Chart HTML
    top_countries_html_file_path = "Top_Countries_Bar_Chart.html"
    with open(top_countries_html_file_path, "r", encoding="utf-8") as top_countries_html_file:
        top_countries_html_content = top_countries_html_file.read()

    # Load the ASes Vertical Bar Chart HTML
    ases_vertical_html_file_path = "ASes_top_vertical_color.html"
    with open(ases_vertical_html_file_path, "r", encoding="utf-8") as ases_vertical_html_file:
        ases_vertical_html_content = ases_vertical_html_file.read()

 # Load the AS_URL_IP_Top_Table HTML content
    as_url_ip_top_table_html_file_path = "AS_URL_IP_Top_Table.html"
    with open(as_url_ip_top_table_html_file_path, "r", encoding="utf-8") as as_url_ip_top_table_html_file:
        as_url_ip_top_table_html_content = as_url_ip_top_table_html_file.read()

    # Display the HTML files using columns
  # Adjust spacing between components
    col1, col2 = st.columns((2, 3.5))

    with col1:
        components.html(all_ases_html_content, width=500, height=500)

    with col2:
        components.html(top_ases_html_content, width=500, height=500)

    # Display the HTML files for Top Countries and ASes Vertical Bar Chart
    col3, col4 = st.columns((2,3.5))

    with col3:
        components.html(top_countries_html_content, width=520, height=345)

    with col4:
        components.html(ases_vertical_html_content, width=500, height=345)

    # Display the AS_URL_IP_Top_Table HTML content
    col5, col6 = st.columns((2,3.5))
    with col5:
        components.html(as_url_ip_top_table_html_content, width=400, height=500)

    with col6:
        pass

# Button to display the "Blacklists" option
if st.sidebar.button("Blacklists"):
    st.header("Blacklists Analysis")

    # Load the Blacklist content (replace with appropriate file paths)
    blacklist_html_file_path = "Four_blacklists.html"
    with open(blacklist_html_file_path, "r", encoding='utf-8') as blacklist_html_file:
        blacklist_html_content = blacklist_html_file.read()

    beta_distribution_html_file_path = "Beta_Distribution.html"
    with open(beta_distribution_html_file_path, "r", encoding='utf-8') as beta_distribution_html_file:
        beta_distribution_html_content = beta_distribution_html_file.read()

    coefficient_variation_html_file_path = "coefficient_variation_online.html"
    with open(coefficient_variation_html_file_path, "r", encoding='utf-8') as coefficient_variation_html_file:
        coefficient_variation_html_content = coefficient_variation_html_file.read()

    active_days_histogram_html_file_path = "Active_Days_Histogram.html"
    with open(active_days_histogram_html_file_path, "r", encoding='utf-8') as active_days_histogram_html_file:
        active_days_histogram_html_content = active_days_histogram_html_file.read()

    # Adjust spacing between components
    col1, col2 = st.columns(2)

    with col1:
        components.html(blacklist_html_content, width=800, height=350)

    with col2:
        components.html(beta_distribution_html_content, width=800, height=350)

    col3, col4 = st.columns(2)

    with col3:
        components.html(coefficient_variation_html_content, width=800, height=350)

    with col4:
        components.html(active_days_histogram_html_content, width=800, height=350)

# Button to display the "DNS" option
if st.sidebar.button("DNS"):
    st.header("DNS")
# Create two columns for the first row of HTML content

    # Load and display the rDNS_Top_Bar_Chart.html file in col1
    with open("rDNS_Top_Bar_Chart.html", "r", encoding='utf-8') as rdns_html_file:
        rdns_html_content = rdns_html_file.read()
   
    # Load and display the TTL_value.html file in col2
    with open("TTL_value.html", "r", encoding='utf-8') as ttl_html_file:
        ttl_html_content = ttl_html_file.read()
   
  # Adjust spacing between components
    col1, col2 = st.columns((2,2.5))

    with col1:
        components.html(rdns_html_content, width=850, height=350)

    with col2:
        components.html(ttl_html_content, width=500, height=350)

  # Load and display the top_DNS_records.html file in col3
    with open("top_DNS_records.html", "r", encoding='utf-8') as top_dns_html_file:
        top_dns_html_content = top_dns_html_file.read()
    components.html(top_dns_html_content, width=800, height=700)

# Button to display the "Scanning activity" option
if st.sidebar.button("Scanning activity"):
    st.header("Scanning activity")
    
    # Create two columns for the first row of HTML content
    col1, col2 = st.columns(2)
# Adjust spacing between components
    col1, col2 = st.columns((2, 2.8))
    
    with col1:
        # Load and display the Top Port Sequences content
        top_port_sequences_html_file_path = "Top_Port_Sequences.html"
        with open(top_port_sequences_html_file_path, "r", encoding='utf-8') as file:
            top_port_sequences_html_content = file.read()
        components.html(top_port_sequences_html_content, width= 650, height=350)

    with col2:
        # Load and display the Top Source IPs content
        top_source_ips_html_file_path = "Top_Source_IPs.html"
        with open(top_source_ips_html_file_path, "r", encoding='utf-8') as file:
            top_source_ips_html_content = file.read()
        components.html(top_source_ips_html_content, width=650, height=350)
    
    # Create two columns for the second row of HTML content
    col3, col4 = st.columns(2)
# Adjust spacing between components
    col3, col4 = st.columns((2, 2.8))

    with col3:
        # Load and display the Filtered Sorted Entropy Unique Ports Step Line Chart
        filtered_sorted_entropy_file_path = "Filtered_Sorted_Entropy_Unique_Ports_Step_Line_Chart.html"
        with open(filtered_sorted_entropy_file_path, "r", encoding='utf-8') as file:
            filtered_sorted_entropy_html_content = file.read()
        components.html(filtered_sorted_entropy_html_content, width=650, height=350)

    with col4:
        # Load and display the Entropy Histogram LogScale
        entropy_histogram_file_path = "Entropy_Histogram_LogScale.html"
        with open(entropy_histogram_file_path, "r", encoding='utf-8') as file:
            entropy_histogram_html_content = file.read()
        components.html(entropy_histogram_html_content, width= 650, height=350)

# Display home content if the flag is set
if display_home_content:
    with open("home.html", "r", encoding='utf-8') as home_html_file:
        home_html_content = home_html_file.read()
    st.markdown(home_html_content, unsafe_allow_html=True)
