# from plugin_framework.plugin_manager import PluginManager

# if __name__ == "__main__":
#     pm = PluginManager()
#     pm.install("plugins")
import sys
from PySide2 import QtWidgets

from gui.main_window import MainWindow
                                                    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())