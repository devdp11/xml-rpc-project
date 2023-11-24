# main.py
import xmlrpc.client
import sys
import os

print("\nconnecting to server")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')
print("\nconnected to server")

def print_results(results, page, res_page):
    sindex = (page - 1) * res_page
    eindex = sindex + res_page
    p_results = results[sindex:eindex]

    print(f"\n Showing {len(p_results)} results from page {page}:")
    print("--------------------------------------------------------------------------")
    for data in p_results:
        print(data)
    print("--------------------------------------------------------------------------")

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

def list_brands():
    page = 1
    results_per_page = 30

    while True:
        try:
            brands = server.fetch_brands()
            if not brands:
                print("\nNo brands found.")
                break

            print_results(brands, page, results_per_page)
            
            cli_response = input("\nType 'n' to go to the next page, 'p' for the previous page, or '/return' to leave: ").lower()
            
            if cli_response == "n" and (page * results_per_page) < len(brands):
                page += 1
            elif cli_response == "p" and page > 1:
                page -= 1
            elif cli_response == "/return":
                break
            else:
                print("\nInvalid action. Try again.")

        except Exception as e:
            print(f"Error: {e}")
            break


def list_models():
    page = 1
    results_per_page = 30

    while True:
        try:
            models = server.fetch_models()
            if not models:
                print("\nNo models found.")
                break

            print_results(models, page, results_per_page)
            
            cli_response = input("\nType 'n' to go to the next page, 'p' for the previous page, or '/return' to leave: ").lower()
            
            if cli_response == "n" and (page * results_per_page) < len(models):
                page += 1
            elif cli_response == "p" and page > 1:
                page -= 1
            elif cli_response == "/return":
                break
            else:
                print("\nInvalid action. Try again.")

        except Exception as e:
            print(f"Error: {e}")
            break


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
                print(f"- Car ID: {car['id']}, Year: {car['year']}, Brand: {car['brand_name']}, Model: {car['model_name']}, MSRP: {car['msrp']}")
        else:
            print("\nNo valuable cars found.")
    except Exception as e:
        print(f"Error: {e}")
        
def list_models_of_brand(brand_name):
    try:
        models = server.fetch_models_by_brand(brand_name)
        if models:
            print(f"\nList of Models for Brand {brand_name}:")
            for model in models:
                print(f"- {model}")
        else:
            print(f"\nNo models found for the brand {brand_name}.")
    except Exception as e:
        print(f"Error: {e}")
        
def list_vehicles_by_category():
    page = 1
    results_per_page = 30

    try:
        category = input("\nEnter the market category: ")

        while True:
            vehicles = server.fetch_vehicles_by_category(category)
            if not vehicles:
                print(f"\nNo vehicles found in the category {category}.")
                break

            print_results(vehicles, page, results_per_page)

            cli_response = input("\nType 'n' to go to the next page, 'p' for the previous page, or '/return' to leave: ").lower()

            if cli_response == "n" and (page * results_per_page) < len(vehicles):
                page += 1
            elif cli_response == "p" and page > 1:
                page -= 1
            elif cli_response == "/return":
                break
            else:
                print("\nInvalid action. Try again.")

    except Exception as e:
        print(f"Error: {e}")

def display_category_statistics(brand_name):
    try:
        statistics = server.fetch_category_statistics(brand_name)
        if statistics:
            print(f"\nStatistics for Brand {brand_name}:")
            for stat in statistics:
                print(f"- Category: {stat['category']}, Vehicle Count: {stat['vehicle_count']}")
        else:
            print(f"\nNo statistics found for the brand {brand_name}.")
    except Exception as e:
        print(f"Error: {e}")

def display_model_statistics(server):
    page = 1
    results_per_page = 30

    try:
        while True:
            model_percentage = server.fetch_model_percentage()
            if not model_percentage:
                print("\nNo model percentage data found.")
                break

            print_results(model_percentage, page, results_per_page)

            cli_response = input("\nType 'n' to go to the next page, 'p' for the previous page, or '/return' to leave: ").lower()

            if cli_response == "n" and (page * results_per_page) < len(model_percentage):
                page += 1
            elif cli_response == "p" and page > 1:
                page -= 1
            elif cli_response == "/return":
                break
            else:
                print("\nInvalid action. Try again.")

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
            print("\n-----> Menu <------")
            print("1 - Select all brands")
            print("2 - Select all models ")
            print("3 - Select market categories ")
            print("4 - Most valuable cars")
            print("5 - List Models By Brand")
            print("6 - List Cars By Categories")
            print("7 - estatisticas")
            print("8 - Model Percentage")
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
                brand_name_input = input("Enter the brand name: ")
                list_models_of_brand(brand_name_input)  
                continue
            if option == '6':
                list_market_categories()
                list_vehicles_by_category() 
                continue
            if option == '7':
                brand_name_input = input("Enter the brand name: ")
                display_category_statistics(brand_name_input)
                continue
            if option == '8':
                display_model_statistics()
                continue


        elif option == '0':
            sys.exit(0)

        else:
            print("\nInvalid Option, Try Again.")

if __name__ == "__main__":
    selected_file = select_database_file()
    main()