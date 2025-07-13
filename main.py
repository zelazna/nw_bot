import sys

from PySide6.QtWidgets import QApplication
from PySide6 import QtGui
from bot.ui import Widget, MainWindow, style


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("nwbot.ico"))
    # QWidget
    widget = Widget()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    app.setStyleSheet(style)

    # Execute application
    sys.exit(app.exec())
