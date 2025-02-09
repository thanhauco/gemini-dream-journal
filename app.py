import streamlit as st

st.title("Gemini Dream Journal 🌙")
st.write("Record your dreams and let AI interpret them.")

dream_input = st.text_area("Describe your dream:", height=150)

if st.button("Interpret"):
    st.info("Interpretation feature coming soon!")
