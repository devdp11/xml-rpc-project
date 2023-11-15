import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from csv_reader import CSVReader
from entities.brand import Brand  # Certifique-se de importar a classe Brand ou ajustar conforme necessário
from entities.country import Country
from entities.model import Model


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):
        # read countries
        countries = self._reader.read_entities(
            attr="Country",
            builder=lambda row: Country(row["Country"])
        )

        # read brands
        brands = self._reader.read_entities(
            attr="Brand",
            builder=lambda row: Brand(row["Brand"], countries[row["Country"]])
        )

        # read models

        def after_creating_model(model, row):
            brands[row["Brand"]].add_model(model)

        self._reader.read_entities(
            attr="Model",
            builder=lambda row: Model(
                name=row["Model"]
            ),
            after_create=after_creating_model
        )

        root_el = ET.Element("VehicleData")

        brands_el = ET.Element("Brands")
        for brand in brands.values():
            brands_el.append(brand.to_xml())

        countries_el = ET.Element("Countries")
        for country in countries.values():
            countries_el.append(country.to_xml())

        root_el.append(brands_el)
        root_el.append(countries_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()
