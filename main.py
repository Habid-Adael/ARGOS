from assistant.status import set_status
from assistant.context import clear

from speech.wake_word import load_wake_word, wait_for_wake_word
from speech.listen import listen
from speech.speak import speak

from assistant.health_check import run_health_check
from assistant.processor import process
from assistant.confirmations import check_confirmation

from ai.tool_loader import load_tools

from gui.window import start_gui

import threading


def assistant_loop():

    # -------------------------
    # Startup
    # -------------------------

    print("Loading tools...")
    load_tools()
    print("Tools loaded.")

    run_health_check()

    print("Loading ARGOS activation system...")
    load_wake_word()
    print("ARGOS activation ready.")

    print("========================================")
    print("A.R.G.O.S.")
    print("Autonomous Reasoning and General Operating System")
    print("========================================")
    print()
    print("System online.")
    print("Awaiting activation...")

    set_status("IDLE")

    # -------------------------
    # Main loop
    # -------------------------

    while True:

        # Wait for wake word
        set_status("IDLE")
        wait_for_wake_word()

        set_status("LISTENING")
        speak("Yes?")

        # Listen for command
        original_prompt = listen()

        if original_prompt == "":
            continue

        print("You:", original_prompt)

        command = original_prompt.strip()

        if command.lower() == "exit":
            speak("Goodbye.")
            break

        # Confirmation check
        confirmation = check_confirmation(command)

        if confirmation:
            print("ARGOS:", confirmation)
            speak(confirmation)
            continue

        # Process command
        set_status("THINKING")
        response = process(command)

        # Speak response
        set_status("SPEAKING")
        print("ARGOS:", response)
        speak(response)

        # Return to idle
        set_status("IDLE")


# -------------------------
# Start assistant in background
# -------------------------

assistant_thread = threading.Thread(
    target=assistant_loop,
    daemon=True
)

assistant_thread.start()


# -------------------------
# Start GUI in main thread
# -------------------------

start_gui()