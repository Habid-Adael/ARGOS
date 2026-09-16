print(">>> LOADED NEW templates.py <<<")

MANIFEST_TEMPLATE = """
{{
    "name": "{name}",
    "version": "1.0.0",
    "description": "{description}",
    "author": "ARGOS",
    "entry": "tool.py"
}}
"""

TOOL_TEMPLATE = '''
NAME = "{name}"

DESCRIPTION = "{description}"

VERSION = "1.0.0"

COMMANDS = [
    "{name}"
]

def execute(command, context=None):
    return "Plugin '{name}' is working!"
'''

README_TEMPLATE = """
# {name}

Generated automatically by ARGOS.

Description:

{description}
"""

TEST_TEMPLATE = """
def test():
    print("Plugin test passed.")
"""