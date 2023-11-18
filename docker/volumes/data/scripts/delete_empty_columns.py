import csv

def remove_rows(input_csv, output_csv, delimiter=';'):
    with open(input_csv, 'r', newline='') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter=delimiter)
        fieldnames = reader.fieldnames

        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()

        for row in reader:
            filtered_row = {key: row[key] for key in fieldnames if key in row}
            
            if all(filtered_row.values()):
                writer.writerow(filtered_row)

remove_rows('../dataset_wt_country.csv', '../data.csv')
