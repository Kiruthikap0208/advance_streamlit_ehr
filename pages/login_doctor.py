import streamlit as st
import mysql.connector
import base64
from streamlit_extras.switch_page_button import switch_page

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nk258627",
        database="srm_ehr",
        auth_plugin="mysql_native_password"
    )

def validate_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s AND role='doctor'", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

st.set_page_config(page_title="login doctor", layout="wide")

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

with open("copy-space-heart-shape-stethoscope.jpg", "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{b64_img}");
    background-size: cover;
    background-attachment: fixed;
}}
.login-box {{
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

    st.title("👨‍⚕️ Doctor Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        user = validate_user(email, password)
        if user:
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.user_email = email
            switch_page("doctor dashboard")
        else:
            st.error("Invalid credentials or not a doctor.")
            
    if st.button("Forgot password?"):
        switch_page("Forgot_Password")

    if st.button("Don't have an account? Sign up"):
        switch_page("signup doctor")

    st.markdown("</div>", unsafe_allow_html=True)
