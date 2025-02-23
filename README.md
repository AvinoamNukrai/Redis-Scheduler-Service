# Redis Message Scheduler Service

A Redis-powered API designed to schedule and execute time-based messages efficiently. The system uses a Flask-based REST API and Redis as a persistent storage layer. It includes functionality for scheduling messages, ensuring fault tolerance, and handling multi-server environments with lock mechanisms to prevent message duplication.

## Key Features

- **Message Scheduling**: Schedule messages for future execution via REST API.
- **Fault Tolerance**: Messages persist through server restarts, ensuring reliability.
- **Multi-Server Safety**: Redis-based locking prevents duplicate message processing.
- **Health Monitoring**: Built-in health check endpoint to monitor system status.

## Prerequisites

### Windows

1. Install Redis:

   - Download from [Redis for Windows](https://github.com/microsoftarchive/redis/releases)
   - OR use Windows Subsystem for Linux (WSL)

2. Start Redis Server:
   ```bash
   redis-server
   ```

### Ubuntu/Linux

1. Install Redis:

   ```bash
   sudo apt update
   sudo apt install redis-server
   ```

2. Start Redis Server:
   ```bash
   sudo service redis-server start
   ```

### macOS

1. Install Redis:

   ```bash
   brew install redis
   ```

2. Start Redis Server:
   ```bash
   redis-server
   ```

## Installation

1. Clone the repository:

   ```bash
   git clone [repository-url]
   cd Redis-Scheduler-Service
   ```

2. Create and activate virtual environment:

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Unix/macOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Service

1. Ensure Redis is running (see Prerequisites)

2. Start the Flask server:
   ```bash
   python app.py
   ```
   Server runs at http://localhost:3000

## Running Tests

```bash
python test.py
```

## API Endpoints

### POST /echoAtTime

- **Description**: Schedule a message to be printed on the server console at a specific time.
- **Request Body**:
  ```json
  {
    "time": 1740307996,
    "message": "Hello from the future!"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "message": "message scheduled"
  }
  ```

### GET /health

- **Description**: Check service health
- **Response**:
  ```json
  {
    "status": "success",
    "message": "server is ok!"
  }
  ```

## Troubleshooting

1. If you get `ModuleNotFoundError: No module named 'distutils'`:

   ```bash
   pip install setuptools
   ```

2. If Redis connection fails:
   - Verify Redis is running: `redis-cli ping` should return "PONG"
   - Check Redis connection string in `appsettings.json`

## Architecture

- **Flask Server**: Handles HTTP requests and message scheduling.
- **Redis Storage**: Persists scheduled messages using Sorted Sets.
- **Scheduler**: Background thread that processes due messages.
- **Locking Mechanism**: Prevents duplicate message processing in multi-server setups.

## How It Works

1. **Scheduling Messages**: Messages are submitted via the POST /echoAtTime endpoint, specifying a future execution time. The scheduler stores these messages in a Redis Sorted Set (`scheduled_messages`), with the execution time as the score.

2. **Executing Messages**: A scheduler thread (`start_scheduler`) continuously fetches due messages (`ZRANGEBYSCORE`) and executes them. Each message is locked using a Redis key (`SETNX`) to ensure only one server processes it.

3. **Locking and Unlocking**: Locks are created with a timeout to prevent stale locks. Once a message is processed, the lock is released and the message is removed from Redis.

4. **Health Check**: The GET /health endpoint verifies the system's health by checking Redis connectivity.

## Detailed Workflow

- **Message Submission**: Users submit messages with a specific execution time via the API. These messages are stored in Redis with their execution time as the score in a sorted set.

- **Scheduler Operation**: The scheduler runs in a separate thread, continuously checking for messages that are due for execution. It uses Redis commands to fetch and process these messages.

- **Concurrency Control**: To handle multiple servers, a locking mechanism is implemented using Redis's `SETNX` command. This ensures that only one server processes a message at a time.

- **Error Handling**: The system includes robust error handling to manage invalid inputs and server errors, ensuring that the service remains reliable and responsive.

This project is designed to efficiently schedule and execute time-based messages, ensuring reliability and consistency across server restarts and in multi-server environments.

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

- if you get this error `ModuleNotFoundError: No module named 'distutils`
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
