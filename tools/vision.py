import pyautogui
import ollama
import os
import tempfile


NAME = "vision"

DESCRIPTION = """
Analyze the computer screen.
Answer questions about what is visible.
Read text from the screen.
Describe images or interfaces.
"""


MODEL = "llava:7b"


def take_screenshot():

    path = os.path.join(
        tempfile.gettempdir(),
        "jarvis_screen.png"
    )

    image = pyautogui.screenshot()

    image.save(path)

    return path



def run(command):

    lower = command.lower()

    if not any(word in lower for word in [
        "screen",
        "see",
        "look",
        "display",
        "what is on"
    ]):
        return None


    image_path = take_screenshot()


    try:

        response = ollama.chat(

            model=MODEL,

            messages=[

                {
                    "role": "user",
                    "content": command,
                    "images": [
                        image_path
                    ]
                }

            ]

        )


        return response["message"]["content"]


    except Exception as e:

        return f"Vision error: {e}"
    