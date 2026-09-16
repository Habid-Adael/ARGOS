from ai.brain import ask


SYSTEM_PROMPT = """
You are generating a Python module.

Rules:

- Return ONLY raw Python source code.
- NEVER use Markdown.
- NEVER use ```python
- NEVER use ```
- NEVER explain anything.
- The first line MUST begin with NAME =

Template:

NAME = ""

DESCRIPTION = ""

EXAMPLES = []

VERSION = "1.0"

AUTHOR = "ARGOS"

def run(command):
    return ""
"""


def clean_code(code: str) -> str:
    code = code.strip()

    if code.startswith("```python"):
        code = code[len("```python"):]

    if code.startswith("```"):
        code = code[3:]

    if code.endswith("```"):
        code = code[:-3]

    return code.strip()


def generate_tool(request):

    prompt = f"""
Create a Python tool.

Purpose:
{request}
"""

    response = ask(SYSTEM_PROMPT + "\n\n" + prompt)

    return clean_code(response)