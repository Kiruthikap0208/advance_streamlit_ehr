import streamlit as st
import mysql.connector
import base64

# --------- DB CONNECTION ----------
def create_connection():
    conn = mysql.connector.connect(
    host=st.secrets["mysql"]["host"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    database=st.secrets["mysql"]["database"]
)


def user_exists(email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def register_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
    conn.commit()
    conn.close()

# --------- PAGE SETUP ----------
st.set_page_config(page_title="Signup | SRM EHR", layout="wide")

# Hide sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Background image
with open(r"C:\Users\Kiruthika\Documents\advance_streamlit_ehr\copy-space-heart-shape-stethoscope.jpg", "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

# --------- CUSTOM CSS ----------
signup_styles = f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{b64_img}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

.signup-box {{
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
st.markdown(signup_styles, unsafe_allow_html=True)

# --------- SIGNUP FORM ----------
col1, col2, col3 = st.columns([1, 1, 2.2])
with col3:

    st.title("SRM Electronic Health Records")
    st.subheader("Create a new account")

    name = st.text_input("Full Name")
    email = st.text_input("Email address")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    

    if st.button("Sign up"):
        if not email or not password or not confirm_password:
            st.warning("Please fill in all fields.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        elif user_exists(email):
            st.error("An account with this email already exists.")
        else:
            register_user(email, password)
            st.success("Account created successfully! Redirecting to login...")
            st.switch_page("login.py")

    st.markdown('<div style="text-align: center; margin-top: 1rem;">', unsafe_allow_html=True)
    if st.button("Already have an account? Login here"):
        st.switch_page("login.py")
    st.markdown('</div>', unsafe_allow_html=True)
