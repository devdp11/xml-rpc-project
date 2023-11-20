""" from database.database import Database
from lxml import etree

database = Database()

def fetch_brands():
        database = Database()
        query = "SELECT xml FROM public.imported_documents WHERE file_name = %s"
        data = ('/data/data.xml',)
        result = database.selectOne(query, data)
        database.disconnect()

        if result is not None:
            xml_data = result[0]
            root = etree.fromstring(xml_data)
            brands = root.xpath('/Data/Brands/Brand')
            return [brand.get('name') for brand in brands]
        else:
            return []

def fetch_models():
    database = Database()
    query = "SELECT xml FROM public.imported_documents WHERE file_name = %s"
    data = ('/data/data.xml',)
    result = database.selectOne(query, data)
    database.disconnect()

    if result is not None:
        xml_data = result[0]
        root = etree.fromstring(xml_data)
        models = root.xpath('/Data/Brands/Brand/Models/Model')
        return [model.get('name') for model in models]
    else:
        return [] """