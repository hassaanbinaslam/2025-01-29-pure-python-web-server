import socket
import threading
import time


def handle_request(conn, addr):
    try:
        request_data = conn.recv(1024).decode()
        if request_data:
            # Simulate a database call or some processing
            time.sleep(0.1)  # 100 milliseconds delay
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
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: text/html\r\n"
            response += f"Content-Length: {len(response_html)}\r\n"
            response += "\r\n"
            response += response_html
            conn.sendall(response.encode())
        else:
            print(f"Client {addr} sent no data")
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()


def threaded_server():
    HOST = ""
    PORT = 8000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on port {PORT}")
        while True:
            conn, addr = s.accept()
            # print(f"Connected by {addr}")
            thread = threading.Thread(target=handle_request, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    threaded_server()
