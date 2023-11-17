import signal
import sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from functions.csv_to_xml_converter import CSVtoXMLConverter
from models.database import Database

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


with SimpleXMLRPCServer(('0.0.0.0', 9000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def signal_handler(signum, frame):
        print("\nReceived signal")
        server.server_close()

        print("\nExiting gracefully")
        sys.exit(0)

    csv_file = "/data/data.csv"
    xml_file = "/data/data.xml"
    xsd_file = "/data/schemas/data.xsd"

    converter = CSVtoXMLConverter(csv_file)
    converter.to_xml_str(xml_file,xsd_file)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    print("\nStarting the RPC Server...")
    server.serve_forever()