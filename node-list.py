import pandas as pd

# Read the CSV file
df = pd.read_csv("missing_with_ids.csv", encoding="utf8")

# Convert the 'OSM_Node_ID' column to a comma-separated string
osm_node_ids = ",n".join(df["OSM_Node_ID"].astype(str))

# Print or use the resulting string
print(osm_node_ids)
