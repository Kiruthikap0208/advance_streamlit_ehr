import streamlit as st
import mysql.connector
import base64
from streamlit_extras.switch_page_button import switch_page

# ---------- DB CONNECTION ----------
def create_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )


def update_password(email, new_password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, email))
    conn.commit()
    conn.close()

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="Reset Password | SRM EHR", layout="wide")

# ---------- HIDE SIDEBAR ----------
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------- BACKGROUND IMAGE ----------
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
    .reset-box {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 3rem 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        text-align: center;
    }}
    .stTextInput > div > input {{
        background-color: #f0f2f6;
        padding: 0.75rem;
        border-radius: 10px;
    }}
    .stButton > button {{
        width: 100%;
        border-radius: 10px;
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
        margin-top: 1rem;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE DEFAULTS ----------
if "verified_email" not in st.session_state:
    st.session_state.verified_email = ""

if "password_updated" not in st.session_state:
    st.session_state.password_updated = False

# ---------- MAIN UI ----------
col1, col2, col3 = st.columns([1, 1, 2.2])
with col3:
    st.title("🔑 Reset Your Password")

    if not st.session_state.verified_email and not st.session_state.password_updated:
        st.error("Invalid access. No email provided.")
        st.stop()

    # Password Reset Form
    if not st.session_state.password_updated:
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        if st.button("Update Password"):
            if not new_password or not confirm_password:
                st.warning("Please fill in both fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                update_password(st.session_state.verified_email, new_password)
                st.session_state.password_updated = True
                st.success("✅ Password updated successfully!")

    # Success Message + Login Button
    if st.session_state.password_updated:
        st.markdown("### 🔁 You may now return to the login portal.")
        if st.button("🔐 Back to Login"):
            # Clear session and redirect
            st.session_state.password_updated = False
            st.session_state.verified_email = ""
            switch_page("main")

    st.markdown('</div>', unsafe_allow_html=True)

