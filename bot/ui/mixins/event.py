from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QTimerEvent
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QMainWindow

from bot.core.constants import TIMER_TIMEOUT_MILLISEC
from bot.utils import format_time

from bot.ui.mixins.record import RecordingMode

if TYPE_CHECKING:
    from bot.core.keystroke_adapter import QtKeystrokeAdapter
    from bot.core.mouse_adapter import MouseAdapter
    from bot.models.command_list import CommandListModel
    from bot.ui.main_window_ui import Ui_MainWindow


class CommandManagementMixin(QMainWindow):
    """Handles command list mutation via UI buttons and the Delete key."""

    ui: "Ui_MainWindow"
    commandModel: "CommandListModel"

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
            index = indexes[0]
            del self.commandModel.commands[index.row()]
            self.commandModel.layoutChanged.emit()
            self.ui.keyListView.clearSelection()


class RecordingEventFilter(QMainWindow):
    """Intercepts Qt keyboard/mouse events during inside-window recording."""

    ui: "Ui_MainWindow"
    key_stroke_adapter: "QtKeystrokeAdapter"
    mouse_adapter: "MouseAdapter"
    recording_mode: RecordingMode

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.recording_mode is RecordingMode.INSIDE:
            self.key_stroke_adapter.on_key_release(event)
        if event.key() == Qt.Key.Key_Delete:
            self.deleteCommand()  # type: ignore[attr-defined]

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.recording_mode is RecordingMode.INSIDE:
            self.mouse_adapter.on_click(event.x(), event.y(), event.button(), True)

    def timerEvent(self, event: QTimerEvent) -> None:
        self.timeLeft -= TIMER_TIMEOUT_MILLISEC  # type: ignore[attr-defined]
        self.ui.remainingTime.setText(format_time(self.timeLeft))


EventMixin = type("EventMixin", (CommandManagementMixin, RecordingEventFilter), {})
