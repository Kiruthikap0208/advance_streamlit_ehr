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
        .login-box {{
            background-color: rgba(255, 255, 255, 0.95);
            padding: 3rem 2.5rem;
            border-radius: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        /* Style for page_link() hyperlinks */
        a[data-testid="stPageLink"] {
            display: inline-block;
            background-color: #0d3438;         /* Updated to your preferred color */
            color: #ECF0F1 !important;         /* Light text */
            font-weight: bold;
            padding: 0.7rem 1.2rem;
            border-radius: 10px;
            text-decoration: none;
            margin: 0.5rem 0;
            font-size: 1rem;
            text-align: center;
            width: 250px;
        }

        a[data-testid="stPageLink"]:hover {
            background-color: #1e5c60;         /* Slightly lighter hover effect */
            color: #00ADB5 !important;         /* Cyan hover text */
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

st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.page_link("pages/login_doctor.py", label="👨‍⚕️ Doctor Portal", icon="🧑‍⚕️")
st.page_link("pages/login_admin.py", label="🧑‍💼 Admin / Receptionist Portal", icon="📋")
st.page_link("pages/login_patient.py", label="🧑‍🦽 Patient Portal", icon="🩺")
st.markdown("</div>", unsafe_allow_html=True)