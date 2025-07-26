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
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QListView, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionSaveConfig = QAction(MainWindow)
        self.actionSaveConfig.setObjectName(u"actionSaveConfig")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.actionSaveConfig.setIcon(icon)
        self.actionLoadConfig = QAction(MainWindow)
        self.actionLoadConfig.setObjectName(u"actionLoadConfig")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.actionLoadConfig.setIcon(icon1)
        self.actionShowLogs = QAction(MainWindow)
        self.actionShowLogs.setObjectName(u"actionShowLogs")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FormatJustifyLeft))
        self.actionShowLogs.setIcon(icon2)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 771, 561))
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
        self.winNum.setMinimumSize(QSize(100, 10))
        self.appVersion = QLabel(self.left)
        self.appVersion.setObjectName(u"appVersion")
        self.appVersion.setGeometry(QRect(20, 530, 231, 16))

        self.horizontalLayout.addWidget(self.left)

        self.middle = QWidget(self.horizontalLayoutWidget)
        self.middle.setObjectName(u"middle")
        self.startRecordButton = QPushButton(self.middle)
        self.startRecordButton.setObjectName(u"startRecordButton")
        self.startRecordButton.setGeometry(QRect(20, 10, 211, 24))
        self.startRecordButton.setMinimumSize(QSize(100, 10))
        self.stopRecordButton = QPushButton(self.middle)
        self.stopRecordButton.setObjectName(u"stopRecordButton")
        self.stopRecordButton.setEnabled(True)
        self.stopRecordButton.setGeometry(QRect(20, 10, 211, 24))
        self.stopRecordButton.setMinimumSize(QSize(100, 10))
        self.keyListView = QListView(self.middle)
        self.keyListView.setObjectName(u"keyListView")
        self.keyListView.setGeometry(QRect(20, 110, 211, 361))
        self.keyListView.setMinimumSize(QSize(100, 175))
        self.deleteKey = QPushButton(self.middle)
        self.deleteKey.setObjectName(u"deleteKey")
        self.deleteKey.setGeometry(QRect(20, 70, 211, 24))
        self.deleteKey.setMinimumSize(QSize(100, 10))
        self.deleteAll = QPushButton(self.middle)
        self.deleteAll.setObjectName(u"deleteAll")
        self.deleteAll.setGeometry(QRect(20, 40, 211, 24))
        self.deleteAll.setMinimumSize(QSize(100, 10))
        self.stopRecordButton.raise_()
        self.startRecordButton.raise_()
        self.keyListView.raise_()
        self.deleteKey.raise_()
        self.deleteAll.raise_()

        self.horizontalLayout.addWidget(self.middle)

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
        self.startButton = QPushButton(self.right)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setGeometry(QRect(10, 510, 121, 31))
        self.startButton.setMinimumSize(QSize(100, 10))
        self.stopButton = QPushButton(self.right)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setGeometry(QRect(140, 510, 101, 31))
        self.stopButton.setMinimumSize(QSize(100, 10))
        self.remainingTime = QLabel(self.right)
        self.remainingTime.setObjectName(u"remainingTime")
        self.remainingTime.setGeometry(QRect(170, 490, 49, 16))

        self.horizontalLayout.addWidget(self.right)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuParametres = QMenu(self.menubar)
        self.menuParametres.setObjectName(u"menuParametres")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuParametres.menuAction())
        self.menuParametres.addAction(self.actionSaveConfig)
        self.menuParametres.addAction(self.actionLoadConfig)
        self.menuParametres.addAction(self.actionShowLogs)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSaveConfig.setText(QCoreApplication.translate("MainWindow", u"Sauver la config", None))
        self.actionLoadConfig.setText(QCoreApplication.translate("MainWindow", u"Charger la config", None))
        self.actionShowLogs.setText(QCoreApplication.translate("MainWindow", u"Afficher le journal", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Nombre de fenetres", None))
        self.appVersion.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.startRecordButton.setText(QCoreApplication.translate("MainWindow", u"Demarrer l'enregistrement", None))
        self.stopRecordButton.setText(QCoreApplication.translate("MainWindow", u"Arreter l'enregistrement", None))
        self.deleteKey.setText(QCoreApplication.translate("MainWindow", u"Supprimer", None))
        self.deleteAll.setText(QCoreApplication.translate("MainWindow", u"Tout supprimer", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Intervale entre les touches", None))
        self.interval.setInputMask("")
        self.interval.setText("")
        self.interval.setPlaceholderText(QCoreApplication.translate("MainWindow", u"1 ou 1-5 pour aleatoire entre deux valeurs", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Limite de temps (en m)", None))
        self.limit.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Depart", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"Arret", None))
        self.remainingTime.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.menuParametres.setTitle(QCoreApplication.translate("MainWindow", u"Fichier", None))
    # retranslateUi

