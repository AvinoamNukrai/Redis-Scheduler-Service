# Moonactive Backend Camp - Home Test Assignment

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


## Code Sections for Candidate
1. **Save Message Logic**: Add the logic to save the time and message on redis
2. **Fetch and Print Messages**: Implement the logic to fetch the messages from Redis and print them on the console at the right time
