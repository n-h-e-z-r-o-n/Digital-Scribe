import http.server
import socketserver

# Define the request handler class
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send HTML content
        self.wfile.write(b"<html><head><title>Simple HTTP Server</title></head>")
        self.wfile.write(b"<body><h1>Welcome to the Simple HTTP Server!</h1></body></html>")

# Set the port number
PORT = 8000

# Create an instance of the server
with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
    print("Server running on port", PORT)
    # Start the server
    httpd.serve_forever()