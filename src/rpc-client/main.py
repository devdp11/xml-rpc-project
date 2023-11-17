import xmlrpc.client

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')

string = "hello world"