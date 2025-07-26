import functools

from pynput.mouse import Button
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QFileDialog, QMainWindow

from bot.core.constants import VERSION
from bot.core.control import run
from bot.core.keystroke_adapter import match
from bot.core.worker import Worker
from bot.models import CommandsModel, MouseClick, Params
from bot.ui.mainwindow import Ui_MainWindow
from bot.ui.modals import FileNameModal, LogViewerModal
from bot.utils import load_config, logger, save_config


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

        self.key_model = CommandsModel()
        self.ui.keyListView.setModel(self.key_model)
        self.ui.keyListView.setDragEnabled(True)
        self.ui.keyListView.setAcceptDrops(True)
        self.ui.keyListView.setDropIndicatorShown(True)

        self.ui.actionSaveConfig.triggered.connect(self._save_config)
        self.ui.actionLoadConfig.triggered.connect(self._load_config)

        self.ui.actionShowLogs.triggered.connect(self._show_logs)

        for i in range(1, 10):
            self.ui.winNum.addItem(str(i))

        self.ui.stopRecordButton.setVisible(False)
        self.ui.startRecordButton.clicked.connect(
            functools.partial(self.switch_record_keystrokes, True)
        )
        self.ui.stopRecordButton.clicked.connect(
            functools.partial(self.switch_record_keystrokes, False)
        )
        self.ui.deleteKey.clicked.connect(self.delete_command)
        self.ui.deleteAll.clicked.connect(self.delete_all_keys)

        self.interval = self.ui.interval
        self.interval.setClearButtonEnabled(True)

        self.limit = self.ui.limit
        self.limit.setClearButtonEnabled(True)

        self.ui.remainingTime.setVisible(False)

        self.ui.stopButton.setDisabled(True)
        self.ui.stopButton.clicked.connect(self.stop_bot)
        self.ui.startButton.clicked.connect(self.start_bot)

        self.ui.appVersion.setText(f"v{VERSION}")

    def switch_record_keystrokes(self, state: bool):
        self.ui.startRecordButton.setVisible(not state)
        self.ui.stopRecordButton.setVisible(state)
        self.is_recording = state

    def delete_all_keys(self):
        self.key_model.commands.clear()
        self.key_model.layoutChanged.emit()
        self.ui.keyListView.clearSelection()

    def delete_command(self):
        indexes = self.ui.keyListView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.key_model.commands[index.row()]
            self.key_model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.ui.keyListView.clearSelection()

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.is_recording:
            if stroke := match(event):
                self.key_model.commands.append(stroke)
                self.key_model.layoutChanged.emit()
        if event.key() == Qt.Key.Key_Delete:
            self.delete_command()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.is_recording:
            button = event.button()
            kind = Button.right if button is Qt.MouseButton.RightButton else Button.left
            self.key_model.commands.append(
                MouseClick(kind=kind, pos=(event.x(), event.y()))
            )
            self.key_model.layoutChanged.emit()

    def bot_thread_complete(self):
        logger.info("bot thread complete!")
        self.ui.startButton.setDisabled(False)
        self.ui.stopButton.setDisabled(True)
        self.ui.remainingTime.setVisible(False)

    @Slot()
    def start_bot(self):
        self.ui.remainingTime.setVisible(True)
        self.ui.stopButton.setDisabled(False)
        self.ui.startButton.setDisabled(True)

        self.start_timer()

        self.worker = Worker(run, self._dump_config())
        self.worker.signals.finished.connect(self.bot_thread_complete)
        self.worker.start()

    def start_timer(self):
        self.time_left_int = (
            int(self.limit.text()) * 60 * 1000
        )  # Convert minutes to milliseconds
        format_time = self._format_time(self.time_left_int)
        logger.info(f"Starting timer with {format_time} minutes")
        self.ui.remainingTime.setText(format_time)
        self.bot_timer.start(500)

    def timer_tick(self):
        self.time_left_int -= 1000  # Decrease by 1 second

        if self.time_left_int <= 0:
            self.stop_bot()

        self.ui.remainingTime.setText(self._format_time(self.time_left_int))

    @Slot()
    def stop_bot(self):
        logger.info("Stopping bot")
        if self.worker:
            self.worker.terminate()
            self.worker.wait()
            self.worker.terminate()
        self.bot_thread_complete()
        self.bot_timer.stop()

    def _save_config(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Sauvegarder le fichier de config"
        )
        if folder:
            dlg = FileNameModal()
            if dlg.exec():
                save_config(dlg.filename, folder, self._dump_config())

    def _load_config(self):
        dialog = QFileDialog(self, "Choisir le fichier de config")
        filename, _ = dialog.getOpenFileName(self, filter="JSON files (*.json)")
        if filename:
            params = load_config(filename)
            self.key_model.commands = params.commands
            self.interval.setText(params.interval)
            self.limit.setText(str(params.limit))
            self.ui.winNum.setCurrentText(str(params.win_num))
            self.key_model.layoutChanged.emit()

    def _dump_config(self) -> Params:
        return Params(
            commands=self.key_model.commands,
            interval=self.interval.text(),
            limit=int(self.limit.text()),
            win_num=int(self.ui.winNum.currentText()),
        )

    def _show_logs(self):
        with open("nw-bot.log", "r") as log_file:
            logs = log_file.read()
            log_viewer = LogViewerModal(logs=logs)
            log_viewer.exec()

    @functools.lru_cache
    def _format_time(self, milliseconds: int) -> str:
        secs = milliseconds / 1000
        secs = secs % (24 * 3600)
        hours = secs // 3600
        secs %= 3600
        mins = secs // 60
        secs %= 60
        return f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}"
