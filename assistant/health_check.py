import os
import ollama


def run_health_check():

    print("\n=================================================")
    print("A.R.G.O.S.")
    print("Autonomous Reasoning and General Operating System")
    print("Version: 1.0")
    print("=================================================")
    print("")
    print("Initializing...")
    # Memory
    if os.path.exists("memory/memory.json"):
        print("✓ Memory")
    else:
        print("✗ Memory")

    # Piper
    if os.path.exists("piper/piper.exe"):
        print("✓ Speech Engine")
    else:
        print("✗ Speech Engine")

    # Voice
    voice = "piper/voices/en_US-ryan-high.onnx"

    if os.path.exists(voice):
        print("✓ Voice")
    else:
        print("✗ Voice")

    # Ollama
    try:

        ollama.list()

        print("✓ AI Assistant")

    except Exception:

        print("✗ AI Assistant")

    print("========================\n")