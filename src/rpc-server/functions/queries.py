from lxml import etree
from database.database import Database

""" SELECTS ALL / ORDER"""
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
    results_categories = []
    results = database.selectAll("SELECT unnest(xpath('//Categories/market_category/@Name', xml)) as result FROM imported_documents WHERE deleted_on IS NULL")
    database.disconnect()

    for category in results:
        if not category in results_categories:
            results_categories.append(category)

    return results_categories

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

""" SELECTS TEXT"""
def fetch_models_by_brand(brand_name):
    database = Database()
    result_models = []


    query = f"""
    SELECT unnest(xpath('//Brand[@name="{brand_name}"]/Models/Model/@name', xml)) as result
    FROM imported_documents
    WHERE deleted_on IS NULL;
    """

    results = database.selectAll(query)
    database.disconnect()

    for model in results:
        if not model in result_models:
            result_models.append(model)

    return result_models

def fetch_brands_by_country(country_name):
    database = Database()

    query = f"""
    WITH brand_data AS (
        SELECT unnest(xpath('//Brands/Brand/@id', xml))::text as brand_id, unnest(xpath('//Brands/Brand/@name', xml))::text as brand_name, unnest(xpath('//Brands/Brand/@country_ref', xml))::text as country_ref
        FROM imported_documents WHERE deleted_on IS NULL
    ),
    country_data AS (
        SELECT unnest(xpath('//Countries/Country/@id', xml))::text as country_id, unnest(xpath('//Countries/Country/@name', xml))::text as country_name
        FROM imported_documents WHERE deleted_on IS NULL
    )

    SELECT brand.brand_id, brand.brand_name, country.country_name
    FROM brand_data brand JOIN country_data country ON brand.country_ref = country.country_id WHERE country.country_name = '{country_name}';
    """

    results = database.selectAllArray(query)
    database.disconnect()

    query_result = [
        {
            "brand_id": brand.get("brand_id", "N/A"),
            "brand_name": brand.get("brand_name", "N/A"),
            "country_name": brand.get("country_name", "N/A"),
        }
        for brand in results
    ]

    return query_result

def fetch_vehicles_by_category(category_name):
    database = Database()

    query = f"""
    WITH vehicle_data AS (
        SELECT unnest(xpath('//Vehicles/Car/@id', xml))::text as id, unnest(xpath('//Vehicles/Car/@year', xml))::text as year, unnest(xpath('//Vehicles/Car/@brand_ref', xml))::text as brand_ref, unnest(xpath('//Vehicles/Car/@model_ref', xml))::text as model_ref, unnest(xpath('//Data/Vehicles/Car/Msrp/@value', xml))::text as msrp
        FROM imported_documents WHERE deleted_on IS NULL
    ),
    model_data AS (
        SELECT unnest(xpath('//Brands/Brand/Models/Model/@id', xml))::text as model_id, unnest(xpath('//Brands/Brand/Models/Model/@name', xml))::text as model_name
        FROM imported_documents WHERE deleted_on IS NULL
    )

    SELECT car.id, car.year, COALESCE(brand.name, 'N/A') as brand_name, COALESCE(model.model_name, 'N/A') as model_name, car.msrp
    FROM vehicle_data car
    LEFT JOIN ( SELECT unnest(xpath('//Brands/Brand/@id', xml))::text as brand_id, unnest(xpath('//Brands/Brand/@name', xml))::text as name
        FROM imported_documents WHERE deleted_on IS NULL
    ) brand ON car.brand_ref = brand.brand_id LEFT JOIN model_data model ON car.model_ref = model.model_id WHERE car.msrp IS NOT NULL;
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

def fetch_vehicles_by_year(year):
    database = Database()

    query = f"""
    WITH vehicle_data AS (
        SELECT unnest(xpath('//Vehicles/Car/@id', xml))::text as id, unnest(xpath('//Vehicles/Car/@year', xml))::text as year, unnest(xpath('//Vehicles/Car/@brand_ref', xml))::text as brand_ref, unnest(xpath('//Vehicles/Car/@model_ref', xml))::text as model_ref, unnest(xpath('//Data/Vehicles/Car/Msrp/@value', xml))::text as msrp
        FROM imported_documents WHERE deleted_on IS NULL
    ),
    model_data AS (
        SELECT unnest(xpath('//Brands/Brand/Models/Model/@id', xml))::text as model_id, unnest(xpath('//Brands/Brand/Models/Model/@name', xml))::text as model_name
        FROM imported_documents WHERE deleted_on IS NULL
    )

    SELECT car.id, car.year as year, COALESCE(brand.name, 'N/A') as brand_name, COALESCE(model.model_name, 'N/A') as model_name, car.msrp
    FROM vehicle_data car
    LEFT JOIN ( SELECT unnest(xpath('//Brands/Brand/@id', xml))::text as brand_id, unnest(xpath('//Brands/Brand/@name', xml))::text as name FROM imported_documents WHERE deleted_on IS NULL
    ) brand ON car.brand_ref = brand.brand_id
    LEFT JOIN model_data model ON car.model_ref = model.model_id
    WHERE car.year is NOT NULL AND car.year = '{year}'
    ORDER BY car.year DESC;
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

