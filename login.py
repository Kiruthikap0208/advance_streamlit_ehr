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


def validate_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

# ----------- SESSION STATE SETUP -----------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

# ----------- PAGE SETUP -----------
st.set_page_config(page_title="SRM Electronic Health Records", layout="wide")

# Hide sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Load background image
with open(r"C:\Users\Kiruthika\Documents\advance_streamlit_ehr\copy-space-heart-shape-stethoscope.jpg", "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

# ----------- STYLING -----------
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

# ----------- LOGIN FORM OR DASHBOARD -----------
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1, 2.2])
    with col3:
        with st.container():
            st.title("SRM Electronic Health Records")
            st.subheader("Welcome to SRM EHR Portal")

            email = st.text_input("Email address")
            password = st.text_input("Password", type="password")
            login_btn = st.button("Log in")

            if login_btn:
                user = validate_user(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

            st.markdown('<div style="text-align: center; margin-top: 1rem;">', unsafe_allow_html=True)

            col_forgot, col_signup = st.columns([1, 1])
            with col_forgot:
                if st.button("Forgot password?"):
                    st.switch_page("pages/2_Forgot_Password.py")
            with col_signup:
                if st.button("Don't have an account? Sign up"):
                    st.switch_page("pages/1_Signup.py")

            st.markdown('</div>', unsafe_allow_html=True)


else:
    st.markdown("---")
    st.subheader(f"Welcome, {st.session_state.user_email} 👋")
    st.info("You're now inside the SRM EHR system!")

    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()
