import subprocess

from assistant.context import set_last_app


NAME = "apps"

DESCRIPTION = """
Open applications.
Close applications.
Launch installed programs.
"""


APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "cmd": "cmd.exe",
    "explorer": "explorer.exe",
}


def run(command):

    print("Apps tool started")

    lower = command.lower()

    # --------------------------
    # Open Apps
    # --------------------------

    for app, exe in APPS.items():

        print("Checking:", app)

        if f"open {app}" in lower:

            print("Matched:", app)

            try:

                subprocess.Popen(exe)

                set_last_app(app)

                print("Launch successful")

                return f"Opening {app}."

            except Exception as e:

                print("Launch error:", e)

                return str(e)

    # --------------------------
    # Close Apps
    # --------------------------

    for app, exe in APPS.items():

        if f"close {app}" in lower:

            process_name = exe.replace(".exe", "")

            try:

                subprocess.run(
                    ["taskkill", "/F", "/IM", exe],
                    capture_output=True,
                    text=True
                )

                return f"Closing {app}."

            except Exception as e:

                return str(e)

    print("No app matched")

    return None