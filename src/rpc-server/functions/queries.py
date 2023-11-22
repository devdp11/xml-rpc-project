from lxml import etree
from database.database import Database

def fetch_brands():
    database = Database()
    result_brands = []

    results = database.selectAll("SELECT unnest(xpath('//Brands/Brand/@name', xml)) as result FROM imported_documents WHERE deleted_on IS NULL")
    database.disconnect()

    for brand in results:
        if not brand in result_brands:
            result_brands.append(brand)

    return result_brands

def fetch_models():
    database = Database()
    result_models = []

    results = database.selectAll("SELECT unnest(xpath('//Brands/Brand/Models/Model/@name', xml)) as result FROM imported_documents WHERE deleted_on IS NULL")
    database.disconnect()

    for model in results:
        if not model in result_models:
            result_models.append(model)

    return result_models


def fetch_market_categories():
    database = Database()
    result_models = []

    results = database.selectAll("SELECT unnest(xpath('//Categories/market_category/@name', xml)) as result FROM imported_documents WHERE deleted_on IS NULL")
    database.disconnect()

    for model in results:
        if not model in result_models:
            result_models.append(model)

    return result_models

def fetch_most_valuable_cars():
    database = Database()

    query = """
    WITH vehicle_data AS ( SELECT
            unnest(xpath('//Vehicles/Car/@id', xml))::text as id,
            unnest(xpath('//Vehicles/Car/@year', xml))::text as year,
            unnest(xpath('//Vehicles/Car/@brand_ref', xml))::text as brand_ref,
            unnest(xpath('//Vehicles/Car/@model_ref', xml))::text as model_ref,
            unnest(xpath('//Data/Vehicles/Car/Msrp/@value', xml))::text as msrp FROM imported_documents WHERE deleted_on IS NULL ),
    
    model_data AS 
    
    (SELECT unnest(xpath('//Brands/Brand/Models/Model/@id', xml))::text as model_id, unnest(xpath('//Brands/Brand/Models/Model/@name', xml))::text as model_name FROM imported_documents WHERE deleted_on IS NULL)
    
    SELECT car.id, car.year, COALESCE(brand.name, 'N/A') as brand_name, COALESCE(model.model_name, 'N/A') as model_name, car.msrp FROM vehicle_data car
    
    LEFT JOIN(SELECT unnest(xpath('//Brands/Brand/@id', xml))::text as brand_id, unnest(xpath('//Brands/Brand/@name', xml))::text as name FROM imported_documents WHERE deleted_on IS NULL) brand ON car.brand_ref = brand.brand_id
    
    LEFT JOIN model_data model ON car.model_ref = model.model_id 
    
    WHERE car.msrp IS NOT NULL 
    
    ORDER BY car.msrp::numeric DESC LIMIT 20;
    """

    results = database.selectAllArray(query)
    database.disconnect()

    query_result = [
        {
            "id": car.get("id", "N/A"),
            "year": car.get("year", "N/A"),
            "brand_name": car.get("brand_name", "N/A"),
            "model_name": car.get("model_name", "N/A"),
            "msrp": car.get("msrp", "N/A"),
        }
        for car in results
    ]

    return query_result