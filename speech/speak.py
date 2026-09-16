import os
import re
import subprocess
import tempfile
import unicodedata
import winsound


# Base folder
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PIPER_EXE = os.path.join(
    BASE_DIR,
    "piper",
    "piper.exe"
)

VOICE = os.path.join(
    BASE_DIR,
    "piper",
    "voices",
    "en_US-ryan-high.onnx"
)


def clean_text(text):

    # Normalize unicode
    text = unicodedata.normalize("NFKD", text)

    # Convert to ASCII
    text = text.encode(
        "ascii",
        "ignore"
    ).decode()

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def speak(text):

    try:

        text = clean_text(text)

        if not text:
            return

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as f:

            wav_file = f.name

        subprocess.run(

            [
                PIPER_EXE,
                "-m",
                VOICE,
                "-f",
                wav_file
            ],

            input=text,

            text=True,

            check=True

        )

        winsound.PlaySound(
            wav_file,
            winsound.SND_FILENAME
        )

        os.remove(wav_file)

    except Exception:

        import traceback

        traceback.print_exc()