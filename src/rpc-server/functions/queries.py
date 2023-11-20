from lxml import etree
from database.database import Database

class QueryFunctions:
    def __init__(self):
        self.database = Database()

    def _execute_query(self, query, data):
        database = Database()
        try:
            result = database.selectOne(query, data)
            return result
        finally:
            database.disconnect()
    
    def fetch_brands(self):
        database = Database()
        result_brands = []

        results = database.selectAll("SELECT unnest(xpath('//Brands/Brand/@name', xml)) as result FROM imported_documents WHERE deleted_on IS NULL")
        database.disconnect()

        for brand in results:
            if not brand in result_brands:
                result_brands.append(brand)

        return result_brands

    def fetch_models(self):
        database = Database()
        result_models = []

        results = database.selectAll("SELECT unnest(xpath('//Brands/Brand/Models/Model/@name', xml)) as result FROM imported_documents WHERE deleted_on IS NULL")
        database.disconnect()

        for model in results:
            if not model in result_models:
                result_models.append(model)

        return result_models

    def fetch_market_categories(self):
        query = "SELECT xml FROM public.imported_documents WHERE file_name = %s"
        data = ('/data/data.xml',)
        result = self._execute_query(query, data)

        if result is not None:
            xml_data = result[0]
            root = etree.fromstring(xml_data)
            categories = root.xpath('/Data/Categories/market_category')
            return [category.get('Name') for category in categories]
        else:
            return []

    def fetch_car_above_year(self, year):
        try:
            year = int(year)  
        except ValueError:
            return "Invalid year. Please enter a valid integer year."

        query = "SELECT xml FROM public.imported_documents WHERE file_name = %s"
        data = ('/data/data.xml',)
        result = self._execute_query(query, data)

        if result is not None:
            xml_data = result[0]
            root = etree.fromstring(xml_data)
            vehicles = root.xpath('/Data/Vehicles/Car[@year > $year]', year=year)
            return [vehicle.get('id') for vehicle in vehicles]
        else:
            return []
    
    def fetch_vehicles_by_category(self, category):
        try:
            category = str(category)
        except ValueError:
            return "Invalid category. Please enter a valid string category."

        database = Database()
        query = "SELECT xml FROM public.imported_documents WHERE file_name = %s"
        data = ('/data/data.xml',)
        result = database.selectOne(query, data)
        database.disconnect()

        if result is not None:
            xml_data = result[0]
            root = etree.fromstring(xml_data)
            vehicles = root.xpath(f'/Data/Vehicles/Car[Market_Categories/market_category[@ref="{category}"]]')

            detailed_info = []
            for vehicle in vehicles:
                vehicle_id = vehicle.get('id')
                brand_element = vehicle.find('./Brand')
                model_element = vehicle.find('./Model')
                year = vehicle.get('year')
                msrp_element = vehicle.find('./Msrp')
                fuel_type_element = vehicle.find('./Engine_Fuel_Type')

                if all([vehicle_id, brand_element, model_element, year, msrp_element, fuel_type_element]):
                    vehicle_info = {
                        "id": vehicle_id,
                        "brand": brand_element.get('name'),
                        "model": model_element.get('name'),
                        "year": year,
                        "msrp": msrp_element.get('value'),
                        "category": category,
                        "fuel_type": fuel_type_element.get('ref')
                    }
                    detailed_info.append(vehicle_info)

            return detailed_info
        else:
            return []

    def fetch_model_by_brand(brand):
        pass
        
