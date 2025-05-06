from dotenv import load_dotenv
import os
import streamlit as st
from groq import Groq


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")



# Groq klientini yaratamiz
client = Groq(api_key=api_key)

# Sahifa sozlamalari
st.set_page_config(page_title="🧠 Groq Coding Copilot", page_icon="🤖", layout="wide")

# Title va tavsif
st.markdown("""
    <div style='text-align: center'>
        <h1>🤖 Groq Coding Copilot</h1>
        <p>Do you need help? I can help write code!</p>
    </div>
""", unsafe_allow_html=True)

# Chat tarixini saqlash
if "messages" not in st.session_state:
    st.session_state.messages = []

# Oldingi xabarlarni ko'rsatish
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Foydalanuvchi inputi
prompt = st.chat_input("Ask me anything related to coding!...")

# Model javobi
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Groq is replying..."):
            try:
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=st.session_state.messages,
                    temperature=0.7,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
            except Exception as e:
                st.error(f"Error: {e}")
                reply = "Sorry, I couldn't reply."

    st.session_state.messages.append({"role": "assistant", "content": reply})