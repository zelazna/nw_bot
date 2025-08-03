from pynput.mouse import Button as PynputButton
from PySide6.QtCore import Qt
import pytest

from bot.core.mouse_adapter import PynputMouseAdapter, QtMouseAdapter
from bot.models import Button, CommandListModel, MouseClick


@pytest.mark.parametrize(
    ("adapter", "button", "kind"),
    [
        (PynputMouseAdapter, PynputButton.left, Button.left),
        (PynputMouseAdapter, PynputButton.right, Button.right),
        (QtMouseAdapter, Qt.MouseButton.RightButton, Button.right),
        (QtMouseAdapter, Qt.MouseButton.LeftButton, Button.left),
    ],
)
def test_adapter(adapter, button, kind):
    model = CommandListModel()
    adapter = adapter(model)
    adapter.on_click(1, 2, button, True)
    assert len(model.commands) == 1
    assert isinstance(model.commands[0], MouseClick)
    assert model.commands[0].kind == kind
