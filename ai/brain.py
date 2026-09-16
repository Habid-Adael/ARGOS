import ollama


MODEL = "qwen2.5:3b"


def ask(prompt):

    response_text = ""

    stream = ollama.chat(
        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": """
You are A.R.G.O.S.

A.R.G.O.S. stands for Autonomous Reasoning and General Operating System.

You are a local desktop AI assistant.
You are concise.
You execute commands safely.
You never use emojis.
You speak naturally.

Rules:
- Never use emojis.
- Keep answers short.
- Do not use unnecessary explanations.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        stream=True,

        options={
            "temperature": 0.7,
            "num_predict": 150
        }
    )


    print("Jarvis:", end=" ", flush=True)


    for chunk in stream:

        text = chunk["message"]["content"]

        print(text, end="", flush=True)

        response_text += text


    print()

    return response_text