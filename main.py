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
# Apply same button style as main login page
st.markdown("""
    <style>
        /* Custom button style */
        .stButton>button {
            background-color: #0e1117;
            color: #ECF0F1;
            border: 3px solid black;
            padding: 0.6rem 1.2rem;
            border-radius: 10px;
            font-weight: bold;
            font-size: 16px;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.4);
        }

        .stButton>button:hover {
            background-color: #20242c;
            color: #00E0FF;
            border-color: #00E0FF;
        }

        /* Optional: Hide Streamlit branding */
        header, footer { visibility: hidden; }
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