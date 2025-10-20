import streamlit as st
import pymongo
from datetime import datetime, timedelta
import random

# --- KONEKSI MONGODB (DINONAKTIFKAN) ---
# client = pymongo.MongoClient("mongodb+srv://user:pass@cluster.mongodb.net/smartbin_db") 
# db = client.smartbin_db
# notifs = db.notifs 

# --- MOCK DATA/MOCK DB UNTUK PENGUJIAN ---
class MockNotifsCollection:
    def __init__(self):
        self.data = [
            {"category": "kapasitas", "message": "Tempat sampah hampir penuh (80%)", "detail": "Tempat sampah di ruang dapur hampir penuh. Segera lakukan pengosongan sebelum meluap.", "timestamp": datetime(2025, 10, 5, 10, 45)},
            {"category": "kapasitas", "message": "Tempat sampah penuh (100%)", "detail": "Tempat sampah sudah penuh. Mohon kosongkan sekarang.", "timestamp": datetime(2025, 10, 5, 18, 22)},
            {"category": "lingkungan", "message": "Suhu meningkat di atas ambang batas (35°C)", "detail": "Suhu di dalam tempat sampah terlalu tinggi. Kemungkinan sampah organik mulai membusuk.", "timestamp": datetime(2025, 10, 4, 13, 15)},
            {"category": "lingkungan", "message": "Kelembapan terlalu tinggi (85%)", "detail": "Kelembapan di dalam tempat sampah meningkat. Periksa kondisi tutup atau kantong sampah.", "timestamp": datetime(2025, 10, 3, 9, 20)}
        ]
    
    def find(self, query=None):
        if query is None:
            return self.data
        category = query.get("category")
        if category:
            return [n for n in self.data if n['category'] == category]
        return self.data

    def sort(self, key, direction):
        return sorted(self.data, key=lambda x: x[key], reverse=(direction == -1))

    def delete_many(self, query):
        self.data = []
        
# Inisialisasi mock data dan session state
notifs = MockNotifsCollection()
if 'page' not in st.session_state:
    st.session_state.page = "NotificationPage"
# --- AKHIR MOCK DATA ---

# Fungsi navigasi sederhana
def navigate_to(page_name):
    st.session_state.page = page_name
    st.experimental_rerun()

def clear_notifications():
    notifs.delete_many({}) 
    st.toast("Semua notifikasi dibersihkan!")
    st.experimental_rerun()

