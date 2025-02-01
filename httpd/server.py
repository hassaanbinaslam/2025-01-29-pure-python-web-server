import http.server
import time
from http import HTTPStatus

PORT = 8000

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Simulate a database call
        time.sleep(0.1)

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response_html = """
            <html>
                <head>
                    <title>My Basic Server</title>
                </head>
                <body>
                    <h1>Hello from my basic server</h1>
                </body>
            </html>
        """
        self.wfile.write(response_html.encode())

if __name__ == "__main__":
    with http.server.HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()