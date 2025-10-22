# app/flask_server/server.py
from flask import Flask, jsonify
from flask_cors import CORS
from app.flask_server.routes.sensor_routes import sensor_bp
from app.flask_server.routes.control_routes import control_bp
from app.database.crud_operations import get_latest_sensor_data
from app.mqtt.mqtt_client import create_mqtt_client
import threading

app = Flask(__name__)
CORS(app)  # supaya bisa diakses dari Streamlit nanti

# Register semua route
app.register_blueprint(sensor_bp, url_prefix="/sensor")
app.register_blueprint(control_bp, url_prefix="/control")

# MQTT client berjalan di thread terpisah
mqtt_client = create_mqtt_client()

def run_mqtt_loop():
    mqtt_client.loop_forever()

mqtt_thread = threading.Thread(target=run_mqtt_loop)
mqtt_thread.daemon = True
mqtt_thread.start()

@app.route("/")
def home():
    return jsonify({
        "message": "SmartBin Flask API is running 🚀",
        "available_endpoints": ["/sensor/status", "/control/send"]
    })
@app.route('/api/latest_data', methods=['GET'])
def get_latest_data():
    from app.database.crud_operations import get_latest_sensor_data
    latest = get_latest_sensor_data(1)
    if latest:
        data = latest[0]
        return {
            "kapasitas": data.get("value", 0),
            "suhu": data.get("temperature", 0),
            "kelembapan": data.get("humidity", 0)
        }
    return {"kapasitas": 0, "suhu": 0, "kelembapan": 0}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
