This project is a Redis-powered API designed to schedule and execute time-based messages efficiently. The system uses a Flask-based REST API and Redis as a persistent storage layer. It includes functionality for scheduling messages, ensuring fault tolerance, and handling multi-server environments with lock mechanisms to prevent message duplication.

Key features include:
1. Message Scheduling: Users can schedule messages to be processed at specific future times via a RESTful POST endpoint. Messages are stored in a Redis Sorted Set, with the execution time as the score.

2. Fault Tolerance: Messages persist in Redis, ensuring they are retained and executed even after server restarts.

3. Multi-Server Safety: Implements Redis-based locking (SETNX) to prevent multiple servers from processing the same message.

4. RESTful API: Exposes endpoints for scheduling (POST /echoAtTime) and health checking (GET /health).

How It Works:
1. Scheduling Messages: Messages are submitted via the POST /echoAtTime endpoint, specifying a future execution time. The scheduler stores these messages in a Redis Sorted Set (scheduled_messages), with the execution time as the score.

2. Executing Messages: A scheduler thread (start_scheduler) continuously fetches due messages (ZRANGEBYSCORE) and executes them. Each message is locked using a Redis key (SETNX) to ensure only one server processes it.

3. Locking and Unlocking: Locks are created with a timeout to prevent stale locks. Once a message is processed, the lock is released and the message is removed from Redis.

4. Health Check: The GET /health endpoint verifies the system's health by checking Redis connectivity.



## Installation Instructions

1. Open the project in pycharm or any suitable IDE

2. Create and run a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```
   OR
    ```sh
    pip3 install -r requirements.txt
    ```

4. Install Redis locally
    - For macOS, you can install Redis using Homebrew:
      `brew install redis`
    - For Ubuntu, you can install Redis using apt:
      ```sh
      sudo apt update
      sudo apt install redis-server
      ```
    - For Windows, download the installation package from the Redis website or use WSL to install Redis via apt.

5. Start Redis server:
    ```sh
    redis-server
    ```

6. Run the application:
    ```sh
    python app.py
    ```
   
7. Go to http://localhost:3000/health to check if the server is up and running

* if you get this error ```ModuleNotFoundError: No module named 'distutils```
run this command
```sh
pip install setuptools
```

## Endpoints
### POST /echoAtTime
- **Description**: Schedule a message to be printed on the server console at a specific time.
- **Request Body**:
    ```json
    {
        "time": "1730104372243",
        "message": "string"
    }
    ```
