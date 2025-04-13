import streamlit as st
import mysql.connector
from streamlit_option_menu import option_menu
from datetime import date, timedelta, datetime
import os
from streamlit_extras.switch_page_button import switch_page
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


def generate_custom_id(prefix, role):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE role = %s", (role,))
    existing_ids = cursor.fetchall()
    max_id = 0
    for row in existing_ids:
        try:
            num = int(row[0].split('_')[1])
            max_id = max(max_id, num)
        except (IndexError, ValueError):
            continue
    conn.close()
    return f"{prefix}_{max_id + 1}"

st.set_page_config(page_title="Admin Dashboard", layout="wide")

st.markdown("""
    <style>
    /* Sidebar transparency and text */
    div[data-testid="stSidebarNav"] > ul {
        display: none;
    }
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Main content text */
    .stApp * {
        color: #f8f9fa !important;
    }

    /* Transparent and styled inputs */
    input, textarea, select {
        background-color: rgba(255, 255, 255, 0.07) !important;
        color: #f1f1f1 !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 0.5rem !important;
        padding: 0.5rem !important;
    }

    /* Placeholder text in inputs */
    input::placeholder, textarea::placeholder {
        color: #bbbbbb !important;
    }

    /* Drop-down arrow color for select */
    select option {
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
    }

    /* Optional: styling button */
    button[kind="primary"] {
        background-color: #0a84ff !important;
        color: white !important;
        border-radius: 0.5rem !important;
    }

    /* Hide menu and footer */
    #MainMenu, footer {
        visibility: hidden;
    }
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
            "Dashboard",
            "Departments",
            "Patients",
            "Doctors",
            "Appointments",
            "Reports",
            "Calendar"
        ],
        icons=[
            "speedometer",
            "building",
            "people",
            "person-badge",
            "calendar",
            "file-earmark-medical",
            "calendar3"
        ],
        menu_icon="hospital",
        default_index=0
    )
    st.markdown("---")
    if st.button("🔙 Back to Main Page"):
        switch_page("main")

st.title("🏥 Admin Dashboard")

user_id = st.session_state.get("user_id")
conn = create_connection()
cursor = conn.cursor()

if selected == "Dashboard":
    st.subheader("📊 Overview")

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='patient'")
    total_patients = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='doctor'")
    total_doctors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = cursor.fetchone()[0]

    st.metric("Total Patients", total_patients)
    st.metric("Total Doctors", total_doctors)
    st.metric("Total Appointments", total_appointments)

    st.subheader("📅 Upcoming Appointments")
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        SELECT a.id, u1.name as patient_name, u2.name as doctor_name, a.appointment_time, a.notes
        FROM appointments a
        JOIN users u1 ON a.patient_id = u1.id
        JOIN users u2 ON a.doctor_id = u2.id
        WHERE a.appointment_time >= %s
        ORDER BY a.appointment_time ASC
        LIMIT 5
    """, (today,))
    upcoming = cursor.fetchall()

    for app in upcoming:
        st.write(f"🗓️ {app[3]} | Patient: {app[1]} | Doctor: {app[2]} | Notes: {app[4]}")

if selected == "Departments":
    st.subheader("🏢 Hospital Departments")
    with st.expander("➕ Add Department"):
        dept_name = st.text_input("Department Name")
        building = st.text_input("Building")
        rooms = st.text_input("Room Numbers")
        if st.button("Add Department"):
            cursor.execute("INSERT INTO departments (dept_name, building, rooms) VALUES (%s, %s, %s)", (dept_name, building, rooms))
            conn.commit()
            st.success("Department added successfully!")

    st.markdown("---")
    cursor.execute("SELECT dept_name, building, rooms FROM departments")
    departments = cursor.fetchall()
    for dept_name, building, rooms in departments:
        with st.expander(dept_name):
            st.write(f"🏢 Building: {building}")
            st.write(f"🚪 Rooms: {rooms}")

