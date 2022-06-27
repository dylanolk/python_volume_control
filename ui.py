from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox, QSpacerItem, QLineEdit
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout
from PyQt5.QtWidgets import QWidget, QFrame

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setCentralWidget(QWidget())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    window= MainWindow()
    sys.exit(app.exec_())
