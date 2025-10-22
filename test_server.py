import requests

BASE_URL = "http://127.0.0.1:5000"

print("🔍 Testing API...")

r1 = requests.get(f"{BASE_URL}/sensor/status")
print("🧩 /sensor/status →", r1.status_code, r1.json())

r2 = requests.post(f"{BASE_URL}/control/send", json={"command": "open_lid"})
print("🧩 /control/send →", r2.status_code, r2.json())
