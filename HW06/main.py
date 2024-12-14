import http.server
import urllib.parse
import socket
import multiprocessing
import datetime
import json
import socketserver
from pymongo import MongoClient
import mimetypes
import os

class HTTPRequestsHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        elif self.path == "/message.html":
            self.path = "/message.html"
        elif self.path == '/error.html':
            self.path = '/error.html'

        file_path = os.getcwd() + self.path
        if os.path.exists(file_path):
            self.send_response(200)
            # Get MIME type
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type:
                self.send_header('Content-type', content_type)
            else:
                self.send_header('Content-type', 'application/octet-stream')
            
            self.end_headers()

            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            # If file has not been found then return 404 error
            self.send_response(404)
            self.path = '/error.html'
            self.end_headers()
            with open(os.getcwd() + self.path, 'rb') as err_file:
                self.wfile.write(err_file.read())

    def do_POST(self):
        try:
            content_len = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_len)

            form_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            username = form_data.get('username', [''])[0]
            message = form_data.get('message', [''])[0]

            data_to_send = {'username': username, 'message': message}
            send_to_socket_server(data_to_send)

            if not username or not message:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><h1>400 Bad Request: Fields are empty</h1></html>")
                return

            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
            
        except Exception as e:
            print(f"Error: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><h1>500 Internal Server Error</h1></html>")

def send_to_socket_server(data):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(data).encode('utf-8'), ('127.0.0.1', 5000))

def socket_server():
    client = MongoClient('mongodb://mongo:27017/')
    db = client.messages
    messages_collection = db.messages

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('0.0.0.0', 5000))
        while True:
            data, _ = s.recvfrom(1024)
            message_dict = json.loads(data.decode('utf-8'))
            message_dict['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            messages_collection.insert_one(message_dict)

def start_http_server():
    PORT = 3000
    with socketserver.TCPServer(('0.0.0.0', PORT), HTTPRequestsHandler) as httpd:
        print(f"HTTP server is running on port: {PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    http_process = multiprocessing.Process(target=start_http_server)
    socket_process = multiprocessing.Process(target=socket_server)

    http_process.start()
    socket_process.start()

    http_process.join()
    socket_process.join()

