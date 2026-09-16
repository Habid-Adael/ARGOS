import json
import os


MEMORY_FILE = "memory/memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):

        save_memory({})

        return {}

    try:

        with open(MEMORY_FILE, "r", encoding="utf-8") as file:

            return json.load(file)

    except:

        return {}


def save_memory(memory):

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:

        json.dump(memory, file, indent=4)


def remember(key, value):

    memory = load_memory()

    memory[key.lower()] = value

    save_memory(memory)


def recall(key):

    memory = load_memory()

    return memory.get(key.lower())


def forget(key):

    memory = load_memory()

    if key.lower() in memory:

        del memory[key.lower()]

        save_memory(memory)