# app/flask_server/routes/sensor_routes.py
from flask import Blueprint, jsonify
from app.database.crud_operations import get_latest_sensor_data

sensor_bp = Blueprint("sensor_bp", __name__)

@sensor_bp.route("/status", methods=["GET"])
def get_sensor_status():
    """Ambil 5 data sensor terbaru dari MongoDB."""
    data = get_latest_sensor_data(5)
    if not data:
        return jsonify({"status": "error", "message": "No sensor data found"}), 404
    return jsonify({"status": "success", "data": data}), 200
