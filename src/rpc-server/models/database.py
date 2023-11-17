import psycopg2

connection = None
cursor = None

try:
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="is-db",
                                  port="5432",
                                  database="is")

except (Exception, psycopg2.Error) as error:
    print("\nFailed to fetch data", error)

finally:
    if connection:
        cursor.close()
        connection.close()