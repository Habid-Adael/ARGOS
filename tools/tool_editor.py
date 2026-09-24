import os
import sys

NAME = "tool_editor"
DESCRIPTION = "Edits, updates, or fixes existing tool files in the tools directory."

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))


def run(command=None, tool_name=None, new_code=None, *args, **kwargs):
    """
    Edits or updates an existing tool file.
    Accepts the target tool name and the replacement Python code.
    """
    if not tool_name or not new_code:
        return None

    # Ensure correct file extension
    if not tool_name.endswith(".py"):
        tool_name = f"{tool_name}.py"

    file_path = os.path.join(TOOLS_DIR, tool_name)

    # Verify target file exists
    if not os.path.exists(file_path):
        return f"Error: The tool '{tool_name}' does not exist and cannot be edited."

    try:
        # Overwrite file with new implementation
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_code)

        # Unload cached module to force fresh import
        module_name = tool_name.replace(".py", "")
        if module_name in sys.modules:
            del sys.modules[module_name]

        return f"Tool '{module_name}' successfully updated."

    except Exception as e:
        return f"Failed to edit tool '{tool_name}': {str(e)}"