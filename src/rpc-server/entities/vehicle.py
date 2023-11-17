import xml.etree.ElementTree as ET
from entities.category import MarketCategoryItem

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
        vehicle_element.set("year", self._year)

        brand_ref_element = ET.SubElement(vehicle_element, "Car_Model")
        brand_ref_element.set("brand_ref", str(self._brand.get_id()))
        brand_ref_element.set("model_ref", str(self._model.get_id()))

        ##model_ref_element = ET.SubElement(vehicle_element, "Model")
        ##model_ref_element.set("ref", str(self._model.get_id()))

        ##year_element = ET.SubElement(vehicle_element, "Year")
        ##year_element.set("year", self._year)

        engine_fuel_type_element =  ET.SubElement(vehicle_element, "Engine_Fuel_Type")
        engine_fuel_type_element.set("ref", str(self._engine_fuel_type.get_id()))

        engine_hp_element =  ET.SubElement(vehicle_element, "Engine_HP")
        engine_hp_element.set("engine_hp", self._engine_hp)

        engine_cylinders_element =  ET.SubElement(vehicle_element, "Engine_Cylinders")
        engine_cylinders_element.set("engine_cylinders", self._engine_cylinders)
        
        transmission_element =  ET.SubElement(vehicle_element, "Engine_Fuel_Type")
        transmission_element.set("ref", str(self._transmission_type.get_id()))

        driven_wheels_element =  ET.SubElement(vehicle_element, "Driven_Wheels")
        driven_wheels_element.set("ref", str(self._driven_wheels.get_id()))

        number_of_doors_element =  ET.SubElement(vehicle_element, "Number_Of_Doors")
        number_of_doors_element.set("numbers_doors", self._number_of_doors)

        market_category_element = ET.SubElement(vehicle_element, "Market_category")
        for category_item in self._market_category:
            category_item_element = ET.SubElement(market_category_element, "Market_category_item")

            # Verificar se category_item é uma instância de MarketCategoryItem
            if isinstance(category_item, MarketCategoryItem):
                category_item_element.set("ref", str(category_item.get_id()))
            else:
                # Se não for uma instância de MarketCategoryItem, assumir que é uma string
                category_item_element.set("Name", category_item)

        size_element =  ET.SubElement(vehicle_element, "Vehicle_Size")
        size_element.set("ref", str(self._vehicle_size.get_id()))

        style_element =  ET.SubElement(vehicle_element, "Vehicle_Style")
        style_element.set("ref", str(self._driven_wheels.get_id()))

        highway_mpg_element =  ET.SubElement(vehicle_element, "Highway_mpg")
        highway_mpg_element.set("highway_mpg", self._highway_mpg)

        city_mpg_element =  ET.SubElement(vehicle_element, "City_mpg")
        city_mpg_element.set("size_mpg", self._city_mpg)

        popularity_element =  ET.SubElement(vehicle_element, "Popularity")
        popularity_element.set("popularity", self._popularity)

        msrp_element =  ET.SubElement(vehicle_element, "Msrp")
        msrp_element.set("msrp", self._msrp)

        return vehicle_element

    def __str__(self):
        return f"Car {self._id}: {self._brand} {self._model} ({self._year})"


Vehicle.counter = 0
