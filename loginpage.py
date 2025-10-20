import streamlit as st
import pymongo
import bcrypt

# Koneksi MongoDB (TETAP SESUAI PERMINTAAN ANDA)
# PERINGATAN: Pastikan Anda mengganti <SmartBin123> dengan kata sandi asli Anda
client = pymongo.MongoClient("mongodb+srv://smartbinuser:<SmartBin123>@cluster0.inq2nbd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.smartbin_db
users = db.users

# Fungsi untuk navigasi halaman melalui tautan HTML
def set_page(page_name):
    """Fungsi setter untuk session_state.page"""
    st.session_state.page = page_name

def show():
    # Inisialisasi session state jika belum ada
    if 'page' not in st.session_state:
        st.session_state.page = "Login"
        
    # --- CSS GLOBAL & FUNGSIONALITAS JAVASCRIPT ---
    st.markdown(
        """
        <script>
            function change_page(page_name) {
                // Mengirim pesan ke Streamlit saat tautan diklik
                window.parent.postMessage({
                    type: 'streamlit:setSessionState',
                    key: 'page',
                    value: page_name
                }, '*');
            }
        </script>
        <style>
        /* 1. Warna latar belakang keseluruhan aplikasi: Ungu muda solid */
        .stApp {
            background-color: #C3B0E1; /* Ungu Muda Solid */
            background: #C3B0E1; 
        }
        
        /* Styling untuk Welcome dan Slogan */
        .welcome {
            color: black;
            font-size: 36px;
            text-align: center;
            margin-top: 50px; 
        }
        .slogan {
            color: black;
            font-size: 24px;
            text-align: center;
        }

        /* Styling Form (Dibuat LEBIH LEBAR dan TERPUSAT) */
        div[data-testid="stForm"] {
            max-width: 600px; /* Lebar formulir */
            margin: 30px auto;
            padding: 30px; 
            background-color: white; /* Latar belakang putih */
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); 
        }
        
        /* Styling tombol Submit/Login */
        div[data-testid="stForm"] .stButton button {
            background-color: black;
            color: white;
            border-radius: 5px;
            margin-top: 20px;
        }

        /* Styling tautan Login/Register */
        .stMarkdown p {
            text-align: center;
        }
        
        /* Styling untuk judul 'Login' */
        .login-title {
            text-align: center;
            font-size: 2em;
            margin-top: 0;
            margin-bottom: 20px;
        }
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
        <h2 class="login-title">Login</h2>
        """,
        unsafe_allow_html=True
    )

    # Form login
    with st.form("login_form"):
        # Saya asumsikan Anda ingin menggunakan Username, Email, dan Password dari kode asli Anda
        username = st.text_input("Username")
        email = st.text_input("Email") # Dikembalikan sesuai kode awal Anda
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            # Menggunakan query yang mencari berdasarkan Username DAN Email
            user = users.find_one({"username": username, "email": email}) 
            
            # Cek password
            if user and 'password' in user:
                 # Menggunakan .encode('utf-8') untuk memastikan perbandingan byte-to-byte yang benar
                stored_password = user["password"].encode('utf-8') if isinstance(user["password"], str) else user["password"]
                
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    st.success("Login berhasil! Mengarahkan ke dashboard...")
                    st.session_state.logged_in = True
                    st.session_state.username = username # Simpan username untuk halaman profile
                    st.session_state.page = "Homepage"  
                    st.experimental_rerun()
                else:
                    st.error("Username/email/password salah!")
            else:
                st.error("Username/email/password salah!")

    # Tautan ke Register
    st.markdown(
        """
        <p style='text-align: center;'>
            Tidak punya akun? 
            <a href='#' onClick='change_page("Register")' style='color: black; font-weight: bold;'>Register</a>
        </p>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    show()