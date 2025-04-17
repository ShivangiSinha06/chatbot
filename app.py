import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import random

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Bruh, set your GOOGLE_API_KEY in the .env file ASAP!")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def spill_the_answers(question, convo_history):
    response = model.generate_content(
        [{"role": "user", "parts": [question]}],
        stream=True
    )
    return response

if 'convo_history' not in st.session_state:
    st.session_state['convo_history'] = []

spinner_messages = [
    "Thinking hard...",
    "Brain loading...",
    "Processing the vibes...",
    "Decoding your thoughts...",
    "Consulting the universe...",
    "Warming up the circuits...",
    "Brewing up an answer...",
    "Crunching the data...",
    "Summoning the knowledge...",
    "Getting my think on...",
    "Pea-brain processing...",
    "My neurons are doing their thing...",
]

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
)

st.markdown("<h1 style='color:#6A5ACD; font-family: sans-serif;'>✨ Your AI Bestie ✨</h1>", unsafe_allow_html=True)

st.subheader("The Receipts")
for role, text in st.session_state.convo_history:
    with st.chat_message(role):
        st.markdown(f"**{role.capitalize()}:** {text}")

if user_input := st.chat_input("Sup👀"):
    with st.chat_message("user", avatar="😎"):
        st.markdown(f"**You:** {user_input}")

    with st.spinner(random.choice(spinner_messages)):
        response_stream = spill_the_answers(user_input, st.session_state.convo_history)
        ai_response = ""
        for chunk in response_stream:
            ai_response += chunk.text if chunk.text else ""

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(f"**Bot:** {ai_response}")

    st.session_state.convo_history.append(("user", user_input))
    st.session_state.convo_history.append(("assistant", ai_response))