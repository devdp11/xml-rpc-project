import xml.etree.ElementTree as ET

class Vehicle:

    def __init__(self, brand, model, year, engine_fuel_type, engine_hp, engine_cylinders, transmission_type, driven_wheels, number_of_doors, market_category, vehicle_size, vehicle_style, highway_mpg, city_mpg, popularity, msrp, country):
        Vehicle.counter += 1
        self._id = Vehicle.counter
        self._brand = brand
        self._model = model
        self._year = year
        self._engine_fuel_type = engine_fuel_type
        self._engine_hp = engine_hp
        self._engine_cylinders = engine_cylinders
        self._transmission_type = transmission_type
        self._driven_wheels = driven_wheels
        self._number_of_doors = number_of_doors
        self._market_category = market_category
        self._vehicle_size = vehicle_size
        self._vehicle_style = vehicle_style
        self._highway_mpg = highway_mpg
        self._city_mpg = city_mpg
        self._popularity = popularity
        self._msrp = msrp
        self._country = country

    def to_xml(self):
        vehicle_element = ET.Element("Car")
        vehicle_element.set("id", str(self._id))

        brand_ref_element = ET.SubElement(vehicle_element, "Brand")
        brand_ref_element.set("ref", str(self._brand.get_id()))

        model_ref_element = ET.SubElement(vehicle_element, "Model")
        model_ref_element.set("ref", str(self._model.get_id()))

        market_category_element = ET.SubElement(vehicle_element, "market_category")
        for category_item in self._market_category:
            category_item_element = ET.SubElement(market_category_element, "market_category_item")
            category_item_element.set("ref", str(category_item.get_id()))

        return vehicle_element

    def __str__(self):
        return f"Car {self._id}: {self._brand} {self._model} ({self._year})"


Vehicle.counter = 0
