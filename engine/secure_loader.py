from cryptography.fernet import Fernet
import os
import json

def load_secure_json(path):
    key = os.environ["CIF_CORE_KEY"].encode()
    fernet = Fernet(key)

    with open(path, "rb") as f:
        decrypted = fernet.decrypt(f.read())

    return json.loads(decrypted)
