from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QTimerEvent

from bot.core.constants import TIMER_TIMEOUT_MILLISEC
from bot.core.keystroke_adapter import QtKeystrokeAdapter
from bot.core.mouse_adapter import MouseAdapter
from bot.core.recorder import Recorder
from bot.models import CommandListModel
from bot.ui.main_window_ui import Ui_MainWindow
from bot.utils import format_time

if TYPE_CHECKING:
    from bot.core.keystroke_adapter import QtKeystrokeAdapter
    from bot.core.mouse_adapter import MouseAdapter
    from bot.core.recorder import Recorder
    from bot.models.command_list import CommandListModel
    from bot.ui.main_window_ui import Ui_MainWindow


class EventMixin(QMainWindow):
    ui: "Ui_MainWindow"
    recorder: "Recorder"
    commandModel: "CommandListModel"
    key_stroke_adapter: "QtKeystrokeAdapter"
    mouse_adapter: "MouseAdapter"
    isRecording: bool

    def setupEvents(self):
        self.ui.deleteKey.clicked.connect(self.deleteCommand)
        self.ui.deleteAll.clicked.connect(self.deleteAllKeys)
        self.ui.remainingTime.setVisible(False)

    def deleteAllKeys(self):
        self.commandModel.commands.clear()
        self.commandModel.layoutChanged.emit()
        self.ui.keyListView.clearSelection()

    def deleteCommand(self):
        indexes = self.ui.keyListView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.commandModel.commands[index.row()]
            self.commandModel.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.ui.keyListView.clearSelection()

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.isRecording:
            self.key_stroke_adapter.on_key_release(event)
        if event.key() == Qt.Key.Key_Delete:
            self.deleteCommand()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.isRecording:
            self.mouse_adapter.on_click(event.x(), event.y(), event.button(), True)

    def timerEvent(self, event: QTimerEvent) -> None:
        self.timeLeft -= TIMER_TIMEOUT_MILLISEC  # Decrease by 0.5 second
        self.ui.remainingTime.setText(format_time(self.timeLeft))
