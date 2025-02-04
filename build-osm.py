import pandas as pd
import xml.etree.ElementTree as ET

# File paths
osm_file = "export.osm"  # Input OSM file
csv_file = "osm_summit_nodes.csv"  # CSV with summit data
output_file = "updated_export.osm"  # Output file

# Load the CSV file
df = pd.read_csv(csv_file, dtype={"OSM_Node_ID": str})  # Ensure OSM_Node_ID is treated as a string

# Parse the OSM XML file
tree = ET.parse(osm_file)
root = tree.getroot()

# Mapping of OSM node ID to (Reference, Points)
summit_data = {row["OSM_Node_ID"]: (row["Reference"], str(row["Points"])) for _, row in df.iterrows()}

# Process each node in the OSM file
for node in root.findall("node"):
    node_id = node.get("id")

    if node_id in summit_data:
        reference, points = summit_data[node_id]

        # Check if the tags already exist
        existing_tags = {tag.get("k"): tag.get("v") for tag in node.findall("tag")}

        if "communication:amateur_radio:sota" not in existing_tags:
            ET.SubElement(node, "tag", k="communication:amateur_radio:sota", v=reference)

        if "communication:amateur_radio:sota:points" not in existing_tags:
            ET.SubElement(node, "tag", k="communication:amateur_radio:sota:points", v=points)

# Save the modified OSM file
tree.write(output_file, encoding="UTF-8", xml_declaration=True)

print(f"Updated OSM file saved as {output_file}")
