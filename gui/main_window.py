from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Univerzitet Singidunum")
        self.setWindowIcon(QIcon("resources/icons/bug.png"))
        self.resize(800, 600)

        self.action_dict = {
            "open": QtWidgets.QAction(QIcon("resources/icons/folder-open-document.png"), "&Open document..."),
            "undo": QtWidgets.QAction(QIcon("resources/icons/arrow-curve-180-left.png"), "&Undo")
        }

        self.menu_bar = QtWidgets.QMenuBar(self)
        self.tool_bar = QtWidgets.QToolBar("Toolbar", self)
        self.text_edit = QtWidgets.QTextEdit(self)
        self.file_menu = QtWidgets.QMenu("&File", self.menu_bar)
        self.edit_menu = QtWidgets.QMenu("&Edit", self.menu_bar)
        self.view_menu = QtWidgets.QMenu("&View", self.menu_bar)
        self.help_menu = QtWidgets.QMenu("&Help", self.menu_bar)

        self._bind_actions()
        self._bind_shortcuts()
        self._populate_toolbar()
        self._populate_menu_bar()

        self.setCentralWidget(self.text_edit)
        self.addToolBar(self.tool_bar)
        self.setMenuBar(self.menu_bar)

    def _bind_actions(self):
        self.action_dict["open"].triggered.connect(self._on_open_file)
        self.action_dict["undo"].triggered.connect(self.text_edit.undo)


    def _bind_shortcuts(self):
        self.action_dict["open"].setShortcut("Ctrl+O")
        # self.action_dict["undo"].setShortcut("Ctrl+Z")
    
    def _populate_toolbar(self):
        self.tool_bar.addAction(self.action_dict["open"])
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.action_dict["undo"])

    def _populate_menu_bar(self):
        self.file_menu.addAction(self.action_dict["open"])
        self.view_menu.addAction(self.tool_bar.toggleViewAction())
        self.edit_menu.addAction(self.action_dict["undo"])

        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.edit_menu)
        self.menu_bar.addMenu(self.view_menu)
        self.menu_bar.addMenu(self.help_menu)

    def _on_open_file(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Open Python script", ".", "Python Files (*.py)")
        with open(file_name[0], "r") as fp:
            self.text_edit.setText(fp.read())


