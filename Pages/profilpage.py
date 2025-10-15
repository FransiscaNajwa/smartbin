import streamlit as st

# Judul dan navigasi
st.write("SmartBin")
st.button("Home")

# Selamat datang dan informasi profil
st.markdown("<h1 style='text-align: center;'>Welcome to Profile Page</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])
with col1:
    st.image("https://via.placeholder.com/100", width=100)  # Placeholder untuk ikon profil
with col2:
    st.write("Francisca Najwa")
    st.write("franciscaa209@gmail.com")
    st.write("@smartbin")

# Formulir edit profil
with st.container():
    st.markdown("<h3 style='text-align: center;'>Profile Edit</h3>", unsafe_allow_html=True)
    with st.form(key="profile_form"):
        email = st.text_input("Email")
        name = st.text_input("Name")
        username = st.text_input("Username")
        submit_button = st.form_submit_button(label="Save")

        # Logika sederhana untuk submit
        if submit_button:
            if email and name and username:
                st.success("Profil berhasil diperbarui!")
            else:
                st.error("Harap isi semua kolom!")

# Footer
st.write("D4 Teknik Komputer A @SmartBin")

# Warna latar belakang menyerupai gambar
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