import csv
import os
import shutil

# Define paths
SOURCE_CSV_FILE = os.path.join('apestudio', 'list', 'apesnftlist.csv')
SOURCE_IMAGES_DIR = os.path.join('apestudio', 'list', 'monkeyCards')
DEST_IMAGES_DIR = os.path.join('apestudio', 'list', 'monkeyNfts')

def copy_and_rename_images():
    """
    Reads cardId and fileName from apesnftlist.csv,
    copies images from monkeyCards, and renames them in monkeyNfts.
    """
    # Create destination directory if it doesn't exist
    if not os.path.exists(DEST_IMAGES_DIR):
        os.makedirs(DEST_IMAGES_DIR)
        print(f"Created directory: {DEST_IMAGES_DIR}")

    copied_count = 0
    error_count = 0

    try:
        with open(SOURCE_CSV_FILE, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            if 'cardId' not in reader.fieldnames or 'fileName' not in reader.fieldnames:
                print(f"Error: 'cardId' or 'fileName' column not found in {SOURCE_CSV_FILE}")
                return

            for row in reader:
                try:
                    card_id = row['cardId']
                    file_name = row['fileName']

                    if not card_id or not file_name:
                        print(f"Warning: Missing cardId or fileName in row: {row}")
                        error_count += 1
                        continue

                    # Handle the special case for cardId '85'
                    if card_id == '85':
                        source_image_name = '085.webp'
                    else:
                        source_image_name = f"{card_id}.webp"
                    
                    source_image_path = os.path.join(SOURCE_IMAGES_DIR, source_image_name)
                    
                    destination_image_path = os.path.join(DEST_IMAGES_DIR, file_name)

                    if os.path.exists(source_image_path):
                        shutil.copy2(source_image_path, destination_image_path)
                        # print(f"Copied {source_image_path} to {destination_image_path}")
                        copied_count += 1
                    else:
                        print(f"Error: Source image not found: {source_image_path}")
                        error_count += 1
                
                except Exception as e:
                    print(f"Error processing row {row}: {e}")
                    error_count += 1

        print(f"\nScript finished.")
        print(f"Successfully copied {copied_count} images.")
        if error_count > 0:
            print(f"Encountered {error_count} errors/warnings.")

    except FileNotFoundError:
        print(f"Error: Source CSV file not found: {SOURCE_CSV_FILE}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    copy_and_rename_images() 