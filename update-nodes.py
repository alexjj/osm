import pandas as pd
import overpy
import xml.etree.ElementTree as ET
import time

# Initialize Overpass API
api = overpy.Overpass()

# Load the CSV file
df = pd.read_csv('osm_summit_nodes.csv')

# Initialize the root of the OSM XML file
osm = ET.Element("osm", version="0.6", generator="Python Script")

# Function to fetch OSM node and add tags
def add_osm_tags(node_id, reference, points):
    # Query OSM for the specific node and its tags
    result = api.query(f'node({node_id});out tags;')

    # Check if node exists in the result
    if not result.nodes:
        print(f"Node {node_id} not found in OSM.")
        return

    # Get the node from the result
    node = result.nodes[0]

    # Create the <node> element in OSM XML (without lat/lon since it's an existing node)
    osm_node = ET.SubElement(osm, "node", id=str(node.id))

    # Check if the node already has the tag "communication:amateur_radio:sota"
    if "communication:amateur_radio:sota" not in node.tags:
        ET.SubElement(osm_node, "tag", k="communication:amateur_radio:sota", v=reference)

    # Check if the node already has the tag "communication:amateur_radio:sota:points"
    if "communication:amateur_radio:sota:points" not in node.tags:
        ET.SubElement(osm_node, "tag", k="communication:amateur_radio:sota:points", v=points)

# Iterate over each row in the CSV and add tags to the nodes
for index, row in df.iterrows():
    node_id = row['OSM_Node_ID']
    reference = row['Reference']
    points = row['Points']

    # Fetch the node and add tags if they are not already present
    add_osm_tags(node_id, reference, points)

    # Sleep for a short time to avoid overwhelming the server
    time.sleep(1)

# Convert the ElementTree to a string and write to an .osm file
tree = ET.ElementTree(osm)
tree.write("updated_nodes.osm", encoding="UTF-8", xml_declaration=True)

print("JOSM .osm file created as 'updated_nodes.osm'.")
