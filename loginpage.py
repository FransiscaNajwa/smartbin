import streamlit as st

st.set_page_config(page_title="SmartBin Login", layout="wide")

st.markdown("""
<style>
/* 🔧 Reset total layout Streamlit */
html, body, [class*="stAppViewContainer"], [class*="block-container"], [class*="main"] {
    padding: 0 !important;
    margin: 0 !important;
    height: 100% !important;
    width: 100% !important;
    overflow: hidden !important;
}

section[data-testid="stSidebar"], header, footer {
    display: none !important;
}

/* 🌈 Fullscreen container */
.fullscreen-container {
    display: flex;
    flex-direction: row;
    height: 100vh !important;
    width: 100vw !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none;
}

/* 🎨 Left side (Login area) */
.left {
    flex: 1;
    background: linear-gradient(180deg, #b9a8dc, #c3b4eb);
    display: flex;
    justify-content: center;
    align-items: center;
}

.login-box {
    width: 80%;
    max-width: 360px;
    background: rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(8px);
    border-radius: 20px;
    padding: 30px 25px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}

.login-box h1 {
    font-size: 2em;
    font-weight: bold;
    color: #1c1c1c;
    margin-bottom: 25px;
}

input[type="text"], input[type="email"], input[type="password"] {
    width: 100%;
    padding: 12px;
    margin-bottom: 15px;
    border: none;
    border-radius: 8px;
    background-color: #f3f3f3;
    font-style: italic;
    font-size: 0.95em;
}

.login-btn {
    width: 100%;
    background-color: #7c6cd6;
    color: white;
    border: none;
    padding: 14px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
    font-size: 1em;
    box-shadow: 0 3px 8px rgba(0,0,0,0.3);
    transition: 0.2s;
}

.login-btn:hover {
    background-color: #6b5cc0;
}

/* 💫 Right side (Welcome text) */
.right {
    flex: 1;
    background: linear-gradient(180deg, #aab1f0, #9ea7f5);
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    color: #222;
    text-align: center;
    padding: 0;
    margin: 0;
}

.right h1 {
    font-size: 3em;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.25);
    margin-bottom: 10px;
}

.right p {
    font-size: 1.4em;
    margin: 0;
    font-family: 'Georgia', serif;
}
</style>
""", unsafe_allow_html=True)

# 🧱 HTML structure
st.markdown("""
<div class="fullscreen-container">
    <div class="left">
        <div class="login-box">
            <h1>Login</h1>
            <input type="text" placeholder="Username">
            <input type="email" placeholder="Email">
            <input type="password" placeholder="Password">
            <button class="login-btn">Login</button>
        </div>
    </div>
    <div class="right">
        <h1>Welcome to SmartBin</h1>
        <p>Track, Monitor,<br>Stay Clean</p>
    </div>
</div>
""", unsafe_allow_html=True)
