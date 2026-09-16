import os

NAME = "files"

DESCRIPTION = """
Create files.
Delete files.
Create folders.
Delete folders.
Rename files.
Move files.
"""


def run(command):

    print("Files tool received:", command)

    lower = command.lower()

    if "create a folder called" in lower:

        name = command.lower().split(
            "create a folder called",
            1
        )[1].strip()

        os.makedirs(name, exist_ok=True)

        return f"Folder {name} created."

    if "create a file called" in lower:

        name = command.lower().split(
            "create a file called",
            1
        )[1].strip()

        if "." not in name:
            name += ".txt"

        with open(name, "w") as file:
            pass

        return f"File {name} created."

    return None