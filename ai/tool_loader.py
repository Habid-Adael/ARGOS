import os
import sys
import importlib.util

TOOLS = {}

IGNORED_TOOLS = [
    "record_wakeword",
]


def get_tools_folder():

    if getattr(sys, "frozen", False):

        exe_dir = os.path.dirname(sys.executable)

        internal = os.path.join(exe_dir, "_internal", "tools")
        if os.path.isdir(internal):
            return internal

        normal = os.path.join(exe_dir, "tools")
        if os.path.isdir(normal):
            return normal

        if hasattr(sys, "_MEIPASS"):
            meipass = os.path.join(sys._MEIPASS, "tools")
            if os.path.isdir(meipass):
                return meipass

    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "tools",
    )


def load_module(module_name, path):

    unique_name = f"argos_tool_{module_name}"

    spec = importlib.util.spec_from_file_location(
        unique_name,
        path
    )

    if spec is None:
        raise ImportError(f"Cannot create spec for {module_name}")

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module


def load_tools():

    global TOOLS
    TOOLS = {}

    folder = get_tools_folder()

    print("Loading tools from:", folder)

    if not os.path.isdir(folder):
        raise FileNotFoundError(folder)

    for file in os.listdir(folder):

        if not file.endswith(".py"):
            continue

        if file == "__init__.py":
            continue

        module_name = file[:-3]

        if module_name in IGNORED_TOOLS:
            continue

        path = os.path.join(folder, file)

        try:

            module = load_module(module_name, path)

            name = getattr(module, "NAME", module_name)

            TOOLS[name] = {

                "name": name,

                "description": getattr(
                    module,
                    "DESCRIPTION",
                    "No description."
                ),

                "examples": getattr(
                    module,
                    "EXAMPLES",
                    []
                ),

                "version": getattr(
                    module,
                    "VERSION",
                    "1.0"
                ),

                "author": getattr(
                    module,
                    "AUTHOR",
                    "Unknown"
                ),

                "module": module,

            }

            print(f"Loaded: {name}")

        except Exception as e:

            print(f"Failed to load {module_name}: {e}")

    return TOOLS


def reload_tools():
    return load_tools()


def get_tools():

    if not TOOLS:
        load_tools()

    return TOOLS


def get_tool(name):

    return get_tools().get(name)


def get_tool_module(name):

    tool = get_tool(name)

    if tool is None:
        return None

    return tool["module"]