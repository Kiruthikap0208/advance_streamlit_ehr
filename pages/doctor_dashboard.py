import streamlit as st
import mysql.connector
from datetime import date,datetime, timedelta
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import os
import base64
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


st.set_page_config(page_title="Doctor Dashboard", layout="wide")
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
            "Today's Appointments",
            "Assigned Patients",
            "Diagnoses",
            "Reports",
            "Prescriptions",
            "Calendar",
            "Profile & Settings"
        ],
        icons=[
            "calendar-day",
            "people",
            "stethoscope",
            "file-earmark-medical",
            "capsule",
            "calendar",
            "person-circle"
        ],
        menu_icon="person",
        default_index=0
    )
    st.markdown("---")
    if st.button("🔙 Back to Main Page"):
        switch_page("main")

st.title("🩺 Doctor Dashboard")

user_id = st.session_state.get("user_id")
conn = create_connection()
cursor = conn.cursor()

st.subheader("🔔 Your Appointments in Next 24 Hours")
cursor.execute("""
    SELECT a.appointment_time, p.name AS patient_name
    FROM appointments a
    JOIN users p ON a.patient_id = p.id
    WHERE a.doctor_id = %s AND a.appointment_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 1 DAY)
    ORDER BY a.appointment_time
""", (user_id,))

reminders = cursor.fetchall()

if reminders:
    for appt_time, pname in reminders:
        st.info(f"🕒 {appt_time} — with {pname}")
else:
    st.success("No upcoming appointments.")

if selected == "Calendar":
    st.subheader("📅 Appointment Calendar")
    cursor.execute("""
        SELECT a.appointment_time, p.name AS patient_name
        FROM appointments a
        JOIN users p ON a.patient_id = p.id
        WHERE a.doctor_id = %s
        ORDER BY a.appointment_time DESC
    """, (user_id,))
    appointments = cursor.fetchall()

    st_cal.calendar(
        events=[
            {
                "title": f"{pname} Appointment",
                "start": appt_time.isoformat(),
                "end": (appt_time + timedelta(minutes=30)).isoformat()
            } for appt_time, pname in appointments
        ],
        options={
            "initialView": "timeGridWeek",
            "height": 600,
            "editable": False
        }
    )

if selected == "Today's Appointments":
    st.subheader("📅 Today's Appointments")
    cursor.execute("""
        SELECT a.id, p.name, a.appointment_time, a.notes
        FROM appointments a
        JOIN users p ON a.patient_id = p.id
        WHERE DATE(a.appointment_time) = CURDATE()
    """)
    results = cursor.fetchall()
    for aid, pname, appt_time, notes in results:
        with st.expander(f"{pname} at {appt_time}"):
            st.write("📝 Notes:", notes)

elif selected == "Assigned Patients":
    st.subheader("👨‍⚕️ Your Patients")
    cursor.execute("""
        SELECT DISTINCT p.id, p.name, p.dob, pt.symptoms, pt.diagnosis
        FROM users p
        JOIN appointments a ON a.patient_id = p.id
        LEFT JOIN patients pt ON p.id = pt.id
    """)
    patients = cursor.fetchall()
    for pid, name, dob, symptoms, diagnosis in patients:
        with st.expander(f"{name} (DOB: {dob})"):
            st.write(f"🆔 Patient ID: {pid}")
            st.write(f"🤒 Symptoms: {symptoms or 'N/A'}")
            st.write(f"🩺 Diagnosis: {diagnosis or 'N/A'}")

