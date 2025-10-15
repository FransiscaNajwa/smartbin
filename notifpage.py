import streamlit as st
import pymongo

# Koneksi MongoDB (ganti dengan connection string Anda)
client = pymongo.MongoClient("mongodb+srv://user:pass@cluster.mongodb.net/smartbin_db")
db = client.smartbin_db
notifs = db.notifs

def show():
    # Judul dan navigasi
    st.title("Notifikasi Page")
    st.button("Home", on_click=lambda: st.session_state.page("Homepage"))

    # Warna latar belakang dan styling
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to right, #C3B1E1, #B0C4DE);
        }
        .stButton {
            background-color: #ffe6e6;
            border-radius: 10px;
        }
        .stSelectbox {
            background-color: #ffe6e6;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Ikon notifikasi dan tombol Clear
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("🔔")
    with col2:
        if st.button("Clear"):
            notifs.delete_many({})  # Hapus semua notifikasi dari MongoDB
            st.experimental_rerun()

    # Dropdown untuk kategori
    selected_category = st.selectbox("Semua", ["Semua", "Kapasitas Sampah", "Suhu & Kelembapan"], index=0)

    # Kategori Kapasitas Sampah
    if selected_category in ["Semua", "Kapasitas Sampah"]:
        with st.container():
            st.markdown("<h3 style='text-align: center; background-color: #ff9999; padding: 10px; border-radius: 10px;'>🔔 Kategori: Kapasitas Sampah</h3>", unsafe_allow_html=True)
            kapasitas_notifs = list(notifs.find({"category": "kapasitas"}).sort("timestamp", -1))
            if kapasitas_notifs:
                for n in kapasitas_notifs:
                    st.write(f"[{n['timestamp'].strftime('%d %b %Y, %H:%M WIB')}] {n['message']}")
            else:
                st.write("Tidak ada notifikasi untuk kategori ini.")

    # Kategori Suhu & Kelembapan
    if selected_category in ["Semua", "Suhu & Kelembapan"]:
        with st.container():
            st.markdown("<h3 style='text-align: center; background-color: #ff9999; padding: 10px; border-radius: 10px;'>🔔 Kategori: Suhu & Kelembapan</h3>", unsafe_allow_html=True)
            lingkungan_notifs = list(notifs.find({"category": "lingkungan"}).sort("timestamp", -1))
            if lingkungan_notifs:
                for n in lingkungan_notifs:
                    st.write(f"[{n['timestamp'].strftime('%d %b %Y, %H:%M WIB')}] {n['message']}")
            else:
                st.write("Tidak ada notifikasi untuk kategori ini.")

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