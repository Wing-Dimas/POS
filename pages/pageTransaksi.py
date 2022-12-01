from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from connect import *
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class PageTransaksi(QHBoxLayout):
    def __init__(self):
        super().__init__()

        # self.setVerticalSpacing(50)
        # self.createTable()
        # self.createInput()
        # self.showData()

    def showData(self):
        pass
        # self.data = query("SELECT t.id_transaksi AS id_transaksi, tanggal, nama_pelanggan, total FROM transaksi AS t JOIN pemesanan AS p1 ON t.id_transaksi=p1.id_transaksi JOIN pelanggan AS p2 ON p1.id_pelanggan=p2.id_pelanggan")
        # if (len(self.data) > 16):
        #     self.table.setRowCount(len(self.data))
        # self.table.clearContents()
        # for i in range(len(self.data)):
        #     for j in range(len(self.data[0])):
        #         newItem = QTableWidgetItem(str(self.data[i][j]))
        #         self.table.setItem(i,j , newItem)


    def createTable(self):
        pass
        # self.table = QTableWidget(16, 4)
        # self.headers = ["id", "Tanggal", "Nama Pelanggan", "Total"]
        # self.table.setHorizontalHeaderLabels(self.headers)
        # self.header = self.table.horizontalHeader()
        # self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        # self.header.setSectionResizeMode(2, QHeaderView.Stretch)
        # self.header.setSectionResizeMode(3, QHeaderView.Stretch)

        # self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.table.clicked.connect(self.select)

        # self.addWidget(self.table, 1,0)

    def createInput(self):
        pass
        # self.inputLayout = QGridLayout()
        # self.inputLayout.setVerticalSpacing(10)
        # self.inputLayout.setHorizontalSpacing(5)
        # self.btnLayout = QHBoxLayout()
        # self.btnLayout.setSpacing(10)

        # self.lblNama = QLabel("Nama Barang")
        # self.lblStok = QLabel("Stok")
        # self.lblHarga = QLabel("Harga")

        # self.inpNama = QLineEdit()
        # self.inpStok = QLineEdit()
        # self.inpHarga = QLineEdit()

        # self.btnTambah = QPushButton("Tambah")
        # self.btnEdit = QPushButton("Edit")
        # self.btnHapus = QPushButton("Hapus")
        # self.btnCancel = QPushButton("Cancel")

        # self.btnTambah.setFixedWidth(80)
        # self.btnTambah.clicked.connect(self.tambah)
        # self.btnEdit.setFixedWidth(80)
        # self.btnEdit.clicked.connect(self.edit)
        # self.btnHapus.setFixedWidth(80)
        # self.btnHapus.clicked.connect(self.hapus)
        # self.btnCancel.setFixedWidth(80)
        # self.btnCancel.clicked.connect(self.cancel)

        # self.inputLayout.addWidget(self.lblNama, 0, 0)
        # self.inputLayout.addWidget(self.lblStok, 1, 0)
        # self.inputLayout.addWidget(self.lblHarga, 2, 0)

        # self.inputLayout.addWidget(self.inpNama, 0, 1)
        # self.inputLayout.addWidget(self.inpStok, 1, 1)
        # self.inputLayout.addWidget(self.inpHarga, 2, 1)

        # self.inputLayout.addLayout(self.btnLayout, 3, 0, 1, 2)

        # self.btnLayout.addWidget(self.btnTambah)
        # self.btnLayout.addWidget(self.btnEdit)
        # self.btnLayout.addWidget(self.btnHapus)
        # self.btnLayout.addWidget(self.btnCancel)
        # self.btnLayout.addStretch()

        # self.switchButton()

        # self.addLayout(self.inputLayout, 0, 0)
