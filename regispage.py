import streamlit as st
import pymongo
import bcrypt

# Koneksi MongoDB (ganti dengan connection string Anda)
client = pymongo.MongoClient("mongodb+srv://smartbinuser:<SmartBin123>@cluster0.inq2nbd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.smartbin_db
users = db.users

def show():
    # Bagian selamat datang
    st.markdown(
        """
        <style>
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
        </style>
        <div class="welcome">Welcome to SmartBin</div>
        <div class="slogan">Track, Monitor, Stay Clean</div>
        """,
        unsafe_allow_html=True
    )

    # Judul dan desain halaman
    st.title("Register")

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
                    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                    users.insert_one({"username": username, "email": email, "password": hashed_pw})
                    st.success("Pendaftaran berhasil! Mengarahkan ke login...")
                    st.session_state.page = "Login"
                    st.experimental_rerun()

    # Tautan ke Login
    st.markdown("<p>Sudah punya akun? <a href='#' onClick='change_page(\"Login\")'>Login</a></p>", unsafe_allow_html=True)

    # Warna latar belakang
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to right, #C3B1E1, #B0C4DE);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    show()