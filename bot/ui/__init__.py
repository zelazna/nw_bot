import functools
import json
import os

from PySide6.QtCore import QTimer, Slot
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QFileDialog, QMainWindow

from bot.core import Keystroke
from bot.core.control import run
from bot.core.keystroke_adapter import ModifierKey, encode_value, match
from bot.core.worker import Worker
from bot.models.keys_model import KeysModel
from bot.ui.mainwindow import Ui_MainWindow
from bot.ui.modals import FileNameModal
from bot.utils import logger


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = None
        self.is_recording = False
        self.time_left_int = 0
        self.bot_timer = QTimer(self)
        self.bot_timer.timeout.connect(self.timer_tick)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # type: ignore

        self.key_model = KeysModel()
        self.ui.keyListView.setModel(self.key_model)

        self.ui.actionSaveConfig.triggered.connect(self.save_config)
        self.ui.actionLoadConfig.triggered.connect(self.load_config)

        for i in range(1, 10):
            self.ui.winNum.addItem(str(i))

        self.ui.stopRecordButton.setVisible(False)
        self.ui.startRecordButton.clicked.connect(
            functools.partial(self.switch_record_keystrokes, True)
        )
        self.ui.stopRecordButton.clicked.connect(
            functools.partial(self.switch_record_keystrokes, False)
        )
        self.ui.deleteKey.clicked.connect(self.delete)

        self.interval = self.ui.interval
        self.interval.setClearButtonEnabled(True)

        self.limit = self.ui.limit
        self.limit.setClearButtonEnabled(True)

        self.ui.remainingTime.setVisible(False)

        self.ui.stopButton.setDisabled(True)
        self.ui.stopButton.clicked.connect(self.stop_bot)
        self.ui.startButton.clicked.connect(self.start_bot)

    def switch_record_keystrokes(self, state: bool):
        self.ui.startRecordButton.setVisible(not state)
        self.ui.stopRecordButton.setVisible(state)
        self.is_recording = state

    def delete(self):
        indexes = self.ui.keyListView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.key_model.keys[index.row()]
            self.key_model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.ui.keyListView.clearSelection()

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.is_recording:
            if stroke := match(event):
                self.key_model.keys.append(stroke)
                self.key_model.layoutChanged.emit()

    def bot_thread_complete(self):
        logger.info("done!")
        self.ui.startButton.setDisabled(False)
        self.ui.stopButton.setDisabled(True)
        self.ui.remainingTime.setVisible(False)

    @Slot()
    def start_bot(self):
        self.ui.remainingTime.setVisible(True)
        self.ui.stopButton.setDisabled(False)
        self.ui.startButton.setDisabled(True)

        interval = self.interval.text()
        self.start_timer()

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
                "win_num": int(self.ui.winNum.currentText()),
            },
        )  # Any other args, kwargs are passed to the run function
        self.worker.signals.finished.connect(self.bot_thread_complete)
        self.worker.start()

    def start_timer(self):
        self.time_left_int = (
            int(self.limit.text()) * 60 * 1000
        )  # Convert minutes to milliseconds
        format_time = self._format_time(self.time_left_int)
        logger.debug(f"Starting timer with {format_time} minutes")
        self.ui.remainingTime.setText(format_time)
        self.bot_timer.start(500)

    def timer_tick(self):
        self.time_left_int -= 1000  # Decrease by 1 second
        print(self.time_left_int)

        if self.time_left_int <= 0:
            self.bot_timer.stop()
            self.bot_thread_complete()

        self.ui.remainingTime.setText(self._format_time(self.time_left_int))

    @Slot()
    def stop_bot(self):
        logger.debug("Stopping")
        if self.worker:
            self.worker.terminate()
            self.worker.wait()
            self.worker.terminate()
        self.ui.startButton.setDisabled(False)
        self.ui.stopButton.setDisabled(True)
        self.ui.remainingTime.setVisible(False)
        self.bot_timer.stop()

    def save_config(self):
        config = self._dump_config()
        folder = QFileDialog.getExistingDirectory(
            self, "Sauvegarder le fichier de config"
        )
        if folder:
            dlg = FileNameModal()
            if dlg.exec():
                filepath = os.path.join(folder, dlg.filename)
                with open(filepath, "w") as f:
                    json.dump(config, f, indent=4, default=encode_value)
                logger.info(f"Config saved to {filepath}")

    def load_config(self):
        dialog = QFileDialog(self, "Choisir le fichier de config")
        filename, _ = dialog.getOpenFileName(self, filter="JSON files (*.json)")
        if filename:
            with open(filename, "r") as f:
                config = json.load(f)

            for key in config["keys"]:
                if modifier := key.get("modifier", {}):
                    self.key_model.keys.append(
                        Keystroke(**{**key, "modifier": ModifierKey(**modifier)})  # type: ignore
                    )
                else:
                    self.key_model.keys.append(Keystroke(**key))

            self.key_model.layoutChanged.emit()
            self.interval.setText(config["interval"])
            self.limit.setText(config["limit"])
            self.ui.winNum.setCurrentText(str(config["win_num"]))

    def _dump_config(self):
        return {
            "keys": self.key_model.keys,
            "interval": self.interval.text(),
            "limit": self.limit.text(),
            "win_num": self.ui.winNum.currentText(),
        }

    def _format_time(self, milliseconds: int) -> str:
        secs = milliseconds / 1000
        secs = secs % (24 * 3600)
        hours = secs // 3600
        secs %= 3600
        mins = secs // 60
        secs %= 60
        return f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}"
