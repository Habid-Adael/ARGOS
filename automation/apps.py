import subprocess

def open_app(name):
    name = name.lower()

    if "chrome" in name:
        subprocess.Popen(
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )
        return "Opening Chrome."

    if "notepad" in name:
        subprocess.Popen("notepad")
        return "Opening Notepad."

    if "calculator" in name:
        subprocess.Popen("calc")
        return "Opening Calculator."

    return None