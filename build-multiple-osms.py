import pandas as pd
import xml.etree.ElementTree as ET
import os

# CSV file with summit data
csv_file = "uk_summit_nodes.csv"  # CSV with summit data

# Load the CSV file
df = pd.read_csv(csv_file, dtype={"OSM_Node_ID": str})  # Ensure OSM_Node_ID is treated as a string

# Mapping of OSM node ID to (Reference, Points)
summit_data = {row["OSM_Node_ID"]: (row["Reference"], str(row["Points"])) for _, row in df.iterrows()}

# Loop through export(#).osm files
for i in range(1, 17):  # Files from export(1).osm to export(16).osm
    osm_file = f"export({i}).osm"  # Input OSM file
    output_file = f"updated_export_{i}.osm"  # Output file

    if os.path.exists(osm_file):  # Ensure the file exists
        # Parse the OSM XML file
        tree = ET.parse(osm_file)
        root = tree.getroot()

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
    else:
        print(f"File {osm_file} does not exist. Skipping.")
