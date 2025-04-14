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

# ----------- STYLING -----------
st.markdown("""
    <style>
        /* Apply dark theme with thick border to all page links */
        a[data-testid="stPageLink"] {
            display: inline-block;
            background-color: #0e1117; /* Default Streamlit dark theme background */
            color: #ECF0F1 !important;
            font-weight: 700;
            padding: 0.8rem 1.5rem;
            border-radius: 12px;
            text-decoration: none;
            margin: 0.75rem 0;
            font-size: 1.1rem;
            text-align: center;
            width: 270px;
            border: 4px solid #000000 !important;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);
        }

        a[data-testid="stPageLink"]:hover {
            background-color: #20242c;
            color: #00E0FF !important;
            border-color: #00E0FF !important;
        }

        .stApp {
            background-image: url("data:image/jpg;base64,""" + b64_img + """);
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
