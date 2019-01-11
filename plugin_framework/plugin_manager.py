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
                                self._plugins.append(inst)
                        if not found:
                            raise ValueError("Main class not found!")
            break # ne ulazimo u podfoldere
    
    def uninstall(self, symoblic_name):
        # TODO:
        return False

    def enable(self, symoblic_name):
        for plugin in self._plugins:
            if (plugin.symbolic_name == symoblic_name) and (plugin.enabled is False):
                plugin.enabled = True
                plugin.activate()
                return True
        return False

    def disable(self, symbolic_name):
        for plugin in self._plugins:
            if plugin.symbolic_name == symbolic_name and plugin.enabled is True:
                plugin.enabled = False
                return True
        return False

    @property
    def enabled_plugins(self):
        enabled = []
        for plugin in self._plugins:
            if plugin.enabled:
                enabled.append(plugin)
        return enabled

    @property
    def disabled_plugins(self):
        return list(filter(lambda x: x.enabled, self._plugins))

    @property
    def plugins(self):
        return self._plugins

    def get_by_symbolic_name(self, symbolic_name):
        """
        :raises: IndexError - u slucaju kada nije pronadjen ni jedan plugin sa datim simbolickim imenom.
        """
        return list(filter(lambda x: x.symbolic_name == symbolic_name, self._plugins))[0]