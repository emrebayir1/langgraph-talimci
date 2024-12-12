import streamlit as st
from compiler import  process_question
import time

st.set_page_config(page_title="Talimci", page_icon="🦉")
st.title("🦉 Talimci")
st.text(
    """
    Hello there! My name is Talimci, your AI-powered course finder. Whatever you're looking to learn, I’ve got a list of top online courses ready for you. Just tell me your interests, and I’ll handle the rest!
    
    May the course be with you!
    """
)

# User input container
with st.container():
    user_query = st.text_input("user_input", key="user_input", placeholder="What would you like to learn?", label_visibility="hidden")

# response container
with st.container():
    if user_query:
        with st.spinner("Running..."):
            result = process_question(user_query)

        def generate_stream(response):
            for word in response.split(" "):
                yield word + " "
                time.sleep(0.05)

        with st.chat_message("assistant", avatar="🦉"):
            st.write_stream(generate_stream(result))