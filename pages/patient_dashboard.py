import streamlit as st
import mysql.connector
from datetime import datetime, timedelta, date
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import os
import base64
import calendar
import streamlit_calendar as st_cal


def create_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=st.secrets["mysql"]["port"],
        auth_plugin='mysql_native_password'
    )


st.set_page_config(page_title="Patient Dashboard", layout="wide")

st.markdown("""
    <style>
    div[data-testid="stSidebarNav"] > ul { display: none; }
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    section[data-testid="stSidebar"] * { color: #ffffff !important; }
    #MainMenu, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

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
            "Prescriptions",
            "Book Appointment",
            "Profile & Settings"
        ],
        icons=[
            "clipboard-heart",
            "calendar",
            "file-earmark-medical",
            "capsule",
            "calendar-plus",
            "person-circle"
        ],
        menu_icon="person",
        default_index=0
    )
    st.markdown("---")
    if st.button("🔙 Back to Main Page"):
        switch_page("main")

st.title("👤 Patient Dashboard")

user_id = st.session_state.get("user_id")
conn = create_connection()
cursor = conn.cursor()

st.subheader("🔔 Your Appointments in Next 24 Hours")
cursor.execute("""
    SELECT a.appointment_time, d.name AS doctor_name
    FROM appointments a
    JOIN users d ON a.doctor_id = d.id
    WHERE a.patient_id = %s AND a.appointment_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 1 DAY)
    ORDER BY a.appointment_time
""", (user_id,))

reminders = cursor.fetchall()

if reminders:
    for appt_time, dname in reminders:
        st.info(f"🕒 {appt_time} — with Dr. {dname}")
else:
    st.success("No upcoming appointments.")

if selected == "My Health Records":
    st.subheader("📋 Personal Health Info")
    cursor.execute("""
        SELECT u.name, u.email, u.dob, p.symptoms, p.diagnosis
        FROM users u
        LEFT JOIN patients p ON u.id = p.id
        WHERE u.id = %s
    """, (user_id,))
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

elif selected == "Book Appointment":
    st.subheader("📅 Book a New Appointment")

    # Connect DB
    conn = create_connection()
    cursor = conn.cursor()

    # Select department first
    cursor.execute("SELECT DISTINCT department FROM approved_doctors")
    departments = [row[0] for row in cursor.fetchall()]

    if not departments:
        st.warning("No departments found.")
    else:
        selected_dept = st.selectbox("Choose Department", departments)

        # Fetch doctors in this department by joining on email
        cursor.execute("""
            SELECT u.name, u.email
            FROM users u
            JOIN approved_doctors ad ON u.email = ad.email
            WHERE ad.department = %s AND u.role = 'doctor'
        """, (selected_dept,))
        doctors = cursor.fetchall()

        if not doctors:
            st.warning("No doctors available in this department.")
        else:
            doc_names = [doc[0] for doc in doctors]
            selected_doc = st.selectbox("Choose Doctor", doc_names)

            appointment_date = st.date_input("Appointment Date")
            appointment_time = st.time_input("Appointment Time")

            reason = st.text_area("Reason for Appointment")

            if st.button("Book Appointment"):
                # Get patient ID from session
                patient_id = st.session_state.get("user_id")  # This will be like 'p_1'

                # Get selected doctor's email
                selected_doc_email = [doc[1] for doc in doctors if doc[0] == selected_doc][0]

                # Get doctor ID from users using email
                cursor.execute("SELECT id FROM users WHERE email = %s AND role = 'doctor'", (selected_doc_email,))
                doc_result = cursor.fetchone()

                if doc_result:
                    doctor_id = doc_result[0]
                    appointment_time = datetime.combine(appointment_date, appointment_time)
                    notes = st.text_area("Reason for Visit")
                    # Insert appointment
                    cursor.execute("""
                        INSERT INTO appointments (patient_id, doctor_id, appointment_time, reason)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (patient_id, doctor_id, appointment_date, appointment_time, notes))
                    conn.commit()
                    st.success("Appointment booked successfully!")
                else:
                    st.error("Selected doctor not found.")


elif selected == "Reports":
    st.subheader("📂 My Medical Reports")
    os.makedirs("reports", exist_ok=True)
    cursor.execute("SELECT file_path, uploaded_by, uploaded_at FROM reports WHERE patient_id = %s", (user_id,))
    reports = cursor.fetchall()
    for path, uploader, uploaded_at in reports:
        with st.expander(f"Uploaded on {uploaded_at} by {uploader}"):
            try:
                with open(path, "rb") as f:
                    file_bytes = f.read()
                st.download_button("Download", data=file_bytes, file_name=os.path.basename(path))
            except:
                st.error("File not found")

elif selected == "Prescriptions":
    st.subheader("💊 My Prescriptions")
    cursor.execute("SELECT medicine, dosage, instructions, date_issued FROM prescriptions WHERE patient_id = %s", (user_id,))
    prescriptions = cursor.fetchall()
    for med, dose, instr, date_issued in prescriptions:
        with st.expander(f"{med} - {date_issued}"):
            st.write(f"**Dosage:** {dose}")
            st.write(f"**Instructions:** {instr}")

elif selected == "Appointments":
    st.subheader("📋 My Appointments")

    cursor.execute("""
        SELECT a.id, a.appointment_time, a.notes,
               d.name AS doctor_name, ad.department
        FROM appointments a
        JOIN users d ON a.doctor_id = d.id
        JOIN approved_doctors ad ON d.id = ad.id
        WHERE a.patient_id = %s
        ORDER BY a.appointment_time DESC
    """, (user_id,))
    rows = cursor.fetchall()

    if not rows:
        st.info("You have no appointments yet.")
    else:
        for appt_id, appt_time, notes, doctor_name, department in rows:
            is_future = appt_time > datetime.now()
            color = "green" if is_future else "gray"

            with st.container():
                st.markdown(f"""
                    <div style='border-left: 5px solid {color}; padding-left: 10px; margin-bottom: 15px;'>
                        <strong>Doctor:</strong> {doctor_name} ({department})<br>
                        <strong>Date & Time:</strong> {appt_time.strftime("%Y-%m-%d %H:%M")}<br>
                        <strong>Notes:</strong> {notes or '—'}
                    </div>
                """, unsafe_allow_html=True)


elif selected == "Profile & Settings":
    st.subheader("⚙️ Profile Settings")
    cursor.execute("SELECT name, email, dob FROM users WHERE id = %s", (user_id,))
    profile = cursor.fetchone()
    if profile:
        name, email, dob = profile
        new_name = st.text_input("Full Name", value=name)
        new_email = st.text_input("Email", value=email)
        new_dob = st.date_input("Date of Birth", value=dob)
        if st.button("Update Profile"):
            cursor.execute("UPDATE users SET name = %s, email = %s, dob = %s WHERE id = %s",
                           (new_name, new_email, new_dob, user_id))
            conn.commit()
            st.success("Profile updated successfully!")
    else:
        st.error("Profile not found.")

conn.close()
