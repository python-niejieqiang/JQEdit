import json
import os
import re
import subprocess
import sys
import time
from functools import partial

import chardet
from PySide6.QtCore import QTranslator, Qt, QUrl, Slot, QRegularExpression
from PySide6.QtGui import QAction, QIcon, QFont, QTextCursor, QDesktopServices, QKeyEvent
from PySide6.QtWidgets import (QApplication, QLabel,QDialog, QCheckBox,QFileDialog, QVBoxLayout,QPushButton,QMainWindow, QFontDialog, QPlainTextEdit,
                               QInputDialog, QLineEdit,QMessageBox, QColorDialog)
from PySide6 import QtGui
from PySide6 import QtCore
from main_window_ui import UI_main_window
from replace_window_ui import Ui_replace_window


class FindReplaceDialog(QDialog, Ui_replace_window):
    def __init__(self, text_edit, parent=None):
        super().__init__(parent)
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

class Notepad(QMainWindow,UI_main_window):
    def __init__(self, file_in_cmd=None):
        super().__init__()
        self.setupUI()
        # 用来记录当前是否打开文件
        self.set_current_file("")
        # 用来记录文件编码，名字
        self.current_file_encoding = ""
        # 记录当前是否打开文件
        self.current_file_name = ""
        # 记录是否需要保存
        self.is_saved = False

        # 最近打开的文件列表
        self.recent_files = []
        self.action_connections = {}
        # 使用os模块读取路径只是为了pyinstaller打包成exe的时候不会报错
        self.recent_files_path = os.path.join(resource_path,"recent_files.json")


        # 把命令行第一个参数作为文件名打开
        if file_in_cmd is not None:
            self.read_file(file_in_cmd)
        # 读取settings.json文件
        self.json_file = os.path.join(resource_path,"settings.json")
        self.set_window_file=os.path.join(resource_path,"window_size.json")
        # 读取并设置启动窗口尺寸
        self.read_startup_size()
        self.load_settings()
        self.load_recent_files()
        self.update_recent_files_menu()

        # 创建查找对话框的实例,暂时不显示,点击查找替换才显示在display_replace函数中使用
        self.find_replace_dialog = FindReplaceDialog(self.text_edit, self)

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

    @Slot()
    def show_startup_size_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("设置启动窗口尺寸")

        width_label = QLabel("宽度:", dialog)
        width_edit = QLineEdit(dialog)
        width_edit.setValidator(QtGui.QIntValidator())

        height_label = QLabel("高度:", dialog)
        height_edit = QLineEdit(dialog)
        height_edit.setValidator(QtGui.QIntValidator())

        maximize_checkbox = QCheckBox("启动最大化", dialog)
        maximize_checkbox.stateChanged.connect(lambda state: self.on_maximize_checkbox_changed(state, width_edit, height_edit))

        button_ok = QPushButton("确定", dialog)
        button_ok.clicked.connect(lambda: self.save_startup_size(dialog, width_edit.text(), height_edit.text(), maximize_checkbox.isChecked()))

        layout = QVBoxLayout()
        layout.addWidget(width_label)
        layout.addWidget(width_edit)
        layout.addWidget(height_label)
        layout.addWidget(height_edit)
        layout.addWidget(maximize_checkbox)
        layout.addWidget(button_ok)

        dialog.setLayout(layout)
        dialog.exec()

    def on_maximize_checkbox_changed(self, state, width_edit, height_edit):
        # 根据复选框的状态启用或禁用宽度和高度编辑框
        width_edit.setEnabled(state == QtCore.Qt.Unchecked)
        height_edit.setEnabled(state == QtCore.Qt.Unchecked)

    def save_startup_size(self, dialog, width, height, is_maximized):
        try:
            if is_maximized:
                width = 0
                height = 0
            else:
                width = int(width)
                height = int(height)
        except ValueError:
            QMessageBox.critical(self, "错误", "请输入有效的数字", QMessageBox.Ok)
            return

        # 保存启动窗口尺寸及最大化状态到settings.json
        with open(self.set_window_file, 'w') as f:
            json.dump({"startup_size": {"width": width, "height": height, "maximized": is_maximized}}, f)
        dialog.close()

    def read_startup_size(self):
        try:
            # 从settings.json读取启动窗口尺寸及最大化状态
            with open(self.set_window_file, 'r') as f:
                settings = json.load(f)
                startup_size = settings.get("startup_size", {})
                width = startup_size.get("width", 800)
                height = startup_size.get("height", 600)
                is_maximized = startup_size.get("maximized", False)
                if is_maximized:
                    self.showMaximized()
                else:
                    self.resize(int(width), int(height))
        except (FileNotFoundError, ValueError):
            # 如果settings.json文件不存在，或者值为空， 默认使用800x600的尺寸
            self.resize(800, 600)

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
                # 一行一行读取文件，再连接起来。
                content = "".join(line for line in f)
            self.text_edit.setPlainText(content)
            self.set_current_file(filename)
            # 将文件路径保存至最近打开
            self.add_recent_file(filename)
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

    def add_recent_file(self, file_path):
        # 添加最近打开的文件路径到列表中
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        # 如果超过十个文件，则移除列表中最早打开的文件
        if len(self.recent_files) > 10:
            self.recent_files.pop(-1)
        # 更新最近打开的文件菜单
        self.update_recent_files_menu()
        self.save_recent_files()

    def clear_recent_files(self):
        # 清空最近打开文件列表
        self.recent_files = []
        # 更新最近打开菜单
        self.update_recent_files_menu()
        # 保存最近打开文件列表
        self.save_recent_files()

    def update_recent_files_menu(self):
        # 清空最近打开的文件菜单
        self.recent_files_menu.clear()

        # 添加最近打开的文件到菜单中
        self.action_connections.clear()  # 清空连接字典
        for file_path in self.recent_files:
            action = QAction(os.path.basename(file_path), self)
            new_connection = partial(self.read_file, file_path)
            action.triggered.connect(new_connection)
            self.action_connections[action] = new_connection
            self.recent_files_menu.addAction(action)

        # 添加清空记录的菜单项，但只有在有记录时才显示
        if self.recent_files:
            self.recent_files_menu.addSeparator()  # 添加分隔符
            self.clear_recent_files_action.setVisible(True)  # 设置可见
            self.recent_files_menu.addAction(self.clear_recent_files_action)

    def load_recent_files(self):
        if os.path.exists(self.recent_files_path):
            with open(self.recent_files_path, "r") as f:
                self.recent_files = json.load(f)

    def save_recent_files(self):
        with open(self.recent_files_path, "w") as f:
            json.dump(self.recent_files, f)

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
                border:none
            }
          """)
        self.theme = "light"
        self.clear_checked()
        self.light_theme_action.setChecked(True)
        self.save_settings()

    def set_dark_style(self):
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color:rgb(19,19,20);
                color: rgb(168, 153, 132);
                selection-background-color: rgb(53, 65, 72);
                selection-color: rgb(168, 153, 132);
                border:1px
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
            self.find_replace_dialog.search_text.setText(selected_text)
        self.find_replace_dialog.exec()

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
            self.current_file_name=""
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

#=====================================================================================

def load_and_install_translator(resource_path, language_code):
    #此方法不要写到MyNotepad类中，翻译文件必须在图形界面初始化前启动
    translator = QTranslator()
    translator_path = os.path.join(resource_path, f"{language_code}.qm")
    translator.load(translator_path)
    app.installTranslator(translator)

def get_file_argument():
    """
    获取命令行参数中的文件路径, 再加上注册表中的设置"program.exe" "%1"，使得双击文件能打开读取
    """
    if len(sys.argv) > 1:
        return os.path.abspath(sys.argv[1])
    else:
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 获取当前程序的绝对路径,构建资源文件夹的绝对路径（资源文件夹在可执行文件内部是 'resources/'）
    current_directory = os.path.dirname(os.path.abspath(__file__))
    resource_path = os.path.join(sys._MEIPASS if hasattr(sys, '_MEIPASS') else current_directory, 'resources')

    # 加载并安装中文翻译文件
    load_and_install_translator(resource_path, "qt_zh_CN")
    load_and_install_translator(resource_path, "widgets")

    icon_path = os.path.join(resource_path, "JQEdit.png")
    app.setWindowIcon(QIcon(icon_path))

    # 如果有参数就传给记事本打开（这样打包成exe双击txt就能被记事本打开），否则创建空窗口
    filename = get_file_argument()
    JQEdit = Notepad(filename) if filename else Notepad()
    JQEdit.show()
    sys.exit(app.exec())
