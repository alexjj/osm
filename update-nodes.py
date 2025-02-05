import pandas as pd
import overpy
import xml.etree.ElementTree as ET
import time  # Import the time module to use sleep()

# Initialize Overpass API
api = overpy.Overpass()

# Load the CSV file
df = pd.read_csv('osm_summit_nodes.csv')

# Initialize the root of the OSM XML file
osm = ET.Element("osm", version="0.6", generator="Python Script")

# Function to fetch OSM nodes in bulk and add tags
def add_osm_tags_bulk(node_ids, reference, points):
    # Prepare the Overpass query to fetch multiple nodes by ID
    node_ids_str = ",".join(map(str, node_ids))  # Convert the node IDs to a comma-separated string
    query = f'node(id:{node_ids_str});out tags;'  # Query nodes by their IDs

    # Send the Overpass query
    result = api.query(query)

    # Iterate over the nodes returned by the query
    for node in result.nodes:
        # Create the <node> element in OSM XML (without lat/lon since it's an existing node)
        osm_node = ET.SubElement(osm, "node", id=str(node.id))

        # Check if the node already has the tag "communication:amateur_radio:sota"
        if "communication:amateur_radio:sota" not in node.tags:
            ET.SubElement(osm_node, "tag", k="communication:amateur_radio:sota", v=reference)

        # Check if the node already has the tag "communication:amateur_radio:sota:points"
        if "communication:amateur_radio:sota:points" not in node.tags:
            ET.SubElement(osm_node, "tag", k="communication:amateur_radio:sota:points", v=points)

# Split the CSV into batches of node IDs to avoid very large queries
batch_size = 100  # Adjust this value based on the Overpass server limits
node_ids_batch = []
for index, row in df.iterrows():
    node_ids_batch.append(row['OSM_Node_ID'])

    # If we have collected a full batch, process it
    if len(node_ids_batch) >= batch_size or index == len(df) - 1:
        # Get the reference and points from the first node in the batch
        reference = df.loc[df['OSM_Node_ID'] == node_ids_batch[0], 'Reference'].values[0]
        points = df.loc[df['OSM_Node_ID'] == node_ids_batch[0], 'Points'].values[0]

        # Add tags for the batch of node IDs
        add_osm_tags_bulk(node_ids_batch, reference, points)

        # Clear the batch for the next set of node IDs
        node_ids_batch = []

    # Sleep between batches to avoid server overload
    time.sleep(2)  # Adjust sleep time as needed to avoid hitting server limits

# Convert the ElementTree to a string and write to an .osm file
tree = ET.ElementTree(osm)
tree.write("updated_nodes.osm", encoding="UTF-8", xml_declaration=True)

print("JOSM .osm file created as 'updated_nodes.osm'.")
