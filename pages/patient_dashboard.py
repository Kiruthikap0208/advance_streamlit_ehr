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

if selected == "Appointments":
    st.subheader("🗕️ My Appointments (Calendar View)")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, a.appointment_time, a.notes,
               d.id AS doctor_id, d.name AS doctor_name
        FROM appointments a
        JOIN users d ON a.doctor_id = d.id
        WHERE a.patient_id = %s
    """, (user_id,))
    appointments = cursor.fetchall()

    events = []
    event_lookup = {}
    for aid, appt_time, notes, did, dname in appointments:
        short_note = (notes[:40] + '...') if notes and len(notes) > 40 else (notes or 'N/A')
        title = f"DID: {did} | 🕒 {appt_time.strftime('%H:%M')}\n📜 {short_note}"
        event = {
            "id": str(aid),
            "title": title,
            "start": appt_time.isoformat(),
            "end": (appt_time + timedelta(minutes=30)).isoformat()
        }
        events.append(event)
        event_lookup[str(aid)] = {
            "Doctor ID": did,
            "Doctor Name": dname,
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
            "height": 850,
        }
    )

    if clicked and "event" in clicked:
        appt_id = clicked["event"].get("id")
        if appt_id and appt_id in event_lookup:
            st.success("📌 Appointment Details")
            for key, value in event_lookup[appt_id].items():
                st.markdown(f"**{key}:** {value}")

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

elif selected == "Book Appointment":
    st.subheader("📆 Book New Appointment")
    cursor.execute("SELECT id, name FROM users WHERE role='doctor'")
    doctors = cursor.fetchall()
    doc_dict = {f"{name} ({doc_id})": doc_id for doc_id, name in doctors}

    with st.form("book_appt_form"):
        doc_choice = st.selectbox("Choose Doctor", list(doc_dict.keys()))
        date_choice = st.date_input("Preferred Date", min_value=date.today())
        time_choice = st.time_input("Preferred Time")
        notes = st.text_area("Any specific notes or symptoms?")
        submit = st.form_submit_button("Book Appointment")

        if submit:
            datetime_combined = f"{date_choice} {time_choice}"
            cursor.execute("""
                INSERT INTO appointments (patient_id, doctor_id, appointment_time, notes)
                VALUES (%s, %s, %s, %s)
            """, (user_id, doc_dict[doc_choice], datetime_combined, notes))
            conn.commit()
            st.success("Appointment booked successfully!")

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