elif selected == "Patients":
    st.subheader("🧑‍🤝‍🧑 Manage Patients")
    with st.expander("➕ Add New Patient"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        dob = st.date_input("Date of Birth", min_value=date(1950, 1, 1), max_value=date.today())
        if st.button("Add Patient"):
            new_id = generate_custom_id("p", "patient")
            cursor.execute("INSERT INTO users (id, name, email, dob, password, role) VALUES (%s, %s, %s, %s, NULL, 'patient')",
                           (new_id, name, email, dob))
            cursor.execute("INSERT INTO approved_patients (name, dob, email) VALUES (%s, %s, %s)", (name, dob, email))
            conn.commit()
            st.success("Patient added successfully!")

    st.markdown("---")
    st.subheader("📋 All Registered Patients")
    cursor.execute("SELECT id, name, email, dob FROM users WHERE role = 'patient'")
    patients = cursor.fetchall()
    for pid, name, email, dob in patients:
        with st.expander(f"{name} ({email})"):
            new_name = st.text_input(f"Name_{pid}", value=name)
            new_email = st.text_input(f"Email_{pid}", value=email)
            new_dob = st.date_input(f"DOB_{pid}", value=dob)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update", key=f"update_{pid}"):
                    cursor.execute("UPDATE users SET name=%s, email=%s, dob=%s WHERE id=%s",
                                   (new_name, new_email, new_dob, pid))
                    conn.commit()
                    st.success("Patient updated successfully!")
            with col2:
                if st.button("Delete", key=f"delete_{pid}"):
                    cursor.execute("DELETE FROM users WHERE id=%s", (pid,))
                    conn.commit()
                    st.warning("Patient deleted!")

elif selected == "Doctors":
    st.subheader("🩺 Manage Doctors")
    with st.expander("➕ Add New Doctor"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        dob = st.date_input("Date of Birth", min_value=date(1950, 1, 1), max_value=date.today())
        cursor.execute("SELECT dept_name FROM departments")
        departments = cursor.fetchall()
        dept_names = [d[0] for d in departments]
        dept = st.selectbox("Department", dept_names)
        if st.button("Add Doctor"):
            new_id = generate_custom_id("d", "doctor")
            cursor.execute("INSERT INTO users (id, name, email, dob, password, role) VALUES (%s, %s, %s, %s, NULL, 'doctor')",
                           (new_id, name, email, dob))
            cursor.execute("INSERT INTO approved_doctors (name, dob, email, department) VALUES (%s, %s, %s, %s)",
                           (name, dob, email, dept))
            conn.commit()
            st.success("Doctor added successfully!")

    st.markdown("---")
    st.subheader("📋 All Registered Doctors")
    cursor.execute("SELECT id, name, email FROM users WHERE role = 'doctor'")
    doctors = cursor.fetchall()
    for did, name, email in doctors:
        with st.expander(f"{name} ({email})"):
            new_name = st.text_input(f"DName_{did}", value=name)
            new_email = st.text_input(f"DEmail_{did}", value=email)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update", key=f"dupdate_{did}"):
                    cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (new_name, new_email, did))
                    cursor.execute("UPDATE approved_doctors SET name=%s, email=%s WHERE email=%s", (new_name, new_email, email))
                    conn.commit()
                    st.success("Doctor info updated!")
            with col2:
                if st.button("Delete", key=f"ddelete_{did}"):
                    cursor.execute("DELETE FROM approved_doctors WHERE email=%s", (email,))
                    cursor.execute("DELETE FROM appointments WHERE doctor_id=%s", (did,))
                    cursor.execute("DELETE FROM users WHERE id=%s", (did,))
                    conn.commit()
                    st.warning("Doctor deleted!")

if selected == "Appointments":
    st.subheader("📅 Book New Appointment")
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM users WHERE role='patient'")
    patients = cursor.fetchall()
    patient_options = {f"{name} ({pid})": pid for pid, name in patients}

    cursor.execute("SELECT id, dept_name FROM departments")
    departments = cursor.fetchall()
    dept_map = {dname: did for did, dname in departments}

    with st.form("appointment_form"):
        selected_dept = st.selectbox("Select Department", list(dept_map.keys()))
        selected_patient = st.selectbox("Select Patient", list(patient_options.keys()))

        # Fetch doctors by selected department
        cursor.execute("""
            SELECT u.id, u.name
            FROM users u
            JOIN approved_doctors ad ON u.email = ad.email
            WHERE u.role = 'doctor' AND ad.department = %s
        """, (selected_dept,))
        filtered_doctors = cursor.fetchall()
        doctor_options = {f"{name} ({did})": did for did, name in filtered_doctors}

        selected_doctor = st.selectbox("Select Doctor", list(doctor_options.keys()))
        appointment_date = st.date_input("Appointment Date")
        appointment_time = st.time_input("Appointment Time")
        notes = st.text_area("Notes")
        submit_appt = st.form_submit_button("Book Appointment")

        if submit_appt:
            datetime_combined = f"{appointment_date} {appointment_time}"
            cursor.execute(
                "INSERT INTO appointments (patient_id, doctor_id, appointment_time, notes) VALUES (%s, %s, %s, %s)",
                (patient_options[selected_patient], doctor_options[selected_doctor], datetime_combined, notes)
            )
            conn.commit()
            st.success("✅ Appointment booked successfully!")

elif selected == "Calendar":
    st.subheader("📅 Appointments Calendar")
    cursor.execute("""
        SELECT a.id, a.appointment_time, a.notes,
            p.id AS patient_id, p.name AS patient_name,
            d.id AS doctor_id, d.name AS doctor_name
        FROM appointments a
        JOIN users p ON a.patient_id = p.id
        JOIN users d ON a.doctor_id = d.id
    """)
    appointments = cursor.fetchall()
    events = []
    event_lookup = {}
    for aid, appt_time, notes, pid, pname, did, dname in appointments:
        short_note = (notes[:40] + '...') if notes and len(notes) > 40 else (notes or 'N/A')
        title = f"PID: {pid} | DID: {did} | 🕒 {appt_time.strftime('%H:%M')}\n📝 {short_note}"
        events.append({
            "id": str(aid),
            "title": title,
            "start": appt_time.isoformat(),
            "end": (appt_time + timedelta(minutes=30)).isoformat()
        })
        event_lookup[str(aid)] = {
            "Patient ID": pid,
            "Doctor ID": did,
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
        }
    )

    if clicked and "event" in clicked:
        appt_id = clicked["event"].get("id")
        if appt_id and appt_id in event_lookup:
            st.success("📌 Appointment Details")
            for key, value in event_lookup[appt_id].items():
                st.markdown(f"**{key}:** {value}")

