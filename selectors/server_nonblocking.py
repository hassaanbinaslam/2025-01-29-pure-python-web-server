import socket
import selectors
import threading

selector = selectors.DefaultSelector()


def send_response(conn, addr, response):
    """Send the response when the timer expires."""
    try:
        conn.sendall(response.encode())
    except Exception as e:
        print(f"Error sending response to {addr}: {e}")
    finally:
        selector.unregister(conn)
        conn.close()


def handle_request(conn, addr):
    try:
        request_data = conn.recv(1024).decode()
        if request_data:
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

            # Use threading.Timer to call send_response after a delay
            timer = threading.Timer(0.1, send_response, args=(conn, addr, response))
            timer.start()
            # Do NOT unregister here when using Timer. Unregister in send_response after sending.
            # selector.unregister(conn)

        else:
            print(f"Client {addr} sent no data")
            selector.unregister(conn)
            conn.close()
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
        selector.unregister(conn)
        conn.close()


def accept_connection(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)  # Set the connection to non-blocking
    selector.register(
        conn, selectors.EVENT_READ, lambda conn: handle_request(conn, addr)
    )
    # print(f"Connected by {addr}")


def asynchronous_server():
    HOST = ""
    PORT = 8000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        sock.setblocking(False)  # Set the main socket to non-blocking

        selector.register(sock, selectors.EVENT_READ, accept_connection)

        print(f"Listening on port {PORT}")

        while True:
            events = selector.select()  # This function returns all the events
            for key, _ in events:
                callback = key.data  # This is the function we registered earlier
                callback(key.fileobj)  # Execute callback with the socket


if __name__ == "__main__":
    asynchronous_server()
