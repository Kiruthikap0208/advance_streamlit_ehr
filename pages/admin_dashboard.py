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

# Sidebar menu
# Sidebar with transparent background
with st.sidebar:
    st.markdown("---")
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Patients", "Doctors", "Departments", "Appointments", "Reports", "Calendar"],
        icons=["speedometer", "people", "person-badge", "building", "calendar", "file-earmark-medical", "calendar3"],
        menu_icon="hospital",
        default_index=0
    )
        
    st.page_link("main.py", label="🔙 Back to Main Page", icon="🏠")




st.title("🏥 Admin Dashboard")

# 🔔 Reminders Section
user_id = st.session_state.get("user_id")
conn = create_connection()
cursor = conn.cursor()

if selected == "Calendar":
    st.subheader("📅 Appointments Calendar")

    conn = create_connection()
    cursor = conn.cursor()
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
        event = {
            "id": str(aid),
            "title": title,
            "start": appt_time.isoformat(),
            "end": (appt_time + timedelta(minutes=30)).isoformat()
        }
        events.append(event)
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
        },
          # Ensure this is outside options
    )

    if clicked and "event" in clicked:
        appt_id = clicked["event"].get("id")
        if appt_id and appt_id in event_lookup:
            st.success("📌 Appointment Details")
            for key, value in event_lookup[appt_id].items():
                st.markdown(f"**{key}:** {value}")


elif selected == "Dashboard":
    st.subheader("🔔 Upcoming Appointments in Next 24 Hours")
    cursor.execute("""
        SELECT a.appointment_time, p.name AS patient_name, d.name AS doctor_name
        FROM appointments a
        JOIN users p ON a.patient_id = p.id
        JOIN users d ON a.doctor_id = d.id
        WHERE a.appointment_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 1 DAY)
        ORDER BY a.appointment_time
    """)
    reminders = cursor.fetchall()

    if reminders:
        for appt_time, pname, dname in reminders:
            st.info(f"🕒 {appt_time} — {pname} with Dr. {dname}")
    else:
        st.success("No upcoming appointments in the next 24 hours.")

    conn.close()

    st.subheader("📊 Overview")
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
    st.subheader("🧑‍🤝‍🧑 Manage Patients")
    conn = create_connection()
    cursor = conn.cursor()

    with st.expander("➕ Add New Patient"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        dob = st.date_input("Date of Birth", min_value=date(1950, 1, 1), max_value=date.today())
        if st.button("Add Patient"):
            new_id = generate_custom_id("p", "patient")
            cursor.execute("INSERT INTO users (id, name, email, dob, role) VALUES (%s, %s, %s, %s, 'patient')",
                        (new_id, name, email, dob))
            cursor.execute("INSERT INTO approved_patients (name, dob, email) VALUES (%s, %s, %s)",
                        (name, dob, email))
            conn.commit()
            st.success("Patient added successfully!")


    st.markdown("---")
    st.subheader("📋 All Registered Patients")
    cursor.execute("SELECT id, name, email, dob FROM users WHERE role = 'patient'")
    patients = cursor.fetchall()

    for patient in patients:
        pid, name, email, dob = patient
        with st.expander(f"{name} ({email})"):
            new_name = st.text_input(f"Name_{pid}", value=name, key=f"name_{pid}")
            new_email = st.text_input(f"Email_{pid}", value=email, key=f"email_{pid}")
            new_dob = st.date_input(f"DOB_{pid}", value=dob, key=f"dob_{pid}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update", key=f"update_{pid}"):
                    cursor.execute("UPDATE users SET name=%s, email=%s, dob=%s WHERE id=%s",
                                   (new_name, new_email, new_dob, pid))
                    conn.commit()
                    st.success("Updated successfully!")
            with col2:
                if st.button("Delete", key=f"delete_{pid}"):
                    cursor.execute("DELETE FROM users WHERE id=%s", (pid,))
                    conn.commit()
                    st.warning("Deleted successfully!")
    conn.close()

elif selected == "Doctors":
    st.subheader("🩺 Manage Doctors")
    conn = create_connection()
    cursor = conn.cursor()

    with st.expander("➕ Add New Doctor"):
        name = st.text_input("Doctor Name")
        email = st.text_input("Email")

        # Fetch departments from DB
        cursor.execute("SELECT dept_name FROM departments")
        dept_list = [row[0] for row in cursor.fetchall()]
        if dept_list:
            dept = st.selectbox("Select Department", dept_list)
        else:
            st.warning("⚠️ No departments found. Please add departments first.")
            dept = None

        dob = st.date_input("Date of Birth", min_value=date(1950, 1, 1), max_value=date.today())
        if st.button("Add Doctor"):
            new_id = generate_custom_id("d", "doctor")
            cursor.execute("INSERT INTO users (id, name, email, role, dob) VALUES (%s, %s, %s, 'doctor', %s)",
                           (new_id, name, email, dob))
            cursor.execute("INSERT INTO approved_doctors (name, dob, department, email) VALUES (%s, %s, %s, %s)",
                           (name, dob, dept, email))
            conn.commit()
            st.success("Doctor added successfully!")

    st.markdown("---")
    st.subheader("📋 All Doctors")
    cursor.execute("SELECT id, name, email FROM users WHERE role = 'doctor'")
    doctors = cursor.fetchall()

    for doc in doctors:
        did, name, email = doc
        with st.expander(f"{name} ({email})"):
            new_name = st.text_input(f"DName_{did}", value=name, key=f"dname_{did}")
            new_email = st.text_input(f"DEmail_{did}", value=email, key=f"demail_{did}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update", key=f"dupdate_{did}"):
                    cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (new_name, new_email, did))
                    cursor.execute("UPDATE approved_doctors SET name=%s, email=%s WHERE email=%s", (new_name, new_email, email))
                    conn.commit()
                    st.success("Doctor info updated in both tables!")

            with col2:
                if st.button("Delete", key=f"ddelete_{did}"):
                    cursor.execute("DELETE FROM approved_doctors WHERE email=%s", (email,))
                    cursor.execute("DELETE FROM appointments WHERE doctor_id=%s", (did,))
                    cursor.execute("DELETE FROM users WHERE id=%s", (did,))
                    conn.commit()
                    st.warning("Doctor deleted from all related tables.")


    conn.close()

