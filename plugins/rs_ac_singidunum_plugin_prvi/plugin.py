from plugin_framework.plugin import Plugin
from PySide2 import QtWidgets

class Main(Plugin):
    def __init__(self, metadata):
        super().__init__(metadata)

    def activate(self):
        self.do_something()

    def do_something(self):
        print("Hello world!")

    def get_widget(self, parent=None):
        return QtWidgets.QTreeWidget(), None, None