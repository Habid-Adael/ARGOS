import re

NAME = "calculator"

DESCRIPTION = """
Use this tool for math calculations (addition, subtraction, multiplication, division, percentages).
"""

def run(command):
    lower = command.lower()

    if not any(word in lower for word in ["calculate", "what is", "+", "-", "*", "/", "%"]):
        return None

    # Extraer únicamente números y operadores
    expr = re.sub(r'[^0-9\+\-\*\/\%\.\(\)]', '', lower)

    if not expr:
        return None

    try:
        result = eval(expr)
        return f"The answer is {result}."
    except Exception:
        return None