elif selected == "Appointments":
    st.subheader("📅 Book New Appointment")
    cursor.execute("SELECT id, name FROM users WHERE role='patient'")
    patients = cursor.fetchall()
    patient_options = {f"{name} ({pid})": pid for pid, name in patients}

    cursor.execute("SELECT dept_name FROM departments")
    department_list = [d[0] for d in cursor.fetchall()]

    cursor.execute("SELECT id, name, email FROM users WHERE role='doctor'")
    doctor_map = cursor.fetchall()

    with st.form("appointment_form"):
        selected_patient = st.selectbox("Select Patient", list(patient_options.keys()))
        selected_department = st.selectbox("Select Department", department_list)

        cursor.execute("SELECT email FROM approved_doctors WHERE department = %s", (selected_department,))
        approved_emails = [row[0] for row in cursor.fetchall()]

        filtered_doctors = [
            (doc_id, doc_name) for doc_id, doc_name, doc_email in doctor_map if doc_email in approved_emails
        ]
        doctor_options = {f"{name} ({did})": did for did, name in filtered_doctors}

        selected_doctor = st.selectbox("Select Doctor", list(doctor_options.keys()))
        appointment_date = st.date_input("Appointment Date")
        appointment_time = st.time_input("Appointment Time")
        notes = st.text_area("Notes")
        submit_appt = st.form_submit_button("Book Appointment")

        if submit_appt:
            datetime_combined = f"{appointment_date} {appointment_time}"
            cursor.execute("INSERT INTO appointments (patient_id, doctor_id, appointment_time, notes) VALUES (%s, %s, %s, %s)", (patient_options[selected_patient], doctor_options[selected_doctor], datetime_combined, notes))
            conn.commit()
            st.success("✅ Appointment booked successfully!")

    st.markdown("---")
    st.subheader("📋 All Appointments")
    cursor.execute("""
        SELECT a.id, p.name AS patient_name, d.name AS doctor_name, a.appointment_time, a.notes
        FROM appointments a
        JOIN users p ON a.patient_id = p.id
        JOIN users d ON a.doctor_id = d.id
    """)

    appointments = cursor.fetchall()
    for aid, pname, dname, time, notes in appointments:
        with st.expander(f"{pname} with {dname} at {time}"):
            st.write("📝 Notes:", notes)
            new_time = st.time_input(f"New Time for {aid}", value=time.time(), key=f"appt_time_{aid}")
            new_date = st.date_input(f"New Date for {aid}", value=time.date(), key=f"appt_date_{aid}")
            new_notes = st.text_area(f"Edit Notes for {aid}", value=notes, key=f"appt_notes_{aid}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update", key=f"update_appt_{aid}"):
                    updated_datetime = f"{new_date} {new_time}"
                    cursor.execute("UPDATE appointments SET appointment_time = %s, notes = %s WHERE id = %s", (updated_datetime, new_notes, aid))
                    conn.commit()
                    st.success("Appointment updated!")
            with col2:
                if st.button("Cancel Appointment", key=f"cancel_appt_{aid}"):
                    cursor.execute("DELETE FROM appointments WHERE id = %s", (aid,))
                    conn.commit()
                    st.warning("Appointment cancelled.")

