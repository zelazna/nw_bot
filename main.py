import os
import sys
from ctypes import windll

from PySide6 import QtGui
from PySide6.QtWidgets import QApplication

from bot.core.constants import APP_NAME
from bot.ui import MainWindow

basedir = os.path.dirname(__file__)

windll.shell32.SetCurrentProcessExplicitAppUserModelID("nwbot")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, "nwbot.ico")))
    window = MainWindow()
    window.setWindowTitle(APP_NAME)
    window.show()
    sys.exit(app.exec())
