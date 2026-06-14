# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QListView, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(540, 560)
        MainWindow.setMinimumSize(QSize(460, 380))
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
        self.actionUnboundRecordToggle = QAction(MainWindow)
        self.actionUnboundRecordToggle.setObjectName(u"actionUnboundRecordToggle")
        self.actionUnboundRecordToggle.setCheckable(True)
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaRecord))
        self.actionUnboundRecordToggle.setIcon(icon3)
        self.actionSaveAs = QAction(MainWindow)
        self.actionSaveAs.setObjectName(u"actionSaveAs")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSaveAs))
        self.actionSaveAs.setIcon(icon4)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralLayout = QVBoxLayout(self.centralwidget)
        self.centralLayout.setSpacing(8)
        self.centralLayout.setObjectName(u"centralLayout")
        self.centralLayout.setContentsMargins(10, 10, 10, 10)
        self.contentLayout = QHBoxLayout()
        self.contentLayout.setSpacing(12)
        self.contentLayout.setObjectName(u"contentLayout")
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setSpacing(6)
        self.leftLayout.setObjectName(u"leftLayout")
        self.recordStack = QStackedWidget(self.centralwidget)
        self.recordStack.setObjectName(u"recordStack")
        self.recordStack.setMaximumSize(QSize(16777215, 28))
        self.page_start = QWidget()
        self.page_start.setObjectName(u"page_start")
        self.page_startLayout = QVBoxLayout(self.page_start)
        self.page_startLayout.setObjectName(u"page_startLayout")
        self.page_startLayout.setContentsMargins(0, 0, 0, 0)
        self.startRecordButton = QPushButton(self.page_start)
        self.startRecordButton.setObjectName(u"startRecordButton")

        self.page_startLayout.addWidget(self.startRecordButton)

        self.recordStack.addWidget(self.page_start)
        self.page_stop = QWidget()
        self.page_stop.setObjectName(u"page_stop")
        self.page_stopLayout = QVBoxLayout(self.page_stop)
        self.page_stopLayout.setObjectName(u"page_stopLayout")
        self.page_stopLayout.setContentsMargins(0, 0, 0, 0)
        self.stopRecordButton = QPushButton(self.page_stop)
        self.stopRecordButton.setObjectName(u"stopRecordButton")

        self.page_stopLayout.addWidget(self.stopRecordButton)

        self.recordStack.addWidget(self.page_stop)
        self.page_startOutside = QWidget()
        self.page_startOutside.setObjectName(u"page_startOutside")
        self.page_startOutsideLayout = QVBoxLayout(self.page_startOutside)
        self.page_startOutsideLayout.setObjectName(u"page_startOutsideLayout")
        self.page_startOutsideLayout.setContentsMargins(0, 0, 0, 0)
        self.startRecordOutsideButton = QPushButton(self.page_startOutside)
        self.startRecordOutsideButton.setObjectName(u"startRecordOutsideButton")

        self.page_startOutsideLayout.addWidget(self.startRecordOutsideButton)

        self.recordStack.addWidget(self.page_startOutside)
        self.page_stopOutside = QWidget()
        self.page_stopOutside.setObjectName(u"page_stopOutside")
        self.page_stopOutsideLayout = QVBoxLayout(self.page_stopOutside)
        self.page_stopOutsideLayout.setObjectName(u"page_stopOutsideLayout")
        self.page_stopOutsideLayout.setContentsMargins(0, 0, 0, 0)
        self.stopRecordOutsideButton = QPushButton(self.page_stopOutside)
        self.stopRecordOutsideButton.setObjectName(u"stopRecordOutsideButton")

        self.page_stopOutsideLayout.addWidget(self.stopRecordOutsideButton)

        self.recordStack.addWidget(self.page_stopOutside)

        self.leftLayout.addWidget(self.recordStack)

        self.deleteAll = QPushButton(self.centralwidget)
        self.deleteAll.setObjectName(u"deleteAll")

        self.leftLayout.addWidget(self.deleteAll)

        self.deleteKey = QPushButton(self.centralwidget)
        self.deleteKey.setObjectName(u"deleteKey")

        self.leftLayout.addWidget(self.deleteKey)

        self.keyListView = QListView(self.centralwidget)
        self.keyListView.setObjectName(u"keyListView")

        self.leftLayout.addWidget(self.keyListView)


        self.contentLayout.addLayout(self.leftLayout)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.contentLayout.addWidget(self.line)

        self.rightLayout = QVBoxLayout()
        self.rightLayout.setSpacing(4)
        self.rightLayout.setObjectName(u"rightLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.rightLayout.addWidget(self.label_2)

        self.interval = QLineEdit(self.centralwidget)
        self.interval.setObjectName(u"interval")

        self.rightLayout.addWidget(self.interval)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.rightLayout.addWidget(self.label_3)

        self.limit = QLineEdit(self.centralwidget)
        self.limit.setObjectName(u"limit")

        self.rightLayout.addWidget(self.limit)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.rightLayout.addWidget(self.label)

        self.winNum = QComboBox(self.centralwidget)
        self.winNum.setObjectName(u"winNum")

        self.rightLayout.addWidget(self.winNum)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightLayout.addItem(self.verticalSpacer)


        self.contentLayout.addLayout(self.rightLayout)


        self.centralLayout.addLayout(self.contentLayout)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setSpacing(8)
        self.bottomLayout.setObjectName(u"bottomLayout")
        self.appVersion = QLabel(self.centralwidget)
        self.appVersion.setObjectName(u"appVersion")

        self.bottomLayout.addWidget(self.appVersion)

        self.bottomSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomLayout.addItem(self.bottomSpacer)

        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setMinimumSize(QSize(90, 0))

        self.bottomLayout.addWidget(self.startButton)

        self.remainingTime = QLabel(self.centralwidget)
        self.remainingTime.setObjectName(u"remainingTime")
        self.remainingTime.setMinimumSize(QSize(68, 0))
        self.remainingTime.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.bottomLayout.addWidget(self.remainingTime)

        self.stopButton = QPushButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setMinimumSize(QSize(90, 0))

        self.bottomLayout.addWidget(self.stopButton)


        self.centralLayout.addLayout(self.bottomLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 540, 21))
        self.menuParametres = QMenu(self.menubar)
        self.menuParametres.setObjectName(u"menuParametres")
        self.menuRecent = QMenu(self.menuParametres)
        self.menuRecent.setObjectName(u"menuRecent")
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setObjectName(u"menuOptions")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuParametres.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menuParametres.addAction(self.actionLoadConfig)
        self.menuParametres.addAction(self.actionSaveConfig)
        self.menuParametres.addAction(self.actionSaveAs)
        self.menuParametres.addAction(self.actionShowLogs)
        self.menuParametres.addAction(self.menuRecent.menuAction())
        self.menuOptions.addAction(self.actionUnboundRecordToggle)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSaveConfig.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(tooltip)
        self.actionSaveConfig.setToolTip(QCoreApplication.translate("MainWindow", u"Save config", None))
