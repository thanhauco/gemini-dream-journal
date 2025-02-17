import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("GEMINI_API_KEY not found in environment variables.")

st.title("Gemini Dream Journal 🌙")
st.write("Record your dreams and let AI interpret them.")

dream_input = st.text_area("Describe your dream:", height=150)

if st.button("Interpret"):
    if not api_key:
        st.warning("Please configure your API key.")
    else:
        
        with st.spinner("Interpreting your dream..."):
            response = model.generate_content(f"Interpret this dream: {dream_input}")
            st.write(response.text)

