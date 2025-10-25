# app/flask_server/server.py

from flask import Flask, jsonify
from flask_cors import CORS
from app.flask_server.routes.sensor_routes import sensor_bp
from app.flask_server.routes.control_routes import control_bp
from app.database.crud_operations import get_latest_sensor_data
from app.mqtt.mqtt_client import create_mqtt_client
from app.config import settings
import threading

app = Flask(__name__)
CORS(app)  # Supaya bisa diakses dari Streamlit atau frontend lain

# 🔌 Register semua route
app.register_blueprint(sensor_bp, url_prefix="/sensor")
app.register_blueprint(control_bp, url_prefix="/control")

# 🚀 Jalankan MQTT client di thread terpisah
mqtt_client = create_mqtt_client()

def run_mqtt_loop():
    mqtt_client.loop_forever()

mqtt_thread = threading.Thread(target=run_mqtt_loop)
mqtt_thread.daemon = True
mqtt_thread.start()

# 🌐 Endpoint utama
@app.route("/")
def home():
    return jsonify({
        "message": "SmartBin Flask API is running 🚀",
        "available_endpoints": ["/sensor/status", "/control/send", "/api/latest_data"]
    })

# 📦 Endpoint untuk ambil data sensor terbaru (kapasitas, suhu, kelembapan)
@app.route('/api/latest_data', methods=['GET'])
def get_latest_data():
    latest = get_latest_sensor_data(10)
    result = {"kapasitas": 0, "suhu": 0, "kelembapan": 0}
    for data in latest:
        if data["sensor_type"] == "capacity":
            result["kapasitas"] = data["value"]
        elif data["sensor_type"] == "temperature":
            result["suhu"] = data["value"]
        elif data["sensor_type"] == "humidity":
            result["kelembapan"] = data["value"]
    return jsonify(result)

# 🚦 Jalankan Flask server
if __name__ == "__main__":
    app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT, debug=settings.DEBUG_MODE)