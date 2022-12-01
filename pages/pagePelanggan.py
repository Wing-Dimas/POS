from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from connect import *

class PagePelanggan(QGridLayout):
    def __init__(self):
        super().__init__()


        self.setVerticalSpacing(50)
        self.createTable()
        self.createInput()
        self.showData()

    def showData(self):
        self.data = query("SELECT * FROM pelanggan")
        if (len(self.data) > 16):
            self.table.setRowCount(len(self.data))
        self.table.clearContents()
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                newItem = QTableWidgetItem(str(self.data[i][j]))
                self.table.setItem(i,j , newItem)


    def createTable(self):
        self.table = QTableWidget(16, 3)
        self.headers = ["id", "Nama", "Alamat"]
        self.table.setHorizontalHeaderLabels(self.headers)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.Stretch)

        self.table.clicked.connect(self.select)

        self.addWidget(self.table, 1,0)

    def createInput(self):
        groupBox = QGroupBox("Form")
        self.inputLayout = QGridLayout()
        self.inputLayout.setVerticalSpacing(10)
        self.inputLayout.setHorizontalSpacing(5)
        self.btnLayout = QHBoxLayout()
        self.btnLayout.setSpacing(10)
        groupBox.setLayout(self.inputLayout)

        self.lblNama = QLabel("Nama")
        self.lblAlamat = QLabel("Alamat")

        self.inpNama = QLineEdit()
        self.inpAlamat = QLineEdit()

        self.btnTambah = QPushButton("Tambah")
        self.btnEdit = QPushButton("Edit")
        self.btnHapus = QPushButton("Hapus")
        self.btnCancel = QPushButton("Cancel")
        self.btnRefresh = QPushButton("Refresh")

        self.btnTambah.setFixedWidth(80)
        self.btnTambah.clicked.connect(self.tambah)
        self.btnEdit.setFixedWidth(80)
        self.btnEdit.clicked.connect(self.edit)
        self.btnHapus.setFixedWidth(80)
        self.btnHapus.clicked.connect(self.hapus)
        self.btnCancel.setFixedWidth(80)
        self.btnCancel.clicked.connect(self.cancel)
        self.btnRefresh.setFixedWidth(80)
        self.btnRefresh.clicked.connect(self.refresh)

        self.inputLayout.addWidget(self.lblNama, 0, 0)
        self.inputLayout.addWidget(self.lblAlamat, 1, 0)

        self.inputLayout.addWidget(self.inpNama, 0, 1)
        self.inputLayout.addWidget(self.inpAlamat, 1, 1)

        self.inputLayout.addLayout(self.btnLayout, 3, 0, 1, 2) 

        self.btnLayout.addWidget(self.btnTambah)
        self.btnLayout.addWidget(self.btnEdit)
        self.btnLayout.addWidget(self.btnHapus)
        self.btnLayout.addWidget(self.btnCancel)
        self.btnLayout.addWidget(self.btnRefresh)
        self.btnLayout.addStretch()

        self.switchButton()

        self.addWidget(groupBox, 0, 0)

    def tambah(self):
        nama = self.inpNama.text()
        alamat = self.inpAlamat.text()
        
        statement(f"INSERT INTO `pelanggan` (`id_pelanggan`, `nama_pelanggan`, `alamat`) VALUES (NULL, '{nama}', '{alamat}');")
        self.showData()
   
    def select(self):
        row = sorted(set(index.row() for index in self.table.selectedIndexes()))[0]
        try:
            data = self.data[row]
            self.id = data[0]
            self.inpNama.setText(data[1])
            self.inpAlamat.setText(str(data[2]))
            self.switchButton(False)
        except:
            self.clearInput()
            self.switchButton()

    def edit(self):
        nama = self.inpNama.text()
        alamat= self.inpAlamat.text()
        
        statement(f"UPDATE `pelanggan` SET `nama_pelanggan` = '{nama}', `alamat` = '{alamat}' WHERE `pelanggan`.`id_pelanggan` = {self.id};")
        self.showData()
        self.clearInput()
        self.switchButton()

    def hapus(self):
        statement(f"DELETE FROM `pelanggan` WHERE `pelanggan`.`id_pelanggan` = {self.id}")
        self.showData()
        self.clearInput()
        self.switchButton()

    def cancel(self):
        self.id = None
        self.clearInput()
        self.switchButton()

    def switchButton(self, activeTambah=True):
        if activeTambah:
            self.btnTambah.setDisabled(False)
            self.btnEdit.setDisabled(True)
            self.btnHapus.setDisabled(True)
            self.btnCancel.setDisabled(True)
        else:
            self.btnTambah.setDisabled(True)
            self.btnEdit.setDisabled(False)
            self.btnHapus.setDisabled(False)
            self.btnCancel.setDisabled(False)

    def clearInput(self):
        self.inpNama.setText("")
        self.inpAlamat.setText("")
    
    def refresh(self):
        self.setVerticalSpacing(50)
        self.createTable()
        self.createInput()
        self.showData()