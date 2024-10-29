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

from core.control import run, KEYMAP
from core.worker import Worker
import logging
import itertools

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)




style = '''
QPushButton {
    padding: 5px;
    min-width: 10em;
}

QLabel#appTitle {
    qproperty-alignment: AlignCenter;
    font: bold 14px;
    font-size: 36px;
    margin: 20px;
}
'''

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.registered_keys = []

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

        for i in itertools.chain("", KEYMAP.keys()):
            self.keys.addItem(str(i))

        self.middle_layout.addWidget(QLabel("Selection"))
        self.middle_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Right
        self.right_layout = QVBoxLayout()
        self.interval = QLineEdit()
        self.interval.setClearButtonEnabled(1)
        self.limit = QLineEdit()
        self.limit.setClearButtonEnabled(1)
        self.right_layout.addWidget(QLabel("Intervale entre les touches (en s)"))
        self.right_layout.addWidget(self.interval)
        self.right_layout.addWidget(QLabel("Limite de temps (en m)"))
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
        self.bot_label.setObjectName("appTitle")
        self.v_layout.addWidget(self.bot_label)
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.end_button)
        self.v_layout.addLayout(self.main_layout, 8)
        self.v_layout.addLayout(self.button_layout)

        # Signals and Slots
        self.keys.currentTextChanged.connect(self.add_key)
        self.start_button.clicked.connect(self.start_bot)
        self.end_button.clicked.connect(self.stop_bot)

    @Slot()
    def add_key(self, key):
        self.registered_keys.append(key)
        b = QPushButton(key)
        b.clicked.connect(
            functools.partial(self.remove_button, b, len(self.registered_keys) - 1)
        )
        self.middle_layout.addWidget(b, 0.1)

    @Slot()
    def remove_button(self, button: QPushButton, idx: int):
        button.deleteLater()
        self.registered_keys.pop(idx)

    def thread_complete(self):
        logging.info("done!")
        self.start_button.setDisabled(False)

    @Slot()
    def start_bot(self):
        # TODO cast in int with QT
        self.start_button.setDisabled(True)
        self.worker = Worker(
            run,
            {
                "keys": self.registered_keys,
                "interval": int(self.interval.text()),
                "limit": int(self.limit.text()),
                "win_num": int(self.window_number.currentText()),
            },
        )  # Any other args, kwargs are passed to the run function
        # TODO handle exit
        self.worker.signals.finished.connect(self.thread_complete)
        self.worker.start()


    @Slot()
    def stop_bot(self):
        self.worker.terminate()
        self.worker.wait()
        self.parent().close()


class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("NW Bot")
        self.setCentralWidget(widget)
        self.resize(800, 600)
        self.show()


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
