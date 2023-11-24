# main.py
import xmlrpc.client
import sys
import os

print("\nconnecting to server")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')
print("\nconnected to server")

def select_database_file():
    while True:
        print("\n---> Select Database File <----")
        files = server.list_documents()

        if not files:
            print("\nNo documents in the database. Please import a document first.")
            main()

        print("\nAvailable files in the database:")
        for number, file in enumerate(files, start=1):
            print(f" {number} - {file[1]}")

        file_number = input("\nEnter the number of the file you want to use: ")

        try:
            file_number = int(file_number)
            if 1 <= file_number <= len(files):
                selected_file = files[file_number - 1][1]
                print(f"\nSelected file: {selected_file}")
                return selected_file
            else:
                print("\nInvalid file number. Try again.")
        except ValueError:
            print("\nInvalid input. Please enter a number.")

def importDocument():
    try:
        xml_file_path = input("\nEnter the path to the XML file (/data/[filename]): ")

        if not xml_file_path:
            print("\nNo XML file selected")
            return

        with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
            xml_content = xml_file.read()

        result = server.import_document_database(xml_content, xml_file_path)
        print(result)

    except Exception as e:
        print(f"Error: {e}")

def listDocuments():
    search_result = server.list_documents()
    if len(search_result) > 0:
        print("\nDatabase documents:")
        for number, file in enumerate(search_result, start=1):
            print(f" {number} - {file[1]}")
        return len(search_result)
    else:
        print("\nEmpty database!")
        return 0

def removeDocument():
    try:
        documents = listDocuments()

        if documents == 0:
            print("\nNo documents on database")
            return
        else:
            file_name = input("\nWrite the file name: ")

            if not file_name:
                print("\nInvalid file name.")
                return

            result = server.remove_documents(file_name)

            if "\nDocument removed successfully." in result:
                print(result)
            else:
                print("\nDocument not found or already removed.")

    except Exception as e:
        print(f"Error: {e}")

""" NORMAL SELECT """
def list_brands():
    try:
        brands = server.fetch_brands()
        if brands:
            print("\nList of Brands:")
            for brand in brands:
                print(f"- {brand}")
        else:
            print("\nNo brands found.")
    except Exception as e:
        print(f"Error: {e}")

def list_models():
    try:
        models = server.fetch_models()
        if models:
            print("\nList of Models:")
            for model in models:
                print(f"- {model}")
        else:
            print("\nNo models found.")
    except Exception as e:
        print(f"Error: {e}")

def list_market_categories():
    try:
        categories = server.fetch_market_categories()
        if categories:
            print("\nList of Market Categories:")
            for category in categories:
                print(f"- {category}")
        else:
            print("\nNo market categories found.")
    except Exception as e:
        print(f"Error: {e}")

def list_most_valuable_cars():
    try:
        cars = server.fetch_most_valuable_cars()
        if cars:
            print("\nMost Valuable Cars:")
            for car in cars:
                print(f"\nCar ID: {car['id']} \nYear: {car['year']} \nBrand: {car['brand_name']} \nModel: {car['model_name']} \nMSRP: {car['msrp']}")
        else:
            print("\nNo valuable cars found.")
    except Exception as e:
        print(f"Error: {e}")

""" SELECT BY TEXT """    
def list_models_brand():
    try:

        brand_name = input("Enter the brand name: ")

        models = server.fetch_models_by_brand(brand_name)
        if models:
            print(f"\nList of Models for Brand {brand_name}:")
            for model in models:
                print(f"{model}")
        else:
            print(f"\nNo models found for the brand {brand_name}.")
    except Exception as e:
        print(f"Error: {e}")

def list_cars_from_year():
    try:
        year = input("Enter the year: ")

        cars = server.fetch_vehicles_by_year(year)
        if cars:
            print(f"\nList of cars from year {year}:")
            for car in cars:
                print(f"\nCar ID: {car['id']} \nYear: {car['year']} \nBrand: {car['brand_name']} \nModel: {car['model_name']} \nMSRP: {car['msrp']}")
        else:
            print(f"\nNo cars found from year {year}.")
    except Exception as e:
        print(f"Error: {e}")
        
