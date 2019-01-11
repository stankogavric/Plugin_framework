class Plugin:
    def __init__(self, metadata):
        self._metadata = metadata
    
    @property
    def name(self):
        return self._metadata.get("name", "")
    
    @property
    def description(self):
        return self._metadata.get("description", "")

    @property
    def symbolic_name(self):
        return self._metadata.get("symbolic_name", "")
    
    @property
    def app_version(self):
        return self._metadata.get("app_version", "")

    @property
    def version(self):
        return self._metadata.get("version", "")

    @property
    def category(self):
        return self._metadata.get("category", "")
    
    @property
    def enabled(self):
        return self._metadata.get("enabled", True)

    @enabled.setter
    def enabled(self, value):
        if isinstance(value, bool):
            self._metadata["enabled"] = value

    def activate(self):
        print("Plugin {} activated!".format(self.symbolic_name))

    def __str__(self):
        return "Plugin: {}, version: {}.".format(self.name, self.version)

    def get_widget(self, parent=None):
        raise NotImplementedError("Ovo mora biti implementirano u konkretnom plugin-u!")