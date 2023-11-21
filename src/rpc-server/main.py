import signal
import sys
from lxml import etree
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

import functions.documents as document
from functions.queries import QueryFunctions
from functions.csv_to_xml_converter import CSVtoXMLConverter

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


with SimpleXMLRPCServer(('0.0.0.0', 9000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()
    queries = QueryFunctions()

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

    # signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    """ FUNCTION REGISTRATION """
    server.register_function(document.import_document_database)
    server.register_function(document.list_documents)
    server.register_function(document.remove_documents)


    server.register_function(queries.fetch_brands)
    server.register_function(queries.fetch_models)
    server.register_function(queries.fetch_market_categories)
    server.register_function(queries.fetch_most_valuable_cars)


    print("\nStarting the RPC Server...")
    server.serve_forever()