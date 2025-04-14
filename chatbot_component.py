import streamlit as st
from streamlit.components.v1 import html
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def ask_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, something went wrong: {e}"


def chatbot_ui():
    with st.container():
        # Floating chatbot button
        html("""
        <style>
        .chat-button {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background-color: #2b90d9;
            color: white;
            border: none;
            border-radius: 50px;
            padding: 12px 20px;
            font-weight: bold;
            cursor: pointer;
            z-index: 9999;
        }
        .chat-popup {
            position: fixed;
            bottom: 80px;
            right: 30px;
            background: white;
            border: 2px solid #ccc;
            border-radius: 10px;
            width: 300px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
            z-index: 9999;
            display: none;
        }
        .chat-header {
            background: #2b90d9;
            color: white;
            padding: 10px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            font-weight: bold;
        }
        </style>

        <script>
        function toggleChat() {
            var chat = document.getElementById("chatBox");
            if (chat.style.display === "none") {
                chat.style.display = "block";
            } else {
                chat.style.display = "none";
            }
        }
        </script>

        <div class="chat-popup" id="chatBox">
            <div class="chat-header">🤖 EHR Assistant</div>
            <iframe srcdoc='<body style="margin:0;">{{CHAT}}</body>' width="100%" height="350px" style="border:none;"></iframe>
        </div>
        <button class="chat-button" onclick="toggleChat()">💬 Chat</button>
        """, height=0)

        # Render actual Streamlit chatbot inside iframe
        with st.empty():
            with st.form("chat_form", clear_on_submit=True):
                st.markdown("**Hi! How can I help you today?**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    book = st.form_submit_button("📅 Book Appointment")
                with col2:
                    reports = st.form_submit_button("📄 View Reports")
                with col3:
                    help_ = st.form_submit_button("❓ Ask a Question")

                user_input = st.text_input("Type your query below", key="chat_input")
                submit = st.form_submit_button("Send")

            if book:
                st.write(ask_openai("I want to book an appointment"))
            elif reports:
                st.write(ask_openai("Show my medical reports"))
            elif help_:
                st.write(ask_openai("I have a question about my treatment"))
            elif submit and user_input:
                st.write(f"You: {user_input}")
                st.write(f"Bot: {ask_openai(user_input)}")
