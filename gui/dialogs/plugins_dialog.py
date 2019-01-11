from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt

class PluginsDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Plugin settings")
        self.resize(600, 400)

        self.plugins_dialog_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout = QtWidgets.QHBoxLayout()

        self.set_plugin_button = QtWidgets.QPushButton(QIcon("resources/icons/application-plus.png"), "Set as central")
        self.uninstall_button = QtWidgets.QPushButton(QIcon("resources/icons/minus-circle.png"), "Uninstall", self)
        self.enable_button = QtWidgets.QPushButton(QIcon("resources/icons/tick.png"), "Enable", self)
        self.disable_button = QtWidgets.QPushButton(QIcon("resources/icons/exclamation-red.png"), "Disable", self)

        self.set_plugin_button.clicked.connect(self._on_set)
        self.enable_button.clicked.connect(self._on_enable_plugin)
        self.disable_button.clicked.connect(self._on_disable_plugin)


        self.buttons_layout.addWidget(self.set_plugin_button)
        self.buttons_layout.addWidget(self.uninstall_button)
        self.buttons_layout.addWidget(self.enable_button)
        self.buttons_layout.addWidget(self.disable_button)

        self.plugins_table = QtWidgets.QTableWidget(self)
        self.plugins_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.plugins_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self._populate_table()

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.on_accept)
        self.button_box.rejected.connect(self.on_reject)

        self.plugins_dialog_layout.addLayout(self.buttons_layout)
        self.plugins_dialog_layout.addWidget(self.plugins_table)
        self.plugins_dialog_layout.addWidget(self.button_box)

        self.setLayout(self.plugins_dialog_layout)

    def on_accept(self):
        # TODO:
        return self.accept()

    def on_reject(self):
        return self.reject()

    def _populate_table(self):
        self.plugins_table.setColumnCount(6)
        self.plugins_table.setRowCount(len(self.parent().plugin_manager.plugins))
        self.plugins_table.setHorizontalHeaderLabels(["Name", "Symbolic name", "Description", "Version", "Application version", "Enabled"])
        for i, plugin in enumerate(self.parent().plugin_manager.plugins):
            name = QtWidgets.QTableWidgetItem(plugin.name)
            name.setFlags(name.flags()^Qt.ItemIsEditable)
            symbolic_name = QtWidgets.QTableWidgetItem(plugin.symbolic_name)
            symbolic_name.setFlags(symbolic_name.flags()^Qt.ItemIsEditable)
            description = QtWidgets.QTableWidgetItem(plugin.description)
            description.setFlags(description.flags()^Qt.ItemIsEditable)
            version = QtWidgets.QTableWidgetItem(plugin.version)
            version.setFlags(version.flags()^Qt.ItemIsEditable)
            app_version = QtWidgets.QTableWidgetItem(plugin.app_version)
            app_version.setFlags(app_version.flags()^Qt.ItemIsEditable)
            enabled = QtWidgets.QTableWidgetItem(QIcon("resources/icons/tick.png") if plugin.enabled else QIcon("resources/icons/cross.png"), "")
            enabled.setFlags(enabled.flags()^Qt.ItemIsEditable)
            self.plugins_table.setItem(i, 0, name)
            self.plugins_table.setItem(i, 1, symbolic_name)
            self.plugins_table.setItem(i, 2, description)
            self.plugins_table.setItem(i, 3, version)
            self.plugins_table.setItem(i, 4, app_version)
            self.plugins_table.setItem(i, 5, enabled)
    
    def _on_set(self):
        """
        Metoda koja se poziva kada se pritisne na dugme set central.
        """
        selected_items = self.plugins_table.selectedItems()
        if len(selected_items) == 0:
            return
        # na drugoj poziciji se nalazi simbolicko ime plugina.
        symbolic_name = selected_items[1].text()
        self.parent().set_central_widget(symbolic_name)

    def _on_enable_plugin(self):
        selected = self.plugins_table.selectedItems()
        filtered_rows = list(map(lambda x: x.row(),filter(lambda x: self.plugins_table.column(x) == 1, selected)))
        filtered= list(map(lambda x: x.text(),filter(lambda x: self.plugins_table.column(x) == 1, selected)))
        for plugin in self.parent.plugin_manager.enabled_plugins:
            if plugin.symbolic_name in filtered:
                plugin.enabled = not plugin.enabled
        print(filtered_rows)
        for r in filtered_rows:
            self.plugins_table.setItem(r, 5, QtWidgets.QTableWidgetItem(QIcon("resources/icons/tick.png"), ""))

    def _on_disable_plugin(self):
        selected = self.plugins_table.selectedItems()
        filtered_rows = list(map(lambda x: x.row(),filter(lambda x: self.plugins_table.column(x) == 1, selected)))
        filtered = list(map(lambda x: x.text(),filter(lambda x: self.plugins_table.column(x) == 1, selected)))
        print(filtered_rows)
        for plugin in self.parent.plugin_manager.disabled_plugins:
            if plugin.symbolic_name in filtered:
                plugin.enabled = not plugin.enabled
        for r in filtered_rows:
            self.plugins_table.setItem(r, 5, QtWidgets.QTableWidgetItem(QIcon("resources/icons/cross.png"), ""))


        
