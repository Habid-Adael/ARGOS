import ollama
from ai.tool_loader import get_tools

MODEL = "qwen2.5:1.5b"


def choose_tool(command):
    tools = get_tools()
    descriptions = ""

    for name, tool in tools.items():
        desc = getattr(tool, "DESCRIPTION", getattr(tool, "description", "No description."))

        descriptions += f"""
Tool name: {name}

Description:
{desc}
"""

    prompt = f"""
You are Jarvis's tool selector.

Choose the correct tool for the user's command.

Available tools:

{descriptions}

User command:
{command}

Rules:
- Reply with ONLY the tool name.
- Do not explain.
- If no tool is needed, reply with "none".
"""

    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0,
                "num_predict": 5
            }
        )

        answer = response["message"]["content"].strip().lower()

        if answer in tools:
            return answer

        return "none"

    except Exception as e:
        print("Tool selector error:", e)
        return "none"