from memory.memory import remember, recall, forget

NAME = "memory"

DESCRIPTION = """
Remember facts.
Recall saved information.
Forget saved information.
"""


def run(command):

    lower = command.lower()

    if lower.startswith("remember that"):

        text = command[13:].strip()

        if " is " in text:

            key, value = text.split(" is ", 1)

            remember(key.strip(), value.strip())

            return f"I'll remember that {key} is {value}."

    if lower.startswith("what is"):

        key = command[7:].strip()

        value = recall(key)

        if value:

            return f"{key} is {value}."

        return f"I don't know what {key} is."

    if lower.startswith("forget"):

        key = command[7:].strip()

        forget(key)

        return f"I forgot {key}."

    return None