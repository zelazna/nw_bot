import functools
from typing import cast

from PySide6.QtCore import Slot
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QComboBox,
    QLineEdit,
    QListView,
    QMainWindow,
    QPushButton,
)

from bot.core.control import run
from bot.core.keystroke_adapter import match
from bot.core.worker import Worker
from bot.models.keys_model import KeysModel
from bot.ui.mainwindow import Ui_MainWindow
from bot.utils import logger


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = None
        self.is_recording = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # type: ignore

        self.key_model = KeysModel()
        self.keys_list_view = cast(QListView, self.findChild(QListView, "keyListView"))
        self.keys_list_view.setModel(self.key_model)
        self.window_number = cast(QComboBox, self.findChild(QComboBox, "winNum"))

        for i in range(1, 10):
            self.window_number.addItem(str(i))

        (
            self.stop_record_button,
            self.start_record_button,
            self.delete_key_button,
            self.start_bot_button,
            self.stop_bot_button,
        ) = self.findChildren(QPushButton)

        self.stop_record_button.setVisible(False)
        self.start_record_button.clicked.connect(
            functools.partial(self.switch_record_keystrokes, True)
        )
        self.stop_record_button.clicked.connect(
            functools.partial(self.switch_record_keystrokes, False)
        )
        self.delete_key_button.pressed.connect(self.delete)

        self.interval = cast(QLineEdit, self.findChild(QLineEdit, "interval"))
        self.interval.setClearButtonEnabled(True)

        self.limit = cast(QLineEdit, self.findChild(QLineEdit, "limit"))
        self.limit.setClearButtonEnabled(True)

        self.stop_bot_button.setDisabled(True)
        self.stop_bot_button.clicked.connect(self.stop_bot)
        self.start_bot_button.clicked.connect(self.start_bot)

    def switch_record_keystrokes(self, state: bool):
        self.start_record_button.setVisible(not state)
        self.stop_record_button.setVisible(state)
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

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.is_recording:
            if stroke := match(event):
                self.key_model.keys.append(stroke)
                self.key_model.layoutChanged.emit()

    def bot_thread_complete(self):
        logger.info("done!")
        self.start_bot_button.setDisabled(False)
        self.stop_bot_button.setDisabled(True)

    @Slot()
    def start_bot(self):
        self.stop_bot_button.setDisabled(False)
        self.start_bot_button.setDisabled(True)

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
        self.start_bot_button.setDisabled(False)
        self.stop_bot_button.setDisabled(True)
