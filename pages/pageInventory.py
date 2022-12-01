from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from connect import *
import numpy as np

class PageInventory(QGridLayout):
    def __init__(self):
        super().__init__()


        self.setVerticalSpacing(50)
        self.createTable()
        self.createInput()
        self.showData()

    def showData(self):
        self.data = query("SELECT i.id_inventory, tanggal, b.nama_barang, s.nama_supplier, jumlah FROM inventory AS i JOIN barang AS b ON i.id_barang=b.id_barang JOIN supplier AS s ON i.id_supplier=s.id_supplier ORDER BY tanggal DESC;")
        if (len(self.data) > 16):
            self.table.setRowCount(len(self.data))
        self.table.clearContents()
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                newItem = QTableWidgetItem(str(self.data[i][j]))
                self.table.setItem(i,j , newItem)


    def createTable(self):
        self.table = QTableWidget(16, 5)
        self.headers = ["id", "Tanggal", "Nama Barang", "Nama Suplier", "Jumlah"]
        self.table.setHorizontalHeaderLabels(self.headers)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.addWidget(self.table, 1,0)

    def createInput(self):
        self.barang = query("SELECT * FROM barang")
        self.supplier = query("SELECT * FROM supplier")

        list_nama_barang = np.array(self.barang)[:, 1].tolist()
        list_nama_supplier = np.array(self.supplier)[:, 1].tolist()

        groupBox = QGroupBox("Form")
        self.inputLayout = QGridLayout()
        self.inputLayout.setVerticalSpacing(10)
        self.inputLayout.setHorizontalSpacing(5)
        self.btnLayout = QHBoxLayout()
        self.btnLayout.setSpacing(10)
        groupBox.setLayout(self.inputLayout)

        self.lblNamaBarang = QLabel("Nama Barang")
        self.lblNamaSupplier = QLabel("Nama Suppplier")
        self.lblJumlah = QLabel("Jumlah")

        self.inpNamaBarang = QComboBox()
        self.inpNamaSupplier = QComboBox()
        self.inpJumlah = QLineEdit()

        self.inpNamaBarang.addItems(list_nama_barang)
        self.inpNamaSupplier.addItems(list_nama_supplier)

        self.btnTambah = QPushButton("Tambah")
        self.btnRefresh = QPushButton("Refresh")

        self.btnTambah.setFixedWidth(80)
        self.btnTambah.clicked.connect(self.tambah)
        self.btnRefresh.setFixedWidth(80)
        self.btnRefresh.clicked.connect(self.refresh)

        self.inputLayout.addWidget(self.lblNamaBarang, 0, 0)
        self.inputLayout.addWidget(self.lblNamaSupplier, 1, 0)
        self.inputLayout.addWidget(self.lblJumlah, 2, 0)

        self.inputLayout.addWidget(self.inpNamaBarang, 0, 1)
        self.inputLayout.addWidget(self.inpNamaSupplier, 1, 1)
        self.inputLayout.addWidget(self.inpJumlah, 2, 1)

        self.inputLayout.addLayout(self.btnLayout, 3, 0, 1, 2) 

        self.btnLayout.addWidget(self.btnTambah)
        self.btnLayout.addWidget(self.btnRefresh)
        self.btnLayout.addStretch()

        self.addWidget(groupBox, 0, 0)

    def tambah(self):
        namaBarang = self.inpNamaBarang.currentText()
        namaSupplier = self.inpNamaSupplier.currentText()
        jumlah = self.inpJumlah.text()

        barang = query(f"SELECT id_barang FROM barang WHERE nama_barang='{namaBarang}'")
        supplier = query(f"SELECT id_supplier FROM supplier WHERE nama_supplier='{namaSupplier}';")
        
        if barang and supplier:
            id_barang = barang[0][0]
            id_supplier = supplier[0][0]
            statement(f"INSERT INTO `inventory` (`id_inventory`, `tanggal`, `jumlah`, `id_barang`, `id_supplier`) VALUES (NULL, current_timestamp(), '{jumlah}', '{id_barang}', '{id_supplier}');")
        else:
            msg = QMessageBox()
            msg.setText("Input yang anda masukan salah, Coba lakukan refersh")
            msg.exec()
            return
        
        self.clearInput()
        self.showData()

    def clearInput(self):
        self.inpJumlah.setText("")

    def refresh(self):
        self.setVerticalSpacing(50)
        self.createTable()
        self.createInput()
        self.showData()