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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStackedWidget, QStatusBar, QTableView, QTextBrowser,
    QToolButton, QWidget)
import View.res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1061, 642)
        icon = QIcon()
        icon.addFile(u":/icon/icons/TitleIcon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"QWidget{\n"
"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(81, 0, 135, 255), stop:0.427447 rgba(41, 61, 132, 235), stop:1 rgba(155, 79, 165, 255));\n"
"font-family: Consolas;\n"
"}\n"
"QPushButton {\n"
"    background-color: rgba(155, 79, 165, 180);\n"
"    border: 1px solid rgba(255, 255, 255, 0.2);\n"
"    border-radius: 5px;\n"
"    padding: 8px 16px;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgba(155, 79, 165, 220);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(81, 0, 135, 200);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgba(155, 79, 165, 80);\n"
"    color: rgba(255, 255, 255, 0.5);\n"
"}\n"
"QStackedWidget {\n"
"	background: transparent;\n"
"	border: none;\n"
"}\n"
"QLineEdit {\n"
"    background-color: rgba(255, 255, 255, 0.1);\n"
"    border: 1px solid rgba(255, 255, 255, 0.3);\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"    color: white;\n"
"    font-"
                        "size: 13px;\n"
"    selection-background-color: rgba(155, 79, 165, 150);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid rgba(155, 79, 165, 200);\n"
"    background-color: rgba(255, 255, 255, 0.15);\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: rgba(255, 255, 255, 0.5);\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainStackedWidget = QStackedWidget(self.centralwidget)
        self.mainStackedWidget.setObjectName(u"mainStackedWidget")
        self.mainStackedWidget.setGeometry(QRect(170, 10, 881, 591))
        self.db_page = QWidget()
        self.db_page.setObjectName(u"db_page")
        self.dataBaseTableView = QTableView(self.db_page)
        self.dataBaseTableView.setObjectName(u"dataBaseTableView")
        self.dataBaseTableView.setGeometry(QRect(0, 100, 881, 491))
        self.dataBaseTableView.setStyleSheet(u"QTableView {\n"
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
        self.dbPlansPushButton = QPushButton(self.db_page)
        self.dbPlansPushButton.setObjectName(u"dbPlansPushButton")
        self.dbPlansPushButton.setGeometry(QRect(240, 0, 121, 31))
        self.dbPlansPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.dbPrepodsPushButton = QPushButton(self.db_page)
        self.dbPrepodsPushButton.setObjectName(u"dbPrepodsPushButton")
        self.dbPrepodsPushButton.setGeometry(QRect(360, 0, 121, 31))
        self.dbPrepodsPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.dbStarostaPushButton = QPushButton(self.db_page)
        self.dbStarostaPushButton.setObjectName(u"dbStarostaPushButton")
        self.dbStarostaPushButton.setGeometry(QRect(480, 0, 131, 31))
        self.dbStarostaPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.sa = QPushButton(self.db_page)
        self.sa.setObjectName(u"sa")
        self.sa.setGeometry(QRect(20, 10, 141, 31))
        self.sa.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.dbPlansPushButton_3 = QPushButton(self.db_page)
        self.dbPlansPushButton_3.setObjectName(u"dbPlansPushButton_3")
        self.dbPlansPushButton_3.setGeometry(QRect(20, 40, 141, 31))
        self.dbPlansPushButton_3.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.dbPlansPushButton_7 = QPushButton(self.db_page)
        self.dbPlansPushButton_7.setObjectName(u"dbPlansPushButton_7")
        self.dbPlansPushButton_7.setGeometry(QRect(20, 70, 141, 31))
        self.dbPlansPushButton_7.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.dbEditPrepodPushButton = QPushButton(self.db_page)
        self.dbEditPrepodPushButton.setObjectName(u"dbEditPrepodPushButton")
        self.dbEditPrepodPushButton.setGeometry(QRect(360, 70, 131, 31))
        self.dbEditPrepodPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.dbAddPrepodPushButton = QPushButton(self.db_page)
        self.dbAddPrepodPushButton.setObjectName(u"dbAddPrepodPushButton")
        self.dbAddPrepodPushButton.setGeometry(QRect(240, 70, 121, 31))
        self.dbAddPrepodPushButton.setStyleSheet(u"")
        self.dbDelPrepodPushButton = QPushButton(self.db_page)
        self.dbDelPrepodPushButton.setObjectName(u"dbDelPrepodPushButton")
        self.dbDelPrepodPushButton.setGeometry(QRect(490, 70, 121, 31))
        self.dbDelPrepodPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.dbAddStarostaPushButton = QPushButton(self.db_page)
        self.dbAddStarostaPushButton.setObjectName(u"dbAddStarostaPushButton")
        self.dbAddStarostaPushButton.setGeometry(QRect(700, 10, 141, 31))
        self.dbAddStarostaPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.dbEditStarostaPushButton = QPushButton(self.db_page)
        self.dbEditStarostaPushButton.setObjectName(u"dbEditStarostaPushButton")
        self.dbEditStarostaPushButton.setGeometry(QRect(700, 40, 141, 31))
        self.dbEditStarostaPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.dbDelStarostaPushButton = QPushButton(self.db_page)
        self.dbDelStarostaPushButton.setObjectName(u"dbDelStarostaPushButton")
        self.dbDelStarostaPushButton.setGeometry(QRect(700, 70, 141, 31))
        self.dbDelStarostaPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
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
        self.otch_next_btn.setGeometry(QRect(340, 0, 75, 31))
        self.otch_next_btn.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.otch_prev_btn = QPushButton(self.otchet_page)
        self.otch_prev_btn.setObjectName(u"otch_prev_btn")
        self.otch_prev_btn.setGeometry(QRect(270, 0, 75, 31))
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
        self.meeting_date_otch_btn.setGeometry(QRect(0, 23, 261, 31))
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
        self.otch_nagr_btn.setGeometry(QRect(440, 0, 91, 31))
        self.otch_nagr_btn.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.otch_pln_btn = QPushButton(self.otchet_page)
        self.otch_pln_btn.setObjectName(u"otch_pln_btn")
        self.otch_pln_btn.setGeometry(QRect(530, 0, 81, 31))
        self.otch_pln_btn.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.otch_tbl_btn = QPushButton(self.otchet_page)
        self.otch_tbl_btn.setObjectName(u"otch_tbl_btn")
        self.otch_tbl_btn.setGeometry(QRect(610, 0, 81, 31))
        self.otch_tbl_btn.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.mainStackedWidget.addWidget(self.otchet_page)
        self.plan_page = QWidget()
        self.plan_page.setObjectName(u"plan_page")
        self.loadTableButton = QPushButton(self.plan_page)
        self.loadTableButton.setObjectName(u"loadTableButton")
        self.loadTableButton.setGeometry(QRect(10, 0, 151, 31))
        self.loadTableButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.loadNagruzkaButton = QPushButton(self.plan_page)
        self.loadNagruzkaButton.setObjectName(u"loadNagruzkaButton")
        self.loadNagruzkaButton.setGeometry(QRect(160, 0, 161, 31))
        self.loadNagruzkaButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.loadPlanPushButton = QPushButton(self.plan_page)
        self.loadPlanPushButton.setObjectName(u"loadPlanPushButton")
        self.loadPlanPushButton.setGeometry(QRect(320, 0, 141, 31))
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
        self.placePlanButton.setGeometry(QRect(100, 40, 141, 31))
        self.placePlanButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.notePlanPushButton = QPushButton(self.plan_page)
        self.notePlanPushButton.setObjectName(u"notePlanPushButton")
        self.notePlanPushButton.setGeometry(QRect(0, 40, 101, 31))
        self.notePlanPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.agreementPlanPushButton = QPushButton(self.plan_page)
        self.agreementPlanPushButton.setObjectName(u"agreementPlanPushButton")
        self.agreementPlanPushButton.setGeometry(QRect(240, 40, 101, 31))
        self.agreementPlanPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.zakupkaPlanPushButton = QPushButton(self.plan_page)
        self.zakupkaPlanPushButton.setObjectName(u"zakupkaPlanPushButton")
        self.zakupkaPlanPushButton.setGeometry(QRect(340, 40, 171, 31))
        self.zakupkaPlanPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.rukPlanPushButton = QPushButton(self.plan_page)
        self.rukPlanPushButton.setObjectName(u"rukPlanPushButton")
        self.rukPlanPushButton.setGeometry(QRect(520, 40, 221, 31))
        self.rukPlanPushButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.savePlanButton = QPushButton(self.plan_page)
        self.savePlanButton.setObjectName(u"savePlanButton")
        self.savePlanButton.setGeometry(QRect(580, 0, 101, 31))
        self.savePlanButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.saveAsPlanButton = QPushButton(self.plan_page)
        self.saveAsPlanButton.setObjectName(u"saveAsPlanButton")
        self.saveAsPlanButton.setGeometry(QRect(680, 0, 121, 31))
        self.saveAsPlanButton.setStyleSheet(u"QPushButton{\n"
"    color: white;\n"
"}")
        self.mainStackedWidget.addWidget(self.plan_page)
        self.faq_page = QWidget()
        self.faq_page.setObjectName(u"faq_page")
        self.faqTextBrowser = QTextBrowser(self.faq_page)
        self.faqTextBrowser.setObjectName(u"faqTextBrowser")
        self.faqTextBrowser.setGeometry(QRect(10, 30, 861, 551))
        self.mainStackedWidget.addWidget(self.faq_page)
        self.lk_page = QWidget()
        self.lk_page.setObjectName(u"lk_page")
        self.lkMainLabel = QLabel(self.lk_page)
        self.lkMainLabel.setObjectName(u"lkMainLabel")
        self.lkMainLabel.setGeometry(QRect(0, 0, 411, 71))
        self.lkMainLabel.setStyleSheet(u"QLabel{\n"
"	color: white;\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    padding: 10px;\n"
"	background: transparent\n"
"}")
        self.label = QLabel(self.lk_page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 110, 121, 16))
        self.label.setStyleSheet(u"QLabel{\n"
"	color: white;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    padding: 10px;\n"
"	background: transparent\n"
"}")
        self.lkMainLabel_2 = QLabel(self.lk_page)
        self.lkMainLabel_2.setObjectName(u"lkMainLabel_2")
        self.lkMainLabel_2.setGeometry(QRect(80, 90, 161, 31))
        self.lkMainLabel_2.setStyleSheet(u"QLabel{\n"
"	color: white;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    padding: 10px;\n"
"	background: transparent\n"
"}")
        self.lkMainLabel_3 = QLabel(self.lk_page)
        self.lkMainLabel_3.setObjectName(u"lkMainLabel_3")
        self.lkMainLabel_3.setGeometry(QRect(80, 130, 161, 31))
        self.lkMainLabel_3.setStyleSheet(u"QLabel{\n"
"	color: white;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    padding: 10px;\n"
"	background: transparent\n"
"}")
        self.lkMainLabel_4 = QLabel(self.lk_page)
        self.lkMainLabel_4.setObjectName(u"lkMainLabel_4")
        self.lkMainLabel_4.setGeometry(QRect(80, 170, 161, 31))
        self.lkMainLabel_4.setStyleSheet(u"QLabel{\n"
"	color: white;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    padding: 10px;\n"
"	background: transparent\n"
"}")
        self.lkMainLabel_5 = QLabel(self.lk_page)
        self.lkMainLabel_5.setObjectName(u"lkMainLabel_5")
        self.lkMainLabel_5.setGeometry(QRect(80, 210, 161, 31))
        self.lkMainLabel_5.setStyleSheet(u"QLabel{\n"
"	color: white;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    padding: 10px;\n"
"	background: transparent\n"
"}")
        self.lkMainLabel_6 = QLabel(self.lk_page)
        self.lkMainLabel_6.setObjectName(u"lkMainLabel_6")
        self.lkMainLabel_6.setGeometry(QRect(80, 250, 161, 31))
        self.lkMainLabel_6.setStyleSheet(u"QLabel{\n"
"	color: white;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    padding: 10px;\n"
"	background: transparent\n"
"}")
        self.lkMainLabel_7 = QLabel(self.lk_page)
        self.lkMainLabel_7.setObjectName(u"lkMainLabel_7")
        self.lkMainLabel_7.setGeometry(QRect(80, 330, 161, 31))
        self.lkMainLabel_7.setStyleSheet(u"QLabel{\n"
"	color: white;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    padding: 10px;\n"
"	background: transparent\n"
"}")
        self.lkMainLabel_8 = QLabel(self.lk_page)
        self.lkMainLabel_8.setObjectName(u"lkMainLabel_8")
        self.lkMainLabel_8.setGeometry(QRect(80, 370, 161, 31))
        self.lkMainLabel_8.setStyleSheet(u"QLabel{\n"
"	color: white;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    padding: 10px;\n"
"	background: transparent\n"
"}")
        self.lkUsernameLine = QLineEdit(self.lk_page)
        self.lkUsernameLine.setObjectName(u"lkUsernameLine")
        self.lkUsernameLine.setGeometry(QRect(240, 90, 191, 31))
        self.lkUsernameLine.setReadOnly(True)
        self.lkLastNameLine = QLineEdit(self.lk_page)
        self.lkLastNameLine.setObjectName(u"lkLastNameLine")
        self.lkLastNameLine.setGeometry(QRect(240, 130, 191, 31))
        self.lkLastNameLine.setReadOnly(True)
        self.lkNameLine = QLineEdit(self.lk_page)
        self.lkNameLine.setObjectName(u"lkNameLine")
        self.lkNameLine.setGeometry(QRect(240, 170, 191, 31))
        self.lkNameLine.setReadOnly(True)
        self.lkMiddleNameLine = QLineEdit(self.lk_page)
        self.lkMiddleNameLine.setObjectName(u"lkMiddleNameLine")
        self.lkMiddleNameLine.setGeometry(QRect(240, 210, 191, 31))
        self.lkMiddleNameLine.setReadOnly(True)
        self.lkTitleLine = QLineEdit(self.lk_page)
        self.lkTitleLine.setObjectName(u"lkTitleLine")
        self.lkTitleLine.setGeometry(QRect(240, 250, 191, 31))
        self.lkTitleLine.setReadOnly(True)
        self.lkEmailLine = QLineEdit(self.lk_page)
        self.lkEmailLine.setObjectName(u"lkEmailLine")
        self.lkEmailLine.setGeometry(QRect(240, 330, 191, 31))
        self.lkEmailLine.setReadOnly(True)
        self.lkPhoneLine = QLineEdit(self.lk_page)
        self.lkPhoneLine.setObjectName(u"lkPhoneLine")
        self.lkPhoneLine.setGeometry(QRect(240, 370, 191, 31))
        self.lkPhoneLine.setReadOnly(True)
        self.lkMainLabel_9 = QLabel(self.lk_page)
        self.lkMainLabel_9.setObjectName(u"lkMainLabel_9")
        self.lkMainLabel_9.setGeometry(QRect(480, 90, 161, 31))
        self.lkMainLabel_9.setStyleSheet(u"QLabel{\n"
"	color: white;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    padding: 10px;\n"
"	background: transparent\n"
"}")
        self.lkNewPassLine = QLineEdit(self.lk_page)
        self.lkNewPassLine.setObjectName(u"lkNewPassLine")
        self.lkNewPassLine.setGeometry(QRect(490, 130, 191, 31))
        self.lkChangePassPushButton = QPushButton(self.lk_page)
        self.lkChangePassPushButton.setObjectName(u"lkChangePassPushButton")
        self.lkChangePassPushButton.setGeometry(QRect(690, 170, 141, 31))
        self.lkRepeatPassLine = QLineEdit(self.lk_page)
        self.lkRepeatPassLine.setObjectName(u"lkRepeatPassLine")
        self.lkRepeatPassLine.setGeometry(QRect(490, 170, 191, 31))
        self.lkDelAccPushButton = QPushButton(self.lk_page)
        self.lkDelAccPushButton.setObjectName(u"lkDelAccPushButton")
        self.lkDelAccPushButton.setGeometry(QRect(720, 550, 141, 31))
        self.lkDegreeLine = QLineEdit(self.lk_page)
        self.lkDegreeLine.setObjectName(u"lkDegreeLine")
        self.lkDegreeLine.setGeometry(QRect(240, 290, 191, 31))
        self.lkDegreeLine.setReadOnly(True)
        self.lkMainLabel_10 = QLabel(self.lk_page)
        self.lkMainLabel_10.setObjectName(u"lkMainLabel_10")
        self.lkMainLabel_10.setGeometry(QRect(80, 290, 161, 31))
        self.lkMainLabel_10.setStyleSheet(u"QLabel{\n"
"	color: white;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    padding: 10px;\n"
"	background: transparent\n"
"}")
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

        self.mainStackedWidget.setCurrentIndex(3)
        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Project P", None))
        self.dbPlansPushButton.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u044b", None))
        self.dbPrepodsPushButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0435\u043f\u043e\u0434\u0430\u0432\u0430\u0442\u0435\u043b\u0438", None))
        self.dbStarostaPushButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0440\u043e\u0441\u0442\u044b \u0433\u0440\u0443\u043f\u043f", None))
        self.sa.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0449\u0438\u0442\u0430 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430", None))
        self.dbPlansPushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442", None))
        self.dbPlansPushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442", None))
        self.dbEditPrepodPushButton.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435\n"
"\u043f\u0440\u0435\u043f\u043e\u0434\u0430\u0432\u0430\u0442\u0435\u043b\u044f", None))
        self.dbAddPrepodPushButton.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435\n"
