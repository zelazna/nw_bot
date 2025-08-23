import functools
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from bot.core.recorder import Recorder
    from bot.ui.main_window_ui import Ui_MainWindow

OUTSIDE_BUTTON_STYLE = "background-color: #0067c0; color:white;"


class RecordMixin:
    ui: "Ui_MainWindow"
    recorder: "Recorder"

    def setupRecording(self):
        self.ui.stopRecordButton.setVisible(False)
        self.ui.startRecordButton.clicked.connect(
            functools.partial(self.toggleRecordKeystrokes, True)
        )
        self.ui.stopRecordButton.clicked.connect(
            functools.partial(self.toggleRecordKeystrokes, False)
        )

        self.ui.startRecordOutsideButton.clicked.connect(self.startRecordOutside)
        self.ui.stopRecordOutsideButton.clicked.connect(self.stopRecordOutside)
        self.ui.startRecordOutsideButton.setStyleSheet(OUTSIDE_BUTTON_STYLE)
        self.ui.stopRecordOutsideButton.setStyleSheet(OUTSIDE_BUTTON_STYLE)
        self.ui.startRecordOutsideButton.setVisible(False)
        self.ui.stopRecordOutsideButton.setVisible(False)

    def toggleRecordKeystrokes(self, state: bool):
        self.ui.startRecordButton.setVisible(not state)
        self.ui.stopRecordButton.setVisible(state)
        self.isRecording = state

    def startRecordOutside(self):
        self.recorder.start()
        self.isRecording = False
        self.ui.startRecordOutsideButton.setVisible(False)
        self.ui.stopRecordOutsideButton.setVisible(True)

    def stopRecordOutside(self):
        self.ui.startRecordOutsideButton.setVisible(True)
        self.ui.stopRecordOutsideButton.setVisible(False)
        self.recorder.stop()

    def toggleOutsideRecord(self, checked: bool):
        if self.isRecording:
            self.toggleRecordKeystrokes(False)
        self.ui.startRecordButton.setVisible(not checked)
        self.ui.startRecordOutsideButton.setVisible(checked)
