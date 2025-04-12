import streamlit as st
import mysql.connector
import base64
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from datetime import date

# -------- DB CONNECTION --------
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nk258627",
        database="srm_ehr",
        auth_plugin = "mysql_native_password"
    )

def get_all_patients():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, symptoms, diagnosis, created_at FROM patients ORDER BY created_at DESC")
    data = cursor.fetchall()
    conn.close()
    return data

# -------- PAGE SETUP --------
st.set_page_config(page_title="Doctor Dashboard | SRM EHR", layout="wide")

# Background
with open("copy-space-heart-shape-stethoscope.jpg", "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{b64_img}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .box {{
        background-color: rgba(255,255,255,0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
    }}
    .stButton>button {{
        background-color: #4A90E2;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        margin-top: 1rem;
    }}
    </style>
""", unsafe_allow_html=True)

# -------- WELCOME --------
col1, col2, col3 = st.columns([1, 1, 2])
with col3:
    st.title("👨‍⚕️ Doctor Dashboard")
    st.write(f"Welcome, **{st.session_state.get('user_email', 'Doctor')}**!")

# -------- STATS --------
    patients_data = get_all_patients()
    total_patients = len(patients_data)

    st.subheader("📊 Quick Stats")
    st.info(f"Total Patients: **{total_patients}**")

    # -------- BUTTONS --------
    st.subheader("➕ Manage Patients")
    if st.button("Add New Patient"):
        switch_page("add patient")  # We'll build this next

    # -------- PATIENT LIST --------
    st.subheader("👥 Patient List")
    if total_patients == 0:
        st.warning("No patients added yet.")
    else:
        df = pd.DataFrame(patients_data, columns=["ID", "Name", "Age", "Symptoms", "Diagnosis", "Added On"])
        st.dataframe(df, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
