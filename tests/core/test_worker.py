import logging
from unittest.mock import Mock

from bot.core.constants import APP_NAME
from bot.core.worker import Worker


def test_worker(params_factory, signals):
    mock = Mock()
    params = params_factory()
    worker = Worker(mock, params)
    worker.signals = signals
    worker.run()
    mock.assert_called_once_with(params, signals)
    signals.result.emit.assert_called_once()
    signals.finished.emit.assert_called_once()


def test_worker_errors(params_factory, caplog, signals):
    mock = Mock(side_effect=Exception("Boom"))
    params = params_factory()
    worker = Worker(mock, params)
    worker.signals = signals
    worker.run()
    assert caplog.record_tuples == [
        (
            APP_NAME,
            logging.ERROR,
            "Something went wrong",
        )
    ]
    signals.finished.emit.assert_called_once()
