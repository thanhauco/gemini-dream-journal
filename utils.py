import google.generativeai as genai
import os

def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')
    return None

def interpret_dream(model, dream, style):
    try:
        return model.generate_content(f"You are a wise dream interpreter. Analyze this dream deeply using a {style} perspective: {dream}").text
    except Exception as e:
        return f"Error: {str(e)}"


def generate_visual_prompt(model, dream):
    try:
        return model.generate_content(f"Create a stable diffusion prompt to visualize this dream: {dream}").text
    except Exception as e:
        return f"Error: {str(e)}"


def analyze_sentiment(model, dream):
    try:
        return model.generate_content(f"Analyze the sentiment of this dream (Positive, Negative, or Neutral) and provide a brief explanation: {dream}").text
    except Exception as e:
        return f"Error: {str(e)}"

def extract_keywords(model, dream):
    try:
        return model.generate_content(f"Extract 3-5 main keywords or tags from this dream, comma-separated: {dream}").text
    except Exception as e:
        return f"Error: {str(e)}"
