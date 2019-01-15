from plugin_framework.plugin_manager import PluginManager
import sys
from PySide2 import QtWidgets
from gui.main_window import MainWindow
                                                    
if __name__ == "__main__":
    pm = PluginManager()
    pm.install("plugins")
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow(None, pm)
    main_window.show()
    sys.exit(app.exec_())