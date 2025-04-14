import streamlit as st
import base64
import mysql.connector

# ----------- DB CONNECTION -----------
def create_connection():
    conn = mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=st.secrets["mysql"]["port"],
        auth_plugin='mysql_native_password'
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

st.markdown("""
    <style>
        /* Apply dark theme to all Streamlit buttons */
        .stButton > button {
            background-color: #2C3E50 !important;  /* Dark slate blue */
            color: #122333 !important;             /* Light text */
            font-weight: bold !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.6rem 1.2rem !important;
            font-size: 1rem !important;
            transition: background-color 0.3s ease;
        }

        /* Hover effect */
        .stButton > button:hover {
            background-color: #34495E !important;  /* Slightly lighter */
            color: #00ADB5 !important;             /* Cyan accent */
        }
    </style>
""", unsafe_allow_html=True)

# ----------- GLOBAL STYLING -----------
st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{b64_img}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Headings color */
        .stMarkdown h2, .stMarkdown h3 {{
            color: white;
            text-shadow: 1px 1px 2px #00000088;
        }}
    </style>
""", unsafe_allow_html=True)

# ----------- MAIN CONTENT -----------
st.markdown("## 🩺 SRM Electronic Health Records")
st.markdown("### Choose your login portal")

st.page_link("pages/login_doctor.py", label="👨‍⚕️ Doctor Portal", icon="🧑‍⚕️")
st.page_link("pages/login_admin.py", label="🧑‍💼 Admin / Receptionist Portal", icon="📋")
st.page_link("pages/login_patient.py", label="🧑‍🦽 Patient Portal", icon="🩺")
