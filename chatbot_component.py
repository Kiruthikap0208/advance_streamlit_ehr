import streamlit as st

def render_chatbot():
    # your existing chatbot UI and logic
    st.markdown("""
    <style>
    .chat-container {
        ...
    </style>
    """, unsafe_allow_html=True)

    # Rule-based chatbot logic
    faq_responses = {
        "book appointment": "To book an appointment, go to the 'Book Appointment' tab in the sidebar.",
        "appointments": "To view your upcoming and past appointments, check the 'Appointments' tab.",
        "reports": "Medical reports can be viewed or downloaded in the 'Reports' tab.",
        "prescriptions": "Check your medications and instructions in the 'Prescriptions' section.",
        "profile": "To edit your personal details, visit 'Profile & Settings'.",
        "support": "For help, please email our support at support@ehrhospital.com."
    }

    def match_faq(user_input):
        user_input = user_input.lower()
        for keyword, response in faq_responses.items():
            if keyword in user_input:
                return response
        return "I'm sorry, I couldn't understand that. Please try asking differently."

    # Modern chatbot box style
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

    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    st.markdown("**🤖 Bot:** Hi there! Welcome to SRM EHR Patient Portal. How may I assist you today?")

    user_choice = st.radio("Choose an option:", [
        "📅 View My Appointments",
        "📝 Book Appointment",
        "📂 View My Medical Reports",
        "☎️ Contact Support"
    ])

    if user_choice == "📅 View My Appointments":
        st.markdown("**🤖 Bot:** To view your appointments, go to the 'Appointments' tab in the sidebar.")

    elif user_choice == "📝 Book Appointment":
        department = st.selectbox("Select Department", ["General", "Cardiology", "Dermatology", "Orthopedics"])
        preferred_date = st.date_input("Choose a date")
        preferred_time = st.time_input("Choose a time")
        if st.button("Submit Booking Request"):
            st.success(f"✅ Your appointment request for {department} on {preferred_date} at {preferred_time} has been noted!")

    elif user_choice == "📂 View My Medical Reports":
        st.markdown("**🤖 Bot:** You can view your medical reports in the 'Reports' tab of the dashboard.")

    elif user_choice == "☎️ Contact Support":
        st.markdown("**🤖 Bot:** You can reach us at:")
        st.info("📧 support@srm-ehr.com\n📞 +91-9876543210")

    st.markdown("</div>", unsafe_allow_html=True)
