from datetime import datetime
from database.database import Database

def import_document_database(xml_content, xml_file):
    try:
        database = Database()

        """ XML FILE INSERTION """
        insert_query = "INSERT INTO public.imported_documents (file_name, xml) VALUES (%s, %s)"
        data = (xml_file, xml_content)
        
        database.insert(insert_query, data)

        return "Document imported successfully."

    except Exception as e:
        print(f"Error: {e}")
        return f"Error1: {e}"

def list_documents():
    pass
