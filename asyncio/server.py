import asyncio


async def send_response(writer, response):
    """Send the response when the timer expires."""
    try:
        writer.write(response.encode())
        await writer.drain()  # Ensure data is sent
    except Exception as e:
        print(f"Error sending response: {e}")
    finally:
        writer.close()
        await writer.wait_closed()  # Wait for the writer to close


async def handle_request(reader, writer):
    addr = writer.get_extra_info("peername")
    # print(f"Connection from {addr}")
    try:
        request_data = await reader.read(1024)  # Asynchronously read data
        request_data = request_data.decode()

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

            # Use asyncio.sleep for non-blocking delay
            await asyncio.sleep(0.1)
            asyncio.create_task(
                send_response(writer, response)
            )  # Create a task to send response asynchronously

        else:
            print(f"Client {addr} sent no data")
            writer.close()
            await writer.wait_closed()

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
        writer.close()
        await writer.wait_closed()


async def main():
    HOST = ""
    PORT = 8000

    async def accept_connection(reader, writer):
        await handle_request(reader, writer)

    server = await asyncio.start_server(accept_connection, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
