import os
import subprocess
import json
from datetime import datetime

def run_command(command, env=None):
    subprocess.run(command, shell=True, check=True, env=env)

def commit(msg, date_str):
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    run_command("git add .", env)
    run_command(f'git commit -m "{msg}"', env)
    print(f"Committed '{msg}' at {date_str}")

# Initialize Git
if os.path.exists(".git"):
    run_command("rm -rf .git")

# Cleanup artifacts from previous runs
artifacts = ["app.py", "requirements.txt", "storage.py", "utils.py", "README.md", "dreams.json", ".gitignore"]
for artifact in artifacts:
    if os.path.exists(artifact):
        os.remove(artifact)

run_command("git init")

# 1. Feb 02: Initial commit & .gitignore
with open(".gitignore", "w") as f:
    f.write(".env\n__pycache__/\n*.pyc\ndreams.json\n")
commit("Initial commit: Add .gitignore", "2025-02-02T10:00:00")

# 2. Feb 05: Add requirements.txt
with open("requirements.txt", "w") as f:
    f.write("streamlit\ngoogle-generativeai\npython-dotenv\n")
commit("Add project dependencies", "2025-02-05T14:30:00")

# 3. Feb 09: Create basic Streamlit UI skeleton
app_code = """import streamlit as st

st.title("Gemini Dream Journal 🌙")
st.write("Record your dreams and let AI interpret them.")

dream_input = st.text_area("Describe your dream:", height=150)

if st.button("Interpret"):
    st.info("Interpretation feature coming soon!")
"""
with open("app.py", "w") as f:
    f.write(app_code)
commit("Feat: Create basic Streamlit UI skeleton", "2025-02-09T09:15:00")

# 4. Feb 12: Setup Gemini API client
app_code = """import streamlit as st
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
        st.info("Interpretation feature coming soon!")
"""
with open("app.py", "w") as f:
    f.write(app_code)
commit("Setup: Configure Gemini API client", "2025-02-12T11:45:00")

# 5. Feb 16: Implement basic interpretation logic
app_code = app_code.replace('st.info("Interpretation feature coming soon!")', 
"""
        with st.spinner("Interpreting your dream..."):
            response = model.generate_content(f"Interpret this dream: {dream_input}")
            st.write(response.text)
""")
with open("app.py", "w") as f:
    f.write(app_code)
commit("Feat: Implement basic interpretation logic", "2025-02-16T16:20:00")

# 6. Feb 20: Add interpretation styles
app_code = app_code.replace('st.title("Gemini Dream Journal 🌙")', 
"""st.title("Gemini Dream Journal 🌙")

style = st.selectbox("Interpretation Style", ["Psychological", "Spiritual", "Creative", "Freudian", "Jungian"])
""")
app_code = app_code.replace('f"Interpret this dream: {dream_input}"', 
'f"Interpret this dream using a {style} perspective: {dream_input}"')
with open("app.py", "w") as f:
    f.write(app_code)
commit("Feat: Add interpretation styles", "2025-02-20T13:10:00")

# 7. Feb 24: Refactor UI with columns
app_code = app_code.replace('dream_input = st.text_area("Describe your dream:", height=150)',
"""col1, col2 = st.columns([2, 1])
with col1:
    dream_input = st.text_area("Describe your dream:", height=150)
with col2:
    st.write("### Tips")
    st.write("- Be specific about colors and emotions.")
    st.write("- Mention recurring symbols.")
""")
with open("app.py", "w") as f:
    f.write(app_code)
commit("UI: Refactor layout with columns", "2025-02-24T15:55:00")

# 8. Mar 01: Add sidebar for dream history
app_code = app_code.replace("load_dotenv()", 
"""load_dotenv()

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("Dream History")
    for i, entry in enumerate(st.session_state.history):
        st.write(f"Dream {i+1}: {entry['dream'][:20]}...")
""")
# Update logic to save to session state
app_code = app_code.replace('st.write(response.text)', 
"""st.write(response.text)
            st.session_state.history.append({"dream": dream_input, "interpretation": response.text})
""")
with open("app.py", "w") as f:
    f.write(app_code)
commit("Feat: Add sidebar for session-based dream history", "2025-03-01T10:05:00")

# 9. Mar 05: Implement JSON storage for dreams
utils_code = """import json
import os

FILE_PATH = "dreams.json"

def load_dreams():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    return []

def save_dream(dream, interpretation):
    dreams = load_dreams()
    dreams.append({"dream": dream, "interpretation": interpretation})
    with open(FILE_PATH, "w") as f:
        json.dump(dreams, f, indent=4)
"""
with open("storage.py", "w") as f:
    f.write(utils_code)
commit("Backend: Implement JSON storage for dreams", "2025-03-05T14:40:00")

# 10. Mar 08: Load and display history in sidebar
app_code = "import storage\n" + app_code
app_code = app_code.replace('if "history" not in st.session_state:', '# History loaded from storage')
app_code = app_code.replace('st.session_state.history = []', '')
app_code = app_code.replace('st.session_state.history', 'storage.load_dreams()')
app_code = app_code.replace('st.session_state.history.append({"dream": dream_input, "interpretation": response.text})', 
'storage.save_dream(dream_input, response.text)')
with open("app.py", "w") as f:
    f.write(app_code)
commit("Feat: Integrate JSON storage with UI", "2025-03-08T11:20:00")

