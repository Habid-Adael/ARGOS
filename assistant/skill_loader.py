import os
import importlib.util
import sys

SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skills"))

def run_skill(skill_name: str, function_name: str = "run", *args, **kwargs):
    """Dynamically loads and executes a skill function."""
    clean_name = skill_name.lower().replace(" ", "_").replace(".py", "")
    filepath = os.path.join(SKILLS_DIR, f"{clean_name}.py")

    if not os.path.exists(filepath):
        return f"Error: Skill '{clean_name}' was not found."

    try:
        # Dynamic import
        spec = importlib.util.spec_from_file_location(clean_name, filepath)
        module = importlib.util.module_from_spec(spec)
        sys.modules[clean_name] = module
        spec.loader.exec_module(module)

        # Execute target function
        if hasattr(module, function_name):
            func = getattr(module, function_name)
            return func(*args, **kwargs)
        else:
            return f"Error: Function '{function_name}' not found in {clean_name}.py"

    except Exception as e:
        return f"Runtime error executing skill '{clean_name}': {e}"