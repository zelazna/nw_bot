import sys
import functools
from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QLabel,
)

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.data = {"keys": []}

        # Left
        self.left_layout = QVBoxLayout()
        self.window_number = QComboBox()
        self.left_layout.addWidget(QLabel("Nombre de fenetres"))
        self.left_layout.addWidget(self.window_number)
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for i in range(10):
            self.window_number.addItem(str(i))

        # Middle
        self.middle_layout = QVBoxLayout()
        self.keys = QComboBox()
        self.middle_layout.addWidget(QLabel("Touches"))
        self.middle_layout.addWidget(self.keys)

        for i in ("", "Q", "E", "R", "T", "A", "ESC", "SPACE"):
            self.keys.addItem(str(i))

        self.middle_layout.addWidget(QLabel("Selection"))
        self.middle_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Right
        self.right_layout = QVBoxLayout()
        self.interval = QLineEdit()
        self.interval.setClearButtonEnabled(1)
        self.limit = QLineEdit()
        self.limit.setClearButtonEnabled(1)
        self.right_layout.addWidget(QLabel("Intervale ( en m )"))
        self.right_layout.addWidget(self.interval)
        self.right_layout.addWidget(QLabel("Limite de temps ( en m )"))
        self.right_layout.addWidget(self.limit)
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Main Layout
        self.v_layout = QVBoxLayout(self)
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout, 1)
        self.main_layout.addLayout(self.middle_layout, 1)
        self.main_layout.addLayout(self.right_layout, 1)
        self.start_button = QPushButton("Depart")
        self.end_button = QPushButton("Arret")
        self.bot_label = QLabel("NW BOT")
        self.bot_label.setObjectName('appTitle')
        self.v_layout.addWidget(self.bot_label)
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.end_button)
        self.v_layout.addLayout(self.main_layout, 8)
        self.v_layout.addLayout(self.button_layout)

        # Signals and Slots
        self.keys.currentTextChanged.connect(self.add_key)
        self.window_number.currentTextChanged.connect(self.set_win_num)
        self.start_button.clicked.connect(self.start_bot)
        self.end_button.clicked.connect(self.stop_bot)

    @Slot()
    def add_key(self, key):
        self.data["keys"].append(key)
        b = QPushButton(key)
        b.clicked.connect(
            functools.partial(self.remove_button, b, len(self.data["keys"]) - 1)
        )
        self.middle_layout.addWidget(b, 0.1)
    
    @Slot()
    def set_win_num(self, win_num):
        self.data["win_num"] = win_num

    @Slot()
    def remove_button(self, button: QPushButton, idx: int):
        button.deleteLater()
        self.data["keys"].pop(idx)

    @Slot()
    def start_bot(self): 
        print(self.data)
        print(self.interval.text())
        print(self.limit.text())

    @Slot()
    def stop_bot(self): 
        self.parent().close()


class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("NW Bot")
        self.setCentralWidget(widget)


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    widget = Widget()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    window.resize(800, 600)
    window.show()

    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    # Execute application
    sys.exit(app.exec())