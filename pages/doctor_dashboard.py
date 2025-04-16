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
    .stApp {
        color: white !important;
    }
    /* 2. Make the sidebar background transparent and glassy */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    button[kind="primary"], button[kind="secondary"] {
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid white !important;
    }

    /* 4. Hide Streamlit footer and main menu */
    #MainMenu, footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Set background image
img_path = os.path.join("images", "dashboard_bh_img.jpg")
with open(img_path, "rb") as img_file:
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
    st.markdown("---")
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
    st.page_link("main.py", label="🔙 Back to Main Page", icon="🏠")


st.title("🩺 Doctor Dashboard")

user_id = st.session_state.get("user_id")
conn = create_connection()
cursor = conn.cursor()



if selected == "Calendar":
    st.subheader("📅 Appointments Calendar")

    cursor.execute("""
        SELECT a.id, a.appointment_time, a.notes,
               p.id AS patient_id, p.name AS patient_name,
               d.id AS doctor_id, d.name AS doctor_name,
               ad.department
        FROM appointments a
        JOIN users p ON a.patient_id = p.id
        JOIN users d ON a.doctor_id = d.id
        JOIN approved_doctors ad ON d.id = ad.id
        WHERE a.doctor_id = %s
    """, (user_id,))
    appointments = cursor.fetchall()

    events = []
    event_lookup = {}

    for aid, appt_time, notes, pid, pname, did, dname, dept in appointments:
        title = f"👤 {pname} | 🏥 Dept: {dept}\n🕒 {appt_time.strftime('%H:%M')} | 📝 {notes or 'No notes'}"
        event = {
            "id": str(aid),
            "title": title,
            "start": appt_time.isoformat(),
            "end": (appt_time + timedelta(minutes=30)).isoformat()
        }
        events.append(event)
        event_lookup[str(aid)] = {
            "Patient ID": pid,
            "Patient Name": pname,
            "Doctor Name": dname,
            "Department": dept,
            "Appointment Time": appt_time.strftime("%Y-%m-%d %H:%M"),
            "Notes": notes or "No notes"
        }

    clicked = st_cal.calendar(
        events=events,
        options={
            "initialView": "timeGridDay",
            "editable": False,
            "eventDisplay": "block",
            "eventMaxLines": 4,
            "height": 850
        },
    )

    if clicked and "event" in clicked:
        appt_id = clicked["event"].get("id")
        if appt_id and appt_id in event_lookup:
            st.success("📌 Appointment Details")
            for key, value in event_lookup[appt_id].items():
                st.markdown(f"**{key}:** {value}")


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

    if st.button("Save Diagnosis"):
        doctor_id = user_id  # Automatically use logged-in doctor ID
        pid = patient_map[selected_patient]

        cursor.execute("SELECT id FROM patients WHERE id = %s", (pid,))
        exists = cursor.fetchone()

        if exists:
            cursor.execute(
                "UPDATE patients SET symptoms = %s, diagnosis = %s, created_by = %s WHERE id = %s",
                (symptoms, diagnosis, doctor_id, pid)
            )
        else:
            cursor.execute(
                "INSERT INTO patients (id, name, symptoms, diagnosis, created_by) VALUES (%s, %s, %s, %s, %s)",
                (pid, selected_patient.split(' (')[0], symptoms, diagnosis, doctor_id)
            )
        conn.commit()
        st.success("Diagnosis saved successfully!")

