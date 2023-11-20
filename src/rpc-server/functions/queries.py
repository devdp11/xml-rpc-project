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
        query = "SELECT xml FROM public.imported_documents WHERE file_name = %s"
        data = ('/data/data.xml',)
        result = self._execute_query(query, data)

        if result is not None:
            xml_data = result[0]
            root = etree.fromstring(xml_data)
            brands = root.xpath('/Data/Brands/Brand')
            return [brand.get('name') for brand in brands]
        else:
            return []

    def fetch_models(self):
        query = "SELECT xml FROM public.imported_documents WHERE file_name = %s"
        data = ('/data/data.xml',)
        result = self._execute_query(query, data)

        if result is not None:
            xml_data = result[0]
            root = etree.fromstring(xml_data)
            models = root.xpath('/Data/Brands/Brand/Models/Model')
            return [model.get('name') for model in models]
        else:
            return []

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
            year = int(year)  # Certifique-se de converter o ano para inteiro
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
                vehicle_info = {
                    "id": vehicle.get('id'),
                    "brand": vehicle.find('./Brand').get('name'),
                    "model": vehicle.find('./Model').get('name'),
                    "year": vehicle.get('year'),
                    "msrp": vehicle.find('./Msrp').get('value'),
                    "category": category,
                    "fuel_type": vehicle.find('./Engine_Fuel_Type').get('ref')
                }
                detailed_info.append(vehicle_info)

            return detailed_info
        else:
            return []

    def fetch_model_by_brand(brand):
        pass
        
