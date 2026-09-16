import ast
import os

from ai.tool_loader import reload_tools

TOOLS_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "tools"
)


def install_tool(filename, code):

    # Syntax validation
    ast.parse(code)

    path = os.path.join(
        TOOLS_FOLDER,
        filename + ".py"
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

    reload_tools()

    return path