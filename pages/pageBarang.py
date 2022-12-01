from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from connect import *

class PageBarang(QGridLayout):
    def __init__(self):
        super().__init__()


        self.setVerticalSpacing(50)
        self.createTable()
        self.createInput()
        self.showData()

    def showData(self):
        self.data = query("SELECT * FROM barang")
        if (len(self.data) > 16):
            self.table.setRowCount(len(self.data))
        self.table.clearContents()
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                newItem = QTableWidgetItem(str(self.data[i][j]))
                self.table.setItem(i,j , newItem)


    def createTable(self):
        self.table = QTableWidget(16, 5)
        self.headers = ["id", "Nama", "Stok","Harga Beli", "Harga Jual"]
        self.table.setHorizontalHeaderLabels(self.headers)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.header.setSectionResizeMode(4, QHeaderView.Stretch)

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

        self.lblNama = QLabel("Nama Barang")
        self.lblHargaBeli = QLabel("Harga Beli")
        self.lblHargaJual = QLabel("Harga Jual")

        self.inpNama = QLineEdit()
        self.inpHragaBeli = QLineEdit()
        self.inpHargaJual = QLineEdit()

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
        self.inputLayout.addWidget(self.lblHargaBeli, 1, 0)
        self.inputLayout.addWidget(self.lblHargaJual, 2, 0)

        self.inputLayout.addWidget(self.inpNama, 0, 1)
        self.inputLayout.addWidget(self.inpHragaBeli, 1, 1)
        self.inputLayout.addWidget(self.inpHargaJual, 2, 1)

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
        hargaBeli = self.inpHragaBeli.text()
        hargaJual = self.inpHargaJual.text()
        print("test")
        
        statement(f"INSERT INTO `barang` (`id_barang`, `nama_barang`, `harga_beli`, `harga_jual`) VALUES (NULL, '{nama}', '{int(hargaBeli)}', '{int(hargaJual)}');")
        self.showData()
   
    def select(self):
        row = sorted(set(index.row() for index in self.table.selectedIndexes()))[0]
        try:
            data = self.data[row]
            self.id = data[0]
            self.inpNama.setText(data[1])
            self.inpHragaBeli.setText(str(data[3]))
            self.inpHargaJual.setText(str(data[4]))
            self.switchButton(False)
        except:
            self.clearInput()
            self.switchButton()

    def edit(self):
        nama = self.inpNama.text()
        hargaBeli= self.inpHragaBeli.text()
        hargaJual = self.inpHargaJual.text()
        
        statement(f"UPDATE `barang` SET `nama_barang` = '{nama}', `harga_jual` = '{hargaJual}', `harga_beli` = '{hargaBeli}' WHERE `barang`.`id_barang` = {self.id};")
        self.showData()
        self.clearInput()
        self.switchButton()

    def hapus(self):
        statement(f"DELETE FROM `barang` WHERE `barang`.`id_barang` = {self.id}")
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
        self.inpHragaBeli.setText("")
        self.inpHargaJual.setText("")
    
    def refresh(self):
        self.setVerticalSpacing(50)
        self.createTable()
        self.createInput()
        self.showData()