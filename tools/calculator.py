NAME = "calculator"

DESCRIPTION = """
Use this tool for:
- math
- calculations
- addition
- subtraction
- multiplication
- division
- percentages
"""


def run(command):

    lower = command.lower()

    if not any(word in lower for word in [
        "calculate",
        "what is",
        "+",
        "-",
        "*",
        "/",
        "%"
    ]):
        return None

    try:

        expression = lower

        for word in [
            "calculate",
            "what is",
            "=",
            "?"
        ]:
            expression = expression.replace(word, "")

        result = eval(expression)

        return f"The answer is {result}."

    except:

        return None