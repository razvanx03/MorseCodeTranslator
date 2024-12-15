# pip install morse-package
# https://pypi.org/project/morsecode-package/
from PyQt5.QtWidgets import QApplication
from morseCodeClass import MorseCodeApp

if __name__ == '__main__':
    app = QApplication([])
    window = MorseCodeApp()
    window.show()
    app.exec_()
