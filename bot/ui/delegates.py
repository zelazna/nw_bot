from typing import Protocol, final, override

from PySide6.QtCore import QModelIndex, QPersistentModelIndex, QRect, QSize, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPalette, QPen
from PySide6.QtWidgets import QStyle, QStyledItemDelegate, QStyleOptionViewItem

from bot.models import Command
from bot.models.keyboard import DirectionalKeystroke, Keystroke
from bot.models.mouse import MouseClick

_COLOR_KEY = QColor("#4FC3F7")
_COLOR_DIR = QColor("#CE93D8")
_COLOR_MOUSE = QColor("#FFB74D")
_COLOR_BG_SELECTED = QColor("#3a3a5a")
_COLOR_TEXT_BADGE = QColor("#ffffff")
_COLOR_TEXT_SECONDARY = QColor("#888888")

_ROW_HEIGHT = 40
_BADGE_H = 24
_BADGE_RADIUS = 6
_PADDING_LEFT = 10
_BADGE_HPAD = 10


class _FullStyleOption(Protocol):
    """Attributes that QStyleOption exposes at runtime but are absent from PySide6 stubs."""

    @property
    def rect(self) -> QRect: ...
    @property
    def state(
        self,
    ) -> QStyle.StateFlag: ...  # QStyle.State (QFlags) not in PySide6 stubs
    @property
    def palette(self) -> QPalette: ...
    @property
    def font(self) -> QFont: ...


def _badge_color(command: Command) -> QColor:
    if isinstance(command, DirectionalKeystroke):
        return _COLOR_DIR
    if isinstance(command, Keystroke):
        return _COLOR_KEY
    if isinstance(command, MouseClick):
        return _COLOR_MOUSE
    return _COLOR_KEY


def _badge_label(command: Command) -> str:
    if isinstance(command, Keystroke):
        try:
            key_repr = command.key.split("_")[1]
        except IndexError:
            key_repr = command.key
        if command.modifier:
            return f"{command.modifier!r}+{key_repr.upper()}"
        return key_repr.upper()
    if isinstance(command, DirectionalKeystroke):
        return command.key.upper()
    if isinstance(command, MouseClick):
        return f"{command.kind.name.upper()} CLICK"
    return repr(command)


def _secondary_text(command: Command) -> str:
    if isinstance(command, (Keystroke, DirectionalKeystroke)):
        return f"{command.hold.milliseconds} ms"
    if isinstance(command, MouseClick):
        return f"{command.pos}"
    return ""


@final
class CommandDelegate(QStyledItemDelegate):
    @override
    def sizeHint(
        self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex
    ) -> QSize:
        hint = super().sizeHint(option, index)
        hint.setHeight(_ROW_HEIGHT)
        return hint

    @override
    def paint(
        self,
        painter: QPainter | None,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        if painter is None:
            return
        painter.save()

        opt: _FullStyleOption = option  # pyright: ignore[reportAssignmentType]
        rect: QRect = opt.rect

        # Background
        if opt.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(rect, _COLOR_BG_SELECTED)
        else:
            painter.fillRect(rect, opt.palette.base())

        command: Command | None = index.data(Qt.ItemDataRole.UserRole)  # pyright: ignore[reportAny]
        if command is None:
            painter.restore()
            return

        color = _badge_color(command)
        label = _badge_label(command)
        secondary = _secondary_text(command)

        # Measure badge width
        badge_font = QFont(opt.font)
        badge_font.setBold(True)
        badge_font.setPointSize(badge_font.pointSize() - 1)
        painter.setFont(badge_font)
        fm = painter.fontMetrics()
        label_w = fm.horizontalAdvance(label)
        badge_w = label_w + _BADGE_HPAD * 2

        badge_x = rect.x() + _PADDING_LEFT
        badge_y = rect.y() + (rect.height() - _BADGE_H) // 2
        badge_rect = QRect(badge_x, badge_y, badge_w, _BADGE_H)

        # Draw badge
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawRoundedRect(badge_rect, _BADGE_RADIUS, _BADGE_RADIUS)

        # Draw badge text
        painter.setPen(QPen(_COLOR_TEXT_BADGE))
        painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, label)

        # Draw secondary text
        if secondary:
            secondary_font = QFont(opt.font)
            secondary_font.setPointSize(secondary_font.pointSize() - 1)
            painter.setFont(secondary_font)
            painter.setPen(QPen(_COLOR_TEXT_SECONDARY))
            text_x = badge_x + badge_w + 10
            text_rect = QRect(
                text_x, rect.y(), rect.right() - text_x - 4, rect.height()
            )
            painter.drawText(
                text_rect,
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                secondary,
            )

        painter.restore()
