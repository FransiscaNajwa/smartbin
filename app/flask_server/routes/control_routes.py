# app/flask_server/routes/control_routes.py
from flask import Blueprint, request, jsonify
from app.mqtt.mqtt_client import publish_sensor_data, create_mqtt_client

control_bp = Blueprint("control_bp", __name__)
mqtt_client = create_mqtt_client()

@control_bp.route("/send", methods=["POST"])
def send_control_command():
    """Kirim perintah ke topik MQTT SmartBin/control"""
    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"status": "error", "message": "Command not found"}), 400

    command = data["command"]
    mqtt_client.publish("SmartBin/control", command)
    return jsonify({"status": "success", "message": f"Command '{command}' sent via MQTT"}), 200
