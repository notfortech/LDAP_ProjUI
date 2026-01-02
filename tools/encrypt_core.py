from cryptography.fernet import Fernet
import os

KEY = os.environ["CIF_CORE_KEY"].encode()
fernet = Fernet(KEY)

files = [
    "core/signals.json",
    "core/skills.json",
    "core/skill_narratives.json",
    "core/validation_registry.json"
]

for path in files:
    with open(path, "rb") as f:
        encrypted = fernet.encrypt(f.read())
    with open(path + ".enc", "wb") as f:
        f.write(encrypted)
