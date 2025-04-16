import streamlit as st

def render_chatbot():
    # Improved FAQ response mapping
    faq_responses = {
        # Appointments
        "book appointment": "Go to the 'Book Appointment' section in the sidebar to schedule an appointment.",
        "appointment details": "You can manage your appointments in the 'Appointments' tab.",
        "reschedule": "Rescheduling is not available. Please cancel and rebook.",
        "cancel": "Cancel appointments in the 'Appointments' section.",
        "date": "Select your appointment date in the 'Book Appointment' tab.",
        "time": "Time slots are shown while booking an appointment.",
        "schedule": "Use the 'Book Appointment' tab to schedule your visit.",
        "doctor": "Doctors are assigned based on the selected department in booking.",

        # Reports
        "report": "Check and upload your medical reports in the 'Reports' section.",
        "upload": "Use the 'Reports' tab to upload your medical documents.",
        "download": "Reports can be downloaded from the 'Reports' section.",
        "file": "Uploaded files are listed under the 'Reports' tab.",

        # Prescriptions
        "prescription": "Your current prescriptions are in the 'Prescriptions' section.",
        "medicine": "Find your prescribed medicines in the 'Prescriptions' tab.",
        "medication": "Medication details like dosage are available in 'Prescriptions'.",
        "dose": "Dosage information is listed with each prescription.",

        # Profile & Personal Info
        "profile": "You can edit your name, email, and DOB in 'Profile & Settings'.",
        "edit": "To change your information, visit 'Profile & Settings'.",
        "settings": "Find personal account settings in the 'Profile & Settings' section.",
        "email": "Your registered email is shown in your profile tab.",
        "dob": "Update your date of birth under 'Profile & Settings'.",
        "age": "Age is automatically calculated based on your DOB.",
        "gender": "Your gender is recorded during registration.",

        # Navigation Help
        "where": "Use the sidebar menu to navigate different sections.",
        "how": "Please choose the feature from the sidebar for assistance.",
        "menu": "All dashboard features are accessible from the left sidebar.",
        "home": "Click 'Back to Main Page' at the bottom of the sidebar.",

        # Departments
        "department": "Available departments include Cardiology, Neurology, Pediatrics, Dermatology, and more.",
        "cardiology": "To consult a cardiologist, select 'Cardiology' while booking.",
        "neurology": "Neurologists are listed under the 'Book Appointment' tab.",
        "pediatrics": "For child-related care, choose Pediatrics in booking.",
        "dermatology": "Dermatology services can be selected from the appointment tab.",

        # Support & Emergency
        "support": "For help, email us at support@ehrhospital.com.",
        "help": "We're here to assist. Contact support or explore the dashboard.",
        "contact": "Reach us via support@ehrhospital.com for any assistance.",
        "emergency": "In emergencies, dial 108 or go to the nearest hospital.",
        "call": "We do not currently offer direct call services.",
        "email": "Our support email is support@ehrhospital.com.",

        # General Queries
        "logout": "To logout, click the top-right corner menu or end the session.",
        "history": "View your history in the 'Appointments' and 'Reports' tabs.",
        "checkup": "Book a routine check-up through 'Book Appointment'.",
        "routine": "Regular health check-ups can be scheduled like any appointment.",
        "error": "If something went wrong, refresh the page or contact support.",
        "issue": "For any issue, please reach out to our support.",
        "slow": "Performance may vary based on internet connection.",
        "insurance": "We currently do not support insurance integration.",
        "vaccine": "Vaccination details are not included in this system.",
        "tips": "Stay hydrated, eat well, and follow your treatment plans.",
        "feedback": "We welcome feedback! Email us at support@ehrhospital.com.",
        "guidelines": "All patient guidelines are provided during diagnosis or consultation."
    }


    def match_faq(user_input):
        user_input = user_input.lower()
        for keyword, response in faq_responses.items():
            if keyword in user_input:
                return response
        return "I'm sorry, I couldn't understand that. Please try asking differently."


    # UI Styling
    st.markdown("""
    <style>
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 1rem;
        max-width: 700px;
        margin: auto;
        box-shadow: 0 0 15px rgba(0,0,0,0.1);
    }
    .chat-bubble {
        background-color: #007BFF;
        color: white;
        padding: 12px;
        border-radius: 20px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .user-bubble {
        background-color: #e0e0e0;
        color: black;
        align-self: flex-end;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("**🤖 Bot:** Hi there! I’m your assistant. Ask me anything related to your dashboard!")

    user_input = st.text_input("You:", key="chat_input")
    if user_input:
        response = match_faq(user_input)
        st.markdown(f"**🧑 You:** {user_input}")
        st.markdown(f"**🤖 Bot:** {response}")

    st.markdown("</div>", unsafe_allow_html=True)
