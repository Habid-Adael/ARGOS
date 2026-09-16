from ai.tool_loader import load_tools

TOOLS = load_tools()


def execute_plan(plan):

    results = []

    for step in plan:

        for tool in TOOLS:

            if tool.__name__.endswith(step["tool"]):

                result = tool.run(step["command"])

                if result:

                    results.append(result)

                break

    return results