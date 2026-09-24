import ollama

MODEL = "qwen2.5:3b"

def ask(prompt, callback_texto=None):
    response_text = ""

    stream = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are A.R.G.O.S. (Autonomous Reasoning and General Operating System).
You have self-extension capabilities.

When asked to learn, create, or modify a capability/skill:
1. Generate valid Python code.
2. ALWAYS include a entry-point function named `run()` in the code.
3. Keep the code isolated and self-contained.
4. Use the `create_skill` tool to save it.

Rules:
- Respond strictly in ENGLISH.
- Keep output concise and direct.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True,
        options={
            "temperature": 0.6,
            "num_predict": 100
        }
    )

    print("ARGOS: ", end="", flush=True)

    buffer_frase = ""
    for chunk in stream:
        texto = chunk["message"]["content"]
        print(texto, end="", flush=True)
        response_text += texto
        buffer_frase += texto

        # Send sentence to TTS as soon as punctuation is detected
        if any(p in texto for p in [".", "\n", "!", "?"]):
            if callback_texto and buffer_frase.strip():
                callback_texto(buffer_frase.strip())
                buffer_frase = ""

    print()
    if callback_texto and buffer_frase.strip():
        callback_texto(buffer_frase.strip())

    return response_text