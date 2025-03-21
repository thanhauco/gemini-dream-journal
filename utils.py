import google.generativeai as genai
import os

def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')
    return None

def interpret_dream(model, dream, style):
    return model.generate_content(f"Interpret this dream using a {style} perspective: {dream}").text

def generate_visual_prompt(model, dream):
    return model.generate_content(f"Create a stable diffusion prompt to visualize this dream: {dream}").text
