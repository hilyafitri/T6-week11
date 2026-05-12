"""
Nama  : Hilya Fitri
NIM   : F1D02310009
Kelas : C

"""

import sys
from PySide6.QtWidgets import QApplication
from ui_main import MainWindow

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())