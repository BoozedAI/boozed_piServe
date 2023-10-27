from flask import Flask, render_template, jsonify, request
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
latest_order_time = None

@app.route('/')
def index():
    return "Boozed Dispenser Service is Running!"

@app.route('/display')
def display_page():
    return render_template('display.html')

@app.route('/check_order')
def check_order():
    global latest_order_time
    start_time = datetime.now()
    # Wait for an update or timeout after 10 seconds
    while (datetime.now() - start_time).seconds < 10:
        if latest_order_time:
            time_to_send = latest_order_time.strftime('%Y-%m-%d %H:%M:%S')
            latest_order_time = None
            return jsonify({"message": "Order Received", "time": time_to_send})
    return jsonify({"message" : "No New Orders"})

@app.route('/receive_order', methods=['POST'])
def receive_order():
    global latest_order_time
    latest_order_time = datetime.now()
    return jsonify({"message": "Order received by Raspberry Pi"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

