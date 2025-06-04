import csv
import json
import os

CSV_FILE_PATH = os.path.join('apestudio', 'list', 'apesnftlist.csv')
JSON_OUTPUT_PATH = os.path.join('apestudio', 'list', 'apes_metadata.json')

def convert_csv_to_json():
    """
    Converts data from apesnftlist.csv to a structured JSON file.
    The meta.name field will include a cycling sequence number (1-10)
    based on the occurrences of each cardId.
    """
    if not os.path.exists(CSV_FILE_PATH):
        print(f"Error: CSV file not found at {CSV_FILE_PATH}")
        return

    json_data_list = []
    card_id_counters = {} # To track the sequence for each cardId

    try:
        with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            if not reader.fieldnames:
                print(f"Error: CSV file {CSV_FILE_PATH} is empty or has no header.")
                return

            required_columns = ['fileName', 'name', 'nftId', 'cardId', 'bitcoinText', 'sticker', 'fortune', 'power', 'rarity']
            missing_columns = [col for col in required_columns if col not in reader.fieldnames]
            if missing_columns:
                print(f"Error: Missing required columns in CSV: {', '.join(missing_columns)}")
                return

            for row in reader:
                try:
                    current_card_id = row.get('cardId', '').strip()
                    original_name = row.get('name', '').strip()

                    if not current_card_id:
                        print(f"Warning: Skipping row due to missing or empty cardId: {row}")
                        continue
                    if not original_name:
                         print(f"Warning: Skipping row due to missing or empty name for cardId {current_card_id}: {row}")
                         continue


                    # Increment counter for the current cardId
                    card_id_counters[current_card_id] = card_id_counters.get(current_card_id, 0) + 1
                    
                    # Calculate sequence number (1-10, cycling)
                    sequence_num = ((card_id_counters[current_card_id] - 1) % 10) + 1
                    
                    meta_name = f"{original_name} #{sequence_num}"

                    attributes = [
                        {"trait_type": "nftId", "value": row.get('nftId', '')},
                        {"trait_type": "name", "value": original_name},
                        {"trait_type": "cardId", "value": current_card_id},
                        {"trait_type": "bitcoinText", "value": row.get('bitcoinText', '')},
                        {"trait_type": "sticker", "value": row.get('sticker', '')},
                        {"trait_type": "fortune", "value": row.get('fortune', '')},
                        {"trait_type": "power", "value": row.get('power', '')},
                        {"trait_type": "rarity", "value": row.get('rarity', '')}
                    ]
                    
                    # Filter out attributes where value might be None from a missing column in a row (though header check exists)
                    # or if explicitly empty and you want to exclude them.
                    # For this implementation, we keep them as empty strings if CSV has empty values for them.
                    # attributes = [attr for attr in attributes if attr['value'] is not None]


                    json_entry = {
                        "file": row.get('fileName', ''),
                        "meta": {
                            "name": meta_name,
                            "attributes": attributes
                        }
                    }
                    json_data_list.append(json_entry)

                except Exception as e:
                    print(f"Error processing row: {row}. Error: {e}")
                    continue # Skip rows that cause an error

        if not json_data_list:
            print("No data processed. Output JSON will be empty or not created.")
            return

        # Write the JSON data to file
        output_dir = os.path.dirname(JSON_OUTPUT_PATH)
        if not os.path.exists(output_dir) and output_dir: # Ensure output_dir is not an empty string
             os.makedirs(output_dir)
             print(f"Created directory: {output_dir}")
             
        with open(JSON_OUTPUT_PATH, 'w', encoding='utf-8') as jsonfile:
            json.dump(json_data_list, jsonfile, indent=2) # indent=2 for pretty printing

        print(f"Successfully converted CSV to JSON. Output saved to: {JSON_OUTPUT_PATH}")
        print(f"Total entries processed: {len(json_data_list)}")

    except FileNotFoundError:
        print(f"Error: Could not find the CSV file at {CSV_FILE_PATH}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    convert_csv_to_json() 