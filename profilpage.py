import streamlit as st
import pymongo

# --- MOCK DATA UNTUK PENGUJIAN ---
class MockUsersCollection:
    def find_one(self, query):
        if query.get("username") == "smartbin":
            return {
                "name": "Fransisca Najwa",
                "email": "fransisccaa209@gmail.com",
                "username": "smartbin",
                "_id": "mock_id_123"
            }
        return None
    
    def update_one(self, query, update):
        pass

class MockSessionState(dict): 
    def __init__(self):
        super().__init__()
        self['username'] = "smartbin" 
    
    def page(self, page_name):
        st.info(f"Navigasi ke halaman: {page_name}") 

if 'username' not in st.session_state:
    st.session_state.username = "smartbin" 

st.session_state = MockSessionState()
users = MockUsersCollection()
# --- AKHIR MOCK DATA ---


def show():
    
    # WARNA LATAR BELAKANG DAN STYLING KUNCI 🎨
    st.markdown(
        """
        <style>
        /* 1. Warna latar belakang keseluruhan aplikasi: Ungu muda kebiruan (Lavender) */
        .stApp {
            background-color: #C3B0E1; 
            color: #000000;
            padding-top: 1rem; /* Tambahkan sedikit padding atas untuk header */
        }
        
        /* 2. Styling untuk box Profile Edit */
        div[data-testid="stForm"] > div:first-child { 
            background-color: white; 
            padding: 30px; 
            border-radius: 15px; 
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); 
            margin-top: 20px;
        }
        
        /* 3. Styling untuk input field */
        .stTextInput > div > div > input {
            background-color: #F0F0F0; 
            border-radius: 5px;
            border: none;
            padding: 10px;
        }
        
        /* 4. Styling untuk tombol Home dan Save */
        /* Tombol Home */
        .stButton button {
            background-color: black;
            color: white;
            border-radius: 5px;
            padding: 8px 15px;
        }
        
        div[data-testid="stForm"] .stButton button {
            background-color: black; 
            color: white;
            border: none;
            padding: 8px 15px;
            margin-top: 10px; 
        }
        
        /* Styling untuk judul "Welcome to Profile Page" */
        h1 {
            font-weight: bold;
            font-size: 2.5em;
        }
        
        /* Styling untuk teks SmartBin di kiri atas */
        .header-text {
            font-weight: bold; 
            font-size: 1.2em;
        }
        
        /* Menghilangkan margin vertikal default pada kolom Streamlit untuk keselarasan */
        div[data-testid="column"] {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }
        
        /* Menyesuaikan posisi vertikal tombol di header kolom kedua */
        div[data-testid="stVerticalBlock"] > div:first-child > div:nth-child(2) {
             padding-top: 0.25rem; /* Sesuaikan untuk sejajar dengan teks SmartBin */
             display: flex; /* Memastikan isinya sejajar */
             justify-content: flex-end; /* Memastikan tombol di kanan */
        }

        </style>
        """,
        unsafe_allow_html=True
    )
    
    # --- HEADER DAN NAVIGASI ---
    # FIX: Mengganti st.markdown position:absolute yang lama.
    # Menggunakan st.columns untuk menempatkan teks di kiri dan tombol di kanan, sejajar.
    header_col1, header_col2 = st.columns([1, 0.15]) 
    
    with header_col1:
        st.markdown('<div class="header-text">SmartBin</div>', unsafe_allow_html=True)

    with header_col2:
        # Menampilkan tombol Home. Padding disesuaikan di CSS di atas.
        st.button("Home", on_click=lambda: st.session_state.page("Homepage"))
    
    # Selamat datang dan informasi profil
    st.markdown("<h1 style='margin-top: 40px; margin-bottom: 50px;'>Welcome to Profile Page</h1>", unsafe_allow_html=True)
    
    user = users.find_one({"username": st.session_state['username']})
    
    if user:
        profile_col1, profile_col2, profile_col3 = st.columns([1, 4, 1])
        
        with profile_col2:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin-bottom: 50px;">
                    <div style="width: 100px; height: 100px; background-color: #CCCCCC; border-radius: 5px; margin-right: 20px; display: flex; justify-content: center; align-items: center;">
                        <div style="font-size: 40px; color: #555;">🖼️</div>
                    </div>
                    <div>
                        <p style="font-size: 1.5em; font-weight: bold; margin: 0;">{user.get('name', 'Fransisca Najwa')}</p>
                        <p style="margin: 0;">{user.get('email', 'fransisccaa209@gmail.com')}</p>
                        <p style="margin: 0; font-style: italic;">@{user.get('username', 'smartbin')}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --- FORMULIR EDIT PROFIL ---
    col_left, col_center, col_right = st.columns([1, 3, 1])

    with col_center:
        st.markdown("<h3>Profile Edit</h3>", unsafe_allow_html=True)
        
        with st.form("profile_form"):
            current_name = user.get('name', 'Fransisca Najwa') if user else ''
            current_email = user.get('email', 'fransisccaa209@gmail.com') if user else ''
            current_username = user.get('username', 'smartbin') if user else ''

            email = st.text_input("Email", value=current_email, label_visibility="collapsed", placeholder="Email")
            name = st.text_input("Name", value=current_name, label_visibility="collapsed", placeholder="Name")
            username = st.text_input("Username", value=current_username, label_visibility="collapsed", placeholder="Username")
            
            # Tombol Save
            submitted = st.form_submit_button("Save")

            if submitted:
                if not all([name, email, username]):
                    st.error("Harap isi semua kolom!")
                elif user:
                    # users.update_one({"_id": user["_id"]}, {"$set": {"name": name, "email": email, "username": username}})
                    st.success("Profil diperbarui!")

    # --- FOOTER ---
    st.markdown(
        """
        <div style='margin-top: 100px; font-style: italic; color: black;'>
        3 D4 Teknik Komputer A
        </div>
        <div style='font-style: italic; color: black;'>
        @SmartBin
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    show()