elif selected == "Reports":
    st.subheader("📄 Upload/View Reports")
    os.makedirs("reports", exist_ok=True)
    uploaded = st.file_uploader("Upload Report", type=["pdf", "jpg", "png"], key="report_upload")
    patient_id = st.text_input("Patient ID for report", key="report_pid")
    uploaded_by = st.text_input("Uploaded by (Admin ID)", key="report_admin")
    submit = st.button("Submit Report")

    if submit and uploaded and patient_id and uploaded_by:
        file_path = f"reports/{uploaded.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded.getvalue())
        cursor.execute(
            "INSERT INTO reports (patient_id, file_path, uploaded_by, uploaded_at) VALUES (%s, %s, %s, NOW())",
            (patient_id, file_path, uploaded_by)
        )
        conn.commit()
        st.success("Report uploaded successfully!")

    st.markdown("---")
    st.subheader("🗂️ All Reports")
    cursor.execute("SELECT id, patient_id, file_path, uploaded_by, uploaded_at FROM reports")
    reports = cursor.fetchall()
    for rid, pid, path, uploader, timestamp in reports:
        with st.expander(f"Patient ID: {pid} | Uploaded by: {uploader} on {timestamp}"):
            try:
                with open(path, "rb") as f:
                    file_bytes = f.read()
                st.download_button("Download Report", data=file_bytes, file_name=os.path.basename(path))
            except FileNotFoundError:
                st.error(f"⚠️ File not found: {path}")

conn.close()
