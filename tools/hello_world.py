```python
NAME = "hello_world"

DESCRIPTION = "Greets the user with 'Hello' from ARGOS."

EXAMPLES = [
    "run('say_hello')",
]

VERSION = "1.0"

AUTHOR = "ARGOS"

def run(command):
    if command == 'say_hello':
        return "Hello from ARGOS"
    else:
        return f"Command {command} not recognized."
```