from dataclasses import dataclass, field

from pynput import keyboard, mouse

from bot.core.keystroke_adapter import BaseKeyStrokeAdapter, PynputKeystrokeAdapter
from bot.core.mouse_adapter import MouseAdapter
from bot.models import CommandListModel


@dataclass
class Recorder:
    model: CommandListModel
    keyBoardListener: keyboard.Listener = field(init=False)
    mouseListener: mouse.Listener = field(init=False)
    mouseAdapter: MouseAdapter = field(init=False)
    keyAdapter: BaseKeyStrokeAdapter = field(init=False)

    def __post_init__(self):
        self.mouseAdapter = MouseAdapter(self.model)
        self.keyAdapter = PynputKeystrokeAdapter(self.model)

    def start(self):
        self.keyBoardListener = keyboard.Listener(
            on_release=self.keyAdapter.on_key_release,
            on_press=self.keyAdapter.on_key_press,
        )
        self.keyBoardListener.start()
        self.mouseListener = mouse.Listener(on_click=self.mouseAdapter.on_click)
        self.mouseListener.start()
        self.keyBoardListener.wait()
        self.mouseListener.wait()

    def stop(self):
        if self.keyBoardListener and self.mouseListener:
            self.keyBoardListener.stop()
            try:
                self.mouseListener.stop()
            except Exception:
                # On Linux/Xvfb the Xlib display connection can be closed
                # before stop() is called — the listener is already stopped
                pass
