#### 2025-01-29-pure-python-web-server

# Building a Web Server From Scratch in Pure Python
This repository contains Python code examples accompanying the blog post [Building a Web Server From Scratch in Pure Python](https://hassaanbinaslam.github.io/myblog/posts/2025-01-29-pure-python-web-server.html).

**Purpose:**

This project is an educational exploration of building basic web servers in pure Python without relying on external libraries.  The goal is to understand the fundamental concepts of networking and concurrency by implementing several web server variations, from simple blocking servers to asynchronous I/O using `asyncio`.

**Files:**

This repository contains the following Python files, each demonstrating a different approach to building a web server:

*   **`httpd/server.py`**:  A basic web server using Python's built-in `http.server` module. This serves as a simple baseline and demonstrates the easiest way to get a web server running in Python.  It uses a single thread and blocking I/O.

*   **`sockets/server.py`**:  A web server built using raw Python sockets. This implementation provides more control and a deeper understanding of socket programming and manual HTTP response construction. It also uses a single thread and blocking I/O.

*   **`threading/server.py`**:  A threaded web server using raw sockets and the `threading` module. This version introduces concurrency by handling each incoming connection in a separate thread, significantly improving performance for concurrent requests compared to the single-threaded versions.

*   **`selectors/server_blocking.py`**:  A web server using `selectors` for asynchronous I/O, but still simulating a blocking delay with `time.sleep`. This example demonstrates the structure of a selector-based event loop but does not fully realize the benefits of non-blocking I/O due to the blocking delay.

*   **`selectors/server_nonblocking.py`**:  A web server using `selectors` and `threading.Timer` to simulate a non-blocking delay. This version attempts to overcome the blocking delay of `server_blocking.py` and shows improved concurrency by offloading the delay to a timer thread.

*   **`asyncio/server.py`**:  A web server built using Python's `asyncio` library for true asynchronous I/O. This implementation showcases the power of coroutines and `async`/`await` for writing efficient, single-threaded concurrent network applications. This is the most advanced and performant example in the repository.

**How to Run:**

To run any of these servers, simply navigate to the repository directory in your terminal and execute the corresponding Python file:

```bash
# Requires Python 3.9.20 or above.
python server.py
```

Each server will start listening on port `8000` (by default). You can then access it in your web browser or using tools like `curl` or `wget` at `http://localhost:8000`.

**Benchmarking (Reproducing Blog Post Results):**

The blog post uses [Apache Benchmark](https://httpd.apache.org/docs/2.4/programs/ab.html) (`ab`) to benchmark the performance of each server.  To reproduce the benchmark results, you can use the following command (adjust the hostname if needed, if running on a remote server replace `localhost` with your server's IP or hostname):

```bash
ab -n 1000 -c 10 http://localhost:8000/
```

*   `-n 1000`:  Sends a total of 1000 requests.
*   `-c 10`:  Uses a concurrency level of 10 (10 concurrent requests at a time).
*   `http://localhost:8000/`:  The URL of the server to benchmark.

**Dependencies:**

This project is written in pure Python and has **no external dependencies** beyond the Python standard library.  You should be able to run these examples with any standard Python installation (Python 3.9+ recommended for `asyncio` features).


Enjoy exploring and learning!

[https://hassaanbinaslam.github.io/myblog/posts/2025-01-29-pure-python-web-server.html](https://hassaanbinaslam.github.io/myblog/posts/2025-01-29-pure-python-web-server.html)