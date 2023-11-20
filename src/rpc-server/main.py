import signal
import sys
from lxml import etree
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from functions.csv_to_xml_converter import CSVtoXMLConverter

from functions.queries import QueryFunctions
from database.database import Database

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


with SimpleXMLRPCServer(('0.0.0.0', 9000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()
    query_functions = QueryFunctions()

    database = Database()

    def signal_handler(signum, frame):
        print("\nReceived signal")
        server.server_close()

        print("\nExiting gracefully")
        sys.exit(0)
            
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
    server.register_function(query_functions.fetch_brands)
    server.register_function(query_functions.fetch_models)
    server.register_function(query_functions.fetch_market_categories)
    server.register_function(query_functions.fetch_car_above_year)
    server.register_function(query_functions.fetch_vehicles_by_category)

    print("\nStarting the RPC Server...")
    server.serve_forever()