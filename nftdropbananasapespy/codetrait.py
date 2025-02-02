import csv

start_id = 357

with open('C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\apespy\\apeslisthold.csv', "r") as input_file, open('C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\nftdropbananasapespy\\clarCodeTrait.csv', 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)
    for row in reader:
        addy = ",".join(row)
        current_id = f"{start_id:01d}"
        text = f"(bananas u{current_id} '{addy}".rstrip(";")
        linecodes = ((text) + ")")
        writer.writerow([linecodes])
        start_id += 1

print("Processing complete!")