# 🗑️ SmartBin Project  

Selamat datang di proyek **SmartBin!**  
SmartBin adalah sistem tempat sampah pintar yang dikembangkan oleh **D4 Teknik Komputer A** untuk memantau status kapasitas, suhu, dan kelembapan tempat sampah secara **real-time**.  
Proyek ini menggunakan **ESP32**, **MQTT**, **MongoDB**, dan **Streamlit** sebagai antarmuka interaktif yang cocok untuk penggunaan pribadi maupun komunitas.  

---

## 🚀 Features  
- 🔐 **Login, Register, & Profil** — Autentikasi pengguna dan fitur edit profil.  
- 📊 **Dashboard Real-time** — Menampilkan data kapasitas, suhu, dan kelembapan tempat sampah.  
- 🔔 **Notifikasi Otomatis** — Peringatan untuk kondisi penuh, suhu tinggi, atau kelembapan berlebih.  
- 🧾 **Riwayat Sensor** — Menampilkan log data sensor terbaru.  

---

## ⚙️ Installation  

### ✅ Prasyarat  
- Python 3.8 atau lebih tinggi  
- pip (Python package manager)  
- MongoDB (lokal atau cloud)  
- MQTT broker (misal: HiveMQ)  

### 📦 Langkah Instalasi  
1. **Clone repository:**
   ```bash
   git clone https://github.com/yourusername/smartbin.git
   cd smartbin
2. Install dependencies:
    pip install -r requirements.txt
3. Konfigurasi koneksi database & MQTT:
    - Edit file app/config/secrets.toml untuk URI MongoDB
    - Edit file app/mqtt/mqtt_client.py untuk broker MQTT
4. Jalankan subscriber MQTT:
    python app/mqtt/mqtt_subscriber.py
5. Jalankan aplikasi Streamlit:
    streamlit run app/main.py

🔌 Hardware
- ESP32 — sebagai mikrokontroler utama
- Ultrasonik HC-SR04 — mendeteksi kapasitas sampah
- DHT11 — membaca suhu dan kelembapan

📍 Dibuat oleh:
3 D4 Teknik Komputer A — @SmartBin