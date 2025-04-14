import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow

from View.workspace import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.dataToolButton.clicked.connect(self.test_function)
        self.ui.cabinetToolButton.clicked.connect(self.cabinet_function)
        self.ui.exitToolButton.clicked.connect(self.exit_function)

    def test_function(self):
        print('test')

    def cabinet_function(self):
        print('cabinet button')

    def faq_function(self):
        print('faq button')

    def genOtch_function(self):
        print('genOtch button')

    def genPlan_function(self):
        print('genOtch button')

    def exit_function(self):
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())