import streamlit as st
import requests
from dotenv import load_dotenv
import os
import json

st.set_page_config(page_title="Chatbot", page_icon=":robot_face:")

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL ="llama-3.3-70b-versatile"




st.title("chatbot")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a helpful assistant."}]

user_input = st.text_input("You",key="user_input")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    with st.spinner("Generating response..."):
        headers = {
        "Authorization": f"Bearer { GROQ_API_KEY }",
        "Content-Type": "application/json"  }
        payload={
        "model": MODEL,
        "messages": st.session_state["messages"],}
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
        else:
            reply = f"Error: {response.status_code} \n {response.text}"

        st.session_state["messages"].append({"role": "assistant", "content": reply})

st.markdown("conversation")
for msg in st.session_state["messages"][1:]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")



