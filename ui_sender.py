# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sender.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1103, 587)
        self.frame_view = QTextBrowser(Form)
        self.frame_view.setObjectName(u"frame_view")
        self.frame_view.setGeometry(QRect(690, 200, 371, 301))
        self.cbox1 = QComboBox(Form)
        self.cbox1.setObjectName(u"cbox1")
        self.cbox1.setGeometry(QRect(930, 150, 131, 41))
        self.clearbutton = QPushButton(Form)
        self.clearbutton.setObjectName(u"clearbutton")
        self.clearbutton.setGeometry(QRect(20, 520, 1041, 51))
        self.button_send = QPushButton(Form)
        self.button_send.setObjectName(u"button_send")
        self.button_send.setGeometry(QRect(940, 20, 141, 51))
        self.button_send.setAutoDefault(False)
        self.input_data = QPlainTextEdit(Form)
        self.input_data.setObjectName(u"input_data")
        self.input_data.setGeometry(QRect(20, 20, 911, 51))
        font = QFont()
        font.setFamily(u"JetBrains Mono")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.input_data.setFont(font)
        self.table1 = QTableWidget(Form)
        if (self.table1.columnCount() < 5):
            self.table1.setColumnCount(5)
        font1 = QFont()
        font1.setFamily(u"Microsoft YaHei UI")
        font1.setPointSize(10)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font1);
        self.table1.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font1);
        self.table1.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font1);
        self.table1.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font1);
        self.table1.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font1);
        self.table1.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.table1.setObjectName(u"table1")
        self.table1.setGeometry(QRect(20, 200, 631, 301))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table1.sizePolicy().hasHeightForWidth())
        self.table1.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setFamily(u"JetBrains Mono")
        font2.setPointSize(7)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setWeight(50)
        self.table1.setFont(font2)
        self.table1.setStyleSheet(u"font: 7pt \"JetBrains Mono\";")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 170, 521, 26))
        font3 = QFont()
        font3.setFamily(u"JetBrains Mono")
        font3.setPointSize(12)
        font3.setBold(False)
        font3.setWeight(50)
        self.label.setFont(font3)
        self.label.setLayoutDirection(Qt.RightToLeft)
        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(20, 80, 1061, 20))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(690, 170, 181, 26))
        font4 = QFont()
        font4.setFamily(u"Microsoft YaHei UI")
        font4.setPointSize(12)
        font4.setBold(False)
        font4.setWeight(50)
        self.label_3.setFont(font4)
        self.label_3.setLayoutDirection(Qt.RightToLeft)
        self.line_3 = QFrame(Form)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(20, 500, 1041, 20))
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.drop_Slider = QSlider(Form)
        self.drop_Slider.setObjectName(u"drop_Slider")
        self.drop_Slider.setGeometry(QRect(720, 110, 341, 22))
        self.drop_Slider.setMouseTracking(False)
        self.drop_Slider.setOrientation(Qt.Horizontal)
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(620, 110, 81, 26))
        font5 = QFont()
        font5.setFamily(u"Microsoft YaHei UI")
        font5.setPointSize(16)
        font5.setBold(False)
        font5.setWeight(50)
        self.label_4.setFont(font5)
        self.label_4.setLayoutDirection(Qt.RightToLeft)
        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(660, 160, 20, 351))
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.retranslateUi(Form)

        self.button_send.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u53d1\u9001\u65b9", None))
        self.cbox1.setPlaceholderText("")
        self.clearbutton.setText(QCoreApplication.translate("Form", u"\u6e05\u9664", None))
        self.button_send.setText(QCoreApplication.translate("Form", u"\u53d1\u9001", None))
#if QT_CONFIG(whatsthis)
        self.input_data.setWhatsThis(QCoreApplication.translate("Form", u"<html><head/><body><p>\u8bf7\u8f93\u5165</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.input_data.setPlainText("")
        self.input_data.setPlaceholderText(QCoreApplication.translate("Form", u"\u8bf7\u8f93\u5165\u5f85\u53d1\u9001\u7684\u6570\u636e>>>", None))
        ___qtablewidgetitem = self.table1.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u5e8f\u5217\u53f7", None));
        ___qtablewidgetitem1 = self.table1.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u6570\u636e", None));
        ___qtablewidgetitem2 = self.table1.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u53d1\u9001", None));
        ___qtablewidgetitem3 = self.table1.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"\u662f\u5426\u63a5\u53d7\u5b8c\u6bd5", None));
        ___qtablewidgetitem4 = self.table1.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"\u5f85\u53d1\u5e8f\u5217\u53f7", None));
        self.label.setText(QCoreApplication.translate("Form", u"Sender log", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5df2\u53d1\u9001\u5e27\u4fe1\u606f", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u4e22\u5305\u7387", None))
    # retranslateUi

