import webbrowser

NAME = "web"

DESCRIPTION = """
Search the internet.
Open websites.
Look up information online.
"""


def run(command):

    lower = command.lower()

    if lower.startswith("search "):

        query = command[7:]

        webbrowser.open(
            "https://www.google.com/search?q=" + query
        )

        return f"Searching for {query}."

    if lower.startswith("open website "):

        website = command[13:].strip()

        if not website.startswith("http"):

            website = "https://" + website

        webbrowser.open(website)

        return "Opening website."

    return None