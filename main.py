import streamlit as st
import base64
import mysql.connector
from streamlit_extras.switch_page_button import switch_page

# ----------- DB CONNECTION -----------
def create_connection():
    conn = mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )
    return conn

# ----------- PAGE SETUP -----------
st.set_page_config(page_title="SRM Electronic Health Records", layout="wide")

# Hide sidebar and header/footer
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        header, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# Load background image
with open("images\health-02.jpg", "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

# ----------- STYLING -----------
page_styles = f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{b64_img}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

.container {{
    display: flex;
    justify-content: flex-end;
    align-items: center;
    height: 100vh;
    padding-right: 5vw;
}}

.login-box {{
    background-color: rgba(255, 255, 255, 0.95);
    padding: 3rem 2.5rem;
    border-radius: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    width: 400px;
}}

.login-box h2 {{
    text-align: center;
    margin-bottom: 2rem;
}}

.stButton button {{
    width: 30%;
    border-radius: 10px;
    background-color: #4A90E2;
    color: white;
    font-weight: bold;
    margin-top: 1rem;
    padding: 0.6rem;
    font-size: 1rem;
}}
</style>
"""
st.markdown(page_styles, unsafe_allow_html=True)

# ----------- MAIN CONTENT -----------

st.markdown("## 🩺 SRM Electronic Health Records")
st.markdown("### Choose your login portal")

if st.button("👨‍⚕️ Doctor Portal"):
    switch_page("login doctor")  # Page title, not file path

if st.button("🧑‍💼 Admin / Receptionist Portal"):
    switch_page("login admin")

if st.button("🧑‍🦽 Patient Portal"):
    switch_page("login patient")

st.markdown('</div></div>', unsafe_allow_html=True)
