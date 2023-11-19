import signal
import sys
from lxml import etree
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from functions.csv_to_xml_converter import CSVtoXMLConverter

from database.database import Database

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


with SimpleXMLRPCServer(('0.0.0.0', 9000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    database = Database()

    def signal_handler(signum, frame):
        print("\nReceived signal")
        server.server_close()

        print("\nExiting gracefully")
        sys.exit(0)

    """ FUNÇÕES SELECT """

    def fetch_brands():
        database = Database()
        query = "SELECT xml FROM public.imported_documents WHERE file_name = %s"
        data = ('/data/data.xml',)
        result = database.selectOne(query, data)
        database.disconnect()

        if result is not None:
            xml_data = result[0]
            root = etree.fromstring(xml_data)
            brands = root.xpath('/Data/Brands/Brand')
            return [brand.get('name') for brand in brands]
        else:
            return []

    def fetch_models():
        database = Database()
        query = "SELECT xml FROM public.imported_documents WHERE file_name = %s"
        data = ('/data/data.xml',)
        result = database.selectOne(query, data)
        database.disconnect()

        if result is not None:
            xml_data = result[0]
            root = etree.fromstring(xml_data)
            models = root.xpath('/Data/Brands/Brand/Models/Model')
            return [model.get('name') for model in models]
        else:
            return []
    
    """ FILE NAME """

    csv_file = "/data/data.csv"
    xml_file = "/data/data.xml"
    xsd_file = "/data/schemas/data.xsd"

    """ CALLED CONVERTION & VALIDATION FUNCTION """

    converter = CSVtoXMLConverter(csv_file)
    file = converter.to_xml_str(xml_file, xsd_file)

    """ XML FILE INSERTION """

    insert_query = "INSERT INTO public.imported_documents (file_name, xml) VALUES (%s, %s)"
    data = (xml_file, file)
    database.insert(insert_query, data)

    # signals

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    """ FUNCTION REGISTRATION """
    
    server.register_function(fetch_brands)
    server.register_function(fetch_models)

    print("\nStarting the RPC Server...")
    server.serve_forever()