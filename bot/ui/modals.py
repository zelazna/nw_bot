from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout

from bot.ui.mainwindow import QLineEdit
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
        self.file_name_edit = QLineEdit()
        layout.addWidget(self.file_name_edit)
        layout.addWidget(self.buttonBox)
        self.file_name_edit.setText("nwbot_config.json")
        self.setLayout(layout)

    def accept(self):
        self.filename = self.file_name_edit.text()
        if not self.filename:
            logger.error("Filename cannot be empty")
            return
        super().accept()
