import os

from tool_factory.templates import (
    MANIFEST_TEMPLATE,
    TOOL_TEMPLATE,
    README_TEMPLATE,
    TEST_TEMPLATE,
)


class PluginGenerator:

    def __init__(self):

        self.root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.plugins_folder = os.path.join(
            self.root,
            "plugins"
        )

    def create_plugin(self, name, description="Generated plugin"):

        plugin_folder = os.path.join(
            self.plugins_folder,
            name
        )

        if os.path.exists(plugin_folder):

            raise Exception("Plugin already exists.")

        os.makedirs(plugin_folder)

        files = {

            "manifest.json":
                MANIFEST_TEMPLATE.format(
                    name=name,
                    description=description
                ),

            "tool.py":
                TOOL_TEMPLATE.format(
                    name=name,
                    description=description
                ),

            "README.md":
                README_TEMPLATE.format(
                    name=name,
                    description=description
                ),

            "tests.py":
                TEST_TEMPLATE

        }

        for filename, content in files.items():

            with open(
                os.path.join(plugin_folder, filename),
                "w",
                encoding="utf-8"
            ) as f:

                f.write(content)

        return plugin_folder