import streamlit as st
import mysql.connector
from datetime import datetime, timedelta, date
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import os
import base64
import calendar
import streamlit_calendar as st_cal
import streamlit.components.v1 as components


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
    st.markdown("---")
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
    st.subheader("📆 Book a New Appointment")

    # Step 1: Select Department
    cursor.execute("SELECT dept_name FROM departments")
    departments = [row[0] for row in cursor.fetchall()]
    selected_dept = st.selectbox("Choose Department", departments)

    # Step 2: Get doctors in that department
    cursor.execute("""
        SELECT u.id, u.name, u.email
        FROM users u
        JOIN approved_doctors ad ON u.email = ad.email
        WHERE u.role = 'doctor' AND ad.department = %s
    """, (selected_dept,))
    doctor_list = cursor.fetchall()

    if not doctor_list:
        st.warning("No doctors found in this department.")
    else:
        doctor_map = {f"Dr. {name} ({doc_id})": (doc_id, email) for doc_id, name, email in doctor_list}
        selected_doc_label = st.selectbox("Choose Doctor", list(doctor_map.keys()))
        selected_doc_id, selected_doc_email = doctor_map[selected_doc_label]

        # Step 3: Select date and time
        appt_date = st.date_input("Select Date", min_value=date.today())
        appt_time = st.time_input("Select Time")
        notes = st.text_area("Reason for Visit / Notes")

        # Step 4: Get department building & room using doctor's email
        cursor.execute("""
            SELECT d.building, d.rooms 
            FROM departments d
            JOIN approved_doctors ad ON ad.department = d.dept_name
            WHERE ad.email = %s
        """, (selected_doc_email,))
        dept_info = cursor.fetchone()
        building, room = dept_info if dept_info else ("", "")

        # Step 5: Submit appointment
        if st.button("📅 Book Appointment"):
            appointment_datetime = datetime.combine(appt_date, appt_time)
            cursor.execute("""
                INSERT INTO appointments 
                (patient_id, doctor_id, appointment_time, notes, dept_name, building, room_no)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, selected_doc_id, appointment_datetime, notes, selected_dept, building, room))
            conn.commit()
            st.success("✅ Appointment booked successfully!")


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
        JOIN approved_doctors ad ON d.email = ad.email
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
                    <div style='border-left: 5px solid {color}; padding-left: 10px; margin-bottom: 15px; color:white'>
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



import streamlit.components.v1 as components

components.html("""
<style>
#chat-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background-color: #4A90E2;
  color: white;
  border: none;
  border-radius: 30px;
  padding: 12px 20px;
  font-size: 16px;
  cursor: pointer;
  z-index: 9999;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

#chat-popup {
  position: fixed;
  bottom: 90px;
  right: 30px;
  width: 320px;
  height: 420px;
  background-color: #ffffff;
  border-radius: 15px;
  padding: 10px;
  display: none;
  flex-direction: column;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  z-index: 9999;
}

#chat-log {
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 10px;
  font-size: 14px;
  color: black;
}

#chat-input {
  width: 100%;
  height: 60px;
  border-radius: 10px;
  resize: none;
  padding: 10px;
  font-size: 14px;
}
</style>

<button id="chat-button">💬 Chat</button>

<div id="chat-popup">
  <div id="chat-log">Hi 👋 I can help you with appointments, reports, and more.<br><br></div>
  <textarea id="chat-input" placeholder="Type your message..."></textarea>
</div>

<script>
const btn = document.getElementById("chat-button");
const popup = document.getElementById("chat-popup");
const input = document.getElementById("chat-input");
const log = document.getElementById("chat-log");

btn.onclick = () => {
  popup.style.display = popup.style.display === "flex" ? "none" : "flex";
};

input.addEventListener("keydown", function(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    const userMsg = input.value.trim();
    if (userMsg) {
      log.innerHTML += `<div><b>You:</b> ${userMsg}</div>`;
      let botReply = "❓ Sorry, I didn’t get that.";
      const lower = userMsg.toLowerCase();
      if (lower.includes("appointment")) {
        botReply = "📅 You can book or check appointments from the dashboard.";
      } else if (lower.includes("report")) {
        botReply = "📂 Check the Reports tab to upload/download medical files.";
      } else if (lower.includes("department")) {
        botReply = "🏥 Our hospital includes Cardiology, Pediatrics, Neurology and more.";
      } else if (lower.includes("contact")) {
        botReply = "☎️ Contact us at +91-1234567890 or email support@hospital.com.";
      }
      log.innerHTML += `<div><b>Bot:</b> ${botReply}</div><br>`;
      input.value = "";
      log.scrollTop = log.scrollHeight;
    }
  }
});
</script>
""", height=0, width=0)

conn.close()
