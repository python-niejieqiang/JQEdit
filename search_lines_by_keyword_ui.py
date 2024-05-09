# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'search_files.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QLabel,
    QLineEdit, QListView, QMainWindow, QPlainTextEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_search_line(object):
    def setupUi(self, search_line):
        if not search_line.objectName():
            search_line.setObjectName(u"search_line")
        search_line.setFixedSize(580, 581)
        self.centralwidget = QWidget(search_line)
        self.centralwidget.setObjectName(u"centralwidget")
        self.search_result_list = QListView(self.centralwidget)
        self.search_result_list.setObjectName(u"search_result_list")
        self.search_result_list.setGeometry(QRect(10, 50, 561, 261))
        self.detail_text_edit = QPlainTextEdit(self.centralwidget)
        self.detail_text_edit.setObjectName(u"detail_text_edit")
        self.detail_text_edit.setGeometry(QRect(10, 330, 561, 241))
        self.search_text = QLineEdit(self.centralwidget)
        self.search_text.setObjectName(u"search_text")
        self.search_text.setGeometry(QRect(10, 10, 241, 31))
        self.detail_label = QLabel(self.centralwidget)
        self.detail_label.setObjectName(u"detail_label")
        self.detail_label.setGeometry(QRect(10, 305, 53, 31))
        self.dir_button = QPushButton(self.centralwidget)
        self.dir_button.setObjectName(u"dir_button")
        self.dir_button.setGeometry(QRect(340, 20, 75, 23))
        self.file_type_combobox = QComboBox(self.centralwidget)
        self.file_type_combobox.addItem("")
        self.file_type_combobox.addItem("")
        self.file_type_combobox.addItem("")
        self.file_type_combobox.addItem("")
        self.file_type_combobox.addItem("")
        self.file_type_combobox.addItem("")
        self.file_type_combobox.addItem("")
        self.file_type_combobox.addItem("")
        self.file_type_combobox.addItem("")
        self.file_type_combobox.addItem("")
        self.file_type_combobox.addItem("")
        self.file_type_combobox.setObjectName(u"file_type_combobox")
        self.file_type_combobox.setGeometry(QRect(420, 20, 61, 21))
        self.include_subdir_checkbox = QCheckBox(self.centralwidget)
        self.include_subdir_checkbox.setObjectName(u"include_subdir_checkbox")
        self.include_subdir_checkbox.setGeometry(QRect(490, 20, 81, 19))
        self.search_button = QPushButton(self.centralwidget)
        self.search_button.setObjectName(u"search_button")
        self.search_button.setGeometry(QRect(259, 20, 75, 23))
        search_line.setCentralWidget(self.centralwidget)

        self.retranslateUi(search_line)

        QMetaObject.connectSlotsByName(search_line)
    # setupUi

    def retranslateUi(self, search_line):
        search_line.setWindowTitle(QCoreApplication.translate("search_line", u"\u67e5\u627e\u5173\u952e\u5b57\u6240\u5728\u884c", None))
        self.detail_label.setText(QCoreApplication.translate("search_line", u"\u8be6\u7ec6\uff1a", None))
        self.dir_button.setText(QCoreApplication.translate("search_line", u"\u9009\u62e9\u76ee\u5f55..", None))
        self.file_type_combobox.setItemText(0, QCoreApplication.translate("search_line", u"*.*", None))
        self.file_type_combobox.setItemText(1, QCoreApplication.translate("search_line", u"*.txt", None))
        self.file_type_combobox.setItemText(2, QCoreApplication.translate("search_line", u"*.py", None))
        self.file_type_combobox.setItemText(3, QCoreApplication.translate("search_line", u"*.json", None))
        self.file_type_combobox.setItemText(4, QCoreApplication.translate("search_line", u"*.cpp", None))
        self.file_type_combobox.setItemText(5, QCoreApplication.translate("search_line", u"*.c", None))
        self.file_type_combobox.setItemText(6, QCoreApplication.translate("search_line", u"*.pl", None))
        self.file_type_combobox.setItemText(7, QCoreApplication.translate("search_line", u"*.java", None))
        self.file_type_combobox.setItemText(8, QCoreApplication.translate("search_line", u"*.kt", None))
        self.file_type_combobox.setItemText(9, QCoreApplication.translate("search_line", u"*.html", None))
        self.file_type_combobox.setItemText(10, QCoreApplication.translate("search_line", u"*.bat", None))

        self.include_subdir_checkbox.setText(QCoreApplication.translate("search_line", u"\u5305\u542b\u5b50\u76ee\u5f55", None))
        self.search_button.setText(QCoreApplication.translate("search_line", u"\u641c\u7d22", None))
    # retranslateUi

