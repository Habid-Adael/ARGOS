import os


pending_action = None


def request(action):

    global pending_action

    pending_action = action


def check_confirmation(text):

    global pending_action

    if not pending_action:
        return None


    answer = text.lower().strip()


    if answer in [
        "yes",
        "confirm",
        "do it",
        "yeah",
        "sure"
    ]:

        if pending_action == "shutdown":

            os.system("shutdown /s /t 5")

            pending_action = None

            return "Shutting down."


        if pending_action == "restart":

            os.system("shutdown /r /t 5")

            pending_action = None

            return "Restarting."


    else:

        pending_action = None

        return "Cancelled."


    return None