def list_vehicles_category():
    try:
        list_market_categories()

        category_name = input("\nEnter the market category: ")
        vehicles = server.fetch_vehicles_by_category(category_name)

        if vehicles:
            print(f"\nVehicles in the category {category_name}:")
            for vehicle in vehicles:
                print(f"\nCar ID: {vehicle['id']} \nYear: {vehicle['year']} \nBrand: {vehicle['brand_name']} \nModel: {vehicle['model_name']} \nMSRP: {vehicle['msrp']}")
        else:
            print(f"\nNo vehicles found in the category {category_name}.")

    except Exception as e:
        print(f"Error: {e}")

""" SELECT STATS/PERCENTAGE """
def display_category_statistics():
    try:

        brand_name = input("Enter the brand name: ")

        statistics = server.fetch_category_statistics(brand_name)
        if statistics:
            print(f"\nStatistics for Brand {brand_name}:")
            for stat in statistics:
                print(f"\nCategory: {stat['category']}, Vehicle Count: {stat['vehicle_count']}")
        else:
            print(f"\nNo statistics found for the brand {brand_name}.")
    except Exception as e:
        print(f"Error: {e}")

def list_brand_model_percentage():
    try:
        model_percentage = server.fetch_model_percentage()
        if model_percentage:
            print("\nModel Percentage:")
            for item in model_percentage:
                percentage_str = str(item['percentage'])
                print(f"\nBrand: {item['brand_name']}, \nModel: {item['model_name']}, \nAmount: {item['count']}, \nPercentage: {percentage_str}%")
        else:
            print("\nNo model percentage data found.")
    except Exception as e:
        print(f"Error: {e}")
        
def list_model_percentage_brand():
    try:

        brand_name_input = input("Enter the brand name: ")

        model_percentage = server.fetch_model_percentage_by_brand(brand_name_input)

        if model_percentage:
            print(f"\nModel Percentage for {brand_name_input}:")
            for item in model_percentage:
                percentage_str = str(item['percentage'])
                print(f"\nModel: {item['model_name']}, \nAmount: {item['count']}, \nPercentage: {percentage_str}%")
        else:
            print(f"No model percentage data found for {brand_name_input}.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        print("\n-----> Menu <------")
        print("1 - Documents")
        print("2 - Queries")
        print("0 - Leave program")
        option = input("Choose an option: ")

        if option == '1':
            print("\n-----> Documents <------")
            print("1 - Import Document")
            print("2 - List Document")
            print("3 - Remove Document")
            option = input("Choose an option: ")

            if option == '1':
                importDocument()
                continue
            if option == '2':
                listDocuments()
                continue
            if option == '3':
                removeDocument()
                continue

        elif option == '2':
            print("\n----------> Menu <----------")
            print("1 - Select all brands")
            print("2 - Select all models ")
            print("3 - Select market categories ")
            print("4 - Most valuable cars")
            print("\n----------> TEXT <----------")
            print("5 - List Models By Brand")
            print("6 - List Cars By Categories")
            print("7 - List Cars By Year")
            print("\n----------> STATS <----------")
            print("8 - NOT WORKING")
            print("9 - Brand Model Percentage")
            print("10 - Model Percentage of a Brand")
            option = input("Choose an option: ")
            
            if option == '1':
                list_brands()
                continue 
            if option == '2':
                list_models()
                continue
            if option == '3':
                list_market_categories()
                continue
            if option == '4':
                list_most_valuable_cars()
                continue
            if option == '5':
                list_models_brand()  
                continue
            if option == '6':
                list_vehicles_category() 
                continue
            if option == '7':
                list_cars_from_year()  
                continue
            if option == '8':
                print("\nNot Working")
                """ display_category_statistics() """
                continue
            if option == '9':
                list_brand_model_percentage()
                continue
            if option == '10':
                list_model_percentage_brand()
                continue
            if option == '10':
                list_cars_from_year()  
                continue


        elif option == '0':
            sys.exit(0)

        else:
            print("\nInvalid Option, Try Again.")

if __name__ == "__main__":
    selected_file = select_database_file()
    main()