import streamlit as st

def render_chatbot():
    # Improved FAQ response mapping
    faq_responses = {
        # ✅ Appointments
        "how do i book an appointment": "Go to the 'Book Appointment' section in the sidebar.",
        "can i reschedule my appointment": "Currently, rescheduling isn't supported. Please cancel and rebook.",
        "can i cancel my appointment": "Yes. Use the 'Appointments' tab to cancel any existing appointment.",
        "how can i view my appointment": "Click on the 'Appointments' tab to see all your bookings.",
        "can i choose a specific doctor": "Yes, use the 'Book Appointment' tab to select a department and doctor.",
        "what if no doctor is available": "Please try a different time or department. Some slots may be full.",
        "can i add notes to appointments": "Yes, you can add a reason or notes when booking an appointment.",
        "how long are appointment slots": "Each appointment typically lasts around 30 minutes.",

        # 🧭 Navigation Help
        "where is my profile": "Click on 'Profile & Settings' in the sidebar.",
        "how do i view my health records": "Use the 'My Health Records' tab to access your symptoms and diagnosis.",
        "where can i download reports": "Go to 'Reports' and click on the download button for each report.",
        "how do i change my email": "Update your email in 'Profile & Settings'.",
        "where do i upload reports": "In the 'Reports' section, use the uploader to add your files.",
        "can i view past prescriptions": "Yes, go to 'Prescriptions' to see your issued medications.",
        "how to logout": "Please use the sidebar navigation to return to the main page and logout.",

        # 🏥 Department & Doctor Info
        "what departments are available": "Departments include Cardiology, Neurology, Pediatrics, Dermatology, and more.",
        "how do i know which doctor is available": "Use 'Book Appointment' to view available doctors by department.",
        "can i choose department first": "Yes. First select a department, then choose an available doctor.",
        "which doctor is in cardiology": "Select 'Cardiology' in the booking tab to see all related doctors.",
        "how do i know doctor timings": "Appointment slots will be shown during the booking process.",
        "are female doctors available": "Doctor details are shown under the 'Book Appointment' tab by name.",
        "what building is my appointment in": "Building and room info will be displayed once your appointment is booked.",

        # 📝 Reports & Uploads
        "how do i upload medical report": "Go to the 'Reports' tab and use the upload feature.",
        "what file formats are allowed": "You can upload PDF, JPG, or PNG files.",
        "can i delete a report": "Currently, patients can't delete reports. Contact support if needed.",
        "how do i view all reports": "Click on 'Reports' to view all uploads associated with your ID.",
        "who can see my reports": "Only authorized medical staff (doctors/admins) can view your reports.",

        # 💊 Prescriptions
        "where can i find my prescriptions": "Go to the 'Prescriptions' tab to view your medication history.",
        "can i download prescriptions": "Prescriptions may be saved as reports and downloaded from the Reports tab.",
        "who uploaded my prescription": "Each prescription/report will display the name of the uploader (doctor/admin).",
        "what if my prescription is missing": "Please contact your assigned doctor or raise the issue via support.",

        # 🔐 Profile & Settings
        "how do i update my dob": "Go to 'Profile & Settings' and change your Date of Birth.",
        "can i edit my name": "Yes, use the 'Profile & Settings' tab.",
        "how do i change my gender info": "Currently, gender can only be changed by the admin. Contact support.",
        "how do i update my login email": "Use 'Profile & Settings' to change your registered email.",
        "how do i reset password": "Currently password management is handled by the admin. Email support for assistance.",

        # ❓ General FAQs
        "how do i contact support": "Email us at support@ehrhospital.com.",
        "do you have emergency services": "In emergencies, dial 108 or go to the nearest emergency room.",
        "is there 24x7 support": "Support is available during working hours via email.",
        "can i use this on mobile": "Yes, the portal is mobile responsive.",
        "what if i forget my appointment time": "Go to the 'Appointments' tab to check your upcoming slots.",
        "what is srm ehr": "SRM EHR is an Electronic Health Record system for managing patient information and care.",
        "can i print my reports": "Yes, after downloading a report you can print it as needed.",
        "how do i get notified for appointments": "Please check your email or visit the Appointments tab regularly.",
        "what is my patient id": "Your Patient ID is shown under 'My Health Records' or 'Appointments'.",
        "can i request a specific room": "Room assignment is automatic based on department."
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
        response = get_response(user_input)
        st.markdown(f"**🧑 You:** {user_input}")
        st.markdown(f"**🤖 Bot:** {response}")

    st.markdown("</div>", unsafe_allow_html=True)
