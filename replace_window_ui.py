# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'replace_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QCheckBox, QGroupBox, QLabel,
                               QLineEdit, QPushButton, QRadioButton)

class Ui_replace_window(object):
    def setupUi(self, replace_window):
        if not replace_window.objectName():
            replace_window.setObjectName(u"replace_window")
        replace_window.setEnabled(True)
        replace_window.setFixedSize(530, 182)
        font = QFont()
        font.setFamilies([u"Microsoft YaHei"])
        font.setPointSize(9)
        replace_window.setFont(font)
        self.label_chazhao = QLabel(replace_window)
        self.label_chazhao.setObjectName(u"label_chazhao")
        self.label_chazhao.setGeometry(QRect(30, 20, 41, 31))
        self.multiline_check = QCheckBox(replace_window)
        self.multiline_check.setObjectName(u"multiline_check")
        self.multiline_check.setGeometry(QRect(30, 140, 111, 30))
        self.search_text = QLineEdit(replace_window)
        self.search_text.setObjectName(u"search_text")
        self.search_text.setGeometry(QRect(80, 20, 291, 31))
        self.findnext_btn = QPushButton(replace_window)
        self.findnext_btn.setObjectName(u"findnext_btn")
        self.findnext_btn.setGeometry(QRect(400, 20, 101, 31))
        self.direction_gbox = QGroupBox(replace_window)
        self.direction_gbox.setObjectName(u"direction_gbox")
        self.direction_gbox.setGeometry(QRect(250, 110, 141, 61))
        self.up_rdbtn = QRadioButton(self.direction_gbox)
        self.up_rdbtn.setObjectName(u"up_rdbtn")
        self.up_rdbtn.setGeometry(QRect(10, 30, 41, 20))
        self.down_rdbtn = QRadioButton(self.direction_gbox)
        self.down_rdbtn.setObjectName(u"down_rdbtn")
        self.down_rdbtn.setGeometry(QRect(80, 30, 51, 20))
        self.down_rdbtn.setChecked(True)
        self.matchcase_check = QCheckBox(replace_window)
        self.matchcase_check.setObjectName(u"matchcase_check")
        self.matchcase_check.setGeometry(QRect(30, 110, 81, 30))
        self.cancel_btn = QPushButton(replace_window)
        self.cancel_btn.setObjectName(u"cancel_btn")
        self.cancel_btn.setGeometry(QRect(400, 140, 101, 31))
        self.replace_btn = QPushButton(replace_window)
        self.replace_btn.setObjectName(u"replace_btn")
        self.replace_btn.setGeometry(QRect(400, 60, 101, 31))
        self.allreplace_btn = QPushButton(replace_window)
        self.allreplace_btn.setObjectName(u"allreplace_btn")
        self.allreplace_btn.setGeometry(QRect(400, 100, 101, 31))
        self.replacewith_text = QLineEdit(replace_window)
        self.replacewith_text.setObjectName(u"replacewith_text")
        self.replacewith_text.setGeometry(QRect(80, 70, 291, 31))
        self.label_tihuan = QLabel(replace_window)
        self.label_tihuan.setObjectName(u"label_tihuan")
        self.label_tihuan.setGeometry(QRect(30, 60, 41, 41))
        self.dotall_check = QCheckBox(replace_window)
        self.dotall_check.setObjectName(u"dotall_check")
        self.dotall_check.setGeometry(QRect(170, 140, 71, 30))
        self.selected_area_only_check = QCheckBox(replace_window)
        self.selected_area_only_check.setObjectName(u"selected_area_only_check")
        self.selected_area_only_check.setGeometry(QRect(150, 110, 91, 30))

        self.retranslateUi(replace_window)

        QMetaObject.connectSlotsByName(replace_window)
    # setupUi

    def retranslateUi(self, replace_window):
        replace_window.setWindowTitle(QCoreApplication.translate("replace_window", u"\u66ff\u6362", None))
        self.label_chazhao.setText(QCoreApplication.translate("replace_window", u"\u67e5  \u627e\uff1a", None))
        self.multiline_check.setText(QCoreApplication.translate("replace_window", u"^$\u5339\u914d\u884c\u5934\u884c\u5c3e", None))
        self.findnext_btn.setText(QCoreApplication.translate("replace_window", u"\u4e0b\u4e00\u4e2a", None))
        self.direction_gbox.setTitle(QCoreApplication.translate("replace_window", u"\u65b9\u5411", None))
        self.up_rdbtn.setText(QCoreApplication.translate("replace_window", u"\u5411\u4e0a", None))
        self.down_rdbtn.setText(QCoreApplication.translate("replace_window", u"\u5411\u4e0b", None))
        self.matchcase_check.setText(QCoreApplication.translate("replace_window", u"\u533a\u5206\u5927\u5c0f\u5199", None))
        self.cancel_btn.setText(QCoreApplication.translate("replace_window", u"\u53d6\u6d88", None))
        self.replace_btn.setText(QCoreApplication.translate("replace_window", u"\u66ff\u6362", None))
        self.allreplace_btn.setText(QCoreApplication.translate("replace_window", u"\u5168\u90e8\u66ff\u6362", None))
        self.replacewith_text.setText("")
        self.label_tihuan.setText(QCoreApplication.translate("replace_window", u"\u66ff\u6362\u4e3a\uff1a", None))
        self.dotall_check.setText(QCoreApplication.translate("replace_window", u"\u8de8\u884c\u5339\u914d", None))
        self.selected_area_only_check.setText(QCoreApplication.translate("replace_window", u"\u4ec5\u4f5c\u4e8e\u4e8e\u9009\u533a", None))
    # retranslateUi

