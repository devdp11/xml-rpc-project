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
            print("List of Brands:")
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
            print("List of Models:")
            for model in models:
                print(f"- {model}")
        else:
            print("No models found.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        print("\n-----> Menu <------")
        print("1 - Select all brands")
        print("2 - Select all models")

        print("0 - Leave program")
        option = input("Choose an option: ")

        if option == '1':
            list_brands()
        if option == '2':
            list_models()
        elif option == '0':
            print("\nLeaving program!")
            break
        else:
            print("\nInvalid Option, Try Again.")

if __name__ == "__main__":
    main()
