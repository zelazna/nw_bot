from pynput.mouse import Button as PynputButton
from PySide6.QtCore import Qt
import pytest

from bot.core.mouse_adapter import MouseAdapter
from bot.models import Button, CommandListModel, MouseClick


@pytest.mark.parametrize(
    ("button", "kind"),
    [
        (PynputButton.left, Button.left),
        (PynputButton.right, Button.right),
        (Qt.MouseButton.RightButton, Button.right),
        (Qt.MouseButton.LeftButton, Button.left),
    ],
)
def test_adapter(button, kind):
    model = CommandListModel()
    adapter = MouseAdapter(model)
    adapter.on_click(1, 2, button, True)
    assert model.rowCount() == 1
    assert isinstance(model.commands[0], MouseClick)
    assert model.commands[0].kind == kind
