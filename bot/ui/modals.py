from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
)

from bot.core.constants import DEFAULT_CONFIG_FILE
from bot.utils import logger


class FileNameModal(QDialog):
    def __init__(self):
        super().__init__()
        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("Nom du fichier de configuration:")
        layout.addWidget(message)
        self.fileNameEdit = QLineEdit()
        layout.addWidget(self.fileNameEdit)
        layout.addWidget(self.buttonBox)
        self.fileNameEdit.setText(DEFAULT_CONFIG_FILE)
        self.setLayout(layout)

    def accept(self):
        self.filename = self.fileNameEdit.text()
        if not self.filename:
            logger.error("Filename cannot be empty")
            return
        super().accept()


class LogViewerModal(QDialog):
    def __init__(self, logs: str = ""):
        super().__init__()
        self.setWindowTitle("Journal des logs")
        layout = QVBoxLayout()
        self.log_label = QLabel("Journal:")
        layout.addWidget(self.log_label)
        self.logText = QTextEdit()
        self.logText.setReadOnly(True)
        self.logText.setText(logs)
        layout.addWidget(self.logText)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        self.resize(800, 600)

