import importlib.util
import os
import sys

TOOLS_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "tools")
)


def get_tools_folder():
    return TOOLS_FOLDER


def load_tools_from_folder(folder_path=None):
    if folder_path is None:
        folder_path = get_tools_folder()

    tools = {}
    print(f"Loading tools from: {folder_path}")

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".py") and not file_name.startswith("__"):
            module_name = file_name[:-3]
            file_path = os.path.join(folder_path, file_name)

            try:
                spec = importlib.util.spec_from_file_location(
                    module_name, file_path
                )
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                tools[module_name] = module
                print(f"Loaded: {module_name}")

            except Exception as e:
                print(
                    f"Failed to load {module_name}: {e}. Triggering auto-fix..."
                )
                try:
                    from tools import tool_editor

                    tool_editor.run(
                        command=f"Fix import failure: {e}",
                        tool_name=file_name,
                        error_msg=str(e),
                    )
                except Exception as editor_err:
                    print(f"Auto-fix failed to launch: {editor_err}")

    return tools


_tools_cache = None


def get_tools():
    global _tools_cache
    if _tools_cache is None:
        _tools_cache = load_tools_from_folder()
    return _tools_cache


def reload_tools():
    global _tools_cache
    _tools_cache = load_tools_from_folder()
    return _tools_cache


load_tools = get_tools