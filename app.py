import utils
import storage
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# History loaded from storage
    

with st.sidebar:
    st.header("Dream History")
    for i, entry in enumerate(storage.load_dreams()):
        st.write(f"Dream {i+1}: {entry['dream'][:20]}...")


# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    # Config moved to utils
    model = utils.get_model()
else:
    st.error("GEMINI_API_KEY not found in environment variables.")

st.title("Gemini Dream Journal 🌙")

style = st.selectbox("Interpretation Style", ["Psychological", "Spiritual", "Creative", "Freudian", "Jungian"])

st.write("Record your dreams and let AI interpret them.")

col1, col2 = st.columns([2, 1])
with col1:
    dream_input = st.text_area("Describe your dream:", height=150)
if st.button("Random Example"):
    dream_input = "I was flying over a city made of crystal..."
    st.experimental_rerun()

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
            
            st.subheader("Visual Prompt")
            visual_prompt = model.generate_content(f"Create a stable diffusion prompt to visualize this dream: {dream_input}").text
            st.code(visual_prompt)

            storage.load_dreams().append({"dream": dream_input, "interpretation": response.text})


