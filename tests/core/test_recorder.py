import logging
from bot.core.recorder import Recorder
from pynput.mouse import Button

from bot.models import CommandListModel


def test_recorder():
    recorder = Recorder(CommandListModel())
    assert recorder.keyBoardListener is None
    assert recorder.mouseListener is None
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
        ("bot.utils.logger", logging.ERROR, "Unknow button Button.middle")
    ]
