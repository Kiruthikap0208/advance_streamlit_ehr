import streamlit as st
import openai

# Load OpenAI API Key
openai.api_key = st.secrets["openai"]["openai_api_key"]

# FAQ handler
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

# OpenAI fallback
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

# Render Chatbot as Popup UI
def render_chatbot_popup():
    # Chatbot Toggle
    st.markdown("""
        <style>
            .chatbot-toggle {
                position: fixed;
                bottom: 25px;
                right: 30px;
                z-index: 1001;
                background-color: #FF4B4B;
                color: white;
                border-radius: 50%;
                width: 55px;
                height: 55px;
                font-size: 28px;
                text-align: center;
                line-height: 55px;
                cursor: pointer;
                box-shadow: 0px 0px 12px rgba(0,0,0,0.3);
            }
        </style>
        <div class='chatbot-toggle' onclick="window.dispatchEvent(new Event('toggle-chatbot'))">💬</div>
        <script>
            const streamlitEvents = window.streamlitEvents || {};
            window.streamlitEvents = streamlitEvents;

            let visible = false;
            window.addEventListener("toggle-chatbot", function() {
                visible = !visible;
                Streamlit.setComponentValue(visible);
            });
        </script>
    """, unsafe_allow_html=True)

    # Use Streamlit component value to toggle visibility
    visible = st.session_state.get("show_chat", False)

    # Show chatbot
    if visible:
        st.markdown("""
            <div style='position: fixed; bottom: 90px; right: 30px; width: 320px;
                        background: rgba(30,30,30,0.95); padding: 15px; border-radius: 15px;
                        color: white; z-index: 9999; box-shadow: 0 0 10px rgba(0,0,0,0.5);'>
                <h4>🤖 EHR Assistant</h4>
        """, unsafe_allow_html=True)

        user_input = st.text_input("Ask something...", key="popup_chat")
        if user_input:
            response = handle_faq(user_input) or ask_openai(user_input)
            st.markdown(f"**You:** {user_input}")
            st.markdown(f"**Bot:** {response}")

        st.markdown("</div>", unsafe_allow_html=True)

# Update chatbot toggle state
def update_toggle_state():
    if "show_chat" not in st.session_state:
        st.session_state.show_chat = False

# Call this in your main patient dashboard
update_toggle_state()
render_chatbot_popup()
