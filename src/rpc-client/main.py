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
                print("\nInvalid file number.")
        except ValueError:
            print("\nInvalid input.")

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
            return
        else:
            file_name = input("\nWrite the file name: ")

            if not file_name:
                print("\nInvalid file name.")
                return

            result = server.remove_documents(file_name)

            if "Document removed successfully." in result:
                print(result)
            else:
                print("\nDocument not found or already removed.")

    except Exception as e:
        print(f"Error: {e}")

""" NORMAL SELECTS """
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
            print(f"\nList of Models of '{brand_name}':")
            for model in models:
                print(f"{model}")
        else:
            print(f"\nNo models found for the brand '{brand_name}'.")
    except Exception as e:
        print(f"Error: {e}")

def list_cars_from_year():
    page = 1
    results_per_page = 40

    try:
        year = input("Enter the year: ")
        results = server.fetch_vehicles_by_year(year)
        len_results = len(results)

        if not results:
            print(f"\nNo cars found from year '{year}'.")
            return

        while True:
            start = (page - 1) * results_per_page
            end = start + results_per_page
            current_page_results = results[start:end]

            print(f"\nList of cars from year '{year}':")
            for car in current_page_results:
                print(f"\nCar ID: {car['id']} \nYear: {car['year']} \nBrand: {car['brand_name']} \nModel: {car['model_name']} \nMSRP: {car['msrp']}")

            print(f"\nShowing results {start + 1} to {min(end, len_results)} out of {len_results}.")

            if len_results > end:
                response = input("\nType 'n' to go to the next page, 'p' to go to the previous page, or '/return' to leave: ").lower()
                if response == "n":
                    page += 1
                elif response == "p" and page > 1:
                    page -= 1
                elif response == "/return":
                    break
                else:
                    print("\nInvalid option")
            else:
                break

    except Exception as e:
        print(f"Error: {e}")

def list_brands_by_country():
    try:
        country_name = input("Enter the country name: ")

        brands = server.fetch_brands_by_country(country_name)

        if brands:
            print(f"\nBrands from '{country_name}':")
            for brand in brands:
                print(f"\nBrand ID: {brand['brand_id']} \nBrand Name: {brand['brand_name']} \nCountry: {brand['country_name']}")
        else:
            print(f"\nNo brands found in '{country_name}'.")

    except Exception as e:
        print(f"Error: {e}")

""" SELECTS STATS/PERCENTAGE """
def list_brand_model_percentage():
    page = 1
    results_per_page = 40

    try:
        results = server.fetch_model_percentage()
        len_results = len(results)

        if not results:
            print("\nNo model percentage data found.")
            return

        while True:
            start = (page - 1) * results_per_page
            end = start + results_per_page
            current_page_results = results[start:end]

            print("\nModel Percentage:")
            for item in current_page_results:
                percentage_str = str(item['percentage'])
                print(f"\nBrand: {item['brand_name']}, \nModel: {item['model_name']}, \nAmount: {item['count']}, \nPercentage: {percentage_str}%")

            print(f"\nShowing results {start + 1} to {min(end, len_results)} out of {len_results}.")

            if len_results > end:
                response = input("\nType 'n' to go to the next page, 'p' to go to the previous page, or '/return' to leave: ").lower()
                if response == "n":
                    page += 1
                elif response == "p" and page > 1:
                    page -= 1
                elif response == "/return":
                    break
                else:
                    print("\nInvalid option")
            else:
                break

    except Exception as e:
        print(f"Error: {e}")

def list_model_percentage_brand():
    try:

        brand_name = input("Enter the brand name: ")

        model_percentage = server.fetch_model_percentage_by_brand(brand_name)

        if model_percentage:
            print(f"\nModel Percentage for '{brand_name}':")
            for item in model_percentage:
                percentage_str = str(item['percentage'])
                print(f"\nModel: {item['model_name']}, \nAmount: {item['count']}, \nPercentage: {percentage_str}%")
        else:
            print(f"No model percentage data found for '{brand_name}'.")
    except Exception as e:
        print(f"Error: {e}")

def start():
    input("\nPress '3nter' to continue...")
    select_database_file()

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
            print("\n---------> MENU <----------")
            print("\n----------> ALL <----------")
            print("1 - List All Brands")
            print("2 - List All Models ")
            print("3 - List All Market Categories ")
            print("4 - List Most Valuable Cars")
            print("\n---------> TEXT <----------")
            print("5 - List Brands By Country ")
            print("6 - List Models By Brand")
            print("7 - List Cars By Year")
            print("\n---------> STATS <---------")
            print("8 - Brand Model Percentage")
            print("9 - Model Percentage of a Brand")
            option = input("Choose an option: ")
            
            if option == '1':
                list_brands()
                continue 
            if option == '2':
                list_models()
                continue
            if option == '3':
                list_market_categories()
            if option == '4':
                list_most_valuable_cars()
                continue
            if option == '5':
                list_brands_by_country()
                continue
            if option == '6':
                list_models_brand()  
                continue
            if option == '7':
                list_cars_from_year()  
                continue
            if option == '8':
                list_brand_model_percentage()
                continue
            if option == '9':
                list_model_percentage_brand()
                continue

        elif option == '0':
            sys.exit(0)

        else:
            print("\nInvalid Option, Try Again.")

start()
main()