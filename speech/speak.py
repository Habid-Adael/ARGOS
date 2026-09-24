import os
import re
import subprocess
import tempfile
import unicodedata
import winsound

# Base folder
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PIPER_EXE = os.path.join(BASE_DIR, "piper", "piper.exe")

VOICE = os.path.join(BASE_DIR, "piper", "voices", "en_US-ryan-high.onnx")


def clean_text(text):
    if text is None:
        return ""

    if not isinstance(text, str):
        text = str(text)

    # Normalize unicode
    text = unicodedata.normalize("NFKD", text)

    # Convert to ASCII
    text = text.encode("ascii", "ignore").decode()

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def speak(text):
    clean_output = clean_text(text)

    if not clean_output:
        clean_output = "Done."

    print(f"ARGOS: {clean_output}")

    if not os.path.exists(PIPER_EXE) or not os.path.exists(VOICE):
        print(f"[Piper Error] Missing executable or voice file at defined paths.")
        return

    wav_file = None
    try:
        # Create temp file and immediately close handle so Piper can write to it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wav_file = f.name

        subprocess.run(
            [PIPER_EXE, "-m", VOICE, "-f", wav_file],
            input=clean_output,
            text=True,
            encoding="utf-8",
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if os.path.exists(wav_file) and os.path.getsize(wav_file) > 0:
            winsound.PlaySound(wav_file, winsound.SND_FILENAME)

    except Exception:
        import traceback

        traceback.print_exc()

    finally:
        # Clean up audio file
        if wav_file and os.path.exists(wav_file):
            try:
                os.remove(wav_file)
            except Exception:
                pass