elif selected == "Reports":
    st.subheader("📂 Upload/View Reports")
    os.makedirs("reports", exist_ok=True)

    # Dropdown for selecting patient
    cursor.execute("SELECT id, name FROM users WHERE role = 'patient'")
    patients = cursor.fetchall()
    patient_map = {f"{name} ({pid})": pid for pid, name in patients}
    selected_patient = st.selectbox("Select Patient", list(patient_map.keys()), key="report_patient_dropdown")

    uploaded = st.file_uploader("Upload Report", type=["pdf", "jpg", "png"], key="doctor_report")

    doctor_id = user_id  # Use session-based doctor ID

    if st.button("Upload Report") and uploaded and selected_patient:
        patient_id = patient_map[selected_patient]
        file_path = f"reports/{uploaded.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded.getvalue())
        cursor.execute(
            "INSERT INTO reports (patient_id, file_path, uploaded_by, uploaded_at) VALUES (%s, %s, %s, NOW())",
            (patient_id, file_path, doctor_id)
        )
        conn.commit()
        st.success("Report uploaded successfully!")

    # View uploaded reports by this doctor
    st.markdown("---")
    st.subheader("📁 My Uploaded Reports")

    cursor.execute("SELECT patient_id, file_path, uploaded_at FROM reports WHERE uploaded_by = %s", (doctor_id,))
    reports = cursor.fetchall()
    for pid, path, uploaded_at in reports:
        with st.expander(f"Report for Patient {pid} - {uploaded_at}"):
            try:
                with open(path, "rb") as f:
                    file_bytes = f.read()
                st.download_button("Download", data=file_bytes, file_name=os.path.basename(path))
            except:
                st.error("File not found.")


elif selected == "Prescriptions":
    st.subheader("💊 Manage Prescriptions")

    # Fetch patients
    cursor.execute("SELECT id, name FROM users WHERE role = 'patient'")
    patients = cursor.fetchall()
    patient_map = {f"{name} ({pid})": pid for pid, name in patients}

    selected_patient = st.selectbox("Choose Patient", list(patient_map.keys()), key="prescription_patient")
    symptoms = st.text_area("Symptoms")
    diagnosis = st.text_area("Diagnosis")
    medicine = st.text_input("Medicine Name")
    dosage = st.text_input("Dosage Instructions")

    doctor_id = user_id  # from session
    patient_id = patient_map[selected_patient]

    if st.button("Save Prescription"):
        if not medicine.strip() or not dosage.strip():
            st.warning("Please enter both medicine and dosage.")
        else:
            # Save to prescriptions table
            cursor.execute("""
                INSERT INTO prescriptions (patient_id, doctor_id, medicine, dosage, date_issued)
                VALUES (%s, %s, %s, %s, NOW())
            """, (patient_id, doctor_id, medicine, dosage))

            # Update patients table
            cursor.execute("SELECT id FROM patients WHERE id = %s", (patient_id,))
            exists = cursor.fetchone()
            if exists:
                cursor.execute("""
                    UPDATE patients
                    SET symptoms = %s, diagnosis = %s, created_by = %s
                    WHERE id = %s
                """, (symptoms, diagnosis, doctor_id, patient_id))
            else:
                cursor.execute("""
                    INSERT INTO patients (id, name, symptoms, diagnosis, created_by)
                    VALUES (%s, %s, %s, %s, %s)
                """, (patient_id, selected_patient.split(" (")[0], symptoms, diagnosis, doctor_id))

            conn.commit()
            st.success("✅ Prescription saved and patient info updated.")


elif selected == "Profile & Settings":
    st.subheader("⚙️ Profile & Settings")

    if not user_id:
        st.warning("⚠️ You are not logged in. Please log in first.")
        st.stop()

    # Use email as join key
    cursor.execute("""
        SELECT u.name, u.email, u.dob, ad.department, d.rooms, d.building
        FROM users u
        JOIN approved_doctors ad ON u.email = ad.email
        JOIN departments d ON ad.department = d.dept_name
        WHERE u.id = %s AND u.role = 'doctor'
    """, (user_id,))

    result = cursor.fetchone()

    if result:
        name, email, dob, dept, room, building = result

        new_name = st.text_input("Full Name", value=name)
        new_email = st.text_input("Email", value=email)
        new_dob = st.date_input("Date of Birth", min_value=date(1950, 1, 1), max_value=date.today())

        st.markdown("### 🏥 Department & Assignment Info")
        st.info(f"**Department:** {dept}")
        st.info(f"**Room:** {room}")
        st.info(f"**Building:** {building}")

        if st.button("Update Profile"):
            cursor.execute("UPDATE users SET name = %s, email = %s, dob = %s WHERE id = %s",
                           (new_name, new_email, new_dob, user_id))
            cursor.execute("UPDATE approved_doctors SET name = %s, email = %s WHERE email = %s",
                           (new_name, new_email, email))
            conn.commit()
            st.success("✅ Profile updated successfully!")
    else:
        st.error("Doctor not found.")

conn.close()
