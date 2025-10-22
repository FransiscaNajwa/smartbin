import streamlit as st
import pymongo
import bcrypt

# --- KONEKSI MONGODB & MOCK DB GLOBAL ---
# Koneksi MongoDB (GANTI <SmartBin123> DENGAN KATA SANDI ASLI ANDA)
# Pastikan Anda mengganti placeholder ini dengan kata sandi asli Anda
MONGO_URI = "mongodb+srv://smartbinuser:<SmartBin123>@cluster0.inq2nbd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = pymongo.MongoClient(MONGO_URI.replace("<SmartBin123>", "YOUR_ACTUAL_PASSWORD_HERE")) # Ganti YOUR_ACTUAL_PASSWORD_HERE
    db = client.smartbin_db
    users = db.users
    if users.__class__.__name__ == 'Collection':
        st.success("Terhubung ke MongoDB. Data akan disimpan.")
except Exception as e:
    st.error(f"Gagal terhubung ke MongoDB. Pastikan string koneksi benar. Error: {e}")
    class MockUsersCollection:
        def find_one(self, query): return None
        def insert_one(self, data): st.warning("Menggunakan Mock DB. Data tidak tersimpan.")
    users = MockUsersCollection()


# Fungsi untuk navigasi halaman (menggunakan st.rerun)
def set_page(page_name):
    """Fungsi setter untuk session_state.page"""
    st.session_state.page = page_name
    st.rerun() 

# --- VISUALISASI HALAMAN REGISTER ---
def show_register():
    
    # PERBAIKAN: CSS di sini harus menghapus style JS yang tidak perlu dan fokus pada styling.
    st.markdown(
        """
        <style>
        .stApp { background-color: #C3B0E1; background: #C3B0E1; }
        .welcome { color: black; font-size: 36px; text-align: center; margin-top: 50px; }
        .slogan { color: black; font-size: 24px; text-align: center; }
        /* Mengatur form agar tetap di tengah */
        div[data-testid="stForm"] { max-width: 600px; margin: 30px auto; padding: 30px; background-color: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); }
        div[data-testid="stForm"] .stButton button { 
            background-color: black; 
            color: white; 
            border-radius: 5px; 
            margin-top: 20px; 
        }
        .stMarkdown p { text-align: center; }
        .center-link { text-align: center; margin-top: 15px; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- HEADER ---
    st.markdown(
        """
        <div class="welcome">Welcome to SmartBin</div>
        <div class="slogan">Track, Monitor, Stay Clean</div>
        <br>
        <h2 style='text-align: center;'>Register</h2>
        """,
        unsafe_allow_html=True
    )

    # Formulir pendaftaran
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Konfirmasi Password", type="password")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if not all([username, email, password, confirm_password]):
                st.error("Harap isi semua kolom!")
            elif password != confirm_password:
                st.error("Password tidak cocok!")
            else:
                # Cek ketersediaan username
                if users.find_one({"username": username}):
                    st.error("Username sudah terdaftar!")
                else:
                    # Hashing password dan menyimpan ke DB
                    # Pastikan password di-encode ke bytes sebelum hashing
                    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    
                    # Simpan data
                    users.insert_one({
                        "username": username, 
                        "email": email, 
                        # Simpan password yang sudah di-decode ke string (UTF-8)
                        "password": hashed_pw.decode('utf-8') 
                    })
                    
                    st.success("Pendaftaran berhasil! Mengarahkan ke Halaman Login...")
                    
                    # Hapus status login yang mungkin ada
                    if 'logged_in' in st.session_state: del st.session_state.logged_in
                    if 'username' in st.session_state: del st.session_state.username
                    
                    # NAVIGASI: Arahkan ke Login Page setelah sukses
                    set_page("Login") 

    # --- Tautan ke Login (Diperbaiki: Menggunakan tombol Streamlit untuk navigasi) ---
    st.markdown(
        """
        <div class="center-link">
            Sudah punya akun? 
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Gunakan 3 kolom untuk memusatkan tombol "Login"
    col_left, col_center, col_right = st.columns([1, 1, 1])
    with col_center:
        # Tombol ini yang akan memicu navigasi, terletak di bawah teks "Sudah punya akun?"
        if st.button("Login", key="reg_to_login_btn"):
            set_page("Login")


if __name__ == "__main__":
    # Inisialisasi state 'page' jika file dijalankan mandiri
    if 'page' not in st.session_state:
        st.session_state.page = "Register" 
        
    # Hanya panggil fungsi show_register jika berada di halaman Register (opsional)
    # Jika aplikasi utamanya sudah ada, ini tidak diperlukan.
    # Namun, karena ini adalah file terpisah, kita akan langsung memanggilnya.
    show_register()