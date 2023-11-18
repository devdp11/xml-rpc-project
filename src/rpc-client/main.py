import xmlrpc.client
import os

def select_company(server):
    while True:
        response = input("\nSearch a car by a car company or type '/return' to quit: ").lower()
        if response == "/return":
            break
        else:
            results = server.select_company(response)
            if not results:
                print(f"\nThere's no cars from company '{response}'\n")
            else:
                print("\n----------------------------------------------")
                print(f"{len(results)} Results from search '{response}'")
                print("----------------------------------------------\n")
                for data in results:
                    print(data)

def select_model(server):
    while True:
        response = input("\nSearch a car by a car model or type '/return' to quit: ").lower()
        if response == "/return":
            break
        else:
            results = server.select_model(response)
            if not results:
                print(f"\nThere's no cars with the model '{response}'\n")
            else:
                print("\n----------------------------------------------")
                print(f"{len(results)} Results from search '{response}'")
                print("----------------------------------------------\n")
                for data in results:
                    print(data)

def main():
    print("connecting to server...")
    server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')

    while True:
        os.system("cls")
        print("\n --------> Menu <---------")
        print("1 - Select by automobile manufacturer")
        print("2 - Select by automobile models")
        print("0 - Leave program")
        option = input("Choose an option: ")
        os.system("cls")

        if option == '1':
            #select_company(server)
            pass
        elif option == '2':
            #select_model(server)
            pass
        else:
            print("\nInvalid Option, Try Again.")


string = "hello world"

