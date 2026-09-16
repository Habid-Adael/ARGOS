from ai.tool_loader import load_tools

TOOLS = {}

for tool in load_tools():
    TOOLS[tool.NAME] = tool


def get(name):
    return TOOLS.get(name)


def descriptions():
    text = ""

    for tool in TOOLS.values():
        text += f"""
Tool: {tool.NAME}
{tool.DESCRIPTION}

"""

    return text

