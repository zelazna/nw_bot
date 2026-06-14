import sys
from pathlib import Path

from PySide6 import QtGui
from PySide6.QtCore import QLocale, QTranslator
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

translator = QTranslator(app)
lang = QLocale.system().name().split("_")[0]
qm_path = basedir / "i18n" / f"nw_bot_{lang}.qm"
if translator.load(str(qm_path)):
    app.installTranslator(translator)

window = MainWindow()
window.setWindowTitle(APP_NAME)
window.show()
sys.exit(app.exec())
