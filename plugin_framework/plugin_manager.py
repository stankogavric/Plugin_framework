import os
import json
import importlib
import inspect
class PluginManager:
    def __init__(self):
        self._plugins = list()
    
    def install(self, path):
        for root, dirs, files in os.walk(path):
            for d in dirs:
                d_path = os.path.join(path, d)
                spec_path = os.path.join(d_path, "spec.json")
                plugin_path = os.path.join(d_path, "plugin").replace(os.path.sep,".")
                if os.path.exists(spec_path):
                    with open(spec_path, "r") as fp:
                        specification = json.load(fp)
                        plugin_module = importlib.import_module(plugin_path)
                        found = False
                        for member in inspect.getmembers(plugin_module):
                            if member[0] == "Main":
                                inst = plugin_module.Main(specification)
                                print(inst)
                                found = True
                        if not found:
                            raise ValueError("Main class not found!")
            break # ne ulazimo u podfoldere
    
    def uninstall(self, symoblic_name):
        return False

    def enable(self, symoblic_name):
        for plugin in self._plugins:
            if (plugin.symbolic_name == symoblic_name) and (plugin.enabled is False):
                plugin.enabled = True
                plugin.activate()
                return True
        return False

    def disable(self, symoblic_name):
        for plugin in self._plugins:
            if plugin.symbolic_name == symoblic_name and plugin.enabled is True:
                plugin.enabled = False
                return True
        return False