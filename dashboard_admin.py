import streamlit as st
import mysql.connector
from streamlit_option_menu import option_menu
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

st.set_page_config(page_title="Admin Dashboard", layout="wide")

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Admin Panel",
        options=["Dashboard", "Patients", "Doctors", "Appointments"],
        icons=["speedometer", "people", "stethoscope", "calendar"],
        menu_icon="hospital",
        default_index=0
    )

st.title("\ud83c\udfe5 Admin Dashboard")

# Page content based on selection
if selected == "Dashboard":
    st.subheader("\ud83d\udcca Overview")
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='patient'")
    patient_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='doctor'")
    doctor_count = cursor.fetchone()[0]
    conn.close()

    col1, col2 = st.columns(2)
    col1.metric("Total Patients", patient_count)
    col2.metric("Total Doctors", doctor_count)

elif selected == "Patients":
    st.subheader("\ud83e\uddb1 Manage Patients")
    # Coming next: Add/Edit/Delete patient records

elif selected == "Doctors":
    st.subheader("\ud83e\uddec View Doctors")
    # Coming next: Doctor listing and filtering

elif selected == "Appointments":
    st.subheader("\ud83d\uddd3\ufe0f Appointment Logs")
    # Coming next: View appointment data
