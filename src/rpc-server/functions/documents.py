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
    try:
        database = Database()
        result = database.selectAll(
            "SELECT id, file_name, xml, created_on, updated_on FROM imported_documents WHERE deleted_on IS NULL")
        database.disconnect()
        return result

    except Exception as e:
        print(f"Error: {e}")
        return f"Error2: {e}"

def remove_documents(file_name):
    try:
        database = Database()

        database.softdelete(file_name)

        return "Document removed successfully."

    except Exception as e:
        print(f"Error removing document: {e}")
        return f"Error: {e}"