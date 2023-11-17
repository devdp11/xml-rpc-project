import signal
import sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from functions.csv_to_xml_converter import CSVtoXMLConverter

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('0.0.0.0', 9000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def signal_handler(signum, frame):
        print("\nReceived signal")
        server.server_close()

        # Perform cleanup, etc. here...

        print("\nExiting gracefully")
        sys.exit(0)

    # Signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        if hasattr(signal, 'SIGHUP'):
            signal.signal(signal.SIGHUP, signal_handler)
    except AttributeError:
        print("\nSIGHUP not supported on this platform")

    converter = CSVtoXMLConverter("data/data.csv")
    xml_str = converter.to_xml_str()
    converter.save_to_file('data.xml')
    print(xml_str)

    print("\nStarting the RPC Server...")
    server.serve_forever()
