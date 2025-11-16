import streamlit as st
from pathlib import Path

def load_css(file_name: str):
    """
    Memuat file CSS dari folder 'app/assets' dan inject ke halaman Streamlit.

    Parameters:
        file_name (str): Nama file CSS (contoh: 'style.css').

    Fungsi ini akan mencari file CSS di folder:
        app/assets/<file_name>
    Jika tidak ditemukan, akan menampilkan info ringan di Streamlit.
    """

    # Path ke folder assets relatif terhadap file ini
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    css_path = assets_dir / file_name

    # Validasi folder
    if not assets_dir.exists():
        st.info("📁 Folder 'assets' belum ada. Lewati pemuatan CSS.")
        return

    # Validasi file
    if not css_path.is_file():
        st.info(f"ℹ️ File CSS tidak ditemukan: {css_path.name}")
        return

    # Baca dan inject CSS
    try:
        css_content = css_path.read_text(encoding="utf-8")
        st.markdown(
            f"<style>{css_content}</style>",
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"❌ Gagal memuat CSS '{file_name}': {e}")
