import csv
import random
import os

# --- Configuration ---
SOURCE_FILE_DIR = "apestudio/list" # Relative to the script's location
SOURCE_FILE_NAME = "cardList.csv"
OUTPUT_FILE_NAME = "metadata.csv"
TOTAL_NFTS = 1111

# Columns to select from the source CSV
COLUMNS_TO_SELECT = ["Card Id", "Name", "Bitcoin Text", "Sticker"]

RARITY_LEVELS = {
    "Common": 0.40,
    "Uncommon": 0.30,
    "Rare": 0.15,
    "Super Rare": 0.10,
    "Ultra Rare": 0.04,
    "Legendary": 0.01
}

# Ensure the order of FORTUNE_ATTRIBUTES matches the intended mapping to RARITY_LEVELS keys
# For example, Common maps to 1B, Uncommon to 5B, etc.
FORTUNE_ATTRIBUTES_ORDERED_BY_RARITY = [
    "1B in Bitcoin",  # Corresponds to Common
    "5B in Bitcoin",  # Corresponds to Uncommon
    "10B in Bitcoin", # Corresponds to Rare
    "2B in Bitcoin",  # Corresponds to Super Rare (Note: User spec had 2B here, might intend different value or order)
    "50B in Bitcoin", # Corresponds to Ultra Rare
    "100B in Bitcoin" # Corresponds to Legendary
]

POWER_RANGE = (1, 10)

# --- Helper Functions ---
def calculate_proportional_counts(proportions_dict, total_items):
    """Calculates counts for each category, ensuring they sum to total_items."""
    names = list(proportions_dict.keys())
    proportions = list(proportions_dict.values())
    
    counts = [int(p * total_items) for p in proportions]
    current_sum = sum(counts)
    remainder = total_items - current_sum
    
    # Distribute remainder: add to categories one by one, starting from the most frequent
    # This is a simple way; more complex logic could distribute based on fractional parts lost
    # Create a list of (original_proportion, index) to sort by proportion for remainder distribution
    sorted_indices_for_remainder = sorted(range(len(proportions)), key=lambda k: proportions[k], reverse=True)
    
    for i in range(remainder):
        counts[sorted_indices_for_remainder[i % len(sorted_indices_for_remainder)]] += 1

    # Final check if sum is still off (should be rare with the above method)
    if sum(counts) != total_items:
        diff = total_items - sum(counts)
        if counts and diff != 0:
            # Add/subtract difference from the category with the largest original proportion
            idx_max_prop = proportions.index(max(proportions))
            counts[idx_max_prop] += diff
            
    return dict(zip(names, counts))

def read_source_data(file_path, columns_to_select):
    """Reads specific columns from the source CSV file."""
    selected_header = []
    selected_data_rows = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            full_header = next(reader, None)
            if not full_header:
                print(f"Warning: Source file {file_path} is empty or header could not be read.")
                return [], [] # Return empty if no header

            # Find indices of the columns we want to select
            column_indices = {}
            for col_name in columns_to_select:
                try:
                    column_indices[col_name] = full_header.index(col_name)
                except ValueError:
                    print(f"Warning: Column '{col_name}' not found in header of {file_path}.")
            
            if not column_indices:
                print(f"Error: None of the specified columns to select were found in {file_path}. Header: {full_header}")
                return [], []
                
            # Create the selected header based on the order in columns_to_select
            selected_header = [col for col in columns_to_select if col in column_indices]

            for row in reader:
                if any(field.strip() for field in row):
                    selected_row_data = []
                    for col_name in selected_header: # Iterate in the desired order
                        idx = column_indices[col_name]
                        if idx < len(row):
                            selected_row_data.append(row[idx])
                        else:
                            selected_row_data.append("") # Append empty string if row is shorter than expected
                            print(f"Warning: Row in {file_path} is shorter than expected for column '{col_name}'. Row: {row}")
                    selected_data_rows.append(selected_row_data)
            
            if not selected_data_rows and selected_header:
                 print(f"Warning: Source file {file_path} contained a header matching some selected columns, but no data rows.")

    except FileNotFoundError:
        print(f"Error: Source file {file_path} not found.")
        return None, None 
    except Exception as e:
        print(f"Error reading source file {file_path}: {e}")
        return None, None 

    return selected_header, selected_data_rows

