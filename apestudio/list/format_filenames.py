import csv
import os

CSV_FILE_PATH = os.path.join('apestudio', 'list', 'apesnftlist.csv')

def format_filenames_in_csv():
    """
    Reads apesnftlist.csv, reformats the fileName column to have 4-digit numbers
    (e.g., 1.webp -> 0001.webp), and writes the changes back to the file.
    """
    if not os.path.exists(CSV_FILE_PATH):
        print(f"Error: File not found: {CSV_FILE_PATH}")
        return

    rows = []
    header = []
    processed_count = 0
    error_count = 0

    try:
        with open(CSV_FILE_PATH, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader) # Read the header
            rows.append(header) # Add header to be written back
            
            try:
                filename_col_index = header.index('fileName')
            except ValueError:
                print(f"Error: 'fileName' column not found in {CSV_FILE_PATH}")
                return

            for row_data in reader:
                if not row_data: # Skip empty rows
                    continue
                try:
                    original_filename = row_data[filename_col_index]
                    if '.' not in original_filename or not original_filename.endswith('.webp'):
                        print(f"Warning: Skipping row with unexpected fileName format: {original_filename} in row: {row_data}")
                        rows.append(row_data) # Add row as is
                        error_count += 1
                        continue

                    base_name, extension = original_filename.rsplit('.', 1)
                    
                    if not base_name.isdigit():
                        print(f"Warning: Skipping row, numeric part of fileName is not a digit: {original_filename} in row: {row_data}")
                        rows.append(row_data) # Add row as is
                        error_count += 1
                        continue
                        
                    number_part = int(base_name)
                    new_filename_base = f"{number_part:04d}"
                    new_filename = f"{new_filename_base}.{extension}"
                    
                    row_data[filename_col_index] = new_filename
                    rows.append(row_data)
                    processed_count += 1
                except IndexError:
                    print(f"Warning: Skipping malformed row (not enough columns): {row_data}")
                    error_count += 1
                    # Decide if you want to add malformed rows back or skip them
                    # rows.append(row_data) 
                except Exception as e:
                    print(f"Error processing row {row_data}: {e}")
                    rows.append(row_data) # Add row as is to preserve data
                    error_count += 1
        
        # Write the modified data back to the CSV file
        with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

        print(f"\nScript finished.")
        print(f"Successfully processed and updated {processed_count} filenames.")
        if error_count > 0:
            print(f"Encountered {error_count} warnings/errors for rows that might not have been updated as expected.")

    except FileNotFoundError:
        print(f"Error: Source CSV file not found during read: {CSV_FILE_PATH}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    format_filenames_in_csv() 