elif selected == "Departments":
    st.subheader("🏢 Manage Departments")
    conn = create_connection()
    cursor = conn.cursor()

    with st.expander("➕ Add New Department"):
        dept_name = st.text_input("Department Name")
        building = st.text_input("Building")
        rooms = st.text_input("Room Numbers (comma-separated)")

        if st.button("Add Department"):
            cursor.execute("INSERT INTO departments (dept_name, building, rooms) VALUES (%s, %s, %s)",
                           (dept_name, building, rooms))
            conn.commit()
            st.success("Department added successfully!")

    st.markdown("---")
    st.subheader("📋 All Departments")
    cursor.execute("SELECT dept_name, building, rooms FROM departments")
    departments = cursor.fetchall()

    for dept_name, building, rooms in departments:
        with st.expander(f"{dept_name}"):
            new_name = st.text_input(f"Edit Name - {dept_name}", value=dept_name, key=f"name_{dept_name}")
            new_building = st.text_input(f"Edit Building - {dept_name}", value=building, key=f"bldg_{dept_name}")
            new_rooms = st.text_input(f"Edit Rooms - {dept_name}", value=rooms, key=f"room_{dept_name}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Update {dept_name}"):
                    cursor.execute("""
                        UPDATE departments SET dept_name=%s, building=%s, rooms=%s
                        WHERE dept_name=%s
                    """, (new_name, new_building, new_rooms, dept_name))
                    conn.commit()
                    st.success("Department updated successfully!")

            with col2:
                if st.button(f"Delete {dept_name}"):
                    cursor.execute("DELETE FROM departments WHERE dept_name=%s", (dept_name,))
                    conn.commit()
                    st.warning("Department deleted successfully!")

    conn.close()


elif selected == "Reports":
    st.subheader("📄 Upload/View Reports")
    os.makedirs("reports", exist_ok=True)

    uploaded = st.file_uploader("Upload Report", type=["pdf", "jpg", "png"], key="report_upload")
    patient_id = st.text_input("Patient ID for report", key="report_pid")
    uploaded_by = st.text_input("Uploaded by (Admin ID)", key="report_admin")
    submit = st.button("Submit Report")

    conn = create_connection()
    cursor = conn.cursor()

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
