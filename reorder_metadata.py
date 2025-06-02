import csv
import os

INPUT_FILENAME = "metadata.csv"
OUTPUT_FILENAME = "apes.csv"
NEW_COLUMN_ORDER = ["nftId", "Card Id", "Name", "Bitcoin Text", "Sticker", "Fortune", "Power", "Rarity"]

def reorder_csv_columns():
    workspace_root = os.getcwd()
    input_filepath = os.path.join(workspace_root, INPUT_FILENAME)
    output_filepath = os.path.join(workspace_root, OUTPUT_FILENAME)

    try:
        with open(input_filepath, 'r', newline='', encoding='utf-8') as infile, \
             open(output_filepath, 'w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            header = next(reader, None)
            if not header:
                print(f"Error: The input file '{INPUT_FILENAME}' is empty or has no header.")
                return

            writer.writerow(NEW_COLUMN_ORDER)

            col_indices_map = {}
            for col_name in NEW_COLUMN_ORDER:
                try:
                    col_indices_map[col_name] = header.index(col_name)
                except ValueError:
                    print(f"Warning: Column '{col_name}' specified in new order not found in '{INPUT_FILENAME}' header. It will be missing in '{OUTPUT_FILENAME}'.")
                    col_indices_map[col_name] = None

            for row in reader:
                reordered_row = []
                for col_name in NEW_COLUMN_ORDER:
                    old_index = col_indices_map.get(col_name)
                    if old_index is not None and old_index < len(row):
                        reordered_row.append(row[old_index])
                    else:
                        reordered_row.append("") 
                writer.writerow(reordered_row)
            
            print(f"Successfully reordered columns from '{INPUT_FILENAME}' to '{OUTPUT_FILENAME}'.")

    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_FILENAME}' not found in '{workspace_root}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    reorder_csv_columns() 