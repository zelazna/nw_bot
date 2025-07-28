from typing import Callable
from unittest.mock import Mock
from bot.core.worker import Worker
from bot.models import Params


def test_worker(params_factory: Callable[[], Params]):
    mock = Mock()
    params = params_factory()
    signal_mock = Mock()
    worker = Worker(mock, params)
    worker.signals = signal_mock
    worker.run()
    mock.assert_called_once_with(params)
    signal_mock.result.emit.assert_called_once()
    signal_mock.finished.emit.assert_called_once()


def test_worker_errors(params_factory: Callable[[], Params]):
    mock = Mock(side_effect=Exception)
    params = params_factory()
    worker = Worker(mock, params)
    signal_mock = Mock()
    worker.signals = signal_mock
    worker.run()
    signal_mock.error.emit.assert_called_once()
    signal_mock.finished.emit.assert_called_once()
