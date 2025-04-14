import streamlit as st
import mysql.connector
import random
import smtplib
from email.mime.text import MIMEText
import base64
from streamlit_extras.switch_page_button import switch_page

# ---------------- DB CONNECTION ----------------
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
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def send_otp(receiver_email, otp):
    sender_email = st.secrets["email"]["address"]
    app_password = st.secrets["email"]["app_password"]

    message = MIMEText(f"Your OTP for SRM EHR password reset is: {otp}")
    message['Subject'] = "SRM EHR OTP Verification"
    message['From'] = sender_email
    message['To'] = receiver_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send OTP: {e}")
        return False

# ---------------- SESSION ----------------
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'generated_otp' not in st.session_state:
    st.session_state.generated_otp = None
if 'verified_email' not in st.session_state:
    st.session_state.verified_email = ""

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Forgot Password | SRM EHR", layout="wide")

# Hide sidebar and header/footer
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        header, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# Background
with open("copy-space-heart-shape-stethoscope.jpg", "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{b64_img}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
.form-box {{
    background-color: rgba(255, 255, 255, 0.95);
    padding: 3rem 2rem;
    border-radius: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    text-align: center;
}}
h2, h3 {{
    text-align: center;
    color: #222;
}}
.stTextInput > div > input {{
    background-color: #f0f2f6;
    padding: 0.75rem;
    border-radius: 10px;
}}
.stButton button {{
    width: 25%;
    border-radius: 10px;
    background-color: #4A90E2;
    color: white;
    font-weight: bold;
    margin-top: 1rem;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------
col1, col2, col3 = st.columns([1, 1, 2.2])
with col3:
    
    st.title("🔐 Forgot Password")
    st.subheader("We'll send you an OTP to reset your password.")

    email = st.text_input("Enter your registered email")

    if st.button("Send OTP"):
        if not email:
            st.warning("Please enter your email.")
        elif not user_exists(email):
            st.error("This email is not registered.")
        else:
            otp = str(random.randint(100000, 999999))
            if send_otp(email, otp):
                st.session_state.generated_otp = otp
                st.session_state.verified_email = email
                st.session_state.otp_sent = True
                st.success("OTP has been sent to your email.")

    if st.session_state.otp_sent:
        entered_otp = st.text_input("Enter the OTP you received")
        if st.button("Verify OTP"):
            if entered_otp == st.session_state.generated_otp:
                st.success("OTP Verified. Redirecting to reset password...")
                st.page_link("pages/Reset_password.py", label="Reset Password")
            else:
                st.error("Incorrect OTP. Please try again.")

    st.markdown('</div>', unsafe_allow_html=True)
