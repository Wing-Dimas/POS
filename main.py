import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from pages.pageBarang import PageBarang
from pages.pageTransaksi import PageTransaksi
from pages.pageKasir import PageKasir
from pages.pageSupplier import PageSupplier
from pages.pageInventory import PageInventory
from pages.pagePelanggan import PagePelanggan

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,600,400)

        self.tabs = QTabWidget()
        pixmap = QPixmap("./favicon.ico")
        icon = QIcon(pixmap)

        list_tabs = [
            [PageBarang(), "Barang"],
            [PageTransaksi(), "Transaksi Penjualan"],
            [PageKasir(), "Kasir"],
            [PageSupplier(), "Supplier"],
            [PageInventory(), "Inventory"],
            [PagePelanggan(), "Pelanggan"],
        ]

        for i in range(len(list_tabs)):
            tab = QWidget()
            tab.setLayout(list_tabs[i][0])
            self.tabs.addTab(tab, list_tabs[i][1])

        self.setWindowIcon(icon)
        self.setCentralWidget(self.tabs)
        self.show()
        self.showMaximized()    

if __name__ == "__main__":
    try :
        app = QApplication(sys.argv)
        app.setApplicationName("POS PEMROGRAMAN DESKTOP")
        mainwindow = MainWindow()
        app.setWindowIcon(QIcon("favicon.ico"))
        app.exec()
        sys.exit(0)
    except NameError:
        print("Name Error")
    except SystemExit:
        print("exit")
    except Exception as e:
        print(e)