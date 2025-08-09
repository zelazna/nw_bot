import sys
from ctypes import windll
from pathlib import Path

from PySide6 import QtGui
from PySide6.QtWidgets import QApplication

from bot.core.constants import APP_NAME
from bot.ui import MainWindow

basedir = Path(__file__).parent.parent
icon = basedir / "nwbot.ico"
windll.shell32.SetCurrentProcessExplicitAppUserModelID("nwbot")

app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(str(icon)))
window = MainWindow()
window.setWindowTitle(APP_NAME)
window.show()
sys.exit(app.exec())
