from memory.memory import remember, recall


def handle_automatic_memory(command):

    lower = command.lower().strip()


    # -----------------------------
    # Recall memory FIRST
    # -----------------------------

    recall_words = [
        "what is my",
        "what's my",
        "tell me my",
        "do you know my",
        "remember my"
    ]


    if any(word in lower for word in recall_words):

        try:

            if "what is my" in lower:
                key = lower.split("what is my", 1)[1]

            elif "what's my" in lower:
                key = lower.split("what's my", 1)[1]

            elif "tell me my" in lower:
                key = lower.split("tell me my", 1)[1]

            elif "do you know my" in lower:
                key = lower.split("do you know my", 1)[1]

            else:
                key = lower.split("remember my", 1)[1]


            key = key.replace("?", "").strip()


            value = recall(key)


            if value:
                return f"Your {key} is {value}."


            return f"I don't remember your {key}."


        except:
            return None



    # -----------------------------
    # Save memory SECOND
    # -----------------------------

    if "my " in lower and " is " in lower:

        try:

            key = lower.split("my ", 1)[1].split(" is ", 1)[0]

            value = command.split(" is ", 1)[1]


            remember(
                key.strip(),
                value.strip()
            )


            return (
                f"I will remember that your "
                f"{key.strip()} is {value.strip()}."
            )


        except:
            pass


    return None