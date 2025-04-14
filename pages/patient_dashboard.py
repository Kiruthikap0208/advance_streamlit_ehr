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


# --- Inject chatbot toggle and popup ---
components.html("""
<style>
.chat-popup-btn {
  position: fixed;
  bottom: 25px;
  right: 25px;
  background-color: #4A90E2;
  color: white;
  padding: 12px 16px;
  border: none;
  border-radius: 50px;
  font-size: 16px;
  cursor: pointer;
  z-index: 9999;
  box-shadow: 2px 2px 12px rgba(0,0,0,0.3);
}

.chat-popup-box {
  display: none;
  position: fixed;
  bottom: 90px;
  right: 25px;
  width: 320px;
  height: 400px;
  background: rgba(0, 0, 0, 0.75);
  color: white;
  border-radius: 10px;
  padding: 10px;
  z-index: 9999;
  overflow-y: auto;
}

.chat-popup-box.open {
  display: block;
}

.chat-popup-header {
  font-weight: bold;
  margin-bottom: 10px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 5px;
}

.chat-popup-input {
  width: 100%;
  padding: 6px;
  border-radius: 5px;
  margin-top: 10px;
  border: none;
}

.chat-msg {
  margin-bottom: 8px;
  font-size: 14px;
}

.user-msg {
  color: #00ccff;
}

.bot-msg {
  color: #ffffff;
}
</style>

<button class="chat-popup-btn" onclick="document.querySelector('.chat-popup-box').classList.toggle('open')">
  💬 Ask Assistant
</button>

<div class="chat-popup-box">
  <div class="chat-popup-header">🤖 Hospital Assistant</div>
  <div id="chat-box"></div>
  <input type="text" id="user-input" class="chat-popup-input" placeholder="Type here..." onkeydown="if(event.key === 'Enter') sendMessage()" />
</div>

<script>
let chatHistory = [];

function sendMessage() {
  let input = document.getElementById("user-input");
  let msg = input.value.trim();
  if (msg === "") return;
  chatHistory.push(["user", msg]);
  renderChat();
  input.value = "";

  setTimeout(() => {
    let reply = getBotReply(msg);
    chatHistory.push(["bot", reply]);
    renderChat();
  }, 500);
}

function renderChat() {
  let chatBox = document.getElementById("chat-box");
  chatBox.innerHTML = "";
  chatHistory.slice(-10).forEach(([sender, msg]) => {
    let cls = sender === "user" ? "user-msg" : "bot-msg";
    chatBox.innerHTML += `<div class="chat-msg ${cls}"><strong>${sender === 'user' ? 'You' : 'Bot'}:</strong> ${msg}</div>`;
  });
  chatBox.scrollTop = chatBox.scrollHeight;
}

function getBotReply(q) {
  q = q.toLowerCase();
  if (q.includes("book")) return "🗓 Go to 'Book Appointment' to schedule a visit.";
  if (q.includes("appointment")) return "📅 Check 'Appointments' tab for your scheduled visits.";
  if (q.includes("report")) return "📂 Visit 'Reports' section to download or view reports.";
  if (q.includes("department")) return "🏥 We offer departments like Cardiology, Neurology, and more.";
  if (q.includes("contact")) return "📞 Call +91-XXXXXXXXXX or visit our helpdesk.";
  return "🤖 I'm here to help! Try asking about appointments, reports, or contact.";
}
</script>
""", height=0)

conn.close()
