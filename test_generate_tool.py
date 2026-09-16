from assistant.tool_generator import generate_tool
from assistant.tool_installer import install_tool

code = generate_tool(
    "A tool called hello_world that says Hello from ARGOS."
)

print(code)

install_tool(
    "hello_world",
    code
)

print("Installed.")