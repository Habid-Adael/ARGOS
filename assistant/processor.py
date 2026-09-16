from ai.brain import ask
from ai.tool_loader import get_tools
from ai.tool_selector import choose_tool

from assistant.fast_router import fast_route
from assistant.planner import create_plan
from assistant.memory_manager import handle_automatic_memory
from assistant.confirmations import request

from assistant.context import get_last_app


def process(command):

    print("Processor started")

    # ----------------------------------
    # Conversation Context
    # ----------------------------------

    last_app = get_last_app()

    if last_app:

        replacements = [
            "it",
            "that",
            "that app",
            "the app"
        ]

        lower = command.lower()

        for word in replacements:

            lower = lower.replace(word, last_app)

        command = lower

    # ----------------------------------
    # Automatic Memory
    # ----------------------------------

    memory_response = handle_automatic_memory(command)

    print("After automatic memory")

    if memory_response:
        return memory_response

    # ----------------------------------
    # Load tools
    # ----------------------------------

    print("Loading tools")

    tools = get_tools()

    print("Available tools:", list(tools.keys()))

    # ----------------------------------
    # Planner
    # ----------------------------------

    print("Creating plan")

    plan = create_plan(command)

    if len(plan) > 1:

        print("Executing plan")

        results = []

        for step in plan:

            tool_name = step.get("tool")
            tool_command = step.get("command")

            if tool_name not in tools:
                print("Planner requested unknown tool:", tool_name)
                continue

            tool = tools[tool_name]

            print("Planner tool:", tool_name)

            result = tool.run(tool_command)

            if result == "CONFIRM_SHUTDOWN":
                request("shutdown")
                return "Are you sure you want to shut down the computer?"

            if result == "CONFIRM_RESTART":
                request("restart")
                return "Are you sure you want to restart the computer?"

            if result:
                results.append(result)

        if results:
            return "\n".join(results)

    # ----------------------------------
    # Fast Router
    # ----------------------------------

    tool_name = fast_route(command)

    print("Fast Router:", tool_name)

    # ----------------------------------
    # AI Tool Selector
    # ----------------------------------

    if tool_name is None:

        tool_name = choose_tool(command)

        print("AI Selector:", tool_name)

    # ----------------------------------
    # Execute Tool
    # ----------------------------------

    if tool_name in tools:

        tool = tools[tool_name]

        print("Executing:", tool_name)

        result = tool.run(command)

        print("Tool returned:", result)

        if result == "CONFIRM_SHUTDOWN":
            request("shutdown")
            return "Are you sure you want to shut down the computer?"

        if result == "CONFIRM_RESTART":
            request("restart")
            return "Are you sure you want to restart the computer?"

        if result:
            return result

    # ----------------------------------
    # AI
    # ----------------------------------

    print("Calling Ollama")

    return ask(command)