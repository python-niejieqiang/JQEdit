from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QMainWindow, QWidget, QFontDialog, QPlainTextEdit,
                               QMenu, QInputDialog, QMenuBar, QStatusBar, QMessageBox, QColorDialog)
from PySide6.QtCore import QTranslator,Qt, QUrl, Slot,QRegularExpression
from PySide6.QtGui import QAction, QColor, QIcon, QFont, QTextCursor, QDesktopServices, QKeyEvent,QPainter
import chardet
import time
import sys
import subprocess
import functools
import os
import re
import json
from replace_window_ui import Ui_replace_window

class ReplaceDialog(QDialog, Ui_replace_window):
    def __init__(self, text_edit, parent=None):
        super().__init__(parent)
        self.setFixedSize(530, 182)
        self.text_edit = text_edit
        self.setupUi(self)
        self.findnext_btn.clicked.connect(self.find_next)
        self.replace_btn.clicked.connect(self.replace)
        self.allreplace_btn.clicked.connect(self.replace_all)
        self.cancel_btn.clicked.connect(self.close_dialog)
        self.regex = None
        self.original_text = None
        self.loop_count = 0

    def update_regex(self):
        pattern = self.search_text.text()
        options = QRegularExpression.PatternOption(0)

        if self.matchcase_check.isChecked():
            options &= ~QRegularExpression.CaseInsensitiveOption
        else:
            options |= QRegularExpression.CaseInsensitiveOption

        if self.multiline_check.isChecked():
            options |= QRegularExpression.MultilineOption
        if self.dotall_check.isChecked():
            options |= QRegularExpression.DotMatchesEverythingOption

        try:
            self.regex = QRegularExpression(pattern, options)
        except QRegularExpression.SyntaxError:
            QApplication.instance().beep()
            QMessageBox.critical(self, "错误", "无效的正则表达式，请重新输入", QMessageBox.Ok)
            self.regex = None

    def find_next(self):
        self.update_regex()
        cursor = self.text_edit.textCursor()
        plain_text = self.text_edit.toPlainText()

        start = cursor.selectionStart() if cursor.hasSelection() else cursor.position()
        end = cursor.selectionEnd() if cursor.hasSelection() else cursor.position()

        if self.up_rdbtn.isChecked():
            direction = -1
            start, end = 0, start
        else:
            direction = 1
            start, end = end, len(plain_text)

        match_iter = self.regex.globalMatch(plain_text, start)

        last_match = None
        while match_iter.hasNext():
            match = match_iter.next()
            match_start = match.capturedStart()
            match_end = match.capturedEnd()

            if direction == -1:
                if match_start >= end:
                    if last_match:
                        cursor.setPosition(last_match.capturedStart())
                        cursor.setPosition(last_match.capturedEnd(), QTextCursor.KeepAnchor)
                        self.text_edit.setTextCursor(cursor)
                        return
                    else:
                        if self.loop_count == 0:
                            QApplication.instance().beep()
                            cursor.setPosition(len(plain_text))
                            self.text_edit.setTextCursor(cursor)
                            return
                        else:
                            self.loop_count = 0
                            return self.find_next()  # 继续从头搜索
                else:
                    last_match = match
            else:
                if match_start >= start:
                    cursor.setPosition(match_start)
                    cursor.setPosition(match_end, QTextCursor.KeepAnchor)
                    self.text_edit.setTextCursor(cursor)
                    return

        if direction == -1:
            if last_match:
                cursor.setPosition(last_match.capturedStart())
                cursor.setPosition(last_match.capturedEnd(), QTextCursor.KeepAnchor)
                self.text_edit.setTextCursor(cursor)
            else:
                if self.loop_count == 0:
                    QApplication.instance().beep()
                    cursor.setPosition(len(plain_text))
                    self.text_edit.setTextCursor(cursor)
                    return
                else:
                    self.loop_count = 0
                    return self.find_next()  # 继续从头搜索
        else:
            if self.loop_count == 0:
                QApplication.instance().beep()
                cursor.setPosition(0)
                self.text_edit.setTextCursor(cursor)
                return
            else:
                self.loop_count = 0
                return self.find_next()  # 继续从头搜索

    def replace(self):
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.replacewith_text.text())
        self.find_next()

    def replace_all(self):
        document = self.text_edit.document()
        cursor = QTextCursor(document)
        pattern = self.search_text.text()
        replacement = self.replacewith_text.text()

        matchcase = self.matchcase_check.isChecked()
        multiline = self.multiline_check.isChecked()
        dotall = self.dotall_check.isChecked()

        flags = 0
        if not matchcase:
            flags |= re.IGNORECASE
        if multiline:
            flags |= re.MULTILINE
        if dotall:
            flags |= re.DOTALL

        cursor.beginEditBlock()

        plain_text = self.text_edit.toPlainText()
        new_text = re.sub(pattern, replacement, plain_text, flags=flags)

        if new_text == plain_text:
            QApplication.instance().beep()

        cursor.select(QTextCursor.Document)
        cursor.removeSelectedText()
        cursor.insertText(new_text)

        cursor.endEditBlock()

    def close_dialog(self):
        self.close()

