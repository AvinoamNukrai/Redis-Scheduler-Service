import time
import base64
from flask import Blueprint, request, jsonify, Response
from redis_client import ma_redis_client
from redis_storage import RedisStorage

echo_at_time_bp = Blueprint('echo_at_time', __name__)
health_check_bp = Blueprint('health_check', __name__)
redis_storage = RedisStorage(ma_redis_client) # our redis storage object

@echo_at_time_bp.route('', methods=['POST'])
def echo_at_time():
    """
    This function responsible for schedule a msg to be printed at some specified time in the future.
    We doing this by using Redis sorted set that will store all the coming messages (for future restoring).
    :return: Json file and Key
    """
    data = request.get_json() # parsing the req data
    # Logic to save to redis will be added here
    if 'time' not in data or 'message' not in data or not data: # checking req data
        return jsonify({"status":"error", "message":"invalid input"}), 400
    try:
       input_time, input_msg = int(data['time']), data['message']
       curr_time = int(time.time())
       if input_time <= curr_time: # this is unwanted situation, the req time is not in the future!
           return jsonify({"status": "error", "message": "'Time' is invalid, must be in the future!"}), 400
       # store messages in sorted set by score = input_time, value = input_msg
       redis_storage.store_msg(input_msg, input_time)
       return jsonify({"status": "success", "message": "message scheduled"}), 200 # success key
    except Exception as e: # some exception
        return jsonify({"status":"error", "message":f"failed execute request due to: {e}"}), 500
    # return jsonify({ "status": "Received your request" })

@health_check_bp.route('', methods=['GET'])
def health_check():
    """
    This function responsible to check that the server is indeed works properly
    :return: json and key status
    """
    base64_image = 'IC4uLiAgICAuLi4gICAuLi4uLi4gIC4uLi4uLiAgLi4uICAuLi4gIC' \
                   'AjIyMjICAjIyMjIyggIyMjIyMjIyAlIyMgIyMsICAlIyMgIyMvLy4KIC4' \
                   'uLi4gICAuLi4gIC4uLiAgLi4gLi4uICAuLiAgLi4uICAuLi4gICAjIy' \
                   'MjICAoIyMgICAgICAjIyMgICAqJSUgJSMjICAjIyAgIyMgICAKIC4uLi4' \
                   'uIC4uLi4uIC4uLiAgLi4uLi4uICAuLi4gLi4uLiAuLi4gICUjJSMjKCAv' \
                   'IyMgICAgICAjIyMgICAsIyMgLiMjIC4jIyAgIyMgICAKIC4uLi4uIC4uL' \
                   'i4uIC4uLiAgLi4uLi4uICAuLi4gLi4uLi4uLi4gICMjIC4jIyAqIyMgICAg' \
                   'ICAjIyMgICAqIyMgICMjICUjIyAgIyMgICAKIC4uLi4uLi4uLi4uIC4uL' \
                   'iAgLi4uLi4uICAuLi4gLi4uLi4uLi4gICMjIyMjIyAuIyMgICAgICAjI' \
                   'yMgICAoIyMgICMjLyMjLiAgIyMjIyAKIC4uIC4uLi4uIC4uIC4uLiAgL' \
                   'i4uLi4uICAuLi4gLi4gLi4uLi4gKiMjICAjIyAgIyMsICAgICAjIyMgIC' \
                   'AlIyMgICgjIyMjICAgIyMgICAKIC4uIC4uLi4gIC4uLiAuLiAgLi4gIC4u' \
                   'ICAuLiAuLi4gIC4uLi4gJSMjICAjIy8gIyMjICAgICAjIyMgICAlIyMgI' \
                   'CAjIyMjICAgIyMgICAKLi4uICAuLi4gIC4uLiAuLi4uLi4gIC4uLi4uLiA' \
                   'uLi4gIC4uLi4gIyMsICAjIyMgIyMjIyMgICAjIyMgICAoIyMgICAjIyMvICAgIyMjIyM='

    # image = base64.b64decode(base64_image).decode('utf-8')
    # print(ma_redis_client.set('key', 'value'))
    # print(ma_redis_client.get('key'))
    # return Response(image, mimetype='text/plain')
    try:
        redis_storage.redis_client.ping() # unsure the server is running
        return jsonify({"status": "success", "message": "server is ok!"}), 200
    except Exception as e:
        return jsonify({"status":"error", "message":f"server is not running due to: {e}"}), 500