# --- Main Logic ---
def generate_metadata():
    workspace_root = os.getcwd()
    source_file_full_path = os.path.join(workspace_root, SOURCE_FILE_DIR, SOURCE_FILE_NAME)
    
    print(f"Attempting to read source file from: {source_file_full_path}")
    # Pass COLUMNS_TO_SELECT to the reading function
    original_selected_header, original_selected_data_rows = read_source_data(source_file_full_path, COLUMNS_TO_SELECT)

    if original_selected_data_rows is None: # Critical error like FileNotFoundError
        print("Halting script due to error reading source file.")
        return
    
    if not original_selected_header:
        print("Warning: No header columns could be selected from the source file. Check column names in COLUMNS_TO_SELECT.")
        # If no original data can be processed, proceed generating NFTs with only new metadata.
        # original_selected_header will be empty, and original_selected_data_rows will be empty lists.

    if not original_selected_data_rows:
        print("Warning: No data rows read (or selected) from source file. Metadata will be generated without these original card data columns.")
        # Proceed with generating NFTs, but they will only have nftId, Rarity, Fortune, Power if header was also empty

    expanded_base_data = []
    if original_selected_data_rows:
        for row in original_selected_data_rows:
            expanded_base_data.extend([row] * 10)
        random.shuffle(expanded_base_data)
    
    current_total_nfts = TOTAL_NFTS
    final_base_data = []

    if expanded_base_data:
        if len(expanded_base_data) < TOTAL_NFTS:
            print(f"Warning: After duplicating selected data 10x, there are {len(expanded_base_data)} rows, "
                  f"less than the required {TOTAL_NFTS}. Output will be {len(expanded_base_data)} NFTs long.")
            final_base_data = expanded_base_data
            current_total_nfts = len(expanded_base_data)
        else:
            final_base_data = expanded_base_data[:TOTAL_NFTS]
    else: # No original data to expand, create empty lists for the base data part
        final_base_data = [[] for _ in range(TOTAL_NFTS)] # Each base data part is an empty list
        if not original_selected_data_rows:
             print(f"Proceeding to generate {TOTAL_NFTS} NFTs with only new metadata columns as source data was empty or not selectable.")

    if current_total_nfts == 0:
        print("Error: No NFTs to generate (current_total_nfts is 0). Check source data and TOTAL_NFTS config. Exiting.")
        return

    nft_ids = list(range(1, current_total_nfts + 1))

    rarity_counts = calculate_proportional_counts(RARITY_LEVELS, current_total_nfts)
    rarity_values = []
    rarity_category_names_ordered = list(RARITY_LEVELS.keys())
    for level in rarity_category_names_ordered:
        rarity_values.extend([level] * rarity_counts.get(level, 0))
    random.shuffle(rarity_values)

    if len(rarity_values) != current_total_nfts:
        print(f"Warning: Rarity values length ({len(rarity_values)}) mismatch with total NFTs ({current_total_nfts}). Adjusting.")
        padding_needed = current_total_nfts - len(rarity_values)
        if padding_needed > 0:
            most_common_rarity = rarity_category_names_ordered[0] 
            rarity_values.extend([most_common_rarity] * padding_needed)
        else:
            rarity_values = rarity_values[:current_total_nfts]

    fortune_mapping = dict(zip(rarity_category_names_ordered, FORTUNE_ATTRIBUTES_ORDERED_BY_RARITY))
    fortune_values = []
    for rarity_level in rarity_category_names_ordered:
        count = rarity_counts.get(rarity_level, 0)
        fortune_attr = fortune_mapping.get(rarity_level, "Default Fortune")
        fortune_values.extend([fortune_attr] * count)
    random.shuffle(fortune_values)

    if len(fortune_values) != current_total_nfts:
        print(f"Warning: Fortune values length ({len(fortune_values)}) mismatch with total NFTs ({current_total_nfts}). Adjusting.")
        padding_needed = current_total_nfts - len(fortune_values)
        if padding_needed > 0:
            default_fortune = FORTUNE_ATTRIBUTES_ORDERED_BY_RARITY[0]
            fortune_values.extend([default_fortune] * padding_needed)
        else:
            fortune_values = fortune_values[:current_total_nfts]

    power_values = [random.randint(POWER_RANGE[0], POWER_RANGE[1]) for _ in range(current_total_nfts)]

    # The header for the output CSV
    output_header = ["nftId", "Rarity", "Fortune", "Power"] + original_selected_header
    
    output_file_full_path = os.path.join(workspace_root, OUTPUT_FILE_NAME)
    print(f"Writing output to: {output_file_full_path}")

    with open(output_file_full_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(output_header)
        
        for i in range(current_total_nfts):
            base_data_for_row = final_base_data[i] if i < len(final_base_data) else []
            current_rarity = rarity_values[i] if i < len(rarity_values) else rarity_category_names_ordered[0]
            current_fortune = fortune_values[i] if i < len(fortune_values) else FORTUNE_ATTRIBUTES_ORDERED_BY_RARITY[0]
            current_power = power_values[i] if i < len(power_values) else POWER_RANGE[0]
            
            row_to_write = [
                nft_ids[i],
                current_rarity,
                current_fortune,
                current_power
            ] + base_data_for_row # base_data_for_row now contains only the selected columns
            writer.writerow(row_to_write)
            
    print(f"Successfully generated {OUTPUT_FILE_NAME} with {current_total_nfts} NFTs.")

if __name__ == "__main__":
    # Note: The dummy file creation part is commented out. 
    # User needs to ensure apestudio/list/cardList.py exists.
    # Example for testing (if you want to enable it for a quick test without real file):
    # if not os.path.exists(os.path.join(os.getcwd(), SOURCE_FILE_DIR)):
    #     os.makedirs(os.path.join(os.getcwd(), SOURCE_FILE_DIR))
    # dummy_source_path = os.path.join(os.getcwd(), SOURCE_FILE_DIR, SOURCE_FILE_NAME)
    # if not os.path.exists(dummy_source_path):
    #     print(f"Creating dummy {SOURCE_FILE_NAME} for testing purposes.")
    #     with open(dummy_source_path, 'w', newline='') as f_dummy:
    #         f_dummy.write("card_name,card_type\n")
    #         # Need enough lines so 10x is >= TOTAL_NFTS
    #         num_dummy_cards = (TOTAL_NFTS // 10) + 1 
    #         for i_dummy in range(1, num_dummy_cards + 1):
    #             f_dummy.write(f"DummyCard_{i_dummy:03},TypeX\n")
                
    generate_metadata() 