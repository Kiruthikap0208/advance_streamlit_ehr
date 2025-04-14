import streamlit as st
import base64
import mysql.connector

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
with open("images/health-02.jpg", "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

page_styles = f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{b64_img}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

.login-box {{
    background-color: rgba(255, 255, 255, 0.95);
    padding: 3rem 2.5rem;
    border-radius: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}}

h1 {{
    text-align: center;
    color: #222;
}}

.stTextInput > div > input {{
    background-color: #f0f2f6;
    padding: 0.75rem;
    border-radius: 10px;
}}

.stButton button {{
    width: 100%;
    border-radius: 10px;
    background-color: #4A90E2;
    color: white;
    font-weight: bold;
    margin-top: 1rem;
}}

a {{
    color: #4A90E2;
    text-decoration: none;
    font-size: 0.9rem;
}}
</style>
"""
st.markdown(page_styles, unsafe_allow_html=True)
# ----------- MAIN CONTENT -----------
st.markdown("## 🩺 SRM Electronic Health Records")
st.markdown("### Choose your login portal")

st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.page_link("pages/login_doctor.py", label="👨‍⚕️ Doctor Portal", icon="🧑‍⚕️")
st.page_link("pages/login_admin.py", label="🧑‍💼 Admin / Receptionist Portal", icon="📋")
st.page_link("pages/login_patient.py", label="🧑‍🦽 Patient Portal", icon="🩺")
st.markdown("</div>", unsafe_allow_html=True)