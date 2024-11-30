import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import os

PORT = 8080
UPLOAD_DIR = './uploads'  # 指定存放上传文件的目录
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            boundary = post_data.split(b'\r\n')[0]
            file_data = post_data.split(boundary)[1].split(b'\r\n\r\n')[1].rsplit(b'\r\n--', 1)[0]
            
            filename = 'uploaded_file'
            for line in post_data.split(b'\r\n'):
                if b'filename=' in line:
                    filename = line.split(b'filename=')[-1].strip().decode('utf-8').replace('"','')
                    break
            
            with open(os.path.join(UPLOAD_DIR, filename), 'wb') as f:
                f.write(file_data)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'File uploaded successfully.')
        else:
            super().do_POST()

with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()