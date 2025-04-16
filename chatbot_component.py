import streamlit as st

def render_chatbot():
    # Improved FAQ response mapping
    faq_responses = {
        # Appointments
        "book appointment": "To book an appointment, go to the 'Book Appointment' tab in the sidebar.",
        "reschedule": "Currently, rescheduling isn't supported. Please cancel and rebook.",
        "cancel appointment": "To cancel an appointment, navigate to the 'Appointments' tab.",
        "appointment time": "Your upcoming appointments are listed in the 'Appointments' tab.",
        "doctor schedule": "Doctor availability is visible in the 'Book Appointment' section.",
        
        # Reports
        "upload report": "Use the 'Reports' tab and click on Upload to submit your medical reports.",
        "view reports": "You can view and download reports in the 'Reports' tab.",
        "download report": "Go to the 'Reports' tab and use the download button next to each file.",
        "report status": "Reports are uploaded manually and stored securely in your dashboard.",
        
        # Prescriptions
        "view prescriptions": "Navigate to the 'Prescriptions' tab to view your medications.",
        "medication details": "Prescription details like dosage and instructions are shown in 'Prescriptions'.",
        "old prescriptions": "Your historical prescriptions are also listed under the 'Prescriptions' tab.",
        
        # Navigation
        "where is": "All sections can be accessed via the sidebar menu.",
        "change my info": "Go to 'Profile & Settings' to update your information.",
        "edit profile": "You can update your name, email, and DOB in 'Profile & Settings'.",
        "where to update": "Profile edits can be made in the 'Profile & Settings' tab.",
        
        # Departments & Doctors
        "available departments": "We offer Cardiology, Neurology, Pediatrics, Dermatology, and more.",
        "doctor availability": "Use the 'Book Appointment' tab to see available doctors by department.",
        "which doctor": "You can choose your doctor from the 'Book Appointment' tab based on department.",
        "dermatology doctor": "Select 'Dermatology' from department in 'Book Appointment' to see options.",
        
        # Account & Security
        "change password": "Password change is not currently supported directly via dashboard.",
        "logout": "To logout, click on the logout button or close your session.",
        "secure": "Your data is securely stored and encrypted in our system.",
        
        # Support & Contact
        "contact support": "Please email us at support@ehrhospital.com for any help.",
        "emergency": "In case of emergency, dial 108 or visit the nearest hospital.",
        "24/7": "Support is available via email, but emergency services should be contacted for critical issues.",
        "help": "For assistance, contact support or check the sidebar options.",
        
        # General Health
        "health tips": "Stay hydrated, follow prescriptions, and attend scheduled check-ups.",
        "routine checkup": "Book an appointment in 'Book Appointment' for routine check-ups.",
        "vaccine record": "Currently, vaccination records are not supported in the dashboard.",
        
        # Technical
        "not working": "Try refreshing your browser. If the issue persists, contact support.",
        "error": "If you're seeing an error, please email us a screenshot at support@ehrhospital.com.",
        "slow": "Performance may vary based on your internet connection.",
        
        # Miscellaneous
        "insurance": "Currently, we don’t integrate with insurance providers.",
        "lab results": "If lab reports are available, you can find them in the 'Reports' tab.",
        "appointment history": "Your past appointments are available under 'Appointments'.",
        "download": "Reports and prescriptions can be downloaded from their respective sections.",
        "upload": "Only PDF and image formats are accepted in the 'Reports' tab.",
        # Appointments
        "book": "To book an appointment, go to the 'Book Appointment' tab in the sidebar.",
        "appointment": "Check or book appointments in the 'Appointments' or 'Book Appointment' tab.",
        "reschedule": "Currently, rescheduling isn't supported. Please cancel and rebook.",
        "cancel": "You can cancel appointments from the 'Appointments' tab.",
        "time": "Appointment times are shown under 'Appointments'.",
        "doctor": "Available doctors are listed in 'Book Appointment' after selecting department.",
        
        # Reports
        "report": "Go to the 'Reports' tab to upload, view or download medical files.",
        "upload": "You can upload reports under the 'Reports' section.",
        "download": "To download a report, open the file from 'Reports' and click download.",
        "file": "All uploaded files are shown under the 'Reports' tab.",
        
        # Prescriptions
        "prescription": "Your prescriptions are located in the 'Prescriptions' tab.",
        "medication": "Medication details like dosage are shown in the 'Prescriptions' section.",
        "medicine": "Check your medicines in the 'Prescriptions' tab.",
        "dose": "Dosage instructions are included with your prescriptions.",
        
        # Profile
        "profile": "You can update your information in the 'Profile & Settings' tab.",
        "edit": "Use the 'Profile & Settings' tab to edit your details.",
        "settings": "Go to 'Profile & Settings' to manage your account details.",
        "email": "Your registered email is shown in the profile section.",
        "dob": "DOB can be updated from 'Profile & Settings'.",
        
        # Navigation
        "where": "All major sections are accessible from the sidebar.",
        "how": "Please select the feature you need from the sidebar to continue.",
        "menu": "Use the sidebar to explore features like Reports, Appointments, etc.",
        
        # Departments
        "department": "We offer Cardiology, Dermatology, Neurology, Pediatrics, and more.",
        "cardiology": "Book an appointment under Cardiology via the 'Book Appointment' tab.",
        "neurology": "Neurology services are available in the 'Book Appointment' tab.",
        "pediatrics": "You can consult a pediatrician using the 'Book Appointment' section.",
        "dermatology": "Dermatology appointments can be booked under 'Book Appointment'.",

        # Support
        "support": "Need help? Contact us at support@ehrhospital.com.",
        "help": "For assistance, email us or explore the sidebar options.",
        "contact": "Reach out to us via support@ehrhospital.com for help.",
        "emergency": "In an emergency, dial 108 or visit the nearest hospital.",
        
        # General
        "tips": "Stay hydrated, follow your treatment, and take rest as advised.",
        "routine": "Routine check-ups can be booked under 'Book Appointment'.",
        "checkup": "Book routine or specialist check-ups from the 'Book Appointment' section.",
        "logout": "You can logout by ending your session or using the top-right menu.",
        "error": "If you're facing an issue, please refresh or contact support.",
        "slow": "Performance depends on your internet. Try refreshing the page.",
        "insurance": "Insurance integration is not supported yet.",
        "vaccine": "Vaccination details are not part of this portal currently.",
        "history": "Check your appointment and report history in their respective tabs.",
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
