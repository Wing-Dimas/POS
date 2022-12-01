from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from connect import *
import numpy as np

class PageKasir(QGridLayout):
    def __init__(self):
        super().__init__()

        # deklarasi keranjang 
        self.keranjang = []

        self.createInput()
        self.createTable()
        self.showData()
        self.createTotal()

    def showData(self):
        if (len(self.keranjang) > 11):
            self.table.setRowCount(len(self.keranjang))

        if self.keranjang:
            self.table.clearContents()
            for i in range(len(self.keranjang)):
                for j in range(0, len(self.keranjang[0]) - 1):
                    newItem = QTableWidgetItem(str(self.keranjang[i][j + 1]))
                    self.table.setItem(i,j , newItem)


    def createTable(self):
        self.table = QTableWidget(11, 4)
        self.headers = ["Nama Barang", "Qty", "Harga", "Sub Total"]
        self.table.setHorizontalHeaderLabels(self.headers)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.addWidget(self.table, 1,0)

    def createInput(self):
        barang = query("SELECT * FROM barang")
        list_nama_barang = np.array(barang)[:, 1].tolist()
        groupBox = QGroupBox("Input Barang")
        self.inputLayout = QGridLayout()
        self.inputLayout.setVerticalSpacing(10)
        self.inputLayout.setHorizontalSpacing(5)
        self.inputBarangLayout = QGridLayout()
        groupBox.setLayout(self.inputBarangLayout)

        self.lblNamaPelanggan = QLabel("Pelanggan")
        self.lblAlamat = QLabel("Alamat")
        self.lblNamaBarang = QLabel("Nama Barang")
        self.lblQty = QLabel("Qty")

        self.inpNamaPelanggan = QLineEdit()
        self.inpAlamat = QLineEdit()
        self.inpNamaBarang = QComboBox()
        self.inpNamaBarang.addItems(list_nama_barang)
        self.inpQty = QLineEdit()

        self.btnTambah = QPushButton("Tambah")
        self.btnReset = QPushButton("Reset")
        self.btnRefresh = QPushButton("Refresh")

        self.btnTambah.clicked.connect(self.tambah)
        self.btnReset.clicked.connect(self.reset)
        self.btnRefresh.clicked.connect(self.refresh)

        self.inputLayout.addWidget(self.lblNamaPelanggan, 0, 0)
        self.inputLayout.addWidget(self.inpNamaPelanggan, 0, 1)
        self.inputLayout.addWidget(self.btnRefresh, 0, 2)
        self.inputLayout.addWidget(self.lblAlamat, 1, 0) 
        self.inputLayout.addWidget(self.inpAlamat, 1, 1)
        self.inputLayout.addWidget(self.btnReset, 1, 2)
        self.inputLayout.addWidget(groupBox, 2,0, 1, 3)

        self.inputBarangLayout.addWidget(self.lblNamaBarang, 0, 0)
        self.inputBarangLayout.addWidget(self.inpNamaBarang, 0, 1)
        self.inputBarangLayout.addWidget(self.lblQty, 1, 0)
        self.inputBarangLayout.addWidget(self.inpQty, 1, 1)
        self.inputBarangLayout.addWidget(self.btnTambah, 2, 0)

        self.addLayout(self.inputLayout, 0, 0)

    def createTotal(self):
        groupBox = QGroupBox("Form Pembayaran")
        self.pembayaranLayout = QGridLayout()
        self.pembayaranLayout.setVerticalSpacing(10)
        self.pembayaranLayout.setHorizontalSpacing(5)
        groupBox.setLayout(self.pembayaranLayout)


        self.lblTotal = QLabel("Total")
        self.inpTotal = QLabel("0")
        self.lblBayar = QLabel("Bayar")
        self.lblKembalian = QLabel("Kembalian")
        self.kembalian = QLabel("0")
        
        self.inpBayar = QLineEdit()
        
        self.btnBayar = QPushButton("Bayar")
        self.btnBayar.clicked.connect(self.pembayaran)

        self.pembayaranLayout.addWidget(self.lblTotal, 0,0)
        self.pembayaranLayout.addWidget(self.inpTotal, 0,1)
        self.pembayaranLayout.addWidget(self.lblBayar, 1, 0)
        self.pembayaranLayout.addWidget(self.inpBayar, 1, 1)
        self.pembayaranLayout.addWidget(self.btnBayar, 2, 1)
        self.pembayaranLayout.addWidget(self.lblKembalian, 3, 0)
        self.pembayaranLayout.addWidget(self.kembalian, 3, 1)

        self.addWidget(groupBox, 2, 0)

    def tambah(self):
        # get input
        namaBarang = self.inpNamaBarang.currentText()
        qty = int(self.inpQty.text())
        # check database
        barang = query(f"SELECT * FROM barang WHERE nama_barang='{namaBarang}'")[0]
        
        # tambah keranjang
        self.tambahKeranjang(barang, qty)
        
        print(self.keranjang)

    def tambahKeranjang(self, barang, qty):
        # cek over qty
        if barang[2] < qty: 
            msg = QMessageBox()
            msg.setText("Jumlah qunatity melebihi batas stok barang")
            msg.exec()
            return
        # check name
        if(self.keranjang and barang[1] in np.array(self.keranjang)[:, 1].tolist()):
            # find index item in keranjang
            for i in range(len(self.keranjang)):
                if(barang[1] in self.keranjang[i]):
                    ind = i
                    break
            temp = self.keranjang[ind]
            # cek over qty
            if barang[2] < temp[2] + qty: 
                msg = QMessageBox()
                msg.setText("Jumlah qunatity melebihi batas stok barang")
                msg.exec()
                return
            
            # update keranjang
            newQty = temp[2] + qty
            self.keranjang[ind] = [barang[0], barang[1], newQty, barang[3] ,newQty * barang[3]]
        else:
            self.keranjang.append([barang[0], barang[1], qty, barang[3], qty * barang[3]])
        
        # update total
        self.total = sum(np.array(self.keranjang)[:, 4].astype(np.int).tolist())
        self.inpTotal.setText(str(self.total))
        # update table
        self.showData()

    def pembayaran(self):
        bayar = int(self.inpBayar.text())
        total = int(self.inpTotal.text())

        # cek jika kurang
        if bayar < total:
            msg = QMessageBox()
            msg.setText("Nominal pembayaran kurang")
            msg.exec()
            self.kembalian.setText("")
            return

        # insert kedalam database
        # 1. pelanggan
        namaPelanggan = self.inpNamaPelanggan.text()
        alamat = self.inpAlamat.text()
        ## cek jika ada nama pelanggan yang sama 
        id_pelanggan = None
        temp = query(f"SELECT * FROM pelanggan WHERE nama_pelanggan='{namaPelanggan}'")
        if temp:
            id_pelanggan = temp[0][0]
        else:
            statement(f"INSERT INTO pelanggan VALUES (NULL, '{namaPelanggan}', '{alamat}')")
            id_pelanggan = query("SELECT * FROM pelanggan ORDER BY id_pelanggan DESC LIMIT 1")[0][0]

        # 2. transaksi
        statement(f"INSERT INTO transaksi VALUES (NULL,current_timestamp(), {total})")
        id_transaksi = query("SELECT id_transaksi FROM transaksi ORDER BY tanggal DESC LIMIT 1")[0][0]

        # 3. pemesanan
        statement(f"INSERT INTO pemesanan VALUES (NULL, {id_pelanggan}, {id_transaksi})")
        id_pemesanan = query("SELECT id_pemesanan FROM pemesanan ORDER BY id_pemesanan DESC LIMIT 1")[0][0]

        # 4. detail pemesanan
        for i in range(len(self.keranjang)):
            statement(f"INSERT INTO detail_pemesanan VALUES (NULL, {self.keranjang[i][0]}, {id_pemesanan}, {self.keranjang[i][2]}, {self.keranjang[i][4]})")

        # tampilkan kembalian
        kembalian = bayar - total
        self.kembalian.setText(str(kembalian))
        msg = QMessageBox()
        msg.setText("Transaksi berhasil")
        msg.exec()

        self.reset()


    def reset(self):
        self.keranjang = []
        self.inpNamaPelanggan.setText("")
        self.inpAlamat.setText("")
        self.inpQty.setText("")
        self.inpTotal.setText("0")
        self.inpBayar.setText("")
        self.kembalian.setText("0")

        msg = QMessageBox()
        msg.setText("Reset Berhasil")
        msg.exec()

    def refresh(self):
        self.createTable()
        self.createInput()
        self.showData()