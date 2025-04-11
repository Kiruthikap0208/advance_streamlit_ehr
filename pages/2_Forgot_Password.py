import streamlit as st
import mysql.connector
import random
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------- SESSION STATE ----------
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'generated_otp' not in st.session_state:
    st.session_state.generated_otp = ''
if 'reset_email' not in st.session_state:
    st.session_state.reset_email = ''

# ---------- DB CONNECTION ----------
def create_connection():
    conn = mysql.connector.connect(
    host=st.secrets["mysql"]["host"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    database=st.secrets["mysql"]["database"]
)

# ---------- SEND OTP ----------
def send_otp_email(receiver_email, otp):
    try:
        sender_email = st.secrets["email"]["address"]
        app_password = st.secrets["email"]["app_password"]


        message = MIMEMultipart("alternative")
        message["Subject"] = "Your SRM EHR OTP Code"
        message["From"] = sender_email
        message["To"] = receiver_email

        html = f"""
        <html>
            <body>
                <p>Hi,<br>
                Your OTP for SRM EHR password reset is: <strong>{otp}</strong></p>
            </body>
        </html>
        """

        message.attach(MIMEText(html, "html"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send OTP: {e}")
        return False

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="Forgot Password | SRM EHR", layout="wide")

# Hide sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# Background Image
with open(r"C:\Users\Kiruthika\Documents\advance_streamlit_ehr\copy-space-heart-shape-stethoscope.jpg", "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

# Styling
page_styles = f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{b64_img}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

.otp-box {{
    background-color: rgba(255, 255, 255, 0.95);
    padding: 3rem 2.5rem;
    border-radius: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    margin-top: 2rem;
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
</style>
"""
st.markdown(page_styles, unsafe_allow_html=True)

# ---------- UI ----------
col1, col2, col3 = st.columns([1, 1, 2.2])
with col3:
    with st.container():
        st.title("🔐 Forgot Password")
        st.subheader("Reset via Email OTP")

        email = st.text_input("Email address")

        if st.button("Send OTP"):
            if email:
                otp = str(random.randint(100000, 999999))
                if send_otp_email(email, otp):
                    st.success("OTP sent successfully to your email!")
                    st.session_state.generated_otp = otp
                    st.session_state.otp_sent = True
                    st.session_state.reset_email = email
            else:
                st.warning("Please enter your email address.")

        if st.session_state.otp_sent:
            st.markdown("---")
            st.subheader("🔍 Verify OTP")
            user_otp = st.text_input("Enter OTP sent to your email")

            if st.button("Verify OTP"):
                if user_otp == st.session_state.generated_otp:
                    st.success("OTP verified successfully!")
                    st.query_params["email"] = email  # ✅ pass email to next page
                    st.switch_page("pages/3_reset_password.py")
                else:
                    st.error("Incorrect OTP. Please try again.")

        st.markdown('</div>', unsafe_allow_html=True)
