import logging

from pynput.mouse import Button

from bot.core.constants import APP_NAME
from bot.core.recorder import Recorder
from bot.models import CommandListModel


def test_recorder():
    recorder = Recorder(CommandListModel())
    recorder.start()
    assert recorder.keyBoardListener.running is True
    assert recorder.mouseListener.running is True

    recorder.stop()
    assert recorder.keyBoardListener.running is False
    assert recorder.mouseListener.running is False


def test_record_errors(caplog):
    recorder = Recorder(CommandListModel())
    recorder.onClick(1, 2, Button.middle, True)
    assert caplog.record_tuples == [
        (APP_NAME, logging.ERROR, "Unknow button Button.middle")
    ]
