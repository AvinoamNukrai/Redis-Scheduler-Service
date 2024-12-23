# Redis-Scheduler-Service
This project is a Redis-powered API designed to schedule and execute time-based messages efficiently. 
The system uses a Flask-based REST API and Redis as a persistent storage layer. It includes functionality for scheduling messages, ensuring fault tolerance, and handling multi-server environments with lock mechanisms to prevent message duplication. 

Key features include:
1. Message Scheduling:
Users can schedule messages to be processed at specific future times via a RESTful POST endpoint.
Messages are stored in a Redis Sorted Set, with the execution time as the score.

2. Fault Tolerance:
Messages persist in Redis, ensuring they are retained and executed even after server restarts.

3. Multi-Server Safety:
Implements Redis-based locking (SETNX) to prevent multiple servers from processing the same message.

4. RESTful API:
Exposes endpoints for scheduling (POST /echoAtTime) and health checking (GET /health).


How It Works:
1. Scheduling Messages:
Messages are submitted via the POST /echoAtTime endpoint, specifying a future execution time.
The scheduler stores these messages in a Redis Sorted Set (scheduled_messages), with the execution time as the score.

2. Executing Messages:
A scheduler thread (start_scheduler) continuously fetches due messages (ZRANGEBYSCORE) and executes them.
Each message is locked using a Redis key (SETNX) to ensure only one server processes it.

3. Locking and Unlocking:
Locks are created with a timeout to prevent stale locks.
Once a message is processed, the lock is released and the message is removed from Redis.

4. Health Check:
The GET /health endpoint verifies the system's health by checking Redis connectivity.
