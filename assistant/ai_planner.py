import ollama

MODEL = "qwen3:4b"


SYSTEM_PROMPT = """
You are Jarvis's planning module.

Never answer the user's question.

Your only job is to produce a numbered plan.

Example:

User:
Create a folder called Test and create a file notes.txt inside it.

Output:

1. Create folder "Test"
2. Create file "notes.txt"

Only output the plan.
"""


def create_ai_plan(command):

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

            ]

        )

        return response["message"]["content"]

    except:

        return None 