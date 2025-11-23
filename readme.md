🗑️ SmartBin Project

Selamat datang di proyek SmartBin!

SmartBin adalah sistem tempat sampah pintar yang dikembangkan oleh D4 Teknik Komputer A untuk memantau status kapasitas, suhu, dan kelembapan tempat sampah secara real-time.
Proyek ini menggunakan ESP32, MQTT, MongoDB, dan Streamlit sebagai antarmuka interaktif yang cocok untuk penggunaan pribadi maupun komunitas.

---

🚀 Features
- 🔐 Login, Register, & Profil — Autentikasi pengguna dan fitur edit profil.
- 📊 Dashboard Real-time — Menampilkan data kapasitas, suhu, dan kelembapan tempat sampah.
- 🔔 Notifikasi Otomatis — Peringatan untuk kondisi penuh, suhu tinggi, atau kelembapan berlebih.
- 🧾 Riwayat Sensor — Menampilkan log data sensor terbaru

---

⚙️ Installation
✅ Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package manager)
- MongoDB (lokal atau cloud)
- MQTT broker (misal: HiveMQ)

📦 Langkah Instalasi
- Clone repository:
git clone https://github.com/FransiscaNajwa/smartbin 

cd smartbin
- Install dependencies:
pip install -r requirements.txt
- Konfigurasi koneksi database & MQTT:
- Edit file app/config/secrets.toml untuk URI MongoDB
- Edit file app/mqtt/mqtt_client.py untuk broker MQTT
- Jalankan subscriber MQTT:
python app/mqtt/mqtt_subscriber.py
- Jalankan aplikasi Streamlit:
streamlit run app/main.py

---

🔌 Hardware
- ESP32 — sebagai mikrokontroler utama
- Ultrasonik HC-SR04 — mendeteksi kapasitas sampah
- DHT11 — membaca suhu dan kelembapan

---

📲 SmartBin Notifier (Telegram Bot)

SmartBin dilengkapi dengan bot Telegram untuk mengirim notifikasi otomatis.
- Link bot: https://t.me/smartbinnotifbot
- Cara akses:
- Buka link bot di aplikasi Telegram.
- Klik Start untuk mulai berinteraksi.
- Setelah itu, sistem akan mencatat chat_id pengguna.
- Semua notifikasi (penuh, suhu tinggi, kelembapan tinggi) akan dikirim ke chat Telegram pengguna.

---

🏗️ Arsitektur Sistem
- ESP32 → membaca data sensor (kapasitas, suhu, kelembapan).
- MQTT Broker → menyalurkan data sensor ke server.
- Python Subscriber → menerima data, simpan ke MongoDB, deteksi threshold.
- MongoDB → menyimpan log sensor.
- Notification Helper → kirim notifikasi ke Telegram & Email.
- Streamlit Web App → dashboard real-time, riwayat, dan halaman notifikasi.

---

📍 Dibuat oleh
3 D4 Teknik Komputer A — @SmartBin