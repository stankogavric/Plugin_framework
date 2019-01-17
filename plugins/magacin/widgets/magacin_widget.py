from PySide2 import QtWidgets
from PySide2 import QtGui
from ..magacin_model import MagacinModel
from .dialogs.dialog import Dialog
from .hala_widget import HalaWidget

class MagacinWidget(QtWidgets.QWidget):
    """
    Klasa koja predstavlja glavni widget plugina za vodjenje magacina.
    """
    def __init__(self, parent=None):
        """
        Inicijalizator widgeta za vodjenje magacina.

        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.set_layout()

    def set_layout(self):
        """
        Postavlja layout ovom widget-u.
        """
        self.open_magacin = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/folder-open-document.png"), "Otvori magacin", self)
        self.save_magacin = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/disk.png"), "Snimi", self)
        self.add_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/plus.png"), "Dodaj halu", self)
        self.remove_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/minus.png"), "Obrisi halu", self)
        self.open_hala = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/folder-open-document.png"), "Otvori halu", self)
        self.add_proizvod_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/plus.png"), "Dodaj proizvod", self)
        self.add_new_proizvod_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/plus.png"), "Novi proizvod", self)
        self.hbox_layout.addWidget(self.open_magacin)
        self.hbox_layout.addWidget(self.save_magacin)
        self.hbox_layout.addWidget(self.add_button)
        self.hbox_layout.addWidget(self.remove_button)
        self.hbox_layout.addWidget(self.open_hala)
        self.hbox_layout.addWidget(self.add_proizvod_button)
        self.hbox_layout.addWidget(self.add_new_proizvod_button)
        self.table_view = QtWidgets.QTableView(self)

        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.open_magacin.clicked.connect(self._on_open)
        self.save_magacin.clicked.connect(self._on_save)
        self.add_button.clicked.connect(self._on_add)
        self.remove_button.clicked.connect(self._on_remove)
        self.open_hala.clicked.connect(self._on_open_hala)
        self.add_proizvod_button.clicked.connect(self._on_add_proizvod)
        self.add_new_proizvod_button.clicked.connect(self._on_add_new_proizvod)

        self.vbox_layout.addLayout(self.hbox_layout)
        self.vbox_layout.addWidget(self.table_view)

        self.setLayout(self.vbox_layout)

        self._open()

    def set_model(self, model):
        """
        Postavlja novi model na tabelarni prikaz.

        :param model: model koji se prikazuje u tabeli.
        :type model: MagacinModel
        """
        self.table_view.setModel(model)

    def _open(self):
        """
        Metoda koja se poziva prilikom pokretanja aplikacije.
        """
        self.set_model(MagacinModel("plugins/magacin/magacin.csv"))

    def _on_open(self):
        """
        Metoda koja se poziva na klik dugmeta open.
        """
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Open magacin file", ".", "CSV Files (*.csv)")
        self.set_model(MagacinModel(path[0]))

    def _on_save(self):
        """
        Metoda koja se poziva na klik dugmeta save.
        """
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save magacin file", ".", "CSV Files (*.csv)")
        self.table_view.model().save_data(path[0])

    def _on_open_hala(self):
        """
        Metoda koja se poziva na klik dugmeta Otvori halu.
        Otvara halu na zadatom indeksu.
        """
        name = self.table_view.model().open_hala(self.table_view.selectedIndexes())
        if(name == -1):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Nijedna hala nije izabrana!")
            message.setInformativeText("Izaberite jednu halu koju zelite da otvorite.")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
            return
        elif(name == 1):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Izabrano je vise od jedne hale!")
            message.setInformativeText("Izaberite samo jednu halu koju zelite da otvorite.")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
            return
        if(name is not None):
            self.unfill(self.vbox_layout)
            HalaWidget(name, self)

    def unfill(self, layout): 
        """
        Metoda koja uklanja sadrzaj layout-a.
        """
        def deleteItems(layout): 
            if layout is not None: 
                while layout.count(): 
                    item = layout.takeAt(0) 
                    widget = item.widget() 
                    if widget is not None: 
                        widget.deleteLater() 
                    else: 
                        deleteItems(item.layout()) 
        deleteItems(layout) 

    def _on_add(self):
        """
        Metoda koja se poziva na klik dugmeta add.
        Otvara dijalog sa formom za kreiranje nove hale u magacinu.
        """
        dialog = Dialog().getAddHalaDialog(self.parent())
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            ind = self.table_view.model().add(dialog.get_data())
            if(ind == -1):
                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Vec postoji hala s istim nazivom!")
                message.setInformativeText("Unesite drugi naziv hale.")
                message.setWindowTitle("Greska")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()
                self._on_add()
            elif(ind == 0):
                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Uspijesno dodavanje hale!")
                message.setWindowTitle("Obavjestenje")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()

    def _on_add_new_proizvod(self):
        """
        Metoda koja se poziva na klik dugmeta add_new_proizvod.
        Otvara dijalog sa formom za kreiranje novog proizvoda.
        """
        dialog = Dialog().getAddNewProizvodDialog(self.parent())
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            ind = self.table_view.model().add_new_proizvod(dialog.get_data())
            if(ind == -1):
                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Vec postoji proizvod s istim nazivom!")
                message.setInformativeText("Unesite drugi naziv proizvoda.")
                message.setWindowTitle("Greska")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()
                self._on_add_new_proizvod()
            elif(ind == 0):
                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Uspijesno dodavanje novog proizvoda!")
                message.setWindowTitle("Obavjestenje")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()

    def _on_remove(self):
        """
        Metoda koja se poziva na klik dugmeta remove.
        """
        ind = self.table_view.model().remove(self.table_view.selectedIndexes())
        if(ind == -1):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Nijedna hala nije izabrana!")
            message.setInformativeText("Izaberite bar jednu halu koju zelite da uklonite.")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
        elif(ind == 0):
                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Uspijesno uklanjanje!")
                message.setWindowTitle("Obavjestenje")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()

    def _on_add_proizvod(self):
        """
        Metoda koja se poziva na klik dugmeta add_proizvod.
        Otvara dijalog sa formom za dodavanje proizvoda u halu.
        """
        dialog = Dialog().getAddProizvodDialog(self.parent())
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            ind = self.table_view.model().add_proizvod(dialog.get_data())
            data = dialog.get_data()
            if(ind[0] == -1):
                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Nedovoljno mjesta u hali!")
                message.setInformativeText("Maksimalna kolicina koju je moguce dodati je: "+str(ind[1]))
                message.setWindowTitle("Greska")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()
                self._on_add_proizvod()
            elif(ind[0] == 1):
                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Neodgovarajuci tip hale!")
                tip = ""
                if((int)(data["proizvod"][1])>=-10 and (int)(data["proizvod"][1])<=0):
                    tip = "Zamrzavanje"
                elif((int)(data["proizvod"][1])>=1 and (int)(data["proizvod"][1])<=18):
                    tip = "Rashladna"
                else:
                    tip = "Sobna temperatura"
                message.setInformativeText("Izaberite tip hale: "+tip)
                message.setWindowTitle("Greska")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()
                self._on_add_proizvod()
            elif(ind[0] == 0):
                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Uspijesno dodavanje proizvoda!")
                message.setWindowTitle("Obavjestenje")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()