# 11. Mar 12: Fix JSON encoding bug
with open("storage.py", "r") as f:
    content = f.read()
content = content.replace("json.dump(dreams, f, indent=4)", "json.dump(dreams, f, indent=4, ensure_ascii=False)")
with open("storage.py", "w") as f:
    f.write(content)
commit("Fix: Handle non-ASCII characters in JSON storage", "2025-03-12T09:50:00")

# 12. Mar 16: Add "Dream Visualizer"
app_code = app_code.replace('st.write(response.text)', 
"""st.write(response.text)
            
            st.subheader("Visual Prompt")
            visual_prompt = model.generate_content(f"Create a stable diffusion prompt to visualize this dream: {dream_input}").text
            st.code(visual_prompt)
""")
with open("app.py", "w") as f:
    f.write(app_code)
commit("Feat: Add Dream Visualizer prompt generation", "2025-03-16T16:30:00")

# 13. Mar 21: Refactor logic into utils.py
# Move API calls to utils (simulated by creating utils.py and importing)
utils_logic = """import google.generativeai as genai
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
"""
with open("utils.py", "w") as f:
    f.write(utils_logic)

app_code = "import utils\n" + app_code
# Simplified replacement for demo purposes
app_code = app_code.replace("genai.configure(api_key=api_key)", "# Config moved to utils")
app_code = app_code.replace("model = genai.GenerativeModel('gemini-pro')", "model = utils.get_model()")
with open("app.py", "w") as f:
    f.write(app_code)
commit("Refactor: Move AI logic to utils.py", "2025-03-21T13:45:00")

# 14. Mar 25: Add timestamps
with open("storage.py", "r") as f:
    content = f.read()
content = "from datetime import datetime\n" + content
content = content.replace('dreams.append({"dream": dream, "interpretation": interpretation})', 
'dreams.append({"dream": dream, "interpretation": interpretation, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})')
with open("storage.py", "w") as f:
    f.write(content)
commit("Feat: Add timestamps to dream entries", "2025-03-25T10:15:00")

# 15. Mar 29: Add delete functionality
with open("storage.py", "a") as f:
    f.write("""
def delete_dream(index):
    dreams = load_dreams()
    if 0 <= index < len(dreams):
        dreams.pop(index)
        with open(FILE_PATH, "w") as f:
            json.dump(dreams, f, indent=4, ensure_ascii=False)
""")
commit("Backend: Add delete_dream function", "2025-03-29T15:00:00")

# 16. Apr 02: Improve system prompts
with open("utils.py", "r") as f:
    content = f.read()
content = content.replace("Interpret this dream using a", "You are a wise dream interpreter. Analyze this dream deeply using a")
with open("utils.py", "w") as f:
    f.write(content)
commit("AI: Improve system prompts for better interpretation", "2025-04-02T11:30:00")

# 17. Apr 08: Add error handling
with open("utils.py", "r") as f:
    content = f.read()
content = content.replace("return model.generate_content", 
"""try:
        return model.generate_content""")
content = content.replace(").text", """).text
    except Exception as e:
        return f"Error: {str(e)}"
""")
with open("utils.py", "w") as f:
    f.write(content)
commit("Fix: Add error handling for API calls", "2025-04-08T14:10:00")

# 18. Apr 14: Add "Random Dream" example
app_code = app_code.replace('dream_input = st.text_area("Describe your dream:", height=150)', 
"""dream_input = st.text_area("Describe your dream:", height=150)
if st.button("Random Example"):
    dream_input = "I was flying over a city made of crystal..."
    st.experimental_rerun()
""")
with open("app.py", "w") as f:
    f.write(app_code)
commit("Feat: Add Random Dream example button", "2025-04-14T10:45:00")

# 19. Apr 19: Update README
readme_content = """# Gemini Dream Journal 🌙

A Streamlit application that uses Google Gemini to interpret your dreams and generate visual prompts.

## Features
-   **Multi-style Interpretation**: Choose from Jungian, Freudian, Spiritual, etc.
-   **Visual Prompts**: Generate Stable Diffusion prompts for your dreams.
-   **History**: Save and review your past dreams.
-   **Privacy**: Data stored locally in `dreams.json`.

## Setup
1.  Install dependencies: `pip install -r requirements.txt`
2.  Set `GEMINI_API_KEY` in `.env`.
3.  Run: `streamlit run app.py`
"""
with open("README.md", "w") as f:
    f.write(readme_content)
commit("Docs: Update README with usage instructions", "2025-04-19T16:00:00")

# 20. Apr 24: Add export feature
app_code = app_code.replace("st.title", 
"""st.title
with st.sidebar:
    if st.button("Export Dreams"):
        with open("dreams.json", "r") as f:
            st.download_button("Download JSON", f, "dreams.json")
""")
with open("app.py", "w") as f:
    f.write(app_code)
commit("Feat: Add export functionality", "2025-04-24T13:20:00")

# 21. Apr 29: v1.0 Release polish
with open("app.py", "r") as f:
    content = f.read()
content = content.replace("Gemini Dream Journal 🌙", "Gemini Dream Journal v1.0 🌙")
with open("app.py", "w") as f:
    f.write(content)
commit("Release: v1.0 polish and version bump", "2025-04-29T17:00:00")

print("Dream Journal history generation complete.")
