import csv
import pathlib # For potential path manipulation, though not strictly used in open()

# --- Configuration Constants ---
# Initial value for the incrementing ID
INITIAL_ID = 4

# File paths (consider making these relative or configurable for better portability)
INPUT_CSV_FILE_PATH = 'C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\tlbpy\\tlbhlist.csv'
OUTPUT_CSV_FILE_PATH = 'C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\nftdropbananaspy\\clarCodeTrait.csv'

# Formatting for the ID string (e.g., "{:02d}" for 2-digit padding like "04", "10")
# The original used "{:01d}", which is like str(); using "{:02d}" as a common improvement.
ID_NUMBER_FORMAT = "{:02d}" 

# --- Core Logic Functions ---

def generate_output_line(id_value, csv_row_elements):
    """
    Generates a single formatted line for the output CSV.
    
    Args:
        id_value (int): The current ID number.
        csv_row_elements (list): A list of strings from a CSV row.
                                 These will be joined by a comma.
    
    Returns:
        str: The formatted output line.
    """
    # Format the ID (e.g., 4 -> "04" if ID_NUMBER_FORMAT is "{:02d}")
    formatted_id_str = ID_NUMBER_FORMAT.format(id_value)
    
    # Join elements from the CSV row to form the address string
    address_string = ",".join(csv_row_elements)
    
    # Remove any trailing semicolon from the address string
    cleaned_address_string = address_string.rstrip(";")
    
    # Construct the final output line string
    # Example format: (bananas u04 'cleaned_address_data')
    return f"(bananas u{formatted_id_str} '{cleaned_address_string}')"

def process_csv_data(input_file_path_str, output_file_path_str, start_id_val):
    """
    Reads from an input CSV, processes each row, and writes to an output CSV.
    """
    current_id = start_id_val
    
    try:
        # Using 'utf-8' encoding as a good practice for text files
        # Using newline='' for both reader and writer to correctly handle CSV line endings
        with open(input_file_path_str, mode="r", newline='', encoding='utf-8') as input_file, \
             open(output_file_path_str, mode='w', newline='', encoding='utf-8') as output_file:
            
            csv_reader = csv.reader(input_file)
            csv_writer = csv.writer(output_file)
            
            for row_elements in csv_reader:
                # Skip empty rows if they might occur
                if not row_elements:
                    continue
                
                # Generate the formatted line for the current row and ID
                line_to_write = generate_output_line(current_id, row_elements)
                
                # Write the line to the output CSV (writerow expects a list/iterable)
                csv_writer.writerow([line_to_write])
                
                # Increment the ID for the next row
                current_id += 1
        
        print("Processing complete!")
        print(f"Output successfully written to: {output_file_path_str}")

    except FileNotFoundError:
        print(f"Error: The input file was not found at '{input_file_path_str}'")
    except Exception as e:
        print(f"An unexpected error occurred during CSV processing: {e}")

# --- Main Execution ---

def main_script_runner():
    """
    Main function to set up and run the CSV processing task.
    """
    # Optional: Convert string paths to pathlib.Path objects if more complex path operations were needed
    # input_path_obj = pathlib.Path(INPUT_CSV_FILE_PATH)
    # output_path_obj = pathlib.Path(OUTPUT_CSV_FILE_PATH)
    
    process_csv_data(INPUT_CSV_FILE_PATH, OUTPUT_CSV_FILE_PATH, INITIAL_ID)

if __name__ == "__main__":
    main_script_runner()