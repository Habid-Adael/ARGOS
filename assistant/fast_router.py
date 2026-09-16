def fast_route(command):

    command = command.lower()

    # -------- FILES --------

    if "create a folder" in command:
        return "files"

    if "create a file" in command:
        return "files"

    if "delete file" in command:
        return "files"

    if "delete folder" in command:
        return "files"

    if "rename file" in command:
        return "files"

    # -------- SYSTEM --------

    if "shutdown" in command:
        return "system"

    if "restart" in command:
        return "system"

    if "sleep" in command:
        return "system"

    if "lock computer" in command:
        return "system"

    # -------- APPS --------

    if command.startswith("open "):
        return "apps"

    if command.startswith("close "):
        return "apps"

    # -------- CALCULATOR --------

    if "calculate" in command:
        return "calculator"

    if "+" in command:
        return "calculator"

    if "-" in command:
        return "calculator"

    if "*" in command:
        return "calculator"

    if "/" in command:
        return "calculator"

    if "%" in command:
        return "calculator"

    return None