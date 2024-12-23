from flask import Flask
from routes import echo_at_time_bp, health_check_bp
from scheduler import start_scheduler

app = Flask(__name__)

@app.route('/')
def index():
    return "Server is running!"

app.register_blueprint(echo_at_time_bp, url_prefix='/echoAtTime')
app.register_blueprint(health_check_bp, url_prefix='/health')

if __name__ == '__main__':
    start_scheduler()
    app.run(port=3000)
