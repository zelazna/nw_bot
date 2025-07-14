import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6 import QtGui
from bot.ui import Widget, MainWindow, style
from ctypes import windll

basedir = os.path.dirname(__file__)

windll.shell32.SetCurrentProcessExplicitAppUserModelID("nwbot")

if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir,"nwbot.ico")))
    # QWidget
    widget = Widget()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    app.setStyleSheet(style)

    # Execute application
    sys.exit(app.exec())
