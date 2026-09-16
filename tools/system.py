NAME = "system"

DESCRIPTION = """
Shutdown.
Restart.
Sleep.
Lock the computer.
"""


def run(command):

    lower = command.lower()

    if "shutdown" in lower:
        return "CONFIRM_SHUTDOWN"

    if "restart" in lower:
        return "CONFIRM_RESTART"

    return None