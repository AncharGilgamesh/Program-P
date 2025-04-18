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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStackedWidget,
    QStatusBar, QTableView, QToolButton, QVBoxLayout,
    QWidget)
import View.res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1061, 642)
        icon = QIcon()
        icon.addFile(u":/icon/icons/TitleIcon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(81, 0, 135, 255), stop:0.427447 rgba(41, 61, 132, 235), stop:1 rgba(155, 79, 165, 255));\n"
"font-family: Consolas;")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainStackedWidget = QStackedWidget(self.centralwidget)
        self.mainStackedWidget.setObjectName(u"mainStackedWidget")
        self.mainStackedWidget.setGeometry(QRect(280, 10, 771, 591))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.loadTableButton = QPushButton(self.page)
        self.loadTableButton.setObjectName(u"loadTableButton")
        self.loadTableButton.setGeometry(QRect(10, 0, 141, 31))
        self.loadNagruzkaButton = QPushButton(self.page)
        self.loadNagruzkaButton.setObjectName(u"loadNagruzkaButton")
        self.loadNagruzkaButton.setGeometry(QRect(160, 0, 141, 31))
        self.loadPlanPushButton = QPushButton(self.page)
        self.loadPlanPushButton.setObjectName(u"loadPlanPushButton")
        self.loadPlanPushButton.setGeometry(QRect(310, 0, 141, 31))
        self.tableView = QTableView(self.page)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(0, 90, 771, 491))
        self.tableView.setStyleSheet(u"QTableView {\n"
"    background-color: rgba(255, 255, 255, 30);\n"
"    border: 1px solid rgba(255, 255, 255, 40);\n"
"    border-bottom-right-radius: 7px;\n"
"    border-bottom-left-radius: 7px;\n"
"}\n"
"QTableView::item {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgba(255, 255, 255, 50);\n"
"    padding: 5px;\n"
"    color: white; /* \u0447\u0442\u043e\u0431\u044b \u043f\u0440\u043e\u0432\u0435\u0440\u0438\u0442\u044c, \u0442\u043e\u0447\u043d\u043e \u043b\u0438 \u0441\u0442\u0438\u043b\u044c \u043f\u0440\u0438\u043c\u0435\u043d\u044f\u0435\u0442\u0441\u044f */\n"
"}\n"
"QTableView::item:selected {\n"
"    border: none;\n"
"    color: white;\n"
"    background-color: rgba(255, 255, 255, 80);\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: rgb(53, 53, 53);\n"
"    color: white;\n"
"    border: none;\n"
"    font-size: 10pt;\n"
"}")
        self.placePlanButton = QPushButton(self.page)
        self.placePlanButton.setObjectName(u"placePlanButton")
        self.placePlanButton.setGeometry(QRect(110, 50, 131, 31))
        self.notePlanPushButton = QPushButton(self.page)
        self.notePlanPushButton.setObjectName(u"notePlanPushButton")
        self.notePlanPushButton.setGeometry(QRect(10, 50, 91, 31))
        self.agreementPlanPushButton = QPushButton(self.page)
        self.agreementPlanPushButton.setObjectName(u"agreementPlanPushButton")
        self.agreementPlanPushButton.setGeometry(QRect(260, 50, 91, 31))
        self.zakupkaPlanPushButton = QPushButton(self.page)
        self.zakupkaPlanPushButton.setObjectName(u"zakupkaPlanPushButton")
        self.zakupkaPlanPushButton.setGeometry(QRect(360, 50, 151, 31))
        self.rukPlanPushButton = QPushButton(self.page)
        self.rukPlanPushButton.setObjectName(u"rukPlanPushButton")
        self.rukPlanPushButton.setGeometry(QRect(520, 50, 191, 31))
        self.savePlanButton = QPushButton(self.page)
        self.savePlanButton.setObjectName(u"savePlanButton")
        self.savePlanButton.setGeometry(QRect(550, 0, 91, 31))
        self.saveAsPlanButton = QPushButton(self.page)
        self.saveAsPlanButton.setObjectName(u"saveAsPlanButton")
        self.saveAsPlanButton.setGeometry(QRect(650, 0, 91, 31))
        self.mainStackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.mainStackedWidget.addWidget(self.page_2)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 261, 521))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cabinetToolButton = QToolButton(self.layoutWidget)
        self.cabinetToolButton.setObjectName(u"cabinetToolButton")
        self.cabinetToolButton.setMinimumSize(QSize(150, 100))
        self.cabinetToolButton.setStyleSheet(u"color: white;\n"
"font-size: 16pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon1 = QIcon()
        icon1.addFile(u":/icon/icons/cabinet.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cabinetToolButton.setIcon(icon1)
        self.cabinetToolButton.setIconSize(QSize(48, 48))
        self.cabinetToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.cabinetToolButton.setAutoRaise(True)

        self.horizontalLayout.addWidget(self.cabinetToolButton)

        self.dataToolButton = QToolButton(self.layoutWidget)
        self.dataToolButton.setObjectName(u"dataToolButton")
        self.dataToolButton.setMinimumSize(QSize(150, 100))
        self.dataToolButton.setStyleSheet(u"color: white;\n"
"font-size: 16pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon2 = QIcon()
        icon2.addFile(u":/icon/icons/base_data.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dataToolButton.setIcon(icon2)
        self.dataToolButton.setIconSize(QSize(48, 48))
        self.dataToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.dataToolButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.genOtchToolButton = QToolButton(self.layoutWidget)
        self.genOtchToolButton.setObjectName(u"genOtchToolButton")
        self.genOtchToolButton.setMinimumSize(QSize(150, 100))
        self.genOtchToolButton.setStyleSheet(u"color: white;\n"
"font-size: 16pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon3 = QIcon()
        icon3.addFile(u":/icon/icons/otchet_generate.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.genOtchToolButton.setIcon(icon3)
        self.genOtchToolButton.setIconSize(QSize(48, 48))
        self.genOtchToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_2.addWidget(self.genOtchToolButton)

        self.genPlanToolButton = QToolButton(self.layoutWidget)
        self.genPlanToolButton.setObjectName(u"genPlanToolButton")
        self.genPlanToolButton.setMinimumSize(QSize(150, 100))
        self.genPlanToolButton.setStyleSheet(u"color: white;\n"
"font-size: 16pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon4 = QIcon()
        icon4.addFile(u":/icon/icons/plan_generate.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.genPlanToolButton.setIcon(icon4)
        self.genPlanToolButton.setIconSize(QSize(48, 48))
        self.genPlanToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_2.addWidget(self.genPlanToolButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.faqToolButton = QToolButton(self.layoutWidget)
        self.faqToolButton.setObjectName(u"faqToolButton")
        self.faqToolButton.setMinimumSize(QSize(150, 100))
        self.faqToolButton.setStyleSheet(u"color: white;\n"
"font-size: 16pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon5 = QIcon()
        icon5.addFile(u":/icon/icons/faq.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.faqToolButton.setIcon(icon5)
        self.faqToolButton.setIconSize(QSize(48, 48))
        self.faqToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_3.addWidget(self.faqToolButton)

        self.exitToolButton = QToolButton(self.layoutWidget)
        self.exitToolButton.setObjectName(u"exitToolButton")
        self.exitToolButton.setMinimumSize(QSize(150, 100))
        self.exitToolButton.setStyleSheet(u"color: white;\n"
"font-size: 16pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon6 = QIcon()
        icon6.addFile(u":/icon/icons/cancel.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exitToolButton.setIcon(icon6)
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
        self.loadPlanPushButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u043f\u043b\u0430\u043d", None))
        self.placePlanButton.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0441\u0442\u043e \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u044f", None))
#if QT_CONFIG(tooltip)
        self.notePlanPushButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u0422\u0432\u043e\u044f \u043c\u0430\u043c\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.notePlanPushButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u0435", None))
        self.agreementPlanPushButton.setText(QCoreApplication.translate("MainWindow", u"\u2116 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430", None))
        self.zakupkaPlanPushButton.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u043e\u0441\u0442\u044c \u0437\u0430\u043a\u0443\u043f\u043a\u0438", None))
        self.rukPlanPushButton.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0443\u043a\u043e\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c \u043e\u0442 \u043f\u0440\u0435\u0434\u043f\u0440\u0438\u044f\u0442\u0438\u044f", None))
        self.savePlanButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.saveAsPlanButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043a\u0430\u043a", None))
        self.cabinetToolButton.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0447\u043d\u044b\u0439\n"
"\u043a\u0430\u0431\u0438\u043d\u0435\u0442", None))
        self.dataToolButton.setText(QCoreApplication.translate("MainWindow", u"\u0411\u0430\u0437\u0430\n"
"\u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.genOtchToolButton.setText(QCoreApplication.translate("MainWindow", u"\u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f\n"
"\u043e\u0442\u0447\u0435\u0442\u0430", None))
        self.genPlanToolButton.setText(QCoreApplication.translate("MainWindow", u"\u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f\n"
"\u043f\u043b\u0430\u043d\u0430", None))
        self.faqToolButton.setText(QCoreApplication.translate("MainWindow", u"F.A.Q", None))
        self.exitToolButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0439\u0442\u0438", None))
#if QT_CONFIG(statustip)
        self.statusbar.setStatusTip(QCoreApplication.translate("MainWindow", u"\u0423 \u0432\u0430\u0441 \u0432\u0437\u043e\u0440\u0432\u0435\u0442\u0441\u044f \u0430\u043d\u0430\u043b \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 \u043d\u0430 \u044d\u0442\u0443 \u043a\u043d\u043e\u043f\u043a\u0443", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.statusbar.setWhatsThis(QCoreApplication.translate("MainWindow", u"\u0416\u043e\u043f\u0430", None))
#endif // QT_CONFIG(whatsthis)
    # retranslateUi

