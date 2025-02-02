import csv

start_id = 29

with open('C:\\Users\\jhosephethierry\\Documents\\Bird\python\\nftdropy\\beanspassmints.csv', "r") as input_file, open('C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\nftdropy\\clarCodeTrait.csv', 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)
    for row in reader:
        addy = ",".join(row)
        current_id = f"{start_id:01d}"
        text = f"(drop u{current_id} '{addy}".rstrip(";")
        linecodes = ((text) + ")")
        writer.writerow([linecodes])
        start_id += 1

print("Processing complete!")