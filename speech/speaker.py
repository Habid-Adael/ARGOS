from threading import Thread

from speech.speak import speak


def speak_async(text):

    Thread(
        target=speak,
        args=(text,),
        daemon=True
    ).start()