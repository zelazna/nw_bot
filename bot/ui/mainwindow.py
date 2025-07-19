# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QListView, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.nwbot_title = QLabel(self.centralwidget)
        self.nwbot_title.setObjectName(u"nwbot_title")
        self.nwbot_title.setGeometry(QRect(280, -40, 261, 121))
        font = QFont()
        font.setPointSize(34)
        font.setBold(True)
        self.nwbot_title.setFont(font)
        self.nwbot_title.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.nwbot_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 60, 771, 441))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.left = QWidget(self.horizontalLayoutWidget)
        self.left.setObjectName(u"left")
        self.label = QLabel(self.left)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 171, 16))
        self.winNum = QComboBox(self.left)
        self.winNum.setObjectName(u"winNum")
        self.winNum.setGeometry(QRect(10, 30, 201, 24))

        self.horizontalLayout.addWidget(self.left)

        self.widget_2 = QWidget(self.horizontalLayoutWidget)
        self.widget_2.setObjectName(u"widget_2")
        self.startRecordButton = QPushButton(self.widget_2)
        self.startRecordButton.setObjectName(u"startRecordButton")
        self.startRecordButton.setGeometry(QRect(20, 10, 211, 24))
        self.stopRecordButton = QPushButton(self.widget_2)
        self.stopRecordButton.setObjectName(u"stopRecordButton")
        self.stopRecordButton.setEnabled(True)
        self.stopRecordButton.setGeometry(QRect(20, 10, 211, 24))
        self.keyListView = QListView(self.widget_2)
        self.keyListView.setObjectName(u"keyListView")
        self.keyListView.setGeometry(QRect(20, 40, 211, 361))
        self.deleteKey = QPushButton(self.widget_2)
        self.deleteKey.setObjectName(u"deleteKey")
        self.deleteKey.setGeometry(QRect(20, 410, 211, 24))
        self.stopRecordButton.raise_()
        self.startRecordButton.raise_()
        self.keyListView.raise_()
        self.deleteKey.raise_()

        self.horizontalLayout.addWidget(self.widget_2)

        self.right = QWidget(self.horizontalLayoutWidget)
        self.right.setObjectName(u"right")
        self.label_2 = QLabel(self.right)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 0, 141, 31))
        self.interval = QLineEdit(self.right)
        self.interval.setObjectName(u"interval")
        self.interval.setGeometry(QRect(10, 30, 231, 24))
        self.label_3 = QLabel(self.right)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 60, 131, 16))
        self.limit = QLineEdit(self.right)
        self.limit.setObjectName(u"limit")
        self.limit.setGeometry(QRect(10, 80, 231, 24))

        self.horizontalLayout.addWidget(self.right)

        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setGeometry(QRect(530, 540, 121, 24))
        self.stopButton = QPushButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setGeometry(QRect(670, 540, 101, 24))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.nwbot_title.setText(QCoreApplication.translate("MainWindow", u"NW BOT", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Nombre de fenetres", None))
        self.startRecordButton.setText(QCoreApplication.translate("MainWindow", u"Demarrer l'enregistrement", None))
        self.stopRecordButton.setText(QCoreApplication.translate("MainWindow", u"Arreter l'enregistrement", None))
        self.deleteKey.setText(QCoreApplication.translate("MainWindow", u"Supprimer", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Intervale entre les touches", None))
        self.interval.setText("")
        self.interval.setPlaceholderText(QCoreApplication.translate("MainWindow", u"1 ou 1-5 pour aleatoire entre deux valeurs", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Limite de temps (en m)", None))
        self.limit.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Depart", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"Arret", None))
    # retranslateUi