def show():
    # --- STYLING (CSS) ---
    st.markdown(
        """
        <style>
        /* 1. Latar Belakang: Ungu Muda Solid (#C3B0E1) */
        .stApp {
            background-color: #C3B0E1; 
            background: #C3B0E1; 
            color: black;
            padding-top: 1rem;
        }
        
        /* 2. Styling Tombol Home dan Clear */
        .stButton button {
            background-color: black; 
            color: white;
            border-radius: 10px; 
            padding: 8px 15px; 
            width: auto; 
            height: auto; 
            white-space: nowrap; 
            line-height: 1.1; 
            font-size: 16px;
        }

        /* 3. CSS untuk Header dan Keselarasan Vertikal */
        .header-text {
            font-weight: bold; 
            font-size: 1.2em;
            /* PENTING: Menghilangkan margin vertikal bawaan pada teks */
            margin: 0; 
            padding: 0;
            line-height: 1.8; /* Menyesuaikan agar teks berada di tengah tinggi baris */
        }
        
        /* Mengatur alignment tombol di kolom kanan */
        div[data-testid="stVerticalBlock"] > div:first-child > div:nth-child(2) {
             padding-top: 0; /* Hapus padding-top yang mengganggu */
             display: flex;
             justify-content: flex-end; 
             align-items: center; /* PENTING: Menyelaraskan konten kolom secara vertikal */
        }
        
        /* Memberi jarak antar tombol di kolom kanan */
        div[data-testid^="stHorizontalBlock"] > div > div:nth-child(2) {
             padding-left: 10px; 
        }
        
        /* 4. Dropdown Filter */
        div[data-testid="stSelectbox"] > div:first-child {
            background-color: white;
            border-radius: 30px; 
            border: none !important;
            padding: 5px 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15); 
            margin-top: 15px;
            margin-bottom: 25px;
        }
        
        /* Styling Judul Kategori */
        .category-title {
            text-align: left;
            background-color: #fce4ec; 
            color: black;
            padding: 10px;
            border-radius: 10px;
            font-weight: bold;
            font-style: italic;
            margin-top: 25px; 
            margin-bottom: 15px;
            display: inline-block; 
            white-space: nowrap;
        }

        .notif-item {
            margin-bottom: 20px;
            padding-left: 10px; 
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- HEADER DAN NAVIGASI (SmartBin Kiri, Tombol Kanan) ---
    header_col1, header_col2 = st.columns([1, 0.3]) 
    
    with header_col1:
        # Teks SmartBin
        st.markdown('<div class="header-text">SmartBin</div>', unsafe_allow_html=True) 

    with header_col2:
        # Menggunakan kolom di dalam kolom (nested columns) untuk menempatkan tombol bersebelahan di kanan
        col_clear, col_home = st.columns([1, 1]) 
        
        with col_clear:
            if st.button("Clear", key="clear_notifs"): 
                clear_notifications()
        
        with col_home:
            if st.button("Home", key="home_button"): 
                navigate_to("Homepage")

    # Judul Halaman
    st.markdown("<h1 style='display: block; font-size: 2.5em; margin-top: 30px; margin-bottom: 20px;'>Notifikasi Page</h1>", unsafe_allow_html=True)
    
    # --- DROPDOWN UNTUK KATEGORI ---
    dropdown_col_left, dropdown_col_center, dropdown_col_right = st.columns([0.5, 4, 0.5])
    
    with dropdown_col_center:
        selected_category = st.selectbox("Filter Notifikasi", ["Semua", "Kapasitas Sampah", "Suhu & Kelembapan"], index=0, label_visibility="collapsed")


    # --- FUNGSI TAMPIL NOTIFIKASI PER KATEGORI ---
    def display_notifications(category_filter_name, category_filter_key, icon):
        
        query = {}
        if selected_category == category_filter_name:
            query = {"category": category_filter_key}
        elif selected_category == "Semua":
            if category_filter_key != "kapasitas":
                return
            query = {} 
        else:
            return

        notifs_to_display = notifs.sort("timestamp", -1) 
        if query and 'category' in query:
             notifs_to_display = [n for n in notifs_to_display if n['category'] == query['category']]
        
        
        icon_title = icon
        title_text = f"Kategori: {category_filter_name}"
        if selected_category == "Semua":
            title_text = "Semua Notifikasi"
            icon_title = "🔔"
        
        
        # --- TAMPILAN KATEGORI ---
        
        if selected_category == category_filter_name or (selected_category == "Semua" and category_filter_key == "kapasitas"):
            
            content_col_left, content_col_center, content_col_right = st.columns([0.5, 4, 0.5])
            
            with content_col_center:
                st.markdown(f"<span class='category-title'>{icon_title} {title_text}</span>", unsafe_allow_html=True)
                
                if notifs_to_display:
                    for i, n in enumerate(notifs_to_display):
                        time_str = n.get('timestamp').strftime('%d %b %Y, %H:%M WIB')
                            
                        cat_info = f"[{'Kapasitas Sampah' if n['category'] == 'kapasitas' else 'Suhu & Kelembapan'}] " if selected_category == "Semua" else ""

                        st.markdown(
                            f"""
                            <div class='notif-item'>
                                <p><strong>{i+1}. {cat_info}{n.get('message', 'Pesan tidak ada')}</strong></p>
                                <p>➤ Waktu: {time_str}</p>
                                <p>➤ Pesan: "{n.get('detail', 'Detail pesan tidak tersedia.')}"</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown("<div class='notif-item'><p>Tidak ada notifikasi untuk kategori ini.</p></div>")


    
    # --- PANGGILAN TAMPILAN KATEGORI ---
    
    display_notifications("Kapasitas Sampah", "kapasitas", "🔔")

    if selected_category != "Semua": 
        display_notifications("Suhu & Kelembapan", "lingkungan", "🌡️")


    # Footer
    st.markdown(
        """
        <div style='text-align: left; margin-top: 60px; font-style: italic; color: black;'>
        3 D4 Teknik Komputer A
        <br>
        @SmartBin
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    show()