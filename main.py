import sys

from PySide6.QtWidgets import QApplication
from bot.ui import Widget, MainWindow, style


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    widget = Widget()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    app.setStyleSheet(style)

    # Execute application
    sys.exit(app.exec())
