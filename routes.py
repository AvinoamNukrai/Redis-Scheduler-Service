import time
from flask import Blueprint, request, jsonify, Response
from redis_client import ma_redis_client
from redis_storage import RedisStorage

echo_at_time_bp = Blueprint('echo_at_time', __name__)
health_check_bp = Blueprint('health_check', __name__)
redis_storage = RedisStorage(ma_redis_client)  # our redis storage object

@echo_at_time_bp.route('', methods=['POST'])
def echo_at_time():
    """
    This function responsible for scheduling a msg to be printed at some specified time in the future.
    We do this by using Redis sorted set that will store all the coming messages (for future restoring).
    :return: Json file and Key
    """
    data = request.get_json()  # parsing the req data
    if 'time' not in data or 'message' not in data or not data:  # checking req data
        return jsonify({"status": "error", "message": "invalid input"}), 400
    try:
        input_time, input_msg = int(data['time']), data['message']
        curr_time = int(time.time())
        if input_time <= curr_time:  # this is an unwanted situation, the req time is not in the future!
            return jsonify({"status": "error", "message": "'Time' is invalid, must be in the future!"}), 400
        # store messages in sorted set by score = input_time, value = input_msg
        redis_storage.store_msg(input_msg, input_time)
        return jsonify({"status": "success", "message": "message scheduled"}), 200  # success key
    except Exception as e:  # some exception
        return jsonify({"status": "error", "message": f"failed to execute request due to: {e}"}), 500


@echo_at_time_bp.route('', methods=['DELETE'])
def delete_echo():
    """
    This function deletes a scheduled message based on the message content and time.
    :return: Json response indicating success or failure
    """
    data = request.get_json()
    if 'time' not in data or 'message' not in data or not data:  # validate input
        return jsonify({"status": "error", "message": "invalid input"}), 400
    try:
        input_time, input_msg = int(data['time']), data['message']
        # Remove the message from Redis sorted set
        deleted_count = redis_storage.remove_msg(input_msg, input_time)
        if deleted_count > 0:
            return jsonify({"status": "success", "message": f"Message '{input_msg}' at time {input_time} deleted."}), 200
        else:
            return jsonify({"status": "error", "message": "Message not found or already processed"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": f"failed to execute request due to: {e}"}), 500


@health_check_bp.route('', methods=['GET'])
def health_check():
    """
    This function checks that the server is indeed working properly.
    :return: json and key status
    """
    try:
        redis_storage.redis_client.ping()  # ensure the server is running
        return jsonify({"status": "success", "message": "server is ok!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"server is not running due to: {e}"}), 500
