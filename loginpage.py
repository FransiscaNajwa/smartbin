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
            margin-top: 20px;
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
    st.title("Login")

    # Form login
    with st.form("login_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            user = users.find_one({"username": username, "email": email})
            if user and bcrypt.checkpw(password.encode(), user["password"]):
                st.success("Login berhasil! Mengarahkan ke dashboard...")
                st.session_state.logged_in = True
                st.session_state.page = "Homepage"  # Diarahkan ke Home Page setelah login
                st.experimental_rerun()
            else:
                st.error("Username/email/password salah!")

    # Tautan ke Register
    st.markdown("<p>Tidak punya akun? <a href='#' onClick='change_page(\"Register\")'>Register</a></p>", unsafe_allow_html=True)

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