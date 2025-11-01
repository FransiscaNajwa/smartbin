import sys
from pathlib import Path

# Pastikan path root (folder SmartBin) masuk ke sys.path
ROOT_DIR = Path(__file__).resolve().parent
APP_DIR = ROOT_DIR / "app"
if str(APP_DIR) not in sys.path:
    sys.path.append(str(APP_DIR))

# Coba impor koneksi database
try:
    from database.connection import db
except ModuleNotFoundError as e:
    print("❌ Gagal impor modul database. Pastikan struktur folder seperti ini:")
    print("   SmartBin/app/database/connection.py")
    print("   Dan file ini (clear_data.py) ada di SmartBin/")
    raise e

def clear_sensor_data():
    confirm = input("⚠️ Apakah kamu yakin ingin menghapus SEMUA data sensor? (y/n): ").lower()
    if confirm == 'y':
        result = db["sensor_data"].delete_many({})
        print(f"✅ {result.deleted_count} data sensor berhasil dihapus.")
    else:
        print("❌ Operasi dibatalkan.")

if __name__ == "__main__":
    clear_sensor_data()
