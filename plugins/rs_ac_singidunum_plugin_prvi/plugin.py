from plugin_framework.plugin import Plugin

class Main(Plugin):
    def __init__(self, metadata):
        super().__init__(metadata)

    def activate(self):
        self.do_something()

    def do_something(self):
        print("Hello world!")