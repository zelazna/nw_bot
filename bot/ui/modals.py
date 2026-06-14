import logging
from typing import final, override

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from bot.core.constants import DEFAULT_CONFIG_FILE, VERSION


@final
class FileNameModal(QDialog):
    buttonBox: QDialogButtonBox
    fileNameEdit: QLineEdit

    def __init__(self) -> None:
        super().__init__()
        self.filename: str = ""
        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(
            QCoreApplication.translate("FileNameModal", "Configuration file name:")
        )
        layout.addWidget(message)
        self.fileNameEdit = QLineEdit()
        layout.addWidget(self.fileNameEdit)
        layout.addWidget(self.buttonBox)
        self.fileNameEdit.setText(DEFAULT_CONFIG_FILE)
        self.setLayout(layout)

    @override
    def accept(self) -> None:
        self.filename = self.fileNameEdit.text()
        if not self.filename:
            return
        super().accept()


@final
class LogDialog(QDialog):
    logs: list[tuple[str, int]]
    current_filter: int
    filter_combo: QComboBox
    text_edit: QPlainTextEdit

    def __init__(
        self, logs: list[tuple[str, int]], parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"Logs ({VERSION})")
        self.resize(700, 500)

        self.logs = logs
        self.current_filter = 0

        layout = QVBoxLayout(self)

        control_layout = QHBoxLayout()
        control_layout.addWidget(
            QLabel(QCoreApplication.translate("LogDialog", "Filter:"))
        )
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(
            [
                QCoreApplication.translate("LogDialog", "All"),
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
            ]
        )
        self.filter_combo.currentIndexChanged.connect(self.refresh_logs)
        layout.addLayout(control_layout)

        self.text_edit = QPlainTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.refresh_logs()

    def should_display(self, levelno: int) -> bool:
        if self.current_filter == 0:
            return True
        filter_levels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]
        return levelno >= filter_levels[self.current_filter - 1]

    def refresh_logs(self) -> None:
        self.current_filter = self.filter_combo.currentIndex()
        self.text_edit.clear()

        color_map = {
            logging.DEBUG: "#808080",
            logging.INFO: "#000000",
            logging.WARNING: "#FFA500",
            logging.ERROR: "#FF9900",
            logging.CRITICAL: "#FA0505",
        }

        for msg, level in self.logs:
            if self.should_display(level):
                color = color_map.get(level, "#000000")
                self.text_edit.appendHtml(f'<span style="color:{color}">{msg}</span>')
