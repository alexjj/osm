import requests
import pandas as pd
import time

def query_overpass(lat, lon, radius=100):
    """Query Overpass API to find an existing OSM node matching the summit name near the given coordinates."""
    query = f"""
    [out:json];
    node(around:{radius},{lat},{lon})["natural"="peak"];
    out body;
    >;
    out skel qt;
    """
    url = "http://overpass-api.de/api/interpreter"
    response = requests.get(url, params={"data": query})
    time.sleep(1)  # Pause to avoid overwhelming the API

    if response.status_code == 200:
        data = response.json()
        if "elements" in data and len(data["elements"]) > 0:
            return data["elements"][0]["id"]
    return None

# Load summit data from csv
df = pd.read_csv("missing.csv", encoding="utf-8")

# Prepare results list
results = []

# Loop through summits and query Overpass
for index, row in df.iterrows():
    node_id = query_overpass(row["Latitude"], row["Longitude"])
    results.append({
        "SummitName": row["SummitName"],
        "Latitude": row["Latitude"],
        "Longitude": row["Longitude"],
        "Reference": row["SummitCode"],
        "Points": row["Points"],
        "OSM_Node_ID": node_id
    })
    print(f"Processed {row['SummitName']}: Node ID {node_id}")

# Save results to a CSV file
results_df = pd.DataFrame(results)
results_df.to_csv("uk_summit_nodes_1.csv", index=False)

print("Done! Results saved to uk_summit_nodes.csv")
