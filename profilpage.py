import streamlit as st
import pymongo

# Koneksi MongoDB (ganti dengan connection string Anda)
client = pymongo.MongoClient("mongodb+srv://user:pass@cluster.mongodb.net/smartbin_db")
db = client.smartbin_db
users = db.users

def show():
    # Judul dan navigasi
    st.title("Profile Page")
    st.button("Home", on_click=lambda: st.session_state.page("Homepage"))

    # Warna latar belakang dan styling
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to right, #C3B1E1, #B0C4DE);
        }
        .stContainer {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 20px auto;
            max-width: 400px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Selamat datang dan informasi profil
    st.markdown("<h1 style='text-align: center;'>Welcome to Profile Page</h1>", unsafe_allow_html=True)
    user = users.find_one({"username": st.session_state.username})  # Asumsi st.session_state.username disimpan saat login
    if user:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://via.placeholder.com/100", width=100, caption="Foto Profil")
        with col2:
            st.write(f"Nama: {user.get('name', 'Not set')}")
            st.write(f"Email: {user.get('email', 'Not set')}")
            st.write(f"Username: {user.get('username', 'Not set')}")

    # Formulir edit profil
    with st.container():
        st.markdown("<h3 style='text-align: center;'>Profile Edit</h3>", unsafe_allow_html=True)
        with st.form("profile_form"):
            name = st.text_input("Name", user.get('name', ''))
            email = st.text_input("Email", user.get('email', ''))
            username = st.text_input("Username", user.get('username', ''))
            submitted = st.form_submit_button("Save")

            if submitted:
                if not all([name, email, username]):
                    st.error("Harap isi semua kolom!")
                else:
                    users.update_one({"_id": user["_id"]}, {"$set": {"name": name, "email": email, "username": username}})
                    st.success("Profil diperbarui!")

    # Footer
    st.markdown(
        """
        <div style='text-align: center; margin-top: 60px; font-style: italic; color: black;'>
        D4 Teknik Komputer A @SmartBin
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    show()