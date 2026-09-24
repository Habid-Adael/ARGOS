import json
import os

NAME = "memory"

DESCRIPTION = """
Remember facts.
Recall saved information.
Forget saved information.
"""

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory_data.json")


def _load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_memory(data):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving memory: {e}")


def remember(key, value):
    data = _load_memory()
    data[key.lower()] = value
    _save_memory(data)


def recall(key):
    data = _load_memory()
    return data.get(key.lower(), None)


def forget(key):
    data = _load_memory()
    if key.lower() in data:
        del data[key.lower()]
        _save_memory(data)


def run(command=None, *args, **kwargs):
    lower = command.lower() if command else ""

    if lower.startswith("remember that"):
        text = command[13:].strip() if command else ""
        if " is " in text:
            key, value = text.split(" is ", 1)
            remember(key.strip(), value.strip())
            return f"I'll remember that {key} is {value}."

    if lower.startswith("what is"):
        key = command[7:].strip() if command else ""
        value = recall(key) if key else None
        if value:
            return f"{key} is {value}."
        return f"I don't know what {key} is."

    if lower.startswith("forget"):
        key = command[6:].strip() if command else ""
        forget(key) if key else None
        return f"I forgot {key}."

    return None