import functools
import logging

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from bot.core.control import run
from bot.core.worker import Worker
from bot.models.keys_model import KeysModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


style = """
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
"""


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.is_recording = False

        # Left
        self.left_layout = QVBoxLayout()
        self.window_number = QComboBox()
        self.left_layout.addWidget(QLabel("Nombre de fenetres"))
        self.left_layout.addWidget(self.window_number)
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for i in range(1, 10):
            self.window_number.addItem(str(i))

        # Middle
        self.start_key_logger_button = QPushButton("Demarrer Enregistrement")
        self.stop_key_logger_button = QPushButton("Arreter Enregistrement")
        self.stop_key_logger_button.setVisible(False)
        self.middle_layout = QVBoxLayout()
        self.middle_layout.addWidget(self.start_key_logger_button)
        self.middle_layout.addWidget(self.stop_key_logger_button)
        self.start_key_logger_button.clicked.connect(
            functools.partial(self.switch_record_keystrokes, True)
        )
        self.stop_key_logger_button.clicked.connect(
            functools.partial(self.switch_record_keystrokes, False)
        )

        self.key_model = KeysModel()
        self.keys_list_view = QListView()
        self.keys_list_view.setModel(self.key_model)

        self.delete_button = QPushButton("Supprimer")
        self.middle_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.middle_layout.addWidget(self.keys_list_view)
        self.middle_layout.addWidget(self.delete_button)
        self.delete_button.pressed.connect(self.delete)

        # Right
        self.right_layout = QVBoxLayout()
        self.interval = QLineEdit(
            placeholderText="1 ou 1-5 pour aleatoire entre deux valeurs"
        )
        self.interval.setClearButtonEnabled(True)
        self.limit = QLineEdit()
        self.limit.setText("2")
        self.limit.setClearButtonEnabled(True)
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
        self.start_button.clicked.connect(self.start_bot)

        self.stop_button = QPushButton("Arret")
        self.stop_button.setDisabled(True)
        self.stop_button.clicked.connect(self.stop_bot)

        self.bot_label = QLabel("NW BOT")
        self.bot_label.setObjectName("appTitle")

        self.v_layout.addWidget(self.bot_label)
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)
        self.v_layout.addLayout(self.main_layout, 8)
        self.v_layout.addLayout(self.button_layout)

    def switch_record_keystrokes(self, state: bool):
        self.start_key_logger_button.setVisible(not state)
        self.stop_key_logger_button.setVisible(state)
        self.is_recording = state

    def delete(self):
        indexes = self.keys_list_view.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.key_model.keys[index.row()]
            self.key_model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.keys_list_view.clearSelection()

    def bot_thread_complete(self):
        logging.info("done!")
        self.start_button.setDisabled(False)
        self.stop_button.setDisabled(True)

    @Slot()
    def start_bot(self):
        # TODO cast in int with QT
        self.stop_button.setDisabled(False)
        self.start_button.setDisabled(True)

        interval = self.interval.text()

        if "-" in interval:
            min, max = interval.split("-")
            final_interval = list(range(int(min), int(max)))
        else:
            final_interval = [int(interval)]

        self.worker = Worker(
            run,
            {
                "keys": self.key_model.keys,
                "interval": final_interval,
                "limit": int(self.limit.text()),
                "win_num": int(self.window_number.currentText()),
            },
        )  # Any other args, kwargs are passed to the run function
        # TODO handle exit
        self.worker.signals.finished.connect(self.bot_thread_complete)
        self.worker.start()

    @Slot()
    def stop_bot(self):
        logger.debug("Stopping")
        if self.worker:
            self.worker.terminate()
            self.worker.wait()
            self.worker.terminate()
        self.start_button.setDisabled(False)
        self.stop_button.setDisabled(True)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.is_recording:
            key = event.text()
            if key.isalpha():
                self.key_model.keys.append((event.nativeScanCode(), key.upper()))
                self.key_model.layoutChanged.emit()


class MainWindow(QMainWindow):
    def __init__(self, widget: QWidget):
        super().__init__()
        self.setWindowTitle("NW Bot")
        self.setCentralWidget(widget)
        self.resize(800, 600)
        self.show()
