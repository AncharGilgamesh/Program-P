# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'workspace.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(561, 458)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lkButton = QPushButton(self.centralwidget)
        self.lkButton.setObjectName(u"lkButton")
        self.lkButton.setMinimumSize(QSize(150, 150))

        self.horizontalLayout.addWidget(self.lkButton)

        self.genOtchButton = QPushButton(self.centralwidget)
        self.genOtchButton.setObjectName(u"genOtchButton")
        self.genOtchButton.setMinimumSize(QSize(150, 150))

        self.horizontalLayout.addWidget(self.genOtchButton)

        self.genPlanButton = QPushButton(self.centralwidget)
        self.genPlanButton.setObjectName(u"genPlanButton")
        self.genPlanButton.setMinimumSize(QSize(150, 150))

        self.horizontalLayout.addWidget(self.genPlanButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.databaseButton = QPushButton(self.centralwidget)
        self.databaseButton.setObjectName(u"databaseButton")
        self.databaseButton.setMinimumSize(QSize(150, 150))

        self.horizontalLayout_2.addWidget(self.databaseButton)

        self.faqButton = QPushButton(self.centralwidget)
        self.faqButton.setObjectName(u"faqButton")
        self.faqButton.setMinimumSize(QSize(0, 150))

        self.horizontalLayout_2.addWidget(self.faqButton)

        self.exitButton = QPushButton(self.centralwidget)
        self.exitButton.setObjectName(u"exitButton")
        self.exitButton.setMinimumSize(QSize(0, 150))

        self.horizontalLayout_2.addWidget(self.exitButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 561, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lkButton.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0447\u043d\u044b\u0439 \u043a\u0430\u0431\u0438\u043d\u0435\u0442", None))
        self.genOtchButton.setText(QCoreApplication.translate("MainWindow", u"\u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f \u043e\u0442\u0447\u0435\u0442\u0430", None))
        self.genPlanButton.setText(QCoreApplication.translate("MainWindow", u"\u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f \u043f\u043b\u0430\u043d\u0430", None))
        self.databaseButton.setText(QCoreApplication.translate("MainWindow", u"\u0411\u0430\u0437\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.faqButton.setText(QCoreApplication.translate("MainWindow", u"F.A.Q", None))
        self.exitButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434", None))
    # retranslateUi

