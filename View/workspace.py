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
    QPushButton, QSizePolicy, QStackedWidget, QStatusBar,
    QToolButton, QVBoxLayout, QWidget)
import View.res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1061, 642)
        MainWindow.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(81, 0, 135, 255), stop:0.427447 rgba(41, 61, 132, 235), stop:1 rgba(155, 79, 165, 255));\n"
"font-family: Consolas;")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainStackedWidget = QStackedWidget(self.centralwidget)
        self.mainStackedWidget.setObjectName(u"mainStackedWidget")
        self.mainStackedWidget.setGeometry(QRect(410, 10, 641, 591))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.loadTableButton = QPushButton(self.page)
        self.loadTableButton.setObjectName(u"loadTableButton")
        self.loadTableButton.setGeometry(QRect(30, 20, 171, 81))
        self.loadNagruzkaButton = QPushButton(self.page)
        self.loadNagruzkaButton.setObjectName(u"loadNagruzkaButton")
        self.loadNagruzkaButton.setGeometry(QRect(220, 20, 171, 81))
        self.mainStackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.mainStackedWidget.addWidget(self.page_2)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 29, 381, 471))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cabinetToolButton = QToolButton(self.widget)
        self.cabinetToolButton.setObjectName(u"cabinetToolButton")
        self.cabinetToolButton.setMinimumSize(QSize(150, 100))
        self.cabinetToolButton.setStyleSheet(u"color: white;\n"
"font-size: 16pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon = QIcon()
        icon.addFile(u":/icon/icons/cabinet.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cabinetToolButton.setIcon(icon)
        self.cabinetToolButton.setIconSize(QSize(48, 48))
        self.cabinetToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.cabinetToolButton.setAutoRaise(True)

        self.horizontalLayout.addWidget(self.cabinetToolButton)

        self.dataToolButton = QToolButton(self.widget)
        self.dataToolButton.setObjectName(u"dataToolButton")
        self.dataToolButton.setMinimumSize(QSize(150, 100))
        self.dataToolButton.setStyleSheet(u"color: white;\n"
"font-size: 16pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon1 = QIcon()
        icon1.addFile(u":/icon/icons/base_data.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dataToolButton.setIcon(icon1)
        self.dataToolButton.setIconSize(QSize(48, 48))
        self.dataToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.dataToolButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.genOtchToolButton = QToolButton(self.widget)
        self.genOtchToolButton.setObjectName(u"genOtchToolButton")
        self.genOtchToolButton.setMinimumSize(QSize(150, 100))
        self.genOtchToolButton.setStyleSheet(u"color: white;\n"
"font-size: 16pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon2 = QIcon()
        icon2.addFile(u":/icon/icons/otchet_generate.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.genOtchToolButton.setIcon(icon2)
        self.genOtchToolButton.setIconSize(QSize(48, 48))
        self.genOtchToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_2.addWidget(self.genOtchToolButton)

        self.genPlanToolButton = QToolButton(self.widget)
        self.genPlanToolButton.setObjectName(u"genPlanToolButton")
        self.genPlanToolButton.setMinimumSize(QSize(150, 100))
        self.genPlanToolButton.setStyleSheet(u"color: white;\n"
"font-size: 16pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon3 = QIcon()
        icon3.addFile(u":/icon/icons/plan_generate.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.genPlanToolButton.setIcon(icon3)
        self.genPlanToolButton.setIconSize(QSize(48, 48))
        self.genPlanToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_2.addWidget(self.genPlanToolButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.faqToolButton = QToolButton(self.widget)
        self.faqToolButton.setObjectName(u"faqToolButton")
        self.faqToolButton.setMinimumSize(QSize(150, 100))
        self.faqToolButton.setStyleSheet(u"color: white;\n"
"font-size: 16pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon4 = QIcon()
        icon4.addFile(u":/icon/icons/faq.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.faqToolButton.setIcon(icon4)
        self.faqToolButton.setIconSize(QSize(48, 48))
        self.faqToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_3.addWidget(self.faqToolButton)

        self.exitToolButton = QToolButton(self.widget)
        self.exitToolButton.setObjectName(u"exitToolButton")
        self.exitToolButton.setMinimumSize(QSize(150, 100))
        self.exitToolButton.setStyleSheet(u"color: white;\n"
"font-size: 16pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon5 = QIcon()
        icon5.addFile(u":/icon/icons/cancel.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exitToolButton.setIcon(icon5)
        self.exitToolButton.setIconSize(QSize(48, 48))
        self.exitToolButton.setCheckable(False)
        self.exitToolButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.exitToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.exitToolButton.setAutoRaise(True)
        self.exitToolButton.setArrowType(Qt.ArrowType.NoArrow)

        self.horizontalLayout_3.addWidget(self.exitToolButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1061, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.mainStackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Project P", None))
        self.loadTableButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0442\u0430\u0431\u043b\u0438\u0446\u0443", None))
        self.loadNagruzkaButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u043d\u0430\u0433\u0440\u0443\u0437\u043a\u0443", None))
        self.cabinetToolButton.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0447\u043d\u044b\u0439 \u043a\u0430\u0431\u0438\u043d\u0435\u0442", None))
        self.dataToolButton.setText(QCoreApplication.translate("MainWindow", u"\u0411\u0430\u0437\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.genOtchToolButton.setText(QCoreApplication.translate("MainWindow", u"\u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f \u043e\u0442\u0447\u0435\u0442\u0430", None))
        self.genPlanToolButton.setText(QCoreApplication.translate("MainWindow", u"\u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f \u043f\u043b\u0430\u043d\u0430", None))
        self.faqToolButton.setText(QCoreApplication.translate("MainWindow", u"F.A.Q", None))
        self.exitToolButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0439\u0442\u0438", None))
    # retranslateUi

