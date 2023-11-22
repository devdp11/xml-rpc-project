# main.py
import xmlrpc.client
import sys
import os

print("\nconnecting to server")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')
print("\nconnected to server")

def importDocument():
    try:
        xml_file_path = input("Enter the path to the XML file (/data/[filename]): ")

        if not xml_file_path:
            print("No XML file selected")
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
        print("Database documents:")
        for number, file in enumerate(search_result, start=1):
            print(f" {number} - {file[1]}")
        return len(search_result)
    else:
        print("Empty database!")
        return 0

def removeDocument():
    try:
        documents = listDocuments()

        if documents == 0:
            print("No documents on database")
            return
        else:
            file_name = input("Write the file name: ")

            if not file_name:
                print("Invalid file name.")
                return

            result = server.remove_documents(file_name)

            if "Document removed successfully." in result:
                print(result)
            else:
                print("Document not found or already removed.")

    except Exception as e:
        print(f"Error: {e}")

def list_brands():
    try:
        brands = server.fetch_brands()
        if brands:
            print("\nList of Brands:")
            for brand in brands:
                print(f"- {brand}")
        else:
            print("No brands found.")
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
            print("No models found.")
    except Exception as e:
        print(f"Error: {e}")

def list_market_categories():
    try:
        categories = server.fetch_market_categories()
        if categories:
            print("\nList of Market Categories ni:")
            for category in categories:
                print(f"- {category}")
        else:
            print("No market categories found.")
    except Exception as e:
        print(f"Error1: {e}")

def list_most_valuable_cars():
    try:
        cars = server.fetch_most_valuable_cars()
        if cars:
            print("\nMost Valuable Cars:")
            for car in cars:
                print(f"- Car ID: {car['id']}, Year: {car['year']}, Brand: {car['brand_name']}, Model: {car['model_name']}, MSRP: {car['msrp']}")
        else:
            print("No valuable cars found.")
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

        elif option == '0':
            sys.exit(0)

        else:
            print("\nInvalid Option, Try Again.")

if __name__ == "__main__":
    main()
