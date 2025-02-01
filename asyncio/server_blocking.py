import asyncio
import time


def blocking_sleep():
    """This simulates a blocking sleep."""
    time.sleep(0.1)  # This is a blocking sleep


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

            # Use blocking sleep in a separate task
            asyncio.create_task(
                blocking_sleep_task()
            )  # Create a separate task for the blocking sleep

            await asyncio.sleep(0.1)  # Simulate some processing time (non-blocking)
            await send_response(writer, response)  # Send the response asynchronously

        else:
            print(f"Client {addr} sent no data")
            writer.close()
            await writer.wait_closed()

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
        writer.close()
        await writer.wait_closed()


async def blocking_sleep_task():
    """Run blocking sleep in a separate task."""
    # This simulates a blocking operation
    loop = asyncio.get_event_loop()  # Get the current event loop
    await loop.run_in_executor(
        None, blocking_sleep
    )  # Run the blocking function in a separate thread


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
