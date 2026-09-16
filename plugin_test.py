from core.plugin_manager import PluginManager

pm = PluginManager()

pm.load_all()

plugin = pm.plugins["hello"]["module"]

response = plugin.execute("Testing plugins!")

print(response)