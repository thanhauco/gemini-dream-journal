import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("Dream History")
    for i, entry in enumerate(st.session_state.history):
        st.write(f"Dream {i+1}: {entry['dream'][:20]}...")


# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("GEMINI_API_KEY not found in environment variables.")

st.title("Gemini Dream Journal 🌙")

style = st.selectbox("Interpretation Style", ["Psychological", "Spiritual", "Creative", "Freudian", "Jungian"])

st.write("Record your dreams and let AI interpret them.")

col1, col2 = st.columns([2, 1])
with col1:
    dream_input = st.text_area("Describe your dream:", height=150)
with col2:
    st.write("### Tips")
    st.write("- Be specific about colors and emotions.")
    st.write("- Mention recurring symbols.")


if st.button("Interpret"):
    if not api_key:
        st.warning("Please configure your API key.")
    else:
        
        with st.spinner("Interpreting your dream..."):
            response = model.generate_content(f"Interpret this dream using a {style} perspective: {dream_input}")
            st.write(response.text)
            st.session_state.history.append({"dream": dream_input, "interpretation": response.text})