class MyNotepad(QMainWindow):
    def __init__(self, file_in_cmd=None):
        super().__init__()

        self.app_name = "JQEdit"
        self.setWindowTitle(self.app_name)
        # 初始化界面，依次添加菜单栏，text_edit，status_bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.text_edit = QPlainTextEdit()
        self.text_edit.cursorPositionChanged.connect(self.get_row_col)
        # 设置文本反锯齿
        self.setDefaultRenderHints()

        self.setCentralWidget(self.text_edit)

        # 添加底部状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # 用来记录当前是否打开文件
        self.set_current_file("")
        # 用来记录文件编码，名字
        self.current_file_encoding = ""
        # 记录当前是否打开文件
        self.current_file_name = ""
        # 记录是否需要保存
        self.is_saved = False

        # 把命令行第一个参数作为文件名打开
        if file_in_cmd is not None:
            self.read_file(file_in_cmd)

        # 添加菜单项
        self.file_menu = QMenu("文件", self.menu_bar)
        self.menu_bar.addMenu(self.file_menu)

        self.edit_menu = QMenu("编辑", self.menu_bar)
        self.menu_bar.addMenu(self.edit_menu)

        self.theme_menu = QMenu("主题", self.menu_bar)
        self.menu_bar.addMenu(self.theme_menu)

        self.find_menu = QMenu("查找", self.menu_bar)
        self.menu_bar.addMenu(self.find_menu)

        self.bianma_menu = QMenu("编码", self.menu_bar)
        self.menu_bar.addMenu(self.bianma_menu)

        self.tool_menu = QMenu("工具", self.menu_bar)
        self.menu_bar.addMenu(self.tool_menu)

        # 文件菜单
        self.new_file_action = QAction("新建(&N)", self)
        self.new_file_action.setShortcut("Ctrl+N")
        self.new_file_action.triggered.connect(self.new_file)
        self.file_menu.addAction(self.new_file_action)

        self.open_action = QAction("打开(&O)", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_dialog)
        self.file_menu.addAction(self.open_action)

        self.save_action = QAction("保存(&S)", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save)
        self.file_menu.addAction(self.save_action)

        self.save_as_action = QAction("另存(&A)", self)
        self.save_as_action.setShortcut("Alt+S")
        self.save_as_action.triggered.connect(self.save_as)
        self.file_menu.addAction(self.save_as_action)

        self.exit_action = QAction("退出(&X)", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

        # 编辑 菜单
        self.undo_action = QAction("撤销(&U)", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.triggered.connect(self.undo)
        self.edit_menu.addAction(self.undo_action)

        self.redo_action = QAction("重做(&Y)", self)
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.triggered.connect(self.redo)
        self.edit_menu.addAction(self.redo_action)
        # 添加菜单分割线
        self.edit_menu.addSeparator()

        self.emptyline_action = QAction(self.tr("清空行(&M)"), self)
        self.emptyline_action.setShortcut("Ctrl+K")
        self.emptyline_action.triggered.connect(self.empty_line)
        self.edit_menu.addAction(self.emptyline_action)

        self.copyline_action = QAction(self.tr("复制行(&H)"), self)
        self.copyline_action.setShortcut("Ctrl+R")
        self.copyline_action.triggered.connect(self.copy_line)
        self.edit_menu.addAction(self.copyline_action)

        self.del_line_action = QAction(self.tr("删除行(&D)"), self)
        self.del_line_action.setShortcut("Alt+D")
        self.del_line_action.triggered.connect(self.delete_line)
        self.edit_menu.addAction(self.del_line_action)

        self.comment_action = QAction(self.tr("切换注释(&S)"), self)
        self.comment_action.setShortcut("Ctrl+/")
        self.comment_action.triggered.connect(self.comment_selected_text)
        self.edit_menu.addAction(self.comment_action)

        self.edit_menu.addSeparator()

        self.cut_action = QAction("剪切(&T)", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.cut_action.triggered.connect(self.cut)
        self.edit_menu.addAction(self.cut_action)

        self.copy_action = QAction("复制(&C)", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.copy_action.triggered.connect(self.copy)
        self.edit_menu.addAction(self.copy_action)

        self.paste_action = QAction("粘贴(&P)", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.paste_action.triggered.connect(self.paste)
        self.edit_menu.addAction(self.paste_action)

        self.delete_action = QAction("删除(&D)", self)
        self.delete_action.setShortcut("Backspace")
        self.delete_action.triggered.connect(self.delete)
        self.edit_menu.addAction(self.delete_action)

        self.selectall_action = QAction("全选(&A)", self)
        self.selectall_action.setShortcut("Ctrl+A")
        self.selectall_action.triggered.connect(self.select_all)
        self.edit_menu.addAction(self.selectall_action)

        self.edit_menu.addSeparator()

        self.date_action = QAction("日期(&Y)", self)
        self.date_action.setShortcut("F6")
        self.date_action.triggered.connect(self.get_date)
        self.edit_menu.addAction(self.date_action)

        # 主题菜单
        # 将主题样式存入数组全部设为未选中，当用户选中哪一个，就把哪一个设为True
        # 也就是点击哪个主题，哪个主题样式前面就显示打勾
        self.theme_actions = []
        self.def_theme_action = QAction("windows默认", self,checkable=True)
        self.def_theme_action.triggered.connect(self.set_default_style)
        self.theme_menu.addAction(self.def_theme_action)
        self.theme_actions.append(self.def_theme_action)

        self.dark_theme_action = QAction("Dark", self,checkable=True)
        self.dark_theme_action.triggered.connect(self.set_dark_style)
        self.theme_menu.addAction(self.dark_theme_action)
        self.theme_actions.append(self.dark_theme_action)

        self.light_theme_action = QAction("light", self,checkable=True)
        self.light_theme_action.triggered.connect(self.set_light_style)
        self.theme_menu.addAction(self.light_theme_action)
        self.theme_actions.append(self.light_theme_action)

        self.font_action = QAction("字体(&Z)", self)
        self.font_action.setShortcut("Alt+Z")
        self.font_action.triggered.connect(self.modify_font)
        self.theme_menu.addAction(self.font_action)

        self.wrap_action = QAction("自动换行(&W)", self, checkable=True)
        self.wrap_action.setChecked(True)
        self.wrap_action.setShortcut("Alt+W")
        self.wrap_action.triggered.connect(self.wrap_line)
        self.theme_menu.addAction(self.wrap_action)

        self.statusbar_action = QAction("状态栏(&L)", self, checkable=True)
        self.statusbar_action.setChecked(True)
        self.statusbar_action.setShortcut("Alt+L")
        self.statusbar_action.triggered.connect(self.statusbar_toggle)
        self.theme_menu.addAction(self.statusbar_action)

        # 读取settings.json文件
        self.json_file = os.path.join(resource_path,"settings.json")
        self.load_settings()

        # 主窗口部分
        self.replace_action = QAction("查找/替换(&Z)", self)
        # 创建查找对话框的实例,暂时不显示,点击查找替换才显示在display_replace函数中使用
        self.find_dialog = ReplaceDialog(self.text_edit, self)
        self.replace_action.triggered.connect(self.display_replace)
        self.find_menu.addAction(self.replace_action)
        # 编码菜单
        encodings = ["utf-8", "gb18030", "utf-32-le", "utf-32-be", "utf-16le", "utf-16be", "iso-8859-1", "ascii",
                     "euc_jisx0213",
                     "euc_kr", "cp866"]
        for code_name in encodings:
            self.encoding_submenu = QMenu(code_name, self.bianma_menu)
            self.bianma_menu.addMenu(self.encoding_submenu)

            self.to_sava_as = QAction("以该编码另存", self)
            self.encoding_submenu.addAction(self.to_sava_as)
            self.to_sava_as.triggered.connect(functools.partial(self.use_code_save, cod=code_name))
            self.to_open = QAction("以该编码重新加载", self)
            self.to_open.triggered.connect(functools.partial(self.re_open, coding=code_name))
            self.encoding_submenu.addAction(self.to_open)

        # 工具菜单
        self.cmd_action = QAction("命令行")
        self.cmd_action.triggered.connect(self.open_terminal)
        self.tool_menu.addAction(self.cmd_action)

        self.color_picker_action = QAction("取色器")
        self.color_picker_action.triggered.connect(self.pick_color)
        self.tool_menu.addAction(self.color_picker_action)

        self.about_action = QAction("关于")
        self.about_action.triggered.connect(self.about_info)
        self.tool_menu.addAction(self.about_action)

        self.help_action = QAction("帮助")
        self.help_action.triggered.connect(self.help_info)
        self.tool_menu.addAction(self.help_action)

        #  自定义右键菜单
        self.context_menu = QMenu()
        self.undo_context = QAction("撤销", self)
        self.undo_context.triggered.connect(self.undo)
        self.context_menu.addAction(self.undo_context)
        # 添加菜单分割线
        self.context_menu.addSeparator()
        self.copy_context = QAction("复制", self)
        self.copy_context.triggered.connect(self.copy)
        self.context_menu.addAction(self.copy_context)
        self.paste_context = QAction("粘贴", self)
        self.paste_context.triggered.connect(self.paste)
        self.context_menu.addAction(self.paste_context)

        self.cut_context = QAction("剪切", self)
        self.cut_context.triggered.connect(self.cut)
        self.context_menu.addAction(self.cut_context)

        self.del_context = QAction("删除", self)
        self.del_context.triggered.connect(self.delete)
        self.context_menu.addAction(self.del_context)
        # 添加菜单分割线
        self.context_menu.addSeparator()

        self.cp_line_context = QAction("复制行", self)
        self.cp_line_context.triggered.connect(self.copy_line)
        self.context_menu.addAction(self.cp_line_context)

        self.del_line_ = QAction("删除行", self)
        self.del_line_.triggered.connect(self.delete_line)
        self.context_menu.addAction(self.del_line_)

        self.empty_context = QAction("清空行", self)
        self.empty_context.triggered.connect(self.empty_line)
        self.context_menu.addAction(self.empty_context)
        # 添加菜单分割线
        self.context_menu.addSeparator()

        self.search_action = QAction("百度搜索", self)
        self.search_action.triggered.connect(self.search_in_baidu)
        self.context_menu.addAction(self.search_action)

        self.redo_context = QAction("重做", self)
        self.redo_context.triggered.connect(self.redo)
        self.context_menu.addAction(self.redo_context)

        self.select_context = QAction("全选", self)
        self.select_context.triggered.connect(self.select_all)
        self.context_menu.addAction(self.select_context)

        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.show_contextmenu)


    # 点击关闭按钮时提示要不要保存（重写closeEvent）
    def closeEvent(self, event):
        if self.tip_to_save():
            event.accept()  # 用户选择保存或确定不保存，继续关闭
        else:
            event.ignore()  # 用户选择取消保存，不关闭窗口

    def keyPressEvent(self, event: QKeyEvent):
        #  Ctrl+F 弹出查找对话框，如果有选中文字则搜索框直接显示
        if event.key() == Qt.Key_F and event.modifiers() & Qt.ControlModifier:
            self.display_replace()
            event.accept()
            return

            # 检测 Ctrl+G 组合键
        if event.key() == Qt.Key_G and event.modifiers() & Qt.ControlModifier:
            # 弹出输入框
            line_number, ok = QInputDialog.getInt(self, "跳转到行", "请输入行号:")
            if ok and line_number > 0:
                # 跳转到指定行
                self.jump_to_line(line_number - 1)  # 行号从1开始计数，但QTextCursor从0开始
            event.accept()
            return  # 阻止默认事件处理
        # 如果不是 Ctrl+G，则调用默认的事件处理
        super().keyPressEvent(event)

    def set_current_file(self, filename_):
        # 如有打开文件，则显示文件名，没有则显示APP名
        self.current_opened_file = filename_
        # 只需要设置文档的修改状态，窗口的修改状态会自动更新
        self.text_edit.document().setModified(False)
        # 合并条件判断，并设置窗口标题
        if filename_:
            self.setWindowTitle(f"{self.app_name} - {filename_}")
        else:
            self.setWindowTitle(self.app_name)

    def tip_to_save(self):
        if self.text_edit.document().isModified():
            result = self.alert_dialog()
            if result == 0:  # 用户选择保存
                return self.save()
            elif result == 1:  # 用户选择不保存
                return True
                # 如果用户选择取消，则不执行任何操作并返回 False
            return False
        return True

        # 提示保存对话框根据用户不同的选择返回不同的值

    def alert_dialog(self):
        alert_box = QMessageBox(self)
        alert_box.setWindowTitle(self.app_name)
        alert_box.setText(self.tr("文件已被修改，是否保存?"))
        save_button = alert_box.addButton("保存", QMessageBox.AcceptRole)
        unsave_button = alert_box.addButton("不保存", QMessageBox.RejectRole)
        cancel_button = alert_box.addButton("取消", QMessageBox.DestructiveRole)
        alert_box.exec()
        button_clicked = alert_box.clickedButton()

        if button_clicked is save_button:
            return 0  # 保存
        elif button_clicked is unsave_button:
            return 1  # 不保存
        # 取消操作不需要返回值，因为 tip_to_save 会根据返回值来判断

    def save_file(self, file_name):
        """
        将文本编辑器的内容保存到指定文件，并更新当前打开的文件名。
        :param file_name: 要保存的文件名
        :return: 如果保存成功返回 True，否则返回 False
        """
        try:
            with open(file_name, "w", encoding=self.current_file_encoding) as outfile:
                text = self.text_edit.toPlainText()
                outfile.write(text)
            self.set_current_file(file_name)
            return True
        except IOError as e:
            # IO 错误，如文件无法创建或写入
            QMessageBox.warning(self, self.app_name, f"文件 {file_name} 保存失败:\n{e}")
        except UnicodeEncodeError as e:
            # 编码错误，如文本包含无法在当前编码中表示的字符
            QMessageBox.warning(self, self.app_name, f"编码错误，文件 {file_name} 保存失败:\n{e}")
        except Exception as e:
            # 其他未知异常
            QMessageBox.warning(self, self.app_name, f"文件 {file_name} 保存时发生未知错误:\n{e}")
        return False

    def read_file(self, filename):
        if not filename:
            return
        try:
            # 尝试读取更多字符以提高编码检测的准确性
            with open(filename, "rb") as f:
                content = f.read(10000)  # 读取更多的内容
                encoding = chardet.detect(content)["encoding"]
                detected = encoding.upper()
                if encoding.upper() in ["GB2312", "GBK"]:
                    encoding = "GB18030"

            # 记录打开文件时的编码和文件名
            self.current_file_name = filename
            self.current_file_encoding = encoding

            with open(filename, "r", encoding=encoding) as f:
                content = f.read()
            self.text_edit.setPlainText(content)
            self.set_current_file(filename)

            # 更新窗口标题以显示文件路径、编码等信息
            self.setWindowTitle(f"{self.app_name} - {detected} - {filename}")

        except FileNotFoundError:
            QMessageBox.warning(self, "错误", "文件未找到，请检查路径是否正确！")
        except PermissionError:
            QMessageBox.warning(self, "错误", "没有足够的权限打开文件！")
        except UnicodeDecodeError:
            QMessageBox.warning(self, "错误", "文件编码无法识别，请尝试手动选择编码！")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"打开文件时发生错误（很可能不支持该文件类型）:{e}")

    def load_settings(self):
        with open(self.json_file, "r") as f:
            settings = json.load(f)

        font_properties = {
            "font_family": "Courier New",
            "pointSize": 12,
            "bold": False,
            "italic": False,
            "underline": False,
            "strikeOut": False
        }

        font_properties.update({k: settings.get(k, v) for k, v in font_properties.items()})

        self.font = QFont(font_properties["font_family"], font_properties["pointSize"])
        self.font.setBold(font_properties["bold"])
        self.font.setItalic(font_properties["italic"])
        self.font.setUnderline(font_properties["underline"])
        self.font.setStrikeOut(font_properties["strikeOut"])

        self.text_edit.setFont(self.font)
        #加载用户字体选择结束

        # 加载用户主题设置
        self.theme = settings.get("theme", "default")

        # 加载用户状态栏，自动换行设置，如果json文件中没有值，使用备选值True
        self.wrap_lines = settings.get("wrap_lines", True)
        self.statusbar_shown = settings.get("statusbar_shown", True)

        self.apply_theme()  # 应用用户的主题选择
        self.apply_wrap_status()  # 应用用户的状态栏，自动换行设置
        self.wrap_action.setChecked(self.wrap_lines)
        self.statusbar_action.setChecked(self.statusbar_shown)

    def apply_wrap_status(self):
        if self.wrap_lines:
            self.text_edit.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        else:
            self.text_edit.setLineWrapMode(QPlainTextEdit.NoWrap)

        if self.statusbar_shown:
            self.status_bar.show()
        else:
            self.status_bar.hide()

    def apply_theme(self):
        if self.theme == "default":
            self.set_default_style()
        elif self.theme == "light":
            self.set_light_style()
        elif self.theme == "dark":
            self.set_dark_style()

    def save_settings(self):
        settings = {
            "font_family": self.font.family(),
            "pointSize": self.font.pointSize(),
            "bold": self.font.bold(),
            "italic": self.font.italic(),
            "underline": self.font.underline(),
            "strikeOut": self.font.strikeOut(),
            "theme": self.theme,
            "wrap_lines": self.wrap_lines,
            "statusbar_shown": self.statusbar_shown
        }
        with open(self.json_file, "w") as f:
            json.dump(settings, f, indent=4)

    def clear_checked(self):
        # 清除主题样式菜单项的选中状态
        for action in self.theme_actions:
            action.setChecked(False)

    def set_default_style(self):
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: white;
                color: black;
                selection-background-color: rgb(100, 149, 237);
                selection-color: white;
                border:none
            }            
          """)
        self.theme = "default"
        self.clear_checked()
        self.def_theme_action.setChecked(True)
        self.save_settings()

    def set_light_style(self):
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: rgb(242, 243, 247);
                color: rgb(38, 38, 38);
                selection-background-color: rgb(184, 221, 224);
                selection-color: rgb(38, 38, 38);
            }
          """)
        self.theme = "light"
        self.clear_checked()
        self.light_theme_action.setChecked(True)
        self.save_settings()

    def set_dark_style(self):
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color:rgb(30,43,50);
                color: rgb(168, 153, 132);
                selection-background-color: rgb(53, 65, 72);
                selection-color: rgb(168, 153, 132);
                border:none
            }

        """)
        self.theme = "dark"
        self.clear_checked()
        self.dark_theme_action.setChecked(True)
        self.save_settings()


    def jump_to_line(self, line_number):
        # 创建 QTextCursor 对象
        cursor = self.text_edit.textCursor()
        # 移动到指定行的开始位置
        cursor.movePosition(QTextCursor.Start)
        for _ in range(line_number):
            # 使用 NextBlock 跳转到下一行
            if not cursor.movePosition(QTextCursor.NextBlock):
                # 如果已经到达文档末尾，则不执行任何操作
                break
                # 将光标设置到文本编辑器中
        self.text_edit.setTextCursor(cursor)
        # 确保光标所在的行是可见的
        self.text_edit.ensureCursorVisible()

    # 行号跳转功能结束
    def is_cursor_at_empty_line_start(self):
        cursor = self.text_edit.textCursor()
        # 获取光标所在位置的文本块
        block = cursor.block()
        # 检查光标是否位于行首且该行是否为空行（去除前后空白字符后）
        return cursor.atBlockStart() and not block.text().strip()

    @Slot()
    def help_info(self):
        help_txt = """   1.匹配中文：[\\u4e00-\\u9fff]+ ,查找框三个选项对应Perl正则中的/i,/m,/s开关)。
   2.鼠标选中想要的文字，按CTRL-F就可以搜索了.按Ctrl-G 可以跳转行号（虽然还没行号）（类似PyCharmIDE中的查找
   3.取色器，点击PICK SCREEN COLOR 拾取颜色）.
        """
        QMessageBox.information(self, self.app_name, help_txt)

    @Slot()
    def about_info(self):
        # 显示关于软件的信息和版权说明
        info_text = """  
        软件希望对使用者有用，但软件及作者不对使用后果负责。
        作者：niejieqiang@copyright
        邮箱：469063190@qq.com  
        """
        QMessageBox.information(self, self.app_name, info_text)

    @Slot()
    def display_replace(self):
        # 点击替换弹出查找对话框,如果有选中文字则直接显示至搜索框
        # 获取选中的文本
        selected_text = self.text_edit.textCursor().selectedText()
        if selected_text:
            # 如果有选中的文本，则将其填充到查找对话框的搜索框中
            self.find_dialog.search_text.setText(selected_text)
        self.find_dialog.exec()

    @Slot()
    def search_in_baidu(self):
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            keyword = cursor.selectedText()
            url = QUrl("https://www.baidu.com/s?wd=" + keyword)
            QDesktopServices.openUrl(url)

    @Slot()
    def open_terminal(self):
        # 获取当前工作目录
        current_dir = os.getcwd()
        try:
            if sys.platform.startswith('win'):
                # 对于Windows系统
                cmd_command = f'start cmd /K cd /D "{current_dir}"'
                subprocess.Popen(cmd_command, shell=True)
            elif sys.platform.startswith('linux'):
                # 对于Linux系统
                # 尝试使用 xdg-open 来打开默认的终端模拟器
                try:
                    term_command = ['xdg-open', '--', 'terminator', '--working-directory', current_dir]
                    subprocess.Popen(term_command)
                except FileNotFoundError:
                    # 如果 terminator 不存在，尝试其他终端
                    try:
                        subprocess.Popen(['gnome-terminal', '--working-directory', current_dir])
                    except FileNotFoundError:
                        # 作为最后的手段，使用 xterm
                        subprocess.Popen(['xterm', '-e', 'bash', '-c', f'cd "{current_dir}" && exec bash'])
            elif sys.platform == 'darwin':
                # 对于macOS系统
                term_command = ['osascript', '-e', f'tell app "Terminal" to do script "cd {current_dir}"']
                subprocess.Popen(term_command)
            else:
                raise Exception("当前系统无法识别，找不到命令行!")
        except Exception as e:
            QMessageBox.warning(self, "发生错误", str(e))

    @Slot()
    def show_contextmenu(self, pos):
        # text_edit中的右键菜单
        self.context_menu.exec(self.text_edit.mapToGlobal(pos))

    @Slot()
    def use_code_save(self, cod, *args):
        # 以该编码另存功能函数
        filename, _ = QFileDialog.getSaveFileName()
        if not filename:
            return
        try:
            with open(filename, "w", encoding=cod) as w:
                w.write(self.text_edit.toPlainText())
                # 更新窗口标题以显示保存成功
            self.setWindowTitle(f"{self.windowTitle()} - 文件已保存")
        except Exception as e:
            # 在这里处理异常，例如通过日志记录或更新窗口标题来显示错误信息
            print(f"保存文件时出错：{e}")

    @Slot()
    def re_open(self, coding, *args):
        # 指定编码加载文件
        try:
            with open(self.current_file_name, "r", encoding=coding, errors="ignore") as infile:
                text = infile.read()
            self.text_edit.setPlainText(text)
            self.current_file_encoding = coding
            self.setWindowTitle(self.current_file_name + " - " + coding.upper() + " - " + self.app_name)
        except FileNotFoundError:
            QMessageBox.warning(self, "错误", "还没打开文件！")

    @Slot()
    def open_dialog(self):
        if self.tip_to_save():
            filename, _ = QFileDialog.getOpenFileName(self, "打开", "",
                                                      "*.txt *.py *.html *.xml *.ini *.bat;;所有文件(*.*)")
            self.read_file(filename)

    # 根据当前是否打开文件来决定是直接保存，还是另存至其他位置（）
    @Slot()
    def save(self):
        if self.current_opened_file:
            return self.save_file(self.current_opened_file)
        else:
            self.save_as()

    @Slot()
    def save_as(self):
        filename, _ = QFileDialog.getSaveFileName(self)
        if filename:
            return self.save_file(filename)
        return False

    @Slot()
    def new_file(self):
        if self.tip_to_save():
            self.text_edit.clear()
            self.setWindowTitle(self.app_name)

    @Slot()
    def modify_font(self):
        # 选择字体
        ok, font = QFontDialog.getFont()
        if not ok: return
        self.text_edit.setFont(font)
        self.font = font  # 更新字体
        self.save_settings()  # 保存字体设置到json

    @Slot()
    def wrap_line(self):
        self.wrap_lines = self.wrap_action.isChecked()
        self.apply_wrap_status()
        self.save_settings()

    @Slot()
    def statusbar_toggle(self):
        self.statusbar_shown = self.statusbar_action.isChecked()
        self.apply_wrap_status()
        self.save_settings()

    @Slot()
    def get_row_col(self):
        # 获取光标所在的行和列
        cursor = self.text_edit.textCursor()
        row = cursor.blockNumber() + 1  # blockNumber() 是从 0 开始的，所以需要加 1
        column = cursor.columnNumber() + 1  # columnNumber() 也是从 0 开始的，加 1 以符合常规的行列计数
        # 将行列信息格式化为字符串并显示在状态栏上
        message = "  行 {}, 列 {}".format(row, column)
        self.status_bar.showMessage(message)

    @Slot()
    def get_date(self):
        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.text_edit.insertPlainText(date_time)

    @Slot()
    def redo(self):
        self.text_edit.redo()

    @Slot()
    def undo(self):
        self.text_edit.undo()

    @Slot()
    def cut(self):
        self.text_edit.cut()

    @Slot()
    def copy(self):
        self.text_edit.copy()

    @Slot()
    def paste(self):
        self.text_edit.paste()

    @Slot()
    def delete(self):
        self.text_edit.textCursor().deletePreviousChar()

    @Slot()
    def comment_selected_text(self):
        # 定义注释符号，python中是 “ # ”
        comment_char = "#"
        # 选取文本注释，在换行符后添加 “ # ”
        cursor = self.text_edit.textCursor()
        has_selection = cursor.hasSelection()

        if has_selection:
            selection_start = cursor.selectionStart()
            selection_end = cursor.selectionEnd()
            #
            cursor.setPosition(selection_start)
            while cursor.position() < selection_end:
                cursor.movePosition(QTextCursor.StartOfLine)
                if cursor.block().text().startswith(comment_char):
                    # 如果行已注释，则去除注释
                    cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, len(comment_char))
                    cursor.removeSelectedText()
                else:
                    # 否则，添加注释
                    cursor.insertText(f"{comment_char}")
                cursor.movePosition(QTextCursor.NextBlock)
        else:
            # 若无选区，注释或取消注释当前行
            cursor.movePosition(QTextCursor.StartOfLine)
            if cursor.block().text().startswith(comment_char):
                cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, len(comment_char))
                cursor.removeSelectedText()
            else:
                cursor.insertText(f"{comment_char}")
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()

    @Slot()
    def delete_line(self):
        cursor = self.text_edit.textCursor()
        # 删除整行包括换行符
        cursor.select(QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()
        # 无需显式删除前一个字符，因为removeSelectedText已经删除了整行
        # 只有在光标位于空行的开头时，才需要删除光标位置的字符以进入下一行
        if self.is_cursor_at_empty_line_start():
            # 删除当前位置的字符（如果它是空行的开头，这将是换行符或空字符）
            cursor.deleteChar()
            # 更新文本编辑器的光标位置
        self.text_edit.setTextCursor(cursor)

    @Slot()
    def copy_line(self):
        # 保存当前光标的位置
        original_cursor_position = self.text_edit.textCursor().position()
        # 复制当前行内容，并且在行首加上 "\n"
        cursor = self.text_edit.textCursor()
        cursor.select(QTextCursor.LineUnderCursor)
        clipboard = QApplication.clipboard()
        clipboard.setText("\n" + cursor.selectedText())

    @Slot()
    def empty_line(self):
        cursor = self.text_edit.textCursor()
        # 移动光标到当前行的末尾
        cursor.movePosition(QTextCursor.EndOfLine)
        # 选中当前行的文本（从行首到光标当前位置）
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        # 移除选中的文本，即清空当前行的内容
        cursor.removeSelectedText()
        # 检查是否处于文本开头且当前行不是空行
        if cursor.atStart() and not self.is_cursor_at_empty_line_start():
            # 在文本开头插入一个换行符，以保留一个空行
            cursor.insertText("\n")
            # 更新文本编辑器的光标位置
        self.text_edit.setTextCursor(cursor)

    @Slot()
    def select_all(self):
        self.text_edit.selectAll()

    @Slot()
    def pick_color(self):
        # 弹出颜色选择器
        QColorDialog.getColor(Qt.white, self, "点击 Pick Screen Color 拾取颜色")

    def setDefaultRenderHints(self):
        # 设置 QPainter 对象的默认渲染策略
        painter = QPainter(self.text_edit.viewport())
        painter.setRenderHint(QPainter.Antialiasing)  # 启用反锯齿
        painter.setRenderHint(QPainter.TextAntialiasing)  # 启用文本反锯齿
        self.text_edit.viewport().update()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 获取当前程序的绝对路径
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # 构建资源文件夹的绝对路径（资源文件夹在可执行文件内部是 'resources/'）
    resource_path = os.path.join(sys._MEIPASS if hasattr(sys, '_MEIPASS') else current_directory, 'resources')
    # 加载图片
    zh_cn_path = os.path.join(resource_path, "qt_zh_CN.qm")
    cn_widgets_path = os.path.join(resource_path, "widgets.qm")
    translator = QTranslator()
    translator1 = QTranslator()

    translator.load(zh_cn_path)
    translator1.load(cn_widgets_path)

    app.installTranslator(translator)
    app.installTranslator(translator1)

    icon_path = os.path.join(resource_path, "JQEdit.png")
    app.setWindowIcon(QIcon(icon_path))
    # 如果有参数就传给记事本打开（这样打包成exe双击txt就能被记事本打开），否则创建空窗口
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    window = MyNotepad(filename) if filename else MyNotepad()
    window.showMaximized()
    sys.exit(app.exec())