import sys
from pathlib import Path

from PySide6 import QtGui
from PySide6.QtWidgets import QApplication

from bot.core.constants import APP_NAME
from bot.ui.main_window import MainWindow

basedir = Path(__file__).parent
icon = basedir / "nwbot.ico"

# Windows-specific: Set app user model ID for taskbar grouping
if sys.platform == "win32":
    from ctypes import windll
    windll.shell32.SetCurrentProcessExplicitAppUserModelID("nwbot")

app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(str(icon)))
window = MainWindow()
window.setWindowTitle(APP_NAME)
window.show()
sys.exit(app.exec())
