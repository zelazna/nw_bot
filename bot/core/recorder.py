from pynput import keyboard, mouse

from bot.core.keystroke_adapter import (
    PynputKeystrokeAdapter,
)
from bot.core.mouse_adapter import MouseAdapter
from bot.models import CommandListModel


class Recorder:
    def __init__(self, model: CommandListModel) -> None:
        self.model = model
        self.keyBoardListener: keyboard.Listener = None  # type: ignore
        self.mouseListener: mouse.Listener = None  # type: ignore
        self.mouse_adapter = MouseAdapter(model)
        self.key_adapter = PynputKeystrokeAdapter(model)

    def onClick(self, x: int, y: int, button: mouse.Button, pressed: bool):
        self.mouse_adapter.on_click(x, y, button, pressed)

    def start(self):
        self.keyBoardListener = keyboard.Listener(
            on_release=self.key_adapter.on_key_release,
            on_press=self.key_adapter.on_key_press,
        )
        self.keyBoardListener.start()
        self.mouseListener = mouse.Listener(on_click=self.onClick)
        self.mouseListener.start()

    def stop(self):
        if self.keyBoardListener and self.mouseListener:
            self.keyBoardListener.stop()
            self.mouseListener.stop()
