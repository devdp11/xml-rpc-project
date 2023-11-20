# main.py
import xmlrpc.client
import os


print("\nconnecting to server")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')
print("\nconnected to server")


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
            print("\nList of Market Categories:")
            for category in categories:
                print(f"- {category}")
        else:
            print("No market categories found.")
    except Exception as e:
        print(f"Error1: {e}")

def list_cars_above_year():
    try:
        year = input("Enter the minimum year: ")
        cars = server.fetch_car_above_year(year)
        if cars:
            print("List of Cars:")
            for car in cars:
                print(f"- Car ID: {car}")
        else:
            print("No cars found.")
    except Exception as e:
        print(f"Error: {e}")

def list_vehicles_by_category(category):
    try:
        vehicles = server.fetch_vehicles_by_category(category)
        if vehicles:
            print(f"\nList of Vehicles in Category '{category}':")
            for vehicles in vehicles:
                print(f"- {vehicles}")
        else:
            print(f"No vehicles found in Category '{category}'.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        print("\n-----> Menu <------")
        print("1 - Select all brands")
        print("2 - Select all models")
        print("3 - Select market categories ")
        print("4 - Select cars according to year ")

        print("0 - Leave program")
        option = input("Choose an option: ")

        if option == '1':
            list_brands()
        if option == '2':
            list_models()
        if option == '3':
            list_market_categories()
        if option == '4':
            list_cars_above_year()
        if option == '5':
            list_vehicles_by_category(category="1 - Factory Tuner")
        elif option == '0':
            print("\nLeaving program!")
            break
        else:
            print("\nInvalid Option, Try Again.")

if __name__ == "__main__":
    main()
