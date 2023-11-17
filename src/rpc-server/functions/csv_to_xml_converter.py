import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET
from csv import DictReader

from entities.country import Country
from entities.brand import Brand
from entities.model import Model
from entities.fuel import Fuel
from entities.size import Size
from entities.style import Style
from entities.traction import Traction
from entities.transmission import Transmission

from entities.category import MarketCategoryItem
from entities.vehicle import Vehicle


class CSVReader:
    def __init__(self, path, delimiter=';'):
        self._path = path
        self._delimiter = delimiter

    def loop(self):
        with open(self._path, 'r') as file:
            for row in DictReader(file, delimiter=self._delimiter):
                yield row

    def read_entities(self, attr, builder, after_create=None):
        entities = {}
        for row in self.loop():
            if attr in row:
                e = row[attr]
                if e not in entities:
                    entities[e] = builder(row)
                    if after_create is not None:
                        after_create(entities[e], row)
        return entities
    
class CSVtoXMLConverter:

    def __init__(self, path):
        self.csv_reader = CSVReader(path)

    def to_xml(self):
        # read countries
        countries = self.csv_reader.read_entities(
            attr="Country",
            builder=lambda row: Country(row["Country"])
        )

        # read brands
        brands = self.csv_reader.read_entities(
            attr="Brand",
            builder=lambda row: Brand(row["Brand"], countries[row["Country"]])
        )

        models = {}

        # read models
        def after_creating_model(model, row):
            brands[row["Brand"]].add_model(model)
            models[row["Model"]] = model

        models = self.csv_reader.read_entities(
            attr="Model",
            builder=lambda row: Model(
                name=row["Model"]
            ),
            after_create=after_creating_model
        )

        # read fuels
        fuels = self.csv_reader.read_entities(
            attr="Engine Fuel Type",
            builder=lambda row: Fuel(row["Engine Fuel Type"])
        )

        # read sizes
        sizes = self.csv_reader.read_entities(
            attr="Vehicle Size",
            builder=lambda row: Size(row["Vehicle Size"])
        )

        # read styles
        styles = self.csv_reader.read_entities(
            attr="Vehicle Style",
            builder=lambda row: Style(row["Vehicle Style"])
        )

        # read traction
        tractions = self.csv_reader.read_entities(
            attr="Driven Wheels",
            builder=lambda row: Traction(row["Driven Wheels"])
        )

        # read transmission
        transmissions = self.csv_reader.read_entities(
            attr="Transmission Type",
            builder=lambda row: Transmission(row["Transmission Type"])
        )

        # read categories
        categories = self.csv_reader.read_entities(
            attr="Market Category",
            builder=lambda row: row["Market Category"].split(",") if row["Market Category"] else [],
            after_create=None
        )

        # read vehicles
        vehicles = self.csv_reader.read_entities(
            attr="Model",
            builder=lambda row: Vehicle(
                brand=brands[row["Brand"]],
                model=models[row["Model"]],
                year=row.get("Year", ""),  # Adiciona uma verificação para a chave "Year"
                engine_fuel_type=fuels.get(row["Engine Fuel Type"], ""),  # Adiciona uma verificação para a chave "Engine Fuel Type"
                engine_hp=row.get("Engine HP", ""),  # Adiciona uma verificação para a chave "Engine HP"
                engine_cylinders=row.get("Engine Cylinders", ""),  # Adiciona uma verificação para a chave "Engine Cylinders"
                transmission_type=transmissions.get(row["Transmission Type"], ""),  # Adiciona uma verificação para a chave "Transmission Type"
                driven_wheels=tractions.get(row["Driven Wheels"], ""),  # Adiciona uma verificação para a chave "Driven Wheels"
                number_of_doors=row.get("Number of Doors", ""),  # Adiciona uma verificação para a chave "Number of Doors"
                market_category=row.get("Market Category", "").split(",") if row.get("Market Category") else [],  # Adiciona uma verificação para a chave "Market Category"
                vehicle_size=sizes.get(row["Vehicle Size"], ""),  # Adiciona uma verificação para a chave "Vehicle Size"
                vehicle_style=styles.get(row["Vehicle Style"], ""),  # Adiciona uma verificação para a chave "Vehicle Style"
                highway_mpg=row.get("Highway MPG", ""),  # Adiciona uma verificação para a chave "Highway MPG"
                city_mpg=row.get("City MPG", ""),  # Adiciona uma verificação para a chave "City MPG"
                popularity=row.get("Popularity", ""),  # Adiciona uma verificação para a chave "Popularity"
                msrp=row.get("MSRP", ""),  # Adiciona uma verificação para a chave "MSRP"
                country=countries.get(row["Country"], "")  # Adiciona uma verificação para a chave "Country"
            )
        )

        root_el = ET.Element("Data")

        brands_el = ET.Element("Brands")
        for brand in brands.values():
            brands_el.append(brand.to_xml())

        countries_el = ET.Element("Countries")
        for country in countries.values():
            countries_el.append(country.to_xml())
        
        fuels_el = ET.Element("Fuels")
        for fuel in fuels.values():
            fuels_el.append(fuel.to_xml())

        sizes_el = ET.Element("Sizes")
        for size in sizes.values():
            sizes_el.append(size.to_xml())

        styles_el = ET.Element("Styles")
        for style in styles.values():
            styles_el.append(style.to_xml())

        tractions_el = ET.Element("Tractions")
        for traction in tractions.values():
            tractions_el.append(traction.to_xml())

        transmissions_el = ET.Element("Transmissions")
        for transmission in transmissions.values():
            transmissions_el.append(transmission.to_xml())

        categories_el = ET.Element("Categories")
        unique_categories = set()
        for category_list in categories.values():
            for category_name in category_list:
                if category_name not in unique_categories:
                    category_el = ET.Element("market_category")
                    category_el.set("id", str(len(unique_categories) + 1))
                    category_el.set("Name", category_name)
                    categories_el.append(category_el)
                    unique_categories.add(category_name)

        vehicles_el = ET.Element("Vehicles")
        for vehicle in vehicles.values():
            vehicles_el.append(vehicle.to_xml())

        root_el.append(brands_el)
        root_el.append(countries_el)
        root_el.append(fuels_el)
        root_el.append(sizes_el)
        root_el.append(styles_el)
        root_el.append(tractions_el)
        root_el.append(transmissions_el)
        root_el.append(categories_el)
        
        root_el.append(vehicles_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()

    def save_xml(self, filename):
        with open(filename, 'w') as file:
            file.write(self.to_xml_str())