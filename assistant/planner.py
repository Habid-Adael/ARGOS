import json
import ollama

MODEL = "qwen3:4b"


SYSTEM_PROMPT = """
You are Jarvis's planning module.

Your ONLY job is to split COMPLEX requests into multiple executable steps.

Return ONLY valid JSON.

Example:

[
    {
        "tool": "files",
        "command": "create folder Homework"
    },
    {
        "tool": "files",
        "command": "create file notes.txt"
    }
]

If the request only needs ONE action,
return:

[]
"""


def needs_planner(command):

    lower = command.lower()

    keywords = [
        " and ",
        " then ",
        " after ",
        " before ",
        "also",
        "next",
        "finally",
        "while"
    ]

    return any(word in lower for word in keywords)


def create_plan(command):

    print("Planner started")

    # ----------------------------
    # Skip planner for simple commands
    # ----------------------------

    if not needs_planner(command):

        print("Planner skipped")

        return []

    # ----------------------------
    # AI planner
    # ----------------------------

    try:

        response = ollama.chat(

            model=MODEL,

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",
                    "content": command
                }

            ],

            options={
                "temperature": 0
            }

        )

        plan = json.loads(
            response["message"]["content"]
        )

        print("Planner finished")

        return plan

    except Exception as e:

        print("Planner error:", e)

        return []