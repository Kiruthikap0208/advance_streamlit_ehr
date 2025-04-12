import streamlit as st
import mysql.connector
import base64
from streamlit_extras.switch_page_button import switch_page
from datetime import date

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nk258627",
        database="srm_ehr",
        auth_plugin="mysql_native_password"
    )

def user_exists(email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def is_approved_admin(name, dob):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM approved_admins WHERE name = %s AND dob = %s", (name, dob))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def register_admin(name, email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, 'admin')",
                   (name, email, password))
    conn.commit()
    conn.close()

st.set_page_config(page_title="signup admin", layout="wide")

# Hide sidebar and header/footer
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        header, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

with open("copy-space-heart-shape-stethoscope.jpg", "rb") as img_file:
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
    st.title("Admin Signup")

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
        elif not is_approved_admin(name, dob):
            st.error("\u274c You’re not approved by the hospital. Please contact higher authority.")
        else:
            register_admin(name, email, password)
            st.success("\u2705 Account created successfully!")
            switch_page("login admin")

    if st.button("Already have an account? Log in"):
        switch_page("login admin")

    st.markdown("</div>", unsafe_allow_html=True)
