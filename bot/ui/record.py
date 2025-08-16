import functools
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from bot.ui import MainWindow

OUTSIDE_BUTTON_STYLE = "background-color: #0067c0; color:white;"


def setupRecording(window: "MainWindow"):
    window.ui.stopRecordButton.setVisible(False)
    window.ui.startRecordButton.clicked.connect(
        functools.partial(window.toggleRecordKeystrokes, True)
    )
    window.ui.stopRecordButton.clicked.connect(
        functools.partial(window.toggleRecordKeystrokes, False)
    )

    window.ui.startRecordOutsideButton.clicked.connect(window.startRecordOutside)
    window.ui.stopRecordOutsideButton.clicked.connect(window.stopRecordOutside)
    window.ui.startRecordOutsideButton.setStyleSheet(OUTSIDE_BUTTON_STYLE)
    window.ui.stopRecordOutsideButton.setStyleSheet(OUTSIDE_BUTTON_STYLE)
    window.ui.startRecordOutsideButton.setVisible(False)
    window.ui.stopRecordOutsideButton.setVisible(False)
