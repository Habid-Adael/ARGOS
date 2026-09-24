import webrowser

def run(user_input):
    try:
        webrowser.open("https://open.spotify.com")
        return "Spotify has been opened in your web browser."
    except Exception as e:
        return f"An error occurred while trying to open Spotify: {e}"