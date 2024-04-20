from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        # Process the received data
        response_data = {'message': 'Data received successfully', 'data': data}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Send response back to the client
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

def run_server():
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Python server is running...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()