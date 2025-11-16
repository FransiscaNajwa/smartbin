from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient, errors
import bcrypt

from app.config.settings import MONGO_URI, MONGO_USER_COLLECTION, MONGO_DB_NAME

# ⚙️ Inisialisasi koneksi MongoDB
client = MongoClient(MONGO_URI, tls=True, serverSelectionTimeoutMS=5000)
db = client[MONGO_DB_NAME]  # langsung pilih database

def ensure_db():
    """Pastikan koneksi database aktif."""
    try:
        client.admin.command("ping")
    except errors.ConnectionFailure as e:
        raise ConnectionError(f"❌ Database belum terhubung: {e}")

# 🔐 Hashing & Verifikasi Password
def hash_password(password: str) -> bytes:
    """Hash password menggunakan bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def check_password(password: str, hashed: bytes) -> bool:
    """Verifikasi password dengan hash."""
    if isinstance(hashed, str):
        hashed = hashed.encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

# 👤 CRUD Pengguna
def register_user(username: str, password: str, email: str) -> str:
    """Daftarkan pengguna baru ke MongoDB."""
    ensure_db()

    # Cegah duplikasi username/email
    if db[MONGO_USER_COLLECTION].find_one({"$or": [{"email": email}, {"username": username}]}):
        raise ValueError("❌ Username atau email sudah digunakan.")

    user = {
        "username": username,
        "password": hash_password(password),
        "email": email,
        "created_at": datetime.utcnow()
    }

    result = db[MONGO_USER_COLLECTION].insert_one(user)
    return str(result.inserted_id)

def get_user_by_email(email: str):
    ensure_db()
    return db[MONGO_USER_COLLECTION].find_one({"email": email})

def get_user_by_username(username: str):
    ensure_db()
    return db[MONGO_USER_COLLECTION].find_one({"username": username})

def get_user_by_id(user_id: str):
    ensure_db()
    try:
        return db[MONGO_USER_COLLECTION].find_one({"_id": ObjectId(user_id)})
    except Exception:
        return None

def verify_user(email: str, password: str):
    """Verifikasi login user berdasarkan email dan password."""
    ensure_db()
    user = get_user_by_email(email)
    if user and check_password(password, user["password"]):
        return user
    return None

def update_user_profile(user_id: str, email=None, username=None, password=None) -> bool:
    """Perbarui profil pengguna."""
    ensure_db()
    update_fields = {}

    if email:
        update_fields["email"] = email
    if username:
        update_fields["username"] = username
    if password:
        update_fields["password"] = hash_password(password)

    if not update_fields:
        return False  # Tidak ada field yang diubah

    try:
        result = db[MONGO_USER_COLLECTION].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_fields}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"❌ Gagal update user: {e}")
        return False
