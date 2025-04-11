import streamlit as st
import mysql.connector
import base64

# -------- DB CONNECTION --------
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nk258627",
        database="srm_ehr"
    )

def add_patient(name, age, symptoms, diagnosis):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patients (name, age, symptoms, diagnosis) VALUES (%s, %s, %s, %s)",
                   (name, age, symptoms, diagnosis))
    conn.commit()
    conn.close()

# -------- PAGE SETUP --------
st.set_page_config(page_title="Add Patient | SRM EHR", layout="wide")

# Background
with open("copy-space-heart-shape-stethoscope.jpg", "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{b64_img}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .form-box {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 3rem 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }}
    .stTextInput > div > input,
    .stTextArea textarea {{
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 0.75rem;
    }}
    .stButton button {{
        width: 100%;
        border-radius: 10px;
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
        margin-top: 1rem;
    }}
    </style>
""", unsafe_allow_html=True)

# -------- FORM --------
col1, col2, col3 = st.columns([1, 1, 2.2])
with col3:
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.title("➕ Add New Patient")

    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    symptoms = st.text_area("Symptoms")
    diagnosis = st.text_area("Diagnosis")

    if st.button("Save Patient"):
        if not name or not symptoms or not diagnosis:
            st.warning("Please fill in all fields.")
        else:
            add_patient(name, age, symptoms, diagnosis)
            st.success(f"✅ Patient '{name}' added successfully!")

    if st.button("🔙 Back to Dashboard"):
        st.switch_page("pages/4_Dashboard_Doctor.py")

    st.markdown("</div>", unsafe_allow_html=True)
