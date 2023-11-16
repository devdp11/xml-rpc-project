import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from csv_reader import CSVReader
from entities.country import Country
from entities.brand import Brand
from entities.model import Model
from entities.fuel import Fuel
from entities.size import Size
from entities.style import Style
from entities.traction import Traction
from entities.transmission import Transmission

from entities.category import MarketCategoryItem


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):
        # read countries
        countries = self._reader.read_entities(
            attr="Country",
            builder=lambda row: Country(row["Country"])
        )

        # read sizes
        fuels = self._reader.read_entities(
            attr="Engine Fuel Type",
            builder=lambda row: Fuel(row["Engine Fuel Type"])
        )

        # read sizes
        sizes = self._reader.read_entities(
            attr="Vehicle Size",
            builder=lambda row: Size(row["Vehicle Size"])
        )

        # read styles
        styles = self._reader.read_entities(
            attr="Vehicle Style",
            builder=lambda row: Style(row["Vehicle Style"])
        )

        # read traction
        tractions = self._reader.read_entities(
            attr="Driven Wheels",
            builder=lambda row: Traction(row["Driven Wheels"])
        )

        # read transmission
        transmissions = self._reader.read_entities(
            attr="Transmission Type",
            builder=lambda row: Transmission(row["Transmission Type"])
        )

        # read categories
        categories = self._reader.read_entities(
            attr="Market Category",
            builder=lambda row: MarketCategoryItem(row["Market Category"])
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
        for category in categories.values():
            categories_el.append(category.to_xml())

        root_el.append(brands_el)
        root_el.append(countries_el)
        root_el.append(fuels_el)
        root_el.append(sizes_el)
        root_el.append(styles_el)
        root_el.append(tractions_el)
        root_el.append(transmissions_el)
        root_el.append(categories_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()