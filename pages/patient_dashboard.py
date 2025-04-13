import streamlit as st
import mysql.connector
from datetime import date
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import os
import base64

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nk258627",
        database="srm_ehr",
        auth_plugin="mysql_native_password"
    )

st.set_page_config(page_title="Patient Dashboard", layout="wide")

st.markdown("""
    <style>
    /* 1. Hide the default Streamlit multipage dropdown in the sidebar */
    div[data-testid="stSidebarNav"] > ul {
        display: none;
    }

    /* 2. Make the sidebar background transparent and glassy */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 3. Optional: Change sidebar text/icon color to white for better contrast */
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* 4. Hide Streamlit footer and main menu */
    #MainMenu, footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Set background image
with open("images/dashboard_bh_img.jpg", "rb") as img_file:
    bg_image = base64.b64encode(img_file.read()).decode()

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=[
            "My Health Records",
            "Appointments",
            "Reports",
            "Profile & Settings"
        ],
        icons=["clipboard-heart", "calendar", "file-earmark-medical", "person-circle"],
        menu_icon="person",
        default_index=0
    )
    st.markdown("---")
    if st.button("🔙 Back to Main Page"):
        switch_page("main")

st.title("👤 Patient Dashboard")

conn = create_connection()
cursor = conn.cursor()

# Replace with session-based ID or manual input for now
patient_id = st.text_input("Enter Your Patient ID")

if patient_id:
    if selected == "My Health Records":
        st.subheader("📋 Personal Health Info")
        cursor.execute("""
            SELECT u.name, u.email, u.dob, p.symptoms, p.diagnosis
            FROM users u
            LEFT JOIN patients p ON u.id = p.id
            WHERE u.id = %s
        """, (patient_id,))
        info = cursor.fetchone()
        if info:
            name, email, dob, symptoms, diagnosis = info
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**DOB:** {dob}")
            st.write(f"**Symptoms:** {symptoms or 'N/A'}")
            st.write(f"**Diagnosis:** {diagnosis or 'N/A'}")
        else:
            st.error("Patient record not found.")

    elif selected == "Appointments":
        st.subheader("📅 My Appointments")
        cursor.execute("""
            SELECT a.appointment_time, a.notes, u.name AS doctor_name
            FROM appointments a
            JOIN users u ON a.doctor_id = u.id
            WHERE a.patient_id = %s
            ORDER BY a.appointment_time DESC
        """, (patient_id,))
        appointments = cursor.fetchall()
        for appt_time, notes, doctor_name in appointments:
            with st.expander(f"With Dr. {doctor_name} at {appt_time}"):
                st.write("📝 Notes:", notes)

    elif selected == "Reports":
        st.subheader("📂 My Medical Reports")
        os.makedirs("reports", exist_ok=True)
        cursor.execute("SELECT file_path, uploaded_by, uploaded_at FROM reports WHERE patient_id = %s", (patient_id,))
        reports = cursor.fetchall()
        for path, uploader, uploaded_at in reports:
            with st.expander(f"Uploaded on {uploaded_at} by {uploader}"):
                try:
                    with open(path, "rb") as f:
                        file_bytes = f.read()
                    st.download_button("Download", data=file_bytes, file_name=os.path.basename(path))
                except:
                    st.error("File not found")

    elif selected == "Profile & Settings":
        st.subheader("⚙️ Profile Settings")
        cursor.execute("SELECT name, email, dob FROM users WHERE id = %s", (patient_id,))
        profile = cursor.fetchone()
        if profile:
            name, email, dob = profile
            new_name = st.text_input("Full Name", value=name)
            new_email = st.text_input("Email", value=email)
            new_dob = st.date_input("Date of Birth", value=dob)
            if st.button("Update Profile"):
                cursor.execute("UPDATE users SET name = %s, email = %s, dob = %s WHERE id = %s",
                               (new_name, new_email, new_dob, patient_id))
                conn.commit()
                st.success("Profile updated successfully!")
        else:
            st.error("Profile not found.")

conn.close()
