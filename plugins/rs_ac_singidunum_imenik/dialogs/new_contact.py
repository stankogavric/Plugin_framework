from PySide2 import QtWidgets

class NewContact(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(400, 350)
        self.setWindowTitle("Kreiraj novi kontakt")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.name_input = QtWidgets.QLineEdit(self)
        self.surname_input = QtWidgets.QLineEdit(self)
        self.birthday = QtWidgets.QDateEdit(self)
        self.email = QtWidgets.QLineEdit(self)

        self.name_input.setPlaceholderText("Ime")
        self.birthday.setCalendarPopup(True)

        self.form_layout.addRow("Ime:", self.name_input)
        self.form_layout.addRow("Prezime:", self.surname_input)
        self.form_layout.addRow("Datum rodjenja:", self.birthday)
        self.form_layout.addRow("Email:", self.email)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)
        self.setLayout(self.vbox_layout)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

    def _populate_form(self):
        pass

    def _on_accept(self):
        print(self.name_input.text())
        print(self.surname_input.text())
        print(self.birthday.text())
        print(self.email.text())
        self.accept()
