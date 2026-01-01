import json
import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

def load_json(relative_path):
    file_path = os.path.join(PROJECT_ROOT, relative_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
