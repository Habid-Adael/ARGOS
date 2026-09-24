import sys
import threading
from assistant.status import set_status
from assistant.context import clear
from speech.wake_word import load_wake_word, wait_for_wake_word
from speech.listen import listen
from speech.speak import speak
from assistant.health_check import run_health_check
from assistant.processor import process
from assistant.confirmations import check_confirmation
from ai.tool_loader import get_tools
from gui.window import start_gui


def assistant_loop():
    # -------------------------
    # Startup
    # -------------------------
    print("Loading tools...")
    get_tools()
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

    set_status("IDLE")

    # ---------------------------------------------------------
    # AUTO-RUN CHECK AFTER RESTART
    # ---------------------------------------------------------
    if "--auto-run" in sys.argv:
        try:
            idx = sys.argv.index("--auto-run")
            if idx + 1 < len(sys.argv):
                pending_command = sys.argv[idx + 1]

                # Cleanup command-line arguments
                sys.argv.remove("--auto-run")
                sys.argv.remove(pending_command)

                print(f"\n[A.R.G.O.S.] Executing pending action after restart: '{pending_command}'")
                speak("System updated. Executing command now.")

                set_status("THINKING")
                response = process(pending_command)

                set_status("SPEAKING")
                print("ARGOS:", response)
                speak(response)
                set_status("IDLE")
        except Exception as e:
            print(f"Error executing auto-run command: {e}")
    # ---------------------------------------------------------

    print("Awaiting activation...")

    # -------------------------
    # Main loop
    # -------------------------
    while True:
        set_status("IDLE")
        wait_for_wake_word()

        set_status("LISTENING")
        speak("Yes?")

        # Listen for command
        original_prompt = listen()

        if not original_prompt:
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