""" ESTATISTICAS """
def fetch_model_percentage():
    database = Database()

    query = """
WITH vehicle_data AS (
    SELECT unnest(xpath('//Vehicles/Car/@id', xml))::text as id, unnest(xpath('//Vehicles/Car/@brand_ref', xml))::text as brand_ref, unnest(xpath('//Vehicles/Car/@model_ref', xml))::text as model_ref
    FROM imported_documents WHERE deleted_on IS NULL
),
model_counts AS ( SELECT brand.brand_name, md.model_name, count(*) as model_count
    FROM vehicle_data vd
    LEFT JOIN ( SELECT unnest(xpath('//Brands/Brand/@id', xml))::text as brand_id, unnest(xpath('//Brands/Brand/@name', xml))::text as brand_name
        FROM imported_documents WHERE deleted_on IS NULL
    ) brand ON vd.brand_ref = brand.brand_id
    LEFT JOIN ( SELECT unnest(xpath('//Brands/Brand/Models/Model/@id', xml))::text as model_id, unnest(xpath('//Brands/Brand/Models/Model/@name', xml))::text as model_name
        FROM imported_documents WHERE deleted_on IS NULL
    ) md ON vd.model_ref = md.model_id
    GROUP BY brand.brand_name, md.model_name
),
total_count AS ( SELECT count(DISTINCT id) as total FROM vehicle_data )

SELECT mc.brand_name, mc.model_name, mc.model_count as count, ROUND(CAST(mc.model_count AS DECIMAL) / CAST(tc.total AS DECIMAL) * 100, 4) as percentage
FROM model_counts mc CROSS JOIN total_count tc 
ORDER BY mc.model_name, mc.brand_name;
    """

    results = database.selectAllArray(query)
    database.disconnect()

    query_result = [
        {
            "brand_name": car.get("brand_name", "N/A"),
            "model_name": car.get("model_name", "N/A"),
            "count": int(car.get("count", 0)),
            "percentage": float(car.get("percentage", 0.0)),
        }
        for car in results
    ]

    return query_result

def fetch_model_percentage_by_brand(brand_name):
    database = Database()

    query = f"""
WITH brand_id AS (
    SELECT unnest(xpath('//Brands/Brand[@name="{brand_name}"]/@id', xml))::text as brand_id
    FROM imported_documents WHERE deleted_on IS NULL LIMIT 1
),
vehicle_data AS (
    SELECT unnest(xpath('//Vehicles/Car/@id', xml))::text as id, unnest(xpath('//Vehicles/Car/@brand_ref', xml))::text as brand_ref, unnest(xpath('//Vehicles/Car/@model_ref', xml))::text as model_ref 
    FROM imported_documents WHERE deleted_on IS NULL
),
filtered_vehicle_data AS ( SELECT * FROM vehicle_data WHERE brand_ref IN (SELECT brand_id FROM brand_id)
),
model_counts AS (
    SELECT brand.brand_name, md.model_name, COUNT(*) as model_count
    FROM filtered_vehicle_data fvd
    LEFT JOIN ( SELECT unnest(xpath('//Brands/Brand/@id', xml))::text as brand_id, unnest(xpath('//Brands/Brand/@name', xml))::text as brand_name
    FROM imported_documents WHERE deleted_on IS NULL ) brand ON fvd.brand_ref = brand.brand_id
    LEFT JOIN ( SELECT unnest(xpath('//Brands/Brand/Models/Model/@id', xml))::text as model_id, unnest(xpath('//Brands/Brand/Models/Model/@name', xml))::text as model_name
    FROM imported_documents WHERE deleted_on IS NULL ) md ON fvd.model_ref = md.model_id
    GROUP BY brand.brand_name, md.model_name
),
total_count_per_brand AS ( SELECT brand.brand_name, COUNT(DISTINCT fvd.id) as total
    FROM filtered_vehicle_data fvd
    LEFT JOIN ( SELECT unnest(xpath('//Brands/Brand/@id', xml))::text as brand_id, unnest(xpath('//Brands/Brand/@name', xml))::text as brand_name
    FROM imported_documents WHERE deleted_on IS NULL ) brand ON fvd.brand_ref = brand.brand_id
    GROUP BY brand.brand_name
)

SELECT mc.brand_name, mc.model_name, mc.model_count as count, ROUND(CAST(mc.model_count AS DECIMAL) / CAST(tc.total AS DECIMAL) * 100, 2) as percentage
FROM model_counts mc JOIN total_count_per_brand tc ON mc.brand_name = tc.brand_name 
ORDER BY mc.model_name, mc.brand_name;
"""

    results = database.selectAllArray(query)
    database.disconnect()

    query_result = [
        {
            "brand_name": car.get("brand_name", "N/A"),
            "model_name": car.get("model_name", "N/A"),
            "count": int(car.get("count", 0)),
            "percentage": float(car.get("percentage", 0.0)),
        }
        for car in results
    ]

    return query_result