elif selected == "Diagnoses":
    st.subheader("📝 Update Diagnoses")
    cursor.execute("SELECT id, name FROM users WHERE role = 'patient'")
    patients = cursor.fetchall()
    patient_map = {f"{name} ({pid})": pid for pid, name in patients}
    selected_patient = st.selectbox("Select Patient", list(patient_map.keys()))
    symptoms = st.text_area("Symptoms")
    diagnosis = st.text_area("Diagnosis")
    doctor_id = st.text_input("Doctor ID (Your ID)")
    if st.button("Save Diagnosis"):
        pid = patient_map[selected_patient]
        cursor.execute("SELECT id FROM patients WHERE id = %s", (pid,))
        exists = cursor.fetchone()
        if exists:
            cursor.execute("UPDATE patients SET symptoms = %s, diagnosis = %s WHERE id = %s",
                           (symptoms, diagnosis, pid))
        else:
            cursor.execute("INSERT INTO patients (id, name, symptoms, diagnosis, created_by) VALUES (%s, %s, %s, %s, %s)",
                           (pid, selected_patient.split(' (')[0], symptoms, diagnosis, doctor_id))
        conn.commit()
        st.success("Diagnosis saved successfully!")

elif selected == "Reports":
    st.subheader("📂 Upload/View Reports")
    os.makedirs("reports", exist_ok=True)
    uploaded = st.file_uploader("Upload Report", type=["pdf", "jpg", "png"], key="doctor_report")
    patient_id = st.text_input("Patient ID")
    doctor_id = st.text_input("Your Doctor ID")
    if st.button("Upload Report") and uploaded and patient_id and doctor_id:
        file_path = f"reports/{uploaded.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded.getvalue())
        cursor.execute("INSERT INTO reports (patient_id, file_path, uploaded_by, uploaded_at) VALUES (%s, %s, %s, NOW())",
                       (patient_id, file_path, doctor_id))
        conn.commit()
        st.success("Report uploaded successfully!")

    st.markdown("---")
    if doctor_id:
        cursor.execute("SELECT patient_id, file_path, uploaded_at FROM reports WHERE uploaded_by = %s", (doctor_id,))
        reports = cursor.fetchall()
        for pid, path, uploaded_at in reports:
            with st.expander(f"Report for {pid} - {uploaded_at}"):
                try:
                    with open(path, "rb") as f:
                        file_bytes = f.read()
                    st.download_button("Download", data=file_bytes, file_name=os.path.basename(path))
                except:
                    st.error("File not found")

elif selected == "Prescriptions":
    st.subheader("💊 Manage Prescriptions")
    cursor.execute("SELECT id, name FROM users WHERE role = 'patient'")
    patients = cursor.fetchall()
    patient_map = {f"{name} ({pid})": pid for pid, name in patients}
    selected_patient = st.selectbox("Choose Patient", list(patient_map.keys()), key="prescription_patient")
    prescription_text = st.text_area("Enter Prescription")
    doctor_id = st.text_input("Your Doctor ID", key="prescription_doc")
    if st.button("Save Prescription"):
        file_path = f"reports/prescription_{patient_map[selected_patient]}.txt"
        with open(file_path, "w") as f:
            f.write(prescription_text)
        cursor.execute("INSERT INTO reports (patient_id, file_path, uploaded_by, uploaded_at) VALUES (%s, %s, %s, NOW())",
                       (patient_map[selected_patient], file_path, doctor_id))
        conn.commit()
        st.success("Prescription saved as report!")

elif selected == "Profile & Settings":
    st.subheader("⚙️ Profile Settings")
    doc_id = st.text_input("Enter your Doctor ID")
    if st.button("Load Profile") and doc_id:
        cursor.execute("SELECT name, email, dob FROM users WHERE id = %s AND role = 'doctor'", (doc_id,))
        result = cursor.fetchone()
        if result:
            name, email, dob = result
            new_name = st.text_input("Full Name", value=name)
            new_email = st.text_input("Email", value=email)
            new_dob = st.date_input("Date of Birth", value=dob)
            if st.button("Update Profile"):
                cursor.execute("UPDATE users SET name = %s, email = %s, dob = %s WHERE id = %s",
                               (new_name, new_email, new_dob, doc_id))
                conn.commit()
                st.success("Profile updated successfully!")
        else:
            st.error("Doctor not found or invalid ID")

conn.close()
