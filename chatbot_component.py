import streamlit as st
import openai

openai.api_key = st.secrets["openai"]["api_key"]

def handle_faq(prompt):
    prompt = prompt.lower()
    if "book" in prompt and "appointment" in prompt:
        return "To book an appointment, go to the 'Book Appointment' tab in the sidebar."
    elif "my appointments" in prompt:
        return "To view your appointments, click on the 'Appointments' tab."
    elif "report" in prompt:
        return "You can upload or view reports under the 'Reports' tab."
    elif "department" in prompt:
        return "We offer departments like Cardiology, Neurology, Pediatrics, etc."
    elif "support" in prompt:
        return "Please contact our support team at support@ehrhospital.com."
    return None

def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Sorry, something went wrong: {e}"

def render_chatbot_popup():
    st.markdown("""
        <style>
            .chatbot-button {
                position: fixed;
                bottom: 25px;
                right: 30px;
                z-index: 9999;
            }
            .chatbot-box {
                position: fixed;
                bottom: 90px;
                right: 30px;
                width: 320px;
                background: rgba(30,30,30,0.95);
                padding: 15px;
                border-radius: 15px;
                color: white;
                z-index: 9998;
                box-shadow: 0 0 10px rgba(0,0,0,0.5);
            }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns([7, 1, 1])
        with col3:
            if st.button("💬", key="toggle_chat_button"):
                st.session_state.show_chat = not st.session_state.get("show_chat", False)

    if st.session_state.get("show_chat", False):
        with st.container():
            st.markdown("<div class='chatbot-box'>", unsafe_allow_html=True)
            st.markdown("#### 🤖 EHR Assistant")

            user_input = st.text_input("Ask something...", key="chat_input")
            if user_input:
                reply = handle_faq(user_input) or ask_openai(user_input)
                st.markdown(f"**You:** {user_input}")
                st.markdown(f"**Bot:** {reply}")

            st.markdown("</div>", unsafe_allow_html=True)

def update_toggle_state():
    if "show_chat" not in st.session_state:
        st.session_state.show_chat = False

