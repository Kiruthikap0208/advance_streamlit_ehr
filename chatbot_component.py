import streamlit as st

def render_chatbot():
    # Improved FAQ response mapping
    faq_responses = {
        "book appointment": "To book an appointment, go to the 'Book Appointment' section in the sidebar.",
        "reschedule": "Currently, rescheduling isn't supported. Please cancel and rebook.",
        "appointments": "To view your appointments, click on the 'Appointments' tab.",
        "reports": "Click on 'Reports' in the sidebar to see your medical reports.",
        "profile": "Go to 'Profile & Settings' to update your information.",
        "departments": "We offer Cardiology, Neurology, Pediatrics, Dermatology and more.",
        "dermatology": "Please use the 'Book Appointment' tab and select Dermatology from the department list.",
        "upload report": "Use the 'Reports' tab and click on Upload.",
        "support": "Support is available via email at support@ehrhospital.com.",
        "emergency": "Please dial 108 or visit the nearest emergency ward.",
        "contact": "You can reach us via support@ehrhospital.com"
    }

    def get_response(user_input):
        user_input = user_input.lower()
        for keyword, response in faq_responses.items():
            if keyword in user_input:
                return response
        return "🤖 I'm sorry, I couldn't understand that. Please try asking differently."

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
