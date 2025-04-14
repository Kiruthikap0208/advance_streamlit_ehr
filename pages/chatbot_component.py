import streamlit as st
import openai

# Load API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["openai_api_key"]

# Define prebuilt actions
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

# OpenAI assistant fallback
def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if you prefer
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Sorry, there was a problem reaching the assistant. ({str(e)})"

# Chatbot UI logic
def render_chatbot():
    with st.container():
        st.markdown("""
        <style>
            .chatbot-popup {
                position: fixed;
                bottom: 20px;
                right: 25px;
                width: 320px;
                background-color: rgba(0, 0, 0, 0.85);
                color: white;
                border-radius: 15px;
                padding: 15px;
                z-index: 9999;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
            }
            .chatbot-popup h4 {
                margin-top: 0;
                font-size: 18px;
                color: #fff;
            }
            .chatbot-input input {
                background: rgba(255,255,255,0.1);
                border: none;
                color: white;
                border-radius: 8px;
                padding: 8px;
                width: 100%;
                margin-top: 10px;
            }
        </style>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown("<div class='chatbot-popup'>", unsafe_allow_html=True)
            st.markdown("#### 🤖 EHR Assistant")
            
            user_input = st.text_input("Ask a question", key="chat_input")
            if user_input:
                faq_reply = handle_faq(user_input)
                response = faq_reply or ask_openai(user_input)
                st.markdown(f"**You:** {user_input}")
                st.markdown(f"**Bot:** {response}")

            st.markdown("</div>", unsafe_allow_html=True)
