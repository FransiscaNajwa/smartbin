import streamlit as st
import pymongo
import bcrypt

# Koneksi MongoDB (GANTI <SmartBin123> DENGAN KATA SANDI ASLI ANDA)
# Disarankan mengganti <SmartBin123> dengan kata sandi asli. Saya biarkan untuk mencegah error sintaks.
try:
    client = pymongo.MongoClient("mongodb+srv://smartbinuser:<SmartBin123>@cluster0.inq2nbd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.smartbin_db
    users = db.users
except Exception as e:
    # Error handling jika koneksi gagal (Anda bisa hapus ini jika koneksi MongoDB Anda stabil)
    st.error(f"Gagal terhubung ke MongoDB. Pastikan string koneksi benar. Error: {e}")
    class MockUsersCollection:
        def find_one(self, query): return None
        def insert_one(self, data): st.warning("Menggunakan Mock DB. Data tidak tersimpan.")
    users = MockUsersCollection()


# Fungsi untuk navigasi halaman melalui tautan HTML (diperlukan untuk tautan Login)
def set_page(page_name):
    """Fungsi setter untuk session_state.page"""
    st.session_state.page = page_name

def show():
    # Inisialisasi session state jika belum ada
    if 'page' not in st.session_state:
        st.session_state.page = "Register"
        
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

        /* Styling Form (DIBUAT LEBIH LEBAR) */
        div[data-testid="stForm"] {
            max-width: 5000px; /* Diubah dari 400px menjadi 600px */
            margin: 30px auto;
            padding: 30px; /* Padding ditingkatkan */
            background-color: white; 
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Bayangan ditingkatkan */
        }
        
        /* Styling tombol Submit */
        div[data-testid="stForm"] .stButton button {
            background-color: black;
            color: white;
            border-radius: 5px;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- HEADER ---
    # st.title("Register") Dihapus karena akan tumpang tindih dengan markdown
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
                if users.find_one({"username": username}):
                    st.error("Username sudah terdaftar!")
                else:
                    # Pastikan password di-encode sebelum hashing
                    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    
                    # Simpan data user
                    users.insert_one({"username": username, "email": email, "password": hashed_pw.decode('utf-8')})
                    
                    st.success("Pendaftaran berhasil! Mengarahkan ke login...")
                    set_page("Login")
                    st.experimental_rerun()

    # Tautan ke Login
    st.markdown(
        """
        <p style='text-align: center;'>
            Sudah punya akun? 
            <a href='#' onClick='change_page("Login")' style='color: black; font-weight: bold;'>Login</a>
        </p>
        """, 
        unsafe_allow_html=True
    )

    # Note: Blok CSS latar belakang di akhir kode sebelumnya sudah dihapus dan dipindah ke blok CSS di awal fungsi show()
    

if __name__ == "__main__":
    show()