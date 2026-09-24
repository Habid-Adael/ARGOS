import os
import ast

SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skills"))

def create_skill(skill_name: str, code: str) -> str:
    """Creates or updates a Python skill file in the skills directory."""
    if not os.path.exists(SKILLS_DIR):
        os.makedirs(SKILLS_DIR)

    # Sanitize skill name
    clean_name = skill_name.lower().replace(" ", "_").replace(".py", "")
    filepath = os.path.join(SKILLS_DIR, f"{clean_name}.py")

    # Syntax validation before saving
    try:
        ast.parse(code)
    except SyntaxError as e:
        return f"Syntax Error in generated code: {e}"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    return f"Skill '{clean_name}' successfully written to {filepath}."


def read_skill(skill_name: str) -> str:
    """Reads the source code of an existing skill."""
    clean_name = skill_name.lower().replace(" ", "_").replace(".py", "")
    filepath = os.path.join(SKILLS_DIR, f"{clean_name}.py")

    if not os.path.exists(filepath):
        return f"Skill '{clean_name}' does not exist."

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def list_skills() -> list:
    """Lists all available custom skills."""
    if not os.path.exists(SKILLS_DIR):
        return []
    return [f.replace(".py", "") for f in os.listdir(SKILLS_DIR) if f.endswith(".py")]