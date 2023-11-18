import psycopg2

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.user ="is"
        self.password = "is"
        self.host = "is-db"
        self.port = "5432"
        self.database = "xml-rpc-project"
        
    def connect(self):
        if self.connection is None:
            try:
                self.connection = psycopg2.connect(
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    database=self.database
                )
                self.cursor = self.connection.cursor()
                print("\nConnection established sucessfully.")
            except psycopg2.Error as error:
                print(f"\nError: {error}")

    def detach(self):
        if self.connection:
            try:
                self.cursor.close()
                self.connection.close()
                print("\nDisconnected sucessfully from database.")
            except psycopg2.Error as e:
                print(f"\nError: {e}")

    def insert(self, sql_query, data):
        self.connect()
        try:
            self.cursor.execute(query=sql_query, vars=data)
            self.connection.commit()
            print("\nThe query was sucessfully made.")
        except psycopg2.Error as error:
            print(f"\nError: {error}")