"\u043f\u0440\u0435\u043f\u043e\u0434\u0430\u0432\u0430\u0442\u0435\u043b\u044f", None))
        self.dbDelPrepodPushButton.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0435\u043d\u0438\u0435\n"
"\u043f\u0440\u0435\u043f\u043e\u0434\u0430\u0432\u0430\u0442\u0435\u043b\u044f", None))
        self.dbAddStarostaPushButton.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435\n"
"\u0441\u0442\u0430\u0440\u043e\u0441\u0442\u044b", None))
        self.dbEditStarostaPushButton.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435\n"
"\u0441\u0442\u0430\u0440\u043e\u0441\u0442\u044b", None))
        self.dbDelStarostaPushButton.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0435\u043d\u0438\u0435\n"
"\u0441\u0442\u0430\u0440\u043e\u0441\u0442\u044b", None))
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
        self.faqTextBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Consolas'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.lkMainLabel.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0447\u043d\u044b\u0439 \u043a\u0430\u0431\u0438\u043d\u0435\u0442 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0435\u0442\u0435\u043b\u044f", None))
        self.lkMainLabel_2.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f", None))
        self.lkMainLabel_3.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u043c\u0438\u043b\u0438\u044f", None))
        self.lkMainLabel_4.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f", None))
        self.lkMainLabel_5.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e", None))
        self.lkMainLabel_6.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c", None))
        self.lkMainLabel_7.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0447\u0442\u0430", None))
        self.lkMainLabel_8.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430", None))
        self.lkMainLabel_9.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043c\u0435\u043d\u0430 \u043f\u0430\u0440\u043e\u043b\u044f", None))
        self.lkNewPassLine.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043d\u043e\u0432\u044b\u0439 \u043f\u0430\u0440\u043e\u043b\u044c", None))
        self.lkChangePassPushButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.lkRepeatPassLine.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0432\u0442\u043e\u0440\u0438\u0442\u0435 \u043f\u0430\u0440\u043e\u043b\u044c", None))
        self.lkDelAccPushButton.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0430\u043a\u043a\u0430\u0443\u043d\u0442", None))
        self.lkMainLabel_10.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0435\u043f\u0435\u043d\u044c", None))
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

