import speech_recognition as sr

recognizer = sr.Recognizer()

# Adjust these values for better detection
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8


def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")

            # Short calibration
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        print("Processing...")

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print("You:", text)
        return text.lower()

    except sr.WaitTimeoutError:
        print("No speech detected.")
        return ""

    except sr.UnknownValueError:
        print("I couldn't understand you.")
        return ""

    except sr.RequestError:
        print("Google speech service unavailable.")
        return ""

    except Exception as e:
        print("Microphone error:", e)
        return ""
    