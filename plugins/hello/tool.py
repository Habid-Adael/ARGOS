NAME = "hello"

DESCRIPTION = "Example plugin"

VERSION = "1.0.0"

COMMANDS = [
    "hello",
    "hi",
    "test"
]


def execute(command, context=None):

    return "Hello from the plugin!"