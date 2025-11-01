🗑️ SmartBin Project
Selamat datang di proyek SmartBin! Aplikasi ini dirancang untuk memantau dan mengelola tempat sampah secara cerdas menggunakan Streamlit. Fitur-fitur utama meliputi pelacakan kapasitas, pemantauan suhu dan kelembapan, notifikasi kondisi kritis, manajemen profil pengguna, dan visualisasi data historis.

📌 Overview
SmartBin adalah alat yang dikembangkan oleh D4 Teknik Komputer A untuk membantu pengguna memantau status tempat sampah, menerima peringatan otomatis, dan mengelola profil pengguna. Proyek ini menggunakan Streamlit sebagai antarmuka interaktif dan cocok untuk penggunaan pribadi maupun komunitas.

🚀 Features
- 🔐 Login & Registrasi: Autentikasi pengguna yang aman dengan fitur edit profil.
- 📊 Dashboard: Pemantauan real-time kapasitas, suhu, dan kelembapan tempat sampah. Notifikasi berisi peringatan otomatis untuk kondisi seperti penuh, suhu tinggi, atau kelembapan berlebih.
- 📁 Riwayat: Lihat data historis dan log status tempat sampah.
- 👤 Edit Profil: Perbarui informasi pengguna dengan mudah.

⚙️ Installation
✅ Prasyarat
- Python 3.7 atau lebih tinggi
- pip (Python package manager)
- MongoDB (lokal atau cloud)
- MQTT broker (misalnya Mosquitto)
📦 Langkah Instalasi
- Clone repository:
git clone https://github.com/yourusername/smartbin.git
cd smartbin
- Install dependencies:
pip install -r requirements.txt
- Konfigurasi database dan MQTT:
- Edit file app/mqtt/mqtt_config.py dan app/database/mongo_client.py sesuai URI dan kredensial kamu.
- Jalankan aplikasi Streamlit:
streamlit run streamlit_app/main.py