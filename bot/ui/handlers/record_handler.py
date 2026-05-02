import functools
from enum import Enum, auto
from typing import TYPE_CHECKING, final

if TYPE_CHECKING:
    from bot.core.recorder import Recorder
    from bot.ui.main_window_ui import Ui_MainWindow


class RecordingMode(Enum):
    IDLE = auto()
    INSIDE = auto()
    OUTSIDE = auto()


@final
class RecordHandler:
    _OUTSIDE_BUTTON_STYLE: str = "background-color: #0067c0; color:white;"
    _ui: "Ui_MainWindow"
    _recorder: "Recorder"
    mode: RecordingMode

    def __init__(self, ui: "Ui_MainWindow", recorder: "Recorder") -> None:
        self._ui = ui
        self._recorder = recorder
        self.mode = RecordingMode.IDLE

        ui.startRecordButton.clicked.connect(
            functools.partial(self.toggle_keystrokes, True)
        )
        ui.stopRecordButton.clicked.connect(
            functools.partial(self.toggle_keystrokes, False)
        )
        ui.startRecordOutsideButton.clicked.connect(self.start_outside)
        ui.stopRecordOutsideButton.clicked.connect(self.stop_outside)
        ui.startRecordOutsideButton.setStyleSheet(self._OUTSIDE_BUTTON_STYLE)
        ui.stopRecordOutsideButton.setStyleSheet(self._OUTSIDE_BUTTON_STYLE)

    def toggle_keystrokes(self, state: bool) -> None:
        self._ui.recordStack.setCurrentIndex(1 if state else 0)
        self.mode = RecordingMode.INSIDE if state else RecordingMode.IDLE

    def start_outside(self) -> None:
        self._recorder.start()
        self.mode = RecordingMode.OUTSIDE
        self._ui.recordStack.setCurrentIndex(3)

    def stop_outside(self) -> None:
        self._ui.recordStack.setCurrentIndex(2)
        self._recorder.stop()
        self.mode = RecordingMode.IDLE

    def toggle_outside(self, checked: bool) -> None:
        if self.mode is RecordingMode.INSIDE:
            self.toggle_keystrokes(False)
        self._ui.recordStack.setCurrentIndex(2 if checked else 0)
