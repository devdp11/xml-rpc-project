from lxml import etree
from database.database import Database

class QueryFunctions:
    def __init__(self):
        self.database = Database()
    
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
        database = Database()
        result_models = []

        results = database.selectAll("SELECT unnest(xpath('//Categories/market_category/@name', xml)) as result FROM imported_documents WHERE deleted_on IS NULL")
        database.disconnect()

        for model in results:
            if not model in result_models:
                result_models.append(model)

        return result_models

    def fetch_most_valuable_cars(self):
        database = Database()

        query = """
        WITH car_data AS (
            SELECT
                unnest(xpath('//Vehicles/Car/@id', xml))::text as id,
                unnest(xpath('//Vehicles/Car/@brand_ref', xml))::text as brand_ref,
                unnest(xpath('//Vehicles/Car/@model_ref', xml))::text as model_ref,
                unnest(xpath('//Data/Vehicles/Car/Msrp/@value', xml))::text as msrp
            FROM
                imported_documents
        )
        SELECT
            id,
            brand_ref,
            model_ref,
            msrp
        FROM
            car_data
        WHERE
            msrp IS NOT NULL
        ORDER BY
            msrp::numeric DESC
        LIMIT 10;
        """

        results = database.selectAllArray(query)
        database.disconnect()

        formatted_cars = [
            {
                "id": car.get("id", "N/A"),
                "brand_ref": car.get("brand_ref", "N/A"),
                "model_ref": car.get("model_ref", "N/A"),
                "msrp": car.get("msrp", "N/A"),
            }
            for car in results
        ]

        return formatted_cars


    