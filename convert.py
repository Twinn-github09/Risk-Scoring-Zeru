import json
import pandas as pd
import os

# Folder containing JSON files
json_folder_path = "g:/projects/Zeru"
output_folder_path = "g:/projects/Zeru/csv_output"

# Ensure the output folder exists
os.makedirs(output_folder_path, exist_ok=True)

# Dictionary to hold dataframes for each transaction type
combined_data = {}

# Iterate through all JSON files in the folder
for file_name in os.listdir(json_folder_path):
    if file_name.endswith(".json"):
        json_file_path = os.path.join(json_folder_path, file_name)
        
        # Load the JSON file
        with open(json_file_path, "r") as f:
            data = json.load(f)

        for tx_type in data:
            records = data[tx_type]
            if records:  # Skip if empty
                df = pd.json_normalize(records)
                if tx_type not in combined_data:
                    combined_data[tx_type] = df
                else:
                    combined_data[tx_type] = pd.concat([combined_data[tx_type], df], ignore_index=True)
            else:
                print(f"No data found for {tx_type} in {file_name}, skipping.")

# Save combined dataframes to CSV files
for tx_type, df in combined_data.items():
    csv_file_path = os.path.join(output_folder_path, f"{tx_type}_combined.csv")
    df.to_csv(csv_file_path, index=False)
    print(f"Saved combined {tx_type} data to {csv_file_path}")
