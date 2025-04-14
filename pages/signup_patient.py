import streamlit as st
import mysql.connector
import base64
from streamlit_extras.switch_page_button import switch_page
from datetime import date

def create_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=st.secrets["mysql"]["port"],
        auth_plugin='mysql_native_password'
    )


def user_exists(email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None and result[0] is not None


def is_approved_patient(name, dob):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM approved_patients WHERE name = %s AND dob = %s", (name, dob))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def register_patient(name, email, password, dob):
    conn = create_connection()
    cursor = conn.cursor()

    # Set password for already-approved user
    cursor.execute("SELECT id FROM users WHERE name = %s AND dob = %s AND role = 'patient'", (name, dob))
    result = cursor.fetchone()

    if result:
        patient_id = result[0]
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (password, patient_id))
        conn.commit()
    else:
        st.error("Patient not found or not approved.")

    conn.close()


st.set_page_config(page_title="signup patient", layout="wide")

# Place this at the top of your Streamlit script
st.markdown("""
    <style>
        .custom-top-left {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 9999;
        }
        .custom-top-left button {
            background-color: rgba(255, 255, 255, 0.2) !important;
            color: black;
            font-weight: bold;
            border: 2px solid rgba(255, 255, 255, 0.5);
            padding: 8px 16px;
            border-radius: 12px;
            transition: 0.3s ease-in-out;
        }
        .custom-top-left button:hover {
            background-color: rgba(255, 255, 255, 0.4) !important;
        }
    </style>

    <div class="custom-top-left">
        <form action="/" method="get">
            <button type="submit">🔙 Back to Main</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# Hide sidebar and header/footer
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        header, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

with open("images/copy-space-heart-shape-stethoscope.jpg", "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{b64_img}");
    background-size: cover;
    background-attachment: fixed;
}}
.signup-box {{
    background-color: rgba(255, 255, 255, 0.95);
    padding: 3rem 2rem;
    border-radius: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    text-align: center;
}}
.stTextInput > div > input {{
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 0.75rem;
}}
.stButton>button {{
    width: 100%;
    font-weight: bold;
    background-color: #4A90E2;
    color: white;
    border-radius: 10px;
    margin-top: 1rem;
}}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 2.2])
with col3:
    st.title("📋 Patient Signup")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    dob = st.date_input("Date of Birth", min_value=date(1950, 1, 1), max_value=date.today())
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if not name or not email or not dob or not password or not confirm:
            st.warning("Please fill in all fields.")
        elif password != confirm:
            st.error("Passwords do not match.")
        elif user_exists(email):
            st.error("An account with this email already exists.")
        elif not is_approved_patient(name, dob):
            st.error("❌ You’re not approved by the hospital. Please contact admin.")
        else:
            register_patient(name, email, password, dob)
            st.success("✅ Account created successfully!")

    # Page navigation using st.page_link
    st.page_link("pages/login_patient.py", label="🔐 Go to Login Page", icon="➡️")
    st.page_link("pages/login_patient.py", label="Already have an account? Log in", icon="👤")

    st.markdown("</div>", unsafe_allow_html=True)