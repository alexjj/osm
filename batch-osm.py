import csv

# Function to read CSV and get OSM_Node_IDs
def read_osm_node_ids(csv_file):
    osm_node_ids = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            osm_node_ids.append(row['OSM_Node_ID'])
    return osm_node_ids

# Function to create the Overpass API query text
def create_overpass_query(node_ids):
    node_ids_str = ",".join(node_ids)
    return f"node(id:{node_ids_str});out meta;"

# Function to save query text to a file
def save_query_to_file(query_text, batch_number):
    with open(f"batch-{batch_number}.txt", 'w') as file:
        file.write(query_text)

# Main function to process CSV, generate query text, and save to files
def process_batches(csv_file):
    osm_node_ids = read_osm_node_ids(csv_file)

    # Split into batches of 100
    batch_size = 100
    for i in range(0, len(osm_node_ids), batch_size):
        batch_ids = osm_node_ids[i:i+batch_size]
        query_text = create_overpass_query(batch_ids)

        # Save the query text to a file
        batch_number = (i // batch_size) + 1
        save_query_to_file(query_text, batch_number)
        print(f"Batch {batch_number} saved as batch-{batch_number}.txt")

# Example Usage
csv_file = 'uk_summit_nodes.csv'  # Replace with your actual CSV file path
process_batches(csv_file)
