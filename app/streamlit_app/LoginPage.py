import streamlit as st
from pathlib import Path
import sys

# === Setup Path untuk import internal ===
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.database.crud_operations import verify_user
from app.mqtt.mqtt_client import publish_login_event
from app.streamlit_app.utils.session_manager import go_to_page


def show_login_page():
    st.set_page_config(page_title="Login | SmartBin", layout="wide")

    LEFT_COLOR = "#B0A8DC"
    RIGHT_COLOR = "#AAB3EF"

    # ===== CSS Styling untuk layout fullscreen =====
    st.markdown(f"""
        <style>
        .block-container {{
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }}
        [data-testid="stHeader"], [data-testid="stToolbar"] {{
            display: none !important;
        }}

        body {{
            margin: 0;
            overflow: hidden;
        }}

        .split-container {{
            display: flex;
            flex-direction: row;
            width: 100vw;
            height: 100vh;
        }}

        .left {{
            flex: 1;
            background-color: {LEFT_COLOR};
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .right {{
            flex: 1;
            background-color: {RIGHT_COLOR};
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #222;
        }}

        .login-box {{
            width: 80%;
            max-width: 400px;
            background-color: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}

        .login-box h1 {{
            text-align: center;
            font-size: 32px;
            color: #4B0082;
            margin-bottom: 20px;
            font-weight: 800;
        }}

        .stTextInput label {{
            font-weight: 600 !important;
        }}

        .register-text {{
            text-align: center;
            font-size: 15px;
            margin-top: 10px;
        }}

        .register-text a {{
            color: #0047ff;
            text-decoration: none;
            font-weight: 600;
        }}
        </style>
    """, unsafe_allow_html=True)

    # ===== Struktur HTML utama (split kiri-kanan) =====
    st.markdown("""
        <div class="split-container">
            <div class="left" id="left-pane">
                <div class="login-box">
                    <h1>Login</h1>
        """, unsafe_allow_html=True)

    # ===== Form login =====
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Masukkan username")
        email = st.text_input("Email", placeholder="Masukkan email")
        password = st.text_input("Password", type="password", placeholder="Masukkan password")
        submitted = st.form_submit_button("Login")

        if submitted:
            user = verify_user(email, password)
            if user:
                st.session_state["user"] = user["username"]
                try:
                    publish_login_event(user["username"])
                except Exception:
                    st.warning("⚠️ Login berhasil, tapi gagal publish event MQTT.")
                st.success("✅ Login berhasil! Mengarahkan ke HomePage...")
                go_to_page("HomePage")
            else:
                st.error("❌ Username, email, atau password salah.")

    # ===== Tombol & link register =====
    st.markdown("""
        <div class="register-text">
            <p>Belum punya akun?</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Register", use_container_width=True):
        go_to_page("RegisterPage")

    # ===== Panel kanan =====
    st.markdown("""
            </div> <!-- Tutup login-box -->
        </div> <!-- Tutup left pane -->

        <div class="right">
            <h1 style="font-size:44px; font-weight:800; margin:0;">Welcome to<br>SmartBin</h1>
            <p style="font-size:24px; margin-top:20px;">Track, Monitor,<br>Stay Clean</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show_login_page()
