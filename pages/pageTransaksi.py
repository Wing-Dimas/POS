from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from connect import *
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from openpyxl import load_workbook
import pandas as pd
from datetime import datetime
import calendar

class PageTransaksi(QHBoxLayout):
    def __init__(self):
        super().__init__()
        
        self.createLeft()
        self.createRight()
        self.addLayout(self.leftLayout)
        self.addLayout(self.rightLayout)
        

    
    def createLeft(self):
        self.leftLayout = QGridLayout()
        btnLayout = QHBoxLayout()

        self.btnRefersh = QPushButton("Refresh")
        self.btnImport = QPushButton("Import Data")
        self.btnExport = QPushButton("Export Data")

        self.btnRefersh.clicked.connect(self.refresh)
        self.btnImport.clicked.connect(self.importFile)
        self.btnExport.clicked.connect(self.exportFile)

        btnLayout.addWidget(self.btnRefersh)
        btnLayout.addWidget(self.btnImport)
        btnLayout.addWidget(self.btnExport)

        self.leftLayout.addLayout(btnLayout,0,0)
        self.createTable()
        self.showData()

    def createRight(self):
        self.rightLayout = QGridLayout()
        self.createGraphic()


    def showData(self, importFile=False):
        self.table.clearContents()
        if not importFile:
            self.data = query("""
                SELECT 
                    DATE(transaksi.tanggal) AS tanggal,
                    barang.nama_barang,
                    SUM(detail_pemesanan.qty) AS qty,
                    barang.harga_jual,
                    barang.harga_beli,
                    (barang.harga_jual - barang.harga_beli) * qty AS laba
                FROM transaksi
                JOIN pemesanan
                    ON transaksi.id_transaksi=pemesanan.id_transaksi
                JOIN detail_pemesanan
                    ON pemesanan.id_pemesanan=detail_pemesanan.id_pemesanan
                JOIN barang
                    ON detail_pemesanan.id_barang=barang.id_barang
                GROUP BY DATE(transaksi.tanggal) ,barang.nama_barang
                HAVING tanggal >= NOW() - INTERVAL WEEKDAY(now()) DAY 
                    AND tanggal < NOW() + INTERVAL (7 - WEEKDAY(now())) DAY;
            """)
        self.data = pd.DataFrame(data=self.data, columns=["Tanggal", "Nama Barang", "Qty", "Harga Jual", "Harga Beli", "Laba"])
        self.table.setRowCount(self.data.shape[0])
        self.table.setColumnCount(self.data.shape[1])

        for row in self.data.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                if isinstance(value, (float, int)):
                    value = '{0:0,.0f}'.format(value)
                newItem = QTableWidgetItem(str(value))
                self.table.setItem(row[0],col_index , newItem)

    def createTable(self):
        self.table = QTableWidget(16, 6)
        self.headers = ["Tanggal", "Nama Barang", "Qty", "Harga Jual", "Harga Beli", "Laba"]
        self.table.setHorizontalHeaderLabels(self.headers)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.header.setSectionResizeMode(4, QHeaderView.Stretch)
        self.header.setSectionResizeMode(5, QHeaderView.Stretch)

        self.leftLayout.addWidget(self.table, 1, 0)

    def createGraphic(self):
        print(self.data)
        y = [
            0, # senin
            0, # selasa
            0, # rabu
            0, # kamis
            0, # jumat
            0, # sabtu
            0, # minggu
        ]
        
        for i in range(self.data.shape[0]): 
            day = int(self.data.iloc[i].Tanggal.strftime("%w"))  - 1 
            y[day] += int(self.data.iloc[i].Qty)


        sc = MplCanvas(self, width=7, height=4, dpi=100)
        sc.axes.bar(["senin","selasa","rabu","kamis","juma'at", "sabtu", "minggu"], y)
        self.rightLayout.addWidget(sc, 0, 0)
    
    def refresh(self):
        self.showData(importFile=False)
        self.createGraphic()
        self.createRight()

    def importFile(self):
        window = QWidget()
        # Show the file dialog and get the file path 
        file_path, _ = QFileDialog.getOpenFileName(window, "Select Excel File to Import", "", "Excel Files (*.xlsx)")

        # Convert the Excel sheet data to a Pandas DataFrame
        data = pd.read_excel(file_path)
        self.data = data
        self.showData(importFile=True)
        self.createGraphic()
        self.createRight()
    
    def exportFile(self):
        date = datetime.now()
        num = date.month
        year = date.year
        month = calendar.month_name[num]
        day = date.day

        self.data.to_excel(f"C:/POS/Laporan penjualan {year} {month} {day}.xlsx",sheet_name='sheet 1', index=False) 
        msg = QMessageBox()
        msg.setText(f"Data berhasil di export pada directory C:/POS/Laporan penjualan {year} {month} {day}.xlsx")
        msg.exec()

        

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
