import os
import time
import wave
import sounddevice as sd


# -----------------------------
# Settings
# -----------------------------

SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 2

POSITIVE_COUNT = 100
NEGATIVE_COUNT = 100


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_DIR = os.path.join(
    BASE_DIR,
    "..",
    "wakeword"
)

POSITIVE_DIR = os.path.join(
    DATASET_DIR,
    "positive"
)

NEGATIVE_DIR = os.path.join(
    DATASET_DIR,
    "negative"
)


os.makedirs(
    POSITIVE_DIR,
    exist_ok=True
)

os.makedirs(
    NEGATIVE_DIR,
    exist_ok=True
)


# -----------------------------
# Recorder
# -----------------------------

def record_audio(path):

    print("\nRecording...")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16"
    )

    sd.wait()

    with wave.open(path, "wb") as file:

        file.setnchannels(CHANNELS)
        file.setsampwidth(2)
        file.setframerate(SAMPLE_RATE)

        file.writeframes(
            audio.tobytes()
        )


    print("Saved:", path)



# -----------------------------
# Countdown
# -----------------------------

def countdown():

    for i in range(3, 0, -1):

        print(i)

        time.sleep(1)



# -----------------------------
# Collect samples
# -----------------------------

def collect_samples(folder, amount, prefix, instruction):

    for i in range(1, amount + 1):

        print("\n========================")
        print(f"Sample {i}/{amount}")
        print("========================")

        print(instruction)

        input("Press ENTER when ready...")

        countdown()

        filename = os.path.join(
            folder,
            f"{prefix}_{i:03}.wav"
        )

        record_audio(filename)

        time.sleep(0.5)



# -----------------------------
# Main
# -----------------------------

print("""
========================================
A.R.G.O.S.
Wake Word Dataset Recorder
========================================
""")


choice = input(
    """
Choose:

1 - Record positive samples (Hey Argos)
2 - Record negative samples
3 - Record both

Selection: """
)


if choice in ["1", "3"]:

    collect_samples(
        POSITIVE_DIR,
        POSITIVE_COUNT,
        "argos",
        """
Say:

ARGOS

Try different voices, speeds,
and distances.
"""
    )


if choice in ["2", "3"]:

    collect_samples(
        NEGATIVE_DIR,
        NEGATIVE_COUNT,
        "negative",
        """
Say anything EXCEPT:

ARGOS

Examples:
hello
open calculator
random sentences
silence
"""
    )


print("""

========================================
Recording Complete

Dataset location:

wakeword/

========================================
""")