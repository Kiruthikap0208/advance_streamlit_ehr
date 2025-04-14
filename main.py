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
with open("images\abstract-health-medical-science-healthcare-icon-digital-technology-science-concept-modern-innovation-treatment-medicine-on-hi-tech-future-blue-background-for-wallpaper-template-web-design-.jpg", "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

# ----------- STYLING -----------
st.markdown("""
    <style>
        /* Apply dark theme to all page links */
        a[data-testid="stPageLink"] {
            display: inline-block;
            background-color: #2C3E50;
            color: #ECF0F1 !important;
            font-weight: bold;
            padding: 0.7rem 1.2rem;
            border-radius: 10px;
            text-decoration: none;
            margin: 0.5rem 0;
            font-size: 1rem;
            text-align: center;
            width: 250px;
            border: 2px solid #1C1C1C !important;
        }

        a[data-testid="stPageLink"]:hover {
            background-color: #34495E;
            color: #00ADB5 !important;
        }

        .stApp {
            background-image: url("data:image/jpg;base64,""" + b64_img + """");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        .stMarkdown h2, .stMarkdown h3 {
            color: white;
            text-shadow: 1px 1px 2px #00000088;
        }
    </style>
""", unsafe_allow_html=True)

# ----------- MAIN CONTENT -----------
st.markdown("## 🩺 SRM Electronic Health Records")
st.markdown("### Choose your login portal")

st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.page_link("pages/login_doctor.py", label="👨‍⚕️ Doctor Portal", icon="🧑‍⚕️")
st.page_link("pages/login_admin.py", label="🧑‍💼 Admin / Receptionist Portal", icon="📋")
st.page_link("pages/login_patient.py", label="🧑‍🦽 Patient Portal", icon="🩺")
st.markdown("</div>", unsafe_allow_html=True)