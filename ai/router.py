from ai.tool_loader import load_tools


TOOLS = load_tools()


def route(command):

    for name, tool in TOOLS.items():

        result = tool.run(command)

        if result:

            return result


    return None


def get_tool_descriptions():

    descriptions = ""

    for name, tool in TOOLS.items():

        descriptions += f"""
Tool: {name}

{tool.DESCRIPTION}

"""

    return descriptions