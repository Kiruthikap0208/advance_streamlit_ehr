# pages/3_reset_password.py

import streamlit as st
import mysql.connector

# --- DB CONNECTION ---
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nk258627",
        database="srm_ehr"
    )

def update_password(email, new_password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, email))
    conn.commit()
    conn.close()

# --- UI SETUP ---
st.set_page_config(page_title="Reset Password | SRM EHR", layout="wide")

st.title("🔑 Reset Your Password")

email = st.query_params.get("email")

if not email:
    st.error("Invalid access. No email provided.")
else:
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Reset Password"):
        if new_password != confirm_password:
            st.error("Passwords do not match.")
        elif not new_password:
            st.warning("Password cannot be empty.")
        else:
            update_password(email, new_password)
            st.success("Password updated successfully! Go back to login.")
            st.page_link("login.py", label="Back to Login", icon="🔐")