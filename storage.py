import json
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
        json.dump(dreams, f, indent=4, ensure_ascii=False)
