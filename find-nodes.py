import requests
import pandas as pd
import time

def query_overpass(lat, lon, summit_name, radius=50):
    """Query Overpass API to find an existing OSM node matching the summit name near the given coordinates."""
    query = f"""
    [out:json];
    node(around:{radius},{lat},{lon})["name"="{summit_name}"];
    out body;
    """
    url = "http://overpass-api.de/api/interpreter"
    response = requests.get(url, params={"data": query})
    time.sleep(1)  # Pause to avoid overwhelming the API

    if response.status_code == 200:
        data = response.json()
        if "elements" in data and len(data["elements"]) > 0:
            return int(data["elements"][0]["id"])  # Return the first matching node ID as an integer

    # If no match found, try querying by alt_name
    query_alt = f"""
    [out:json];
    node(around:{radius},{lat},{lon})["alt_name"="{summit_name}"];
    out body;
    """
    response_alt = requests.get(url, params={"data": query_alt})
    time.sleep(1)

    if response_alt.status_code == 200:
        data_alt = response_alt.json()
        if "elements" in data_alt and len(data_alt["elements"]) > 0:
            return int(data_alt["elements"][0]["id"])  # Return the first matching node ID using alt_name

    return None

# Load summit data from csv
df = pd.read_csv("summits.csv", encoding="utf-8")

# Prepare results list
results = []

# Loop through summits and query Overpass
for index, row in df.iterrows():
    node_id = query_overpass(row["Latitude"], row["Longitude"], row["SummitName"])
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
results_df.to_csv("osm_summit_nodes.csv", index=False)

print("Done! Results saved to osm_summit_nodes.csv")
