import logging
from unittest.mock import Mock
from bot.core.recorder import Recorder
from pynput.mouse import Button

from bot.models import CommandsModel


def test_recorder():
    recorder = Recorder()
    recorder.signals = Mock()
    recorder.onClick(1, 2, Button.left, True)
    recorder.signals.interaction.emit.assert_called_once()

    assert recorder.keyBoardListener is None
    assert recorder.mouseListener is None
    recorder.start(CommandsModel())
    assert recorder.keyBoardListener.running is True
    assert recorder.mouseListener.running is True

    recorder.stop()
    assert recorder.keyBoardListener.running is False
    assert recorder.mouseListener.running is False


def test_record_errors(caplog):
    recorder = Recorder()
    recorder.onClick(1, 2, Button.middle, True)
    assert caplog.record_tuples == [
        ("bot.utils.logger", logging.ERROR, "Unknow button Button.middle")
    ]
