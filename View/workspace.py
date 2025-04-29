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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStackedWidget,
    QStatusBar, QTableView, QToolButton, QWidget)
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
"font-family: Consolas;\n"
"QPushButton {\n"
"    color: white;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainStackedWidget = QStackedWidget(self.centralwidget)
        self.mainStackedWidget.setObjectName(u"mainStackedWidget")
        self.mainStackedWidget.setGeometry(QRect(170, 10, 881, 591))
        self.db_page = QWidget()
        self.db_page.setObjectName(u"db_page")
        self.label = QLabel(self.db_page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(140, 200, 321, 91))
        self.mainStackedWidget.addWidget(self.db_page)
        self.otchet_page = QWidget()
        self.otchet_page.setObjectName(u"otchet_page")
        self.otch_lbl_page_info = QLabel(self.otchet_page)
        self.otch_lbl_page_info.setObjectName(u"otch_lbl_page_info")
        self.otch_lbl_page_info.setGeometry(QRect(0, 0, 131, 21))
        self.otch_lbl_page_info.setStyleSheet(u"QLabel{\n"
"    color: white;\n"
"}")
        self.otch_lbl_stage = QLabel(self.otchet_page)
        self.otch_lbl_stage.setObjectName(u"otch_lbl_stage")
        self.otch_lbl_stage.setGeometry(QRect(140, 0, 131, 21))
        self.otch_lbl_stage.setStyleSheet(u"QLabel{\n"
"    color: white;\n"
"}")
        self.otch_next_btn = QPushButton(self.otchet_page)
        self.otch_next_btn.setObjectName(u"otch_next_btn")
        self.otch_next_btn.setGeometry(QRect(340, 0, 75, 24))
        self.otch_next_btn.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.otch_prev_btn = QPushButton(self.otchet_page)
        self.otch_prev_btn.setObjectName(u"otch_prev_btn")
        self.otch_prev_btn.setGeometry(QRect(270, 0, 75, 24))
        self.otch_prev_btn.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.stackedWidget = QStackedWidget(self.otchet_page)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 30, 881, 551))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.otchFirstTableView = QTableView(self.page)
        self.otchFirstTableView.setObjectName(u"otchFirstTableView")
        self.otchFirstTableView.setGeometry(QRect(0, 60, 881, 491))
        self.otchFirstTableView.setStyleSheet(u"QTableView {\n"
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
        self.meeting_date_otch_btn = QPushButton(self.page)
        self.meeting_date_otch_btn.setObjectName(u"meeting_date_otch_btn")
        self.meeting_date_otch_btn.setGeometry(QRect(0, 30, 251, 24))
        self.meeting_date_otch_btn.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.otchSecondTableView = QTableView(self.page_2)
        self.otchSecondTableView.setObjectName(u"otchSecondTableView")
        self.otchSecondTableView.setGeometry(QRect(0, 60, 881, 491))
        self.otchSecondTableView.setStyleSheet(u"QTableView {\n"
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
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.otchThirdTableView = QTableView(self.page_3)
        self.otchThirdTableView.setObjectName(u"otchThirdTableView")
        self.otchThirdTableView.setGeometry(QRect(0, 60, 881, 491))
        self.otchThirdTableView.setStyleSheet(u"QTableView {\n"
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
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.otchFourthTableView = QTableView(self.page_4)
        self.otchFourthTableView.setObjectName(u"otchFourthTableView")
        self.otchFourthTableView.setGeometry(QRect(0, 60, 881, 491))
        self.otchFourthTableView.setStyleSheet(u"QTableView {\n"
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
        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.otchFivethTableView = QTableView(self.page_5)
        self.otchFivethTableView.setObjectName(u"otchFivethTableView")
        self.otchFivethTableView.setGeometry(QRect(0, 60, 881, 491))
        self.otchFivethTableView.setStyleSheet(u"QTableView {\n"
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
        self.stackedWidget.addWidget(self.page_5)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.otchSixthTableView = QTableView(self.page_6)
        self.otchSixthTableView.setObjectName(u"otchSixthTableView")
        self.otchSixthTableView.setGeometry(QRect(0, 60, 881, 491))
        self.otchSixthTableView.setStyleSheet(u"QTableView {\n"
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
        self.stackedWidget.addWidget(self.page_6)
        self.otch_nagr_btn = QPushButton(self.otchet_page)
        self.otch_nagr_btn.setObjectName(u"otch_nagr_btn")
        self.otch_nagr_btn.setGeometry(QRect(440, 0, 91, 24))
        self.otch_nagr_btn.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.otch_pln_btn = QPushButton(self.otchet_page)
        self.otch_pln_btn.setObjectName(u"otch_pln_btn")
        self.otch_pln_btn.setGeometry(QRect(530, 0, 81, 24))
        self.otch_pln_btn.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.otch_tbl_btn = QPushButton(self.otchet_page)
        self.otch_tbl_btn.setObjectName(u"otch_tbl_btn")
        self.otch_tbl_btn.setGeometry(QRect(610, 0, 81, 24))
        self.otch_tbl_btn.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.mainStackedWidget.addWidget(self.otchet_page)
        self.plan_page = QWidget()
        self.plan_page.setObjectName(u"plan_page")
        self.loadTableButton = QPushButton(self.plan_page)
        self.loadTableButton.setObjectName(u"loadTableButton")
        self.loadTableButton.setGeometry(QRect(10, 0, 141, 21))
        self.loadTableButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.loadNagruzkaButton = QPushButton(self.plan_page)
        self.loadNagruzkaButton.setObjectName(u"loadNagruzkaButton")
        self.loadNagruzkaButton.setGeometry(QRect(150, 0, 141, 21))
        self.loadNagruzkaButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.loadPlanPushButton = QPushButton(self.plan_page)
        self.loadPlanPushButton.setObjectName(u"loadPlanPushButton")
        self.loadPlanPushButton.setGeometry(QRect(290, 0, 141, 21))
        self.loadPlanPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.tableView = QTableView(self.plan_page)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(0, 100, 881, 491))
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
        self.placePlanButton = QPushButton(self.plan_page)
        self.placePlanButton.setObjectName(u"placePlanButton")
        self.placePlanButton.setGeometry(QRect(100, 40, 131, 21))
        self.placePlanButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.notePlanPushButton = QPushButton(self.plan_page)
        self.notePlanPushButton.setObjectName(u"notePlanPushButton")
        self.notePlanPushButton.setGeometry(QRect(10, 40, 91, 21))
        self.notePlanPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.agreementPlanPushButton = QPushButton(self.plan_page)
        self.agreementPlanPushButton.setObjectName(u"agreementPlanPushButton")
        self.agreementPlanPushButton.setGeometry(QRect(230, 40, 91, 21))
        self.agreementPlanPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.zakupkaPlanPushButton = QPushButton(self.plan_page)
        self.zakupkaPlanPushButton.setObjectName(u"zakupkaPlanPushButton")
        self.zakupkaPlanPushButton.setGeometry(QRect(320, 40, 151, 21))
        self.zakupkaPlanPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.rukPlanPushButton = QPushButton(self.plan_page)
        self.rukPlanPushButton.setObjectName(u"rukPlanPushButton")
        self.rukPlanPushButton.setGeometry(QRect(470, 40, 191, 21))
        self.rukPlanPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.savePlanButton = QPushButton(self.plan_page)
        self.savePlanButton.setObjectName(u"savePlanButton")
        self.savePlanButton.setGeometry(QRect(590, 0, 91, 21))
        self.savePlanButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.saveAsPlanButton = QPushButton(self.plan_page)
        self.saveAsPlanButton.setObjectName(u"saveAsPlanButton")
        self.saveAsPlanButton.setGeometry(QRect(680, 0, 91, 21))
        self.saveAsPlanButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.mainStackedWidget.addWidget(self.plan_page)
        self.faq_page = QWidget()
        self.faq_page.setObjectName(u"faq_page")
        self.label_3 = QLabel(self.faq_page)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(160, 190, 49, 16))
        self.mainStackedWidget.addWidget(self.faq_page)
        self.lk_page = QWidget()
        self.lk_page.setObjectName(u"lk_page")
        self.label_2 = QLabel(self.lk_page)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(290, 220, 281, 101))
        self.mainStackedWidget.addWidget(self.lk_page)
        self.genOtchToolButton = QToolButton(self.centralwidget)
        self.genOtchToolButton.setObjectName(u"genOtchToolButton")
        self.genOtchToolButton.setGeometry(QRect(10, 190, 150, 100))
        self.genOtchToolButton.setMinimumSize(QSize(150, 100))
        self.genOtchToolButton.setStyleSheet(u"color: white;\n"
"font-size: 12pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon1 = QIcon()
        icon1.addFile(u":/icon/icons/otchet_generate.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.genOtchToolButton.setIcon(icon1)
        self.genOtchToolButton.setIconSize(QSize(32, 32))
        self.genOtchToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.genPlanToolButton = QToolButton(self.centralwidget)
        self.genPlanToolButton.setObjectName(u"genPlanToolButton")
        self.genPlanToolButton.setGeometry(QRect(10, 310, 150, 100))
        self.genPlanToolButton.setMinimumSize(QSize(150, 100))
        self.genPlanToolButton.setStyleSheet(u"color: white;\n"
"font-size: 12pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon2 = QIcon()
        icon2.addFile(u":/icon/icons/plan_generate.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.genPlanToolButton.setIcon(icon2)
        self.genPlanToolButton.setIconSize(QSize(32, 32))
        self.genPlanToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.exitToolButton = QToolButton(self.centralwidget)
        self.exitToolButton.setObjectName(u"exitToolButton")
        self.exitToolButton.setGeometry(QRect(10, 510, 150, 100))
        self.exitToolButton.setMinimumSize(QSize(150, 100))
        self.exitToolButton.setStyleSheet(u"color: white;\n"
"font-size: 12pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon3 = QIcon()
        icon3.addFile(u":/icon/icons/cancel.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exitToolButton.setIcon(icon3)
        self.exitToolButton.setIconSize(QSize(32, 32))
        self.exitToolButton.setCheckable(False)
        self.exitToolButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.exitToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.exitToolButton.setAutoRaise(True)
        self.exitToolButton.setArrowType(Qt.ArrowType.NoArrow)
        self.faqToolButton = QToolButton(self.centralwidget)
        self.faqToolButton.setObjectName(u"faqToolButton")
        self.faqToolButton.setGeometry(QRect(10, 420, 150, 100))
        self.faqToolButton.setMinimumSize(QSize(150, 100))
        self.faqToolButton.setStyleSheet(u"color: white;\n"
"font-size: 12pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon4 = QIcon()
        icon4.addFile(u":/icon/icons/faq.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.faqToolButton.setIcon(icon4)
        self.faqToolButton.setIconSize(QSize(32, 32))
        self.faqToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.cabinetToolButton = QToolButton(self.centralwidget)
        self.cabinetToolButton.setObjectName(u"cabinetToolButton")
        self.cabinetToolButton.setGeometry(QRect(10, 0, 150, 100))
        self.cabinetToolButton.setMinimumSize(QSize(150, 100))
        self.cabinetToolButton.setStyleSheet(u"color: white;\n"
"font-size: 12pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon5 = QIcon()
        icon5.addFile(u":/icon/icons/cabinet.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cabinetToolButton.setIcon(icon5)
        self.cabinetToolButton.setIconSize(QSize(32, 32))
        self.cabinetToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.cabinetToolButton.setAutoRaise(True)
        self.dataToolButton = QToolButton(self.centralwidget)
        self.dataToolButton.setObjectName(u"dataToolButton")
        self.dataToolButton.setGeometry(QRect(10, 90, 150, 100))
        self.dataToolButton.setMinimumSize(QSize(150, 100))
        self.dataToolButton.setStyleSheet(u"color: white;\n"
"font-size: 12pt;\n"
"background-color: none;\n"
"border:none;\n"
"font-family: Consolas;")
        icon6 = QIcon()
        icon6.addFile(u":/icon/icons/base_data.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dataToolButton.setIcon(icon6)
        self.dataToolButton.setIconSize(QSize(32, 32))
        self.dataToolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1061, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.mainStackedWidget.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(5)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Project P", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0411\u0430\u0437\u0430 \u0434\u0430\u043d\u043d\u044b\u0445 \u0442\u0443\u0442", None))
        self.otch_lbl_page_info.setText(QCoreApplication.translate("MainWindow", u"\u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f \u043e\u0442\u0447\u0435\u0442\u0430", None))
        self.otch_lbl_stage.setText(QCoreApplication.translate("MainWindow", u"1 \u044d\u0442\u0430\u043f", None))
        self.otch_next_btn.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0430\u043b\u0435\u0435", None))
        self.otch_prev_btn.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0437\u0430\u0434", None))
        self.meeting_date_otch_btn.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0437\u043d\u0430\u0447\u0438\u0442\u044c \u0434\u0430\u0442\u0443 \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u044f \u0441\u043e\u0431\u0440\u0430\u043d\u0438\u044f", None))
        self.otch_nagr_btn.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0433\u0440\u0443\u0437\u043a\u0430", None))
        self.otch_pln_btn.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043b\u0430\u043d", None))
        self.otch_tbl_btn.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430", None))
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
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"faq \u0442\u0443\u0442", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0447\u043d\u044b\u0439 \u043a\u0430\u0431\u0438\u043d\u0435\u0442 \u0442\u0443\u0442", None))
        self.genOtchToolButton.setText(QCoreApplication.translate("MainWindow", u"\u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f\n"
"\u043e\u0442\u0447\u0435\u0442\u0430", None))
        self.genPlanToolButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043b\u0430\u043d", None))
        self.exitToolButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0439\u0442\u0438", None))
        self.faqToolButton.setText(QCoreApplication.translate("MainWindow", u"F.A.Q", None))
        self.cabinetToolButton.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0447\u043d\u044b\u0439\n"
"\u043a\u0430\u0431\u0438\u043d\u0435\u0442", None))
        self.dataToolButton.setText(QCoreApplication.translate("MainWindow", u"\u0411\u0430\u0437\u0430\n"
"\u0434\u0430\u043d\u043d\u044b\u0445", None))
#if QT_CONFIG(statustip)
        self.statusbar.setStatusTip(QCoreApplication.translate("MainWindow", u"\u0423 \u0432\u0430\u0441 \u0432\u0437\u043e\u0440\u0432\u0435\u0442\u0441\u044f \u0430\u043d\u0430\u043b \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 \u043d\u0430 \u044d\u0442\u0443 \u043a\u043d\u043e\u043f\u043a\u0443", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.statusbar.setWhatsThis(QCoreApplication.translate("MainWindow", u"\u0416\u043e\u043f\u0430", None))
#endif // QT_CONFIG(whatsthis)
    # retranslateUi

