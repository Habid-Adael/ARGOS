import sounddevice as sd

print("Microphones found:")

print(sd.query_devices())


input("\nPress ENTER to record 3 seconds...")


print("Recording...")

audio = sd.rec(
    int(16000 * 3),
    samplerate=16000,
    channels=1,
    dtype="int16"
)

sd.wait()


print("Recording finished.")

print("Samples recorded:", len(audio))