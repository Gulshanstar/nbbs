import csv
import json
import os

def extract_all_values_from_json(json_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        return data

def update_csv(csv_file, json_folder):
    all_keys = set()  # Set to store all unique keys from JSON files
    output_rows = []

    # Extract all keys from JSON files
    for json_file in os.listdir(json_folder):
        json_path = os.path.join(json_folder, json_file)
        if os.path.isfile(json_path) and json_file.endswith('.json'):
            json_data = extract_all_values_from_json(json_path)
            all_keys.update(json_data.keys())

    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            post_order_id = row['postOrderId']
            json_filename = post_order_id + '.json'
            json_path = os.path.join(json_folder, json_filename)
            if os.path.exists(json_path):
                print(f"Processing JSON file: {json_path}")
                json_data = extract_all_values_from_json(json_path)
                for key in all_keys:
                    row[key] = json_data.get(key, '')  # Add value to row, or empty string if key not present
            else:
                print(f"JSON file not found for {post_order_id}: {json_path}")
            output_rows.append(row)

    output_file = os.path.join(os.path.dirname(csv_file), 'updated_' + os.path.basename(csv_file))
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = list(output_rows[0].keys())  # Use keys from first row as fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Updated CSV written to: {output_file}")

if __name__ == "__main__":
    csv_file = r'/home/gulshan/Downloads/Book.csv'
    json_folder = r'/home/gulshan/Desktop/apna/'  # Provide the path to your JSON folder
    update_csv(csv_file, json_folder)
