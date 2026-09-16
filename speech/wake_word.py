import os
import sys

import openwakeword
from openwakeword.model import Model

import sounddevice as sd
import numpy as np

model = None


def resource_path(relative_path):
    """
    Returns the correct path whether running from Python
    or from a PyInstaller executable.
    """
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


def load_wake_word():
    global model

    print("Loading ARGOS wake word model...")

    # Download OpenWakeWord base models if needed
    openwakeword.utils.download_models()

    model_path = resource_path(
        os.path.join(
            "training",
            "output",
            "argos",
            "argos.onnx"
        )
    )

    print(f"Using wake word model:\n{model_path}")

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Wake word model not found:\n{model_path}"
        )

    model = Model(
        wakeword_models=[model_path],
        inference_framework="onnx"
    )

    print("ARGOS wake word model loaded successfully.")


def wait_for_wake_word():
    global model

    if model is None:
        load_wake_word()

    print("Waiting for ARGOS...")

    detected = False

    audio_buffer = np.zeros(16000, dtype=np.int16)

    def callback(indata, frames, time, status):
        nonlocal detected, audio_buffer

        if status:
            print(status)

        new_audio = np.frombuffer(indata, dtype=np.int16)

        audio_buffer = np.concatenate(
            (
                audio_buffer[len(new_audio):],
                new_audio
            )
        )

        prediction = model.predict(audio_buffer)

        score = float(prediction.get("argos", 0))

        print(f"ARGOS score: {score:.3f}")

        if score >= 0.10:
            print("Wake word detected!")
            detected = True

    with sd.InputStream(
        samplerate=16000,
        channels=1,
        dtype="int16",
        blocksize=1280,
        callback=callback
    ):
        while not detected:
            sd.sleep(100)