import csv
import json

with open('../car_brands.json', 'r', encoding='utf-8') as json_file:
    brand_country_map = json.load(json_file)

with open('../dataset_wt_country.csv', mode='r', newline='', encoding='utf-8') as input_file, open('../data.csv', mode='w', newline='', encoding='utf-8') as output_file:
    reader = csv.DictReader(input_file, delimiter=';')
    fieldnames = reader.fieldnames + ['Country']

    writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()

    for row in reader:
        brand = row['Brand']

        country = brand_country_map.get(brand, 'Unknown')

        row['Country'] = country
        writer.writerow(row)

print("Column 'Country' added to output arquive.")