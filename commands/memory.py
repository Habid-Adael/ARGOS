from memory.memory import remember, recall, forget


def handle_memory(command):
    command = command.strip()

    # Remember
    if command.lower().startswith("remember that"):

        text = command[13:].strip()

        if " is " in text:
            key, value = text.split(" is ", 1)

            remember(key.strip(), value.strip())

            return f"I'll remember that {key.strip()} is {value.strip()}."

    # Recall
    if command.lower().startswith("what is"):

        key = command[7:].strip()

        value = recall(key)

        if value:
            return f"{key} is {value}."

        return f"I don't know what {key} is."

    # Forget
    if command.lower().startswith("forget"):

        key = command[7:].strip()

        forget(key)

        return f"I forgot {key}."

    return None