#endif // QT_CONFIG(tooltip)
        self.actionLoadConfig.setText(QCoreApplication.translate("MainWindow", u"Load config", None))
        self.actionShowLogs.setText(QCoreApplication.translate("MainWindow", u"Show logs", None))
        self.actionUnboundRecordToggle.setText(QCoreApplication.translate("MainWindow", u"Record outside", None))
        self.actionSaveAs.setText(QCoreApplication.translate("MainWindow", u"Save as", None))
        self.startRecordButton.setText(QCoreApplication.translate("MainWindow", u"Start recording", None))
        self.stopRecordButton.setText(QCoreApplication.translate("MainWindow", u"Stop recording", None))
        self.startRecordOutsideButton.setText(QCoreApplication.translate("MainWindow", u"Start recording", None))
        self.stopRecordOutsideButton.setText(QCoreApplication.translate("MainWindow", u"Stop recording", None))
        self.deleteAll.setText(QCoreApplication.translate("MainWindow", u"Delete all", None))
        self.deleteKey.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Interval between keystrokes", None))
        self.interval.setText("")
        self.interval.setPlaceholderText(QCoreApplication.translate("MainWindow", u"1 or 1-5 for a random value between two", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Time limit (in m)", None))
        self.limit.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Number of windows", None))
        self.appVersion.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.remainingTime.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.menuParametres.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuRecent.setTitle(QCoreApplication.translate("MainWindow", u"Recent", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi
