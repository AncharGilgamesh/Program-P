# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'appearance.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QStackedWidget,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(409, 487)
        Dialog.setStyleSheet(u"QWidget {\n"
"    background-color: qlineargradient(\n"
"        spread:pad, \n"
"        x1:1, y1:1, x2:0, y2:0, \n"
"        stop:0 rgba(81, 0, 135, 255), \n"
"        stop:0.427447 rgba(41, 61, 132, 235), \n"
"        stop:1 rgba(155, 79, 165, 255)\n"
"    );\n"
"    font-family: 'Consolas';\n"
"    color: white;\n"
"}\n"
"QLabel {\n"
"    font-size: 12px;\n"
"    color: white;\n"
"    padding: 5px;\n"
"	background: transparent;\n"
"}\n"
"QLineEdit {\n"
"    background-color: rgba(255, 255, 255, 0.1);\n"
"    border: 1px solid rgba(255, 255, 255, 0.3);\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"    color: white;\n"
"    font-size: 10px;\n"
"    selection-background-color: rgba(155, 79, 165, 150);\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 1px solid rgba(155, 79, 165, 200);\n"
"    background-color: rgba(255, 255, 255, 0.15);\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: rgba(255, 255, 255, 0.5);\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: rgba(155, 79, 165, 180);\n"
"    bord"
                        "er: 1px solid rgba(255, 255, 255, 0.2);\n"
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
"}")
        self.stackedWidget = QStackedWidget(Dialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 50, 401, 331))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.authUsernameLine = QLineEdit(self.page)
        self.authUsernameLine.setObjectName(u"authUsernameLine")
        self.authUsernameLine.setGeometry(QRect(140, 140, 211, 31))
        self.authPassLine = QLineEdit(self.page)
        self.authPassLine.setObjectName(u"authPassLine")
        self.authPassLine.setGeometry(QRect(140, 180, 211, 31))
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 140, 121, 21))
        self.label_3 = QLabel(self.page)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 180, 111, 21))
        self.authPushButton = QPushButton(self.page)
        self.authPushButton.setObjectName(u"authPushButton")
        self.authPushButton.setGeometry(QRect(140, 260, 111, 31))
        self.loginStatusLabel = QLabel(self.page)
        self.loginStatusLabel.setObjectName(u"loginStatusLabel")
        self.loginStatusLabel.setGeometry(QRect(40, 170, 321, 31))
        self.checkBox = QCheckBox(self.page)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(130, 300, 151, 20))
        self.stackedWidget.addWidget(self.page)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.label_11 = QLabel(self.page_3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 100, 121, 21))
        self.recoverUsernameLine = QLineEdit(self.page_3)
        self.recoverUsernameLine.setObjectName(u"recoverUsernameLine")
        self.recoverUsernameLine.setGeometry(QRect(150, 100, 211, 31))
        self.revocerRegisterCodeLine = QLineEdit(self.page_3)
        self.revocerRegisterCodeLine.setObjectName(u"revocerRegisterCodeLine")
        self.revocerRegisterCodeLine.setGeometry(QRect(150, 140, 211, 31))
        self.label_12 = QLabel(self.page_3)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 140, 121, 21))
        self.recoverPushButton = QPushButton(self.page_3)
        self.recoverPushButton.setObjectName(u"recoverPushButton")
        self.recoverPushButton.setGeometry(QRect(130, 300, 131, 31))
        self.label_13 = QLabel(self.page_3)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 180, 121, 21))
        self.recoverPassLine = QLineEdit(self.page_3)
        self.recoverPassLine.setObjectName(u"recoverPassLine")
        self.recoverPassLine.setGeometry(QRect(150, 180, 211, 31))
        self.recoverRepeatPassLine = QLineEdit(self.page_3)
        self.recoverRepeatPassLine.setObjectName(u"recoverRepeatPassLine")
        self.recoverRepeatPassLine.setGeometry(QRect(150, 220, 211, 31))
        self.label_14 = QLabel(self.page_3)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(10, 220, 121, 21))
        self.stackedWidget.addWidget(self.page_3)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.regUsernamLine = QLineEdit(self.page_2)
        self.regUsernamLine.setObjectName(u"regUsernamLine")
        self.regUsernamLine.setGeometry(QRect(150, 20, 211, 31))
        self.label_4 = QLabel(self.page_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 20, 121, 21))
        self.regPassLine = QLineEdit(self.page_2)
        self.regPassLine.setObjectName(u"regPassLine")
        self.regPassLine.setGeometry(QRect(150, 60, 211, 31))
        self.label_5 = QLabel(self.page_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 60, 121, 21))
        self.nameLine = QLineEdit(self.page_2)
        self.nameLine.setObjectName(u"nameLine")
        self.nameLine.setGeometry(QRect(150, 140, 211, 31))
        self.label_6 = QLabel(self.page_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 140, 121, 21))
        self.familiaLine = QLineEdit(self.page_2)
        self.familiaLine.setObjectName(u"familiaLine")
        self.familiaLine.setGeometry(QRect(150, 180, 211, 31))
        self.label_7 = QLabel(self.page_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 180, 121, 21))
        self.otchestvoLine = QLineEdit(self.page_2)
        self.otchestvoLine.setObjectName(u"otchestvoLine")
        self.otchestvoLine.setGeometry(QRect(150, 220, 211, 31))
        self.label_8 = QLabel(self.page_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 220, 121, 21))
        self.regCodeLine = QLineEdit(self.page_2)
        self.regCodeLine.setObjectName(u"regCodeLine")
        self.regCodeLine.setGeometry(QRect(150, 260, 211, 31))
        self.label_9 = QLabel(self.page_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 260, 121, 21))
        self.regRepeatPassLine = QLineEdit(self.page_2)
        self.regRepeatPassLine.setObjectName(u"regRepeatPassLine")
        self.regRepeatPassLine.setGeometry(QRect(150, 100, 211, 31))
        self.label_10 = QLabel(self.page_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(10, 100, 121, 21))
        self.registerButton = QPushButton(self.page_2)
        self.registerButton.setObjectName(u"registerButton")
        self.registerButton.setGeometry(QRect(110, 300, 181, 31))
        self.stackedWidget.addWidget(self.page_2)
        self.mainInfoLabel = QLabel(Dialog)
        self.mainInfoLabel.setObjectName(u"mainInfoLabel")
        self.mainInfoLabel.setGeometry(QRect(100, 10, 201, 31))
        self.mainInfoLabel.setStyleSheet(u"QLabel {\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    color: rgba(255, 255, 255, 0.9);\n"
"}")
        self.authPagePushButton = QPushButton(Dialog)
        self.authPagePushButton.setObjectName(u"authPagePushButton")
        self.authPagePushButton.setGeometry(QRect(110, 390, 181, 31))
        self.regPagePushButton = QPushButton(Dialog)
        self.regPagePushButton.setObjectName(u"regPagePushButton")
        self.regPagePushButton.setGeometry(QRect(110, 420, 181, 31))
        self.recoverPagePushButton = QPushButton(Dialog)
        self.recoverPagePushButton.setObjectName(u"recoverPagePushButton")
        self.recoverPagePushButton.setGeometry(QRect(110, 450, 181, 31))

        self.retranslateUi(Dialog)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044f", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u0418\u043c\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u041f\u0430\u0440\u043e\u043b\u044c", None))
        self.authPushButton.setText(QCoreApplication.translate("Dialog", u"\u0412\u043e\u0439\u0442\u0438", None))
        self.loginStatusLabel.setText("")
        self.checkBox.setText(QCoreApplication.translate("Dialog", u"\u0417\u0430\u043f\u043e\u043c\u043d\u0438\u0442\u044c \u043c\u0435\u043d\u044f", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"\u0418\u043c\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"\u041a\u043e\u0434 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438", None))
        self.recoverPushButton.setText(QCoreApplication.translate("Dialog", u"\u0412\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"\u041f\u0430\u0440\u043e\u043b\u044c", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"\u041f\u043e\u0432\u0442\u043e\u0440\u0438\u0442\u044c \u043f\u0430\u0440\u043e\u043b\u044c", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u0418\u043c\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u041f\u0430\u0440\u043e\u043b\u044c", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"\u0418\u043c\u044f", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"\u0424\u0430\u043c\u0438\u043b\u0438\u044f", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"\u041a\u043e\u0434 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"\u041f\u043e\u0432\u0442\u043e\u0440\u0438\u0442\u0435 \u043f\u0430\u0440\u043e\u043b\u044c", None))
        self.registerButton.setText(QCoreApplication.translate("Dialog", u"\u0417\u0430\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c\u0441\u044f", None))
        self.mainInfoLabel.setText("")
        self.authPagePushButton.setText(QCoreApplication.translate("Dialog", u"\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044f", None))
        self.regPagePushButton.setText(QCoreApplication.translate("Dialog", u"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f", None))
        self.recoverPagePushButton.setText(QCoreApplication.translate("Dialog", u"\u0412\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435 \u043f\u0430\u0440\u043e\u043b\u044f", None))
    # retranslateUi

