import functools
from enum import Enum, auto
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from bot.core.recorder import Recorder
    from bot.ui.main_window_ui import Ui_MainWindow


class RecordingMode(Enum):
    IDLE = auto()
    INSIDE = auto()
    OUTSIDE = auto()


class RecordMixin:
    ui: "Ui_MainWindow"
    recorder: "Recorder"
    recording_mode: RecordingMode
    outside_button_style = "background-color: #0067c0; color:white;"

    def setupRecording(self):
        self.ui.startRecordButton.clicked.connect(
            functools.partial(self.toggleRecordKeystrokes, True)
        )
        self.ui.stopRecordButton.clicked.connect(
            functools.partial(self.toggleRecordKeystrokes, False)
        )
        self.ui.startRecordOutsideButton.clicked.connect(self.startRecordOutside)
        self.ui.stopRecordOutsideButton.clicked.connect(self.stopRecordOutside)
        self.ui.startRecordOutsideButton.setStyleSheet(self.outside_button_style)
        self.ui.stopRecordOutsideButton.setStyleSheet(self.outside_button_style)

    def toggleRecordKeystrokes(self, state: bool):
        self.ui.recordStack.setCurrentIndex(1 if state else 0)
        self.recording_mode = RecordingMode.INSIDE if state else RecordingMode.IDLE

    def startRecordOutside(self):
        self.recorder.start()
        self.recording_mode = RecordingMode.OUTSIDE
        self.ui.recordStack.setCurrentIndex(3)

    def stopRecordOutside(self):
        self.ui.recordStack.setCurrentIndex(2)
        self.recorder.stop()
        self.recording_mode = RecordingMode.IDLE

    def toggleOutsideRecord(self, checked: bool):
        if self.recording_mode is RecordingMode.INSIDE:
            self.toggleRecordKeystrokes(False)
        self.ui.recordStack.setCurrentIndex(2 if checked else 0)
