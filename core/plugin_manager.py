import os
import json
import importlib.util


class PluginManager:

    def __init__(self):

        self.root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.plugins_folder = os.path.join(
            self.root,
            "plugins"
        )

        self.registry_file = os.path.join(
            self.root,
            "registry",
            "plugins.json"
        )

        self.plugins = {}

        self.registry = self.load_registry()

    # ==========================================================
    # Registry
    # ==========================================================

    def load_registry(self):

        if not os.path.exists(self.registry_file):
            return {}

        with open(self.registry_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_registry(self):

        os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)

        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, indent=4)

    # ==========================================================
    # Discovery
    # ==========================================================

    def discover_plugins(self):

        self.plugins = {}

        if not os.path.exists(self.plugins_folder):
            return

        for folder in os.listdir(self.plugins_folder):

            plugin_path = os.path.join(
                self.plugins_folder,
                folder
            )

            if not os.path.isdir(plugin_path):
                continue

            manifest_path = os.path.join(
                plugin_path,
                "manifest.json"
            )

            tool_path = os.path.join(
                plugin_path,
                "tool.py"
            )

            if not os.path.exists(manifest_path):
                continue

            if not os.path.exists(tool_path):
                continue

            try:

                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)

            except Exception as e:

                print(f"[PLUGIN] Invalid manifest in {folder}")
                print(e)
                continue

            self.plugins[manifest["name"]] = {
                "manifest": manifest,
                "path": plugin_path,
                "tool": tool_path,
                "module": None
            }

    # ==========================================================
    # Loading
    # ==========================================================

    def load_plugin(self, name):

        if name not in self.plugins:
            return False

        plugin = self.plugins[name]

        spec = importlib.util.spec_from_file_location(
            name,
            plugin["tool"]
        )

        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        plugin["module"] = module

        return True

    def load_all(self):

        self.discover_plugins()

        for name in self.plugins:

            try:

                self.load_plugin(name)

                print(f"[PLUGIN] Loaded {name}")

            except Exception as e:

                print(f"[PLUGIN] Failed to load {name}")
                print(e)

    # ==========================================================
    # Lookup
    # ==========================================================

    def get_plugin(self, name):

        return self.plugins.get(name)

    def find_plugin(self, command):

        command = command.lower().strip()

        for plugin in self.plugins.values():

            module = plugin.get("module")

            if module is None:
                continue

            if not hasattr(module, "COMMANDS"):
                continue

            commands = [c.lower() for c in module.COMMANDS]

            if command in commands:
                return module

        return None

    # ==========================================================
    # Execution
    # ==========================================================

    def execute(self, command, context=None):

        plugin = self.find_plugin(command)

        if plugin is None:
            return None

        return plugin.execute(command, context)