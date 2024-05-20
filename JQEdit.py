# -*- coding: utf-8 -*-
import codecs
import json
import os
import re
import shutil
import subprocess
import sys
import threading
from functools import partial

import chardet
import pyperclip
from PySide6.QtCore import (QTranslator, QFile, QRunnable, QThreadPool, QThread, QObject, QTextStream, QTimer, QSize,
                            QFileInfo,
                            Qt, QEvent, QRect,
                            Signal, QUrl, Slot,
                            QRegularExpression)
from PySide6.QtGui import (QAction, QIntValidator, QGuiApplication, QKeySequence, QShortcut, QPalette, QPainter,
                           QSyntaxHighlighter,
                           QColor, QTextCharFormat,
                           QIcon, QFont,
                           QTextCursor, QDesktopServices)
from PySide6.QtWidgets import (QApplication, QListWidget, QDialog, QHBoxLayout, QWidget, QLabel, QLineEdit, QCheckBox,
                               QVBoxLayout, QPushButton,
                               QFileDialog, QMainWindow, QDialogButtonBox, QFontDialog, QPlainTextEdit,
                               QMenu, QInputDialog, QMenuBar, QStatusBar, QMessageBox, QColorDialog)

from replace_window_ui import Ui_replace_window

class FileLoader(QThread):
    contentLoaded = Signal(str)

    def __init__(self, filename, encoding, position):
        super().__init__()
        self.filename = filename
        self.encoding = encoding
        self.position = position

    def run(self):
        try:
            with open(self.filename, "rb") as f:
                f.seek(self.position)
                while True:
                    lines = []
                    for _ in range(20000):
                        line = f.readline()
                        if not line:
                            break
                        lines.append(line)
                    if not lines:
                        break
                    content = b"".join(lines).decode(self.encoding,"ignore")
                    self.contentLoaded.emit(content.rstrip())
        except Exception as e:
            print(f"Error loading file: {e}")

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor  # 保存与之关联的文本编辑器实例

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)  # 返回建议的尺寸

    def paintEvent(self, event):
        if not self.editor.show_line_numbers:  # 检查是否应该显示行号
            return

        painter = QPainter(self)
        text_color = self.editor.palette().color(QPalette.Text)
        painter.setPen(text_color)  # 使用文本颜色绘制行号
        painter.fillRect(event.rect(), self.editor.palette().color(QPalette.Base))  # 绘制背景色

        document = self.editor.document()
        top_left = self.editor.viewport().mapToGlobal(event.rect().topLeft())  # 将视口坐标转换为全局坐标
        top_left = self.editor.mapFromGlobal(top_left)  # 将全局坐标转换为编辑器内坐标
        block = document.findBlock(self.editor.cursorForPosition(top_left).position())  # 找到位于指定位置的文本块
        block_number = block.blockNumber()
        top = int(self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top())
        bottom = top + int(self.editor.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                # 在行号区域绘制行号
                painter.drawText(0, top, self.width(), self.editor.fontMetrics().height(),
                                 Qt.AlignCenter, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.editor.blockBoundingRect(block).height())
            block_number += 1

class LineNumberWorker(QRunnable):
    def __init__(self, editor, event_rect, dy):
        super().__init__()
        self.editor = editor
        self.event_rect = event_rect
        self.dy = dy

    def run(self):
        # 确保此处的更新逻辑正确处理event_rect和dy
        self.editor.line_number_area.update(self.event_rect)

class TextEditor(QPlainTextEdit):
    def __init__(self, notepad_instance):
        super().__init__()
        self.untitled_name = "Untitled.txt"
        self.notepad = notepad_instance  # 保存与之关联的记事本实例
        # 数字9最高最宽，由此计算出行号所需的最合适的宽度
        self.line_number_digit_width = self.fontMetrics().horizontalAdvance('9')

        self.show_line_numbers = self.notepad.show_line_numbers  # 添加此行，保存行号显示状态
        self.line_number_area = LineNumberArea(self)  # 创建行号区域实例

        # 连接文本块计数变化和更新请求信号到对应槽函数
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        self.update_line_number_area_width()  # 初始化行号区域的宽度

        self.cursorPositionChanged.connect(self.get_row_col)
        self.display_default_file_name(self.notepad.current_file_name)

        self.paste_shortcut = QShortcut(QKeySequence(Qt.CTRL | Qt.SHIFT |Qt.Key_V), self)
        self.paste_shortcut.activated.connect(self.notepad.show_paste_dialog)

        self.setFont(self.notepad.font) # 设置文本区域字体
        self.init_context_menu()

        self.thread_pool = QThreadPool.globalInstance()

    def display_default_file_name(self, filename_):
        # 只需要设置文档的修改状态，窗口的修改状态会自动更新
        self.document().setModified(False)
        # 合并条件判断，并设置窗口标题
        if filename_:
            self.notepad.setWindowTitle(f"{self.notepad.app_name} - {filename_}")
        else:
            self.notepad.setWindowTitle(f"{self.notepad.app_name} - [{self.untitled_name}]")

    def update_status_bar(self, row, column):
        total_lines = self.document().blockCount()
        left_message = "  行 {:d} , 列 {:d} , 总行数 {:d}".format(row, column, total_lines)
        self.notepad.status_bar.showMessage(left_message)

    @Slot()
    def get_row_col(self):
        cursor = self.textCursor()
        row = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.update_status_bar(row, column)

    def update_total_lines(self):
        total_lines = self.document().blockCount()
        self.update_status_bar(1, 1)

    def line_number_area_width(self):
        digits = len(str(self.blockCount()))  # 计算当前文本行数的位数
        return 5 + self.fontMetrics().horizontalAdvance('9') * digits  # 返回行号区域的宽度

    def update_line_number_area_width(self):
        if self.show_line_numbers:
            self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)  # 设置视口边距
        else:
            self.setViewportMargins(0, 0, 0, 0)

    def update_line_number_area(self, event_rect, dy):
        if dy:
            self.line_number_area.scroll(dy, 0)
        else:
            # 限制重绘区域
            self.line_number_area.update(
                event_rect.intersected(QRect(0, 0, self.line_number_area.width(), event_rect.height())))

        if event_rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()

    def update_line_number_display(self, checked):
        self.show_line_numbers = checked  # 切换行号显示状态
        self.update_line_number_area_width()
        if self.show_line_numbers:
            self.line_number_area.setGeometry(QRect(self.viewport().rect().left(), self.viewport().rect().top(),
                                                    self.line_number_area_width(), self.viewport().rect().height()))
        self.line_number_area.setVisible(self.show_line_numbers)
        self.notepad.show_line_numbers = self.show_line_numbers  # 更新记事本的行号显示状态
        self.notepad.save_settings()  # 保存设置到文件

    def update_line_number_area_async(self, event_rect, dy):
        worker = LineNumberWorker(self, event_rect, dy)
        self.thread_pool.start(worker)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.viewport().rect()
        if self.show_line_numbers:
            self.line_number_area.setGeometry(QRect(cr.left(), cr.top(),
                                                     self.line_number_area_width(), cr.height()))

    def setFont(self, font):
        super().setFont(font)
        self.line_number_area.setFont(font)

    def paintEvent(self, event):
        super().paintEvent(event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_QuoteDbl, Qt.Key_Apostrophe):
            cursor = self.textCursor()
            if cursor.hasSelection():
                selected_text = cursor.selectedText()
                start_pos = cursor.selectionStart()
                end_pos = cursor.selectionEnd()

                quote_char = '"' if event.key() == Qt.Key_QuoteDbl else "'"
                cursor.beginEditBlock()
                cursor.setPosition(start_pos)
                cursor.insertText(quote_char)
                cursor.setPosition(end_pos + 1)
                cursor.insertText(quote_char)
                cursor.setPosition(start_pos + 1)
                cursor.setPosition(end_pos + 1, QTextCursor.KeepAnchor)
                cursor.endEditBlock()
                self.setTextCursor(cursor)
                event.accept()
                return  # 一旦处理了这个事件，就不再向下执行，避免与其他逻辑冲突

        if event.key() == Qt.Key_Backspace:
            cursor = self.textCursor()
            if cursor.hasSelection():
                cursor.removeSelectedText()
            else:
                current_block = cursor.block()
                current_line = current_block.text()
                cursor_position = cursor.positionInBlock()

                # 检查当前行是否为全空格（空行）
                if current_line.isspace():
                    # 确保光标位置不是行首，并且从光标位置开始有至少4个空格可以删除
                    if cursor_position > 3:  # 由于索引是从0开始，cursor_position为4时才能删除四个空格
                        # 计算删除的起始位置（从光标前四个字符开始）
                        delete_start = cursor.block().position() + cursor_position - 4
                        cursor.setPosition(delete_start)
                        cursor.setPosition(delete_start + 4, QTextCursor.KeepAnchor)  # 选择四个空格
                        cursor.removeSelectedText()
                        event.accept()  # 阻止默认的退格行为
                    # 如果光标位置不足以删除四个空格，则不做处理，保持默认行为

        if event.key() == Qt.Key_Tab and not event.modifiers():
            cursor = self.textCursor()
            if cursor.hasSelection():
                selected_text = cursor.selectedText().strip()
                if selected_text == "":
                    # 如果选中的是空格或空行，删除选中内容
                    cursor.removeSelectedText()
                    cursor.insertText(" "*4)
                    self.setTextCursor(cursor)
                    event.accept()  # 接受事件以阻止默认的Tab行为
                    return
            self.indent_selected_text()
            event.accept()
        elif event.key() == Qt.Key_Backtab:
            self.shift_unindent_selected_text()
            event.accept()
        elif event.key() == Qt.Key_Tab and event.modifiers() & Qt.ShiftModifier:
            self.shift_unindent_selected_text()
            event.accept()
        else:
            super().keyPressEvent(event)

    def indent_selected_text(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.insertText(" " * 4)
            self.setTextCursor(cursor)
            return

        cursor.beginEditBlock()
        # 获取选区的起始块和结束块
        at_line_start = cursor.positionInBlock() == 0
        initial_start_pos = cursor.selectionStart()
        initial_end_pos = cursor.selectionEnd()
        cursor.setPosition(initial_start_pos)
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.setPosition(initial_end_pos, QTextCursor.KeepAnchor)
        # 复制选中文本到新字符串以避免直接操作导致的问题
        selected_text = cursor.selectedText()
        lines = selected_text.splitlines()  # 安全地分割为多行

        # 初始化计数器
        total_spaces_inserted = 0

        # 在每行前添加缩进，并计算插入的空格总数
        indented_lines = [
            ("    " + line, 4) for line in lines  # 注意这里每行添加了4个空格
        ]
        for _, spaces in indented_lines:  # 这里第二个元素是每行添加的空格数，用于累加
            total_spaces_inserted += spaces

        # 合并回字符串（这一步保持不变）
        indented_text = "\n".join(text for text, _ in indented_lines)
        if at_line_start:
            indented_text+="\n"
        # 清除选区并插入新文本
        cursor.removeSelectedText()
        cursor.insertText(indented_text)
        cursor.setPosition(initial_start_pos + 4)
        cursor.setPosition(initial_end_pos + total_spaces_inserted, QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)
        cursor.endEditBlock()

    def shift_unindent_selected_text(self):
        cursor = self.textCursor()
        initial_selection_start = cursor.selectionStart()
        initial_selection_end = cursor.selectionEnd()
        if cursor.hasSelection():
            cursor.beginEditBlock()

            cursor.setPosition(initial_selection_start)
            num = 0
            while cursor.position() < initial_selection_end and not cursor.atEnd():
                cursor.movePosition(QTextCursor.StartOfLine)

                cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
                line_text = cursor.selectedText()

                if line_text.startswith(" " * 4):
                    # 记录是否所有行都以四个空格开头
                    num += 1
                    # 删除前四个空格
                    cursor.movePosition(QTextCursor.StartOfLine)
                    cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 4)
                    cursor.removeSelectedText()
                # 移动到下一行
                cursor.movePosition(QTextCursor.NextBlock)

                # 检查是否已经到达选区的结束位置
                if cursor.position() >= initial_selection_end:
                    break

            cursor.endEditBlock()

            if num > 0:
                # 调整选区的起始位置
                new_selection_start = max(initial_selection_start - 4, 0)
                new_selection_end = initial_selection_end - 4 * num
                cursor.setPosition(new_selection_start)
                cursor.setPosition(new_selection_end, QTextCursor.KeepAnchor)
                self.setTextCursor(cursor)
        else:
            # 处理未选中文本的情况
            cursor_position = cursor.position()

            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            line_text = cursor.selectedText()

            leading_spaces = len(line_text) - len(line_text.lstrip())
            spaces_to_remove = min(4, leading_spaces)

            cursor.removeSelectedText()
            cursor.insertText(line_text[spaces_to_remove:])

            cursor.setPosition(cursor_position - min(cursor_position, spaces_to_remove))

            self.setTextCursor(cursor)

    def init_context_menu(self):
        #   自定义右键菜单
        self.context_menu = QMenu()
        self.undo_context = QAction("撤销", self)
        self.undo_context.triggered.connect(self.notepad.undo)
        self.context_menu.addAction(self.undo_context)

        self.selection_replace_context = QAction("选区替换", self)
        self.selection_replace_context.triggered.connect(self.notepad.show_replace_dialog)
        self.context_menu.addAction(self.selection_replace_context)

        # 添加菜单分割线
        self.context_menu.addSeparator()
        self.copy_context = QAction("复制", self)
        self.copy_context.triggered.connect(self.notepad.copy)
        self.context_menu.addAction(self.copy_context)

        self.paste_context = QAction("粘贴", self)
        self.paste_context.triggered.connect(self.notepad.paste)
        self.context_menu.addAction(self.paste_context)

        self.cut_context = QAction("剪切", self)
        self.cut_context.triggered.connect(self.notepad.cut)
        self.context_menu.addAction(self.cut_context)

        self.del_context = QAction("删除", self)
        self.del_context.triggered.connect(self.notepad.delete)
        self.context_menu.addAction(self.del_context)
        # 添加菜单分割线
        self.context_menu.addSeparator()

        self.cp_line_context = QAction("复制行", self)
        self.cp_line_context.triggered.connect(self.notepad.copy_line)
        self.context_menu.addAction(self.cp_line_context)

        self.del_line_ = QAction("删除行", self)
        self.del_line_.triggered.connect(self.notepad.delete_line)
        self.context_menu.addAction(self.del_line_)

        self.empty_context = QAction("清空行", self)
        self.empty_context.triggered.connect(self.notepad.empty_line)
        self.context_menu.addAction(self.empty_context)

        # 添加菜单分割线
        self.context_menu.addSeparator()

        self.search_action = QAction("百度搜索", self)
        self.search_action.triggered.connect(self.search_in_baidu)
        self.context_menu.addAction(self.search_action)

        self.redo_context = QAction("重做", self)
        self.redo_context.triggered.connect(self.notepad.redo)
        self.context_menu.addAction(self.redo_context)

        self.select_context = QAction("全选", self)
        self.select_context.triggered.connect(self.notepad.select_all)
        self.context_menu.addAction(self.select_context)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_contextmenu)

    @Slot()
    def search_in_baidu(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            keyword = cursor.selectedText()
            url = QUrl("https://www.baidu.com/s?wd=" + keyword)
            QDesktopServices.openUrl(url)

    @Slot()
    def show_contextmenu(self, pos):
        # text_edit中的右键菜单
        self.context_menu.exec(self.mapToGlobal(pos))

class SyntaxHighlighterBase(QSyntaxHighlighter):
    def __init__(self, parent=None, theme_name="dark"):
        super().__init__(parent)

        self.keyword_format = QTextCharFormat()
        self.string_format = QTextCharFormat()
        self.comment_format = QTextCharFormat()
        self.operator_format = QTextCharFormat()

        self.highlight_rules = [
            (QRegularExpression(r"[\/\*\.\-\+\=\:\|\,\>\<\!\&\%]"), self.operator_format),
            (QRegularExpression(r"\"[^\n]*?\"|\'[^\n]*?\'"), self.string_format)
        ]
        self.load_theme_colors(theme_name)

    def load_theme_colors(self, theme_name):
        try:
            syntax_highlighter_file = os.path.join(resource_path, "syntax_highlighter_file.json")
            with open(syntax_highlighter_file, "r") as f:
                themes = json.load(f)
                theme_colors = themes.get(theme_name, {})
                self.keyword_format.setForeground(
                    QColor(*theme_colors.get("keyword", {}).get("color", [200, 120, 50])))
                self.comment_format.setForeground(
                    QColor(*theme_colors.get("comment", {}).get("color", [150, 150, 150])))
                self.string_format.setForeground(
                    QColor(*theme_colors.get("string", {}).get("color", [42, 161, 152])))
                self.operator_format.setForeground(
                    QColor(*theme_colors.get("operator", {}).get("color", [200, 120, 50])))

                # 设置粗体和斜体
                self.set_format_attributes(self.comment_format, theme_colors.get("comment", {}))
                self.set_format_attributes(self.string_format, theme_colors.get("string", {}))
                self.set_format_attributes(self.operator_format, theme_colors.get("operator", {}))
                self.set_format_attributes(self.keyword_format, theme_colors.get("keyword", {}))

        except FileNotFoundError:
            # 如果文件不存在，使用默认颜色
            pass

    def set_format_attributes(self, format_, attributes):
        bold = attributes.get("bold", False)
        italic = attributes.get("italic", False)
        format_.setFontWeight(QFont.Bold if bold else QFont.Normal)
        format_.setFontItalic(italic)

    def highlightBlock(self, text):
        for expression, format_ in self.highlight_rules:
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, format_)

class PythonHighlighter(SyntaxHighlighterBase):
    def __init__(self, parent=None, theme_name="dark"):  # 添加 theme_name 参数
        super().__init__(parent, theme_name=theme_name)  # 传递 theme_name 参数

        self.highlight_rules.extend([
            (QRegularExpression(r"\b(?:and|as|assert|break|class|continue|def|del|elif|else|except|"
                                r"False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|"
                                r"not|or|pass|raise|return|True|try|while|with|yield)\b"), self.keyword_format),
            (QRegularExpression(r"^\s*\#[^\n]*",QRegularExpression.MultilineOption), self.comment_format)
        ])

class BatchHighlighter(SyntaxHighlighterBase):
    def __init__(self, parent=None, theme_name="dark"):  # 添加 theme_name 参数
        super().__init__(parent, theme_name=theme_name)  # 传递 theme_name 参数

        self.highlight_rules.extend([
            (QRegularExpression(r"(?i)\b(?:rem|call|echo|set|cd|if|else|goto|pause|exit|exist)\b"), self.keyword_format),
            (QRegularExpression(r"(?i)^\s*(?:\:\:|REM)[^\n]*",QRegularExpression.MultilineOption), self.comment_format)
        ])

class KotlinHighlighter(SyntaxHighlighterBase):
    def __init__(self, parent=None, theme_name="dark"):
        super().__init__(parent, theme_name=theme_name)

        self.highlight_rules.extend([
            (QRegularExpression(r"\b(?:abstract|actual|annotation|companion|constructor|crossinline|data|"
                                r"enum|expect|external|final|in|infix|init|inline|inner|internal|"
                                r"lateinit|noinline|open|operator|out|override|private|protected|"
                                r"public|reified|sealed|suspend|tailrec|vararg)\b"), self.keyword_format),
            (QRegularExpression(r"^\s*\/\/[^\n]*",QRegularExpression.MultilineOption), self.comment_format)
        ])

class BashHighlighter(SyntaxHighlighterBase):
    def __init__(self, parent=None, theme_name="dark"):
        super().__init__(parent, theme_name=theme_name)

        self.highlight_rules.extend([
            (QRegularExpression(r"\b(?:alias|bg|bind|break|builtin|case|cd|command|compgen|complete|"
                                r"continue|declare|dirs|disown|echo|enable|eval|exec|exit|export|"
                                r"fc|fg|getopts|hash|help|history|if|jobs|kill|let|local|logout|mapfile|"
                                r"popd|printf|pushd|pwd|read|readonly|return|set|shift|shopt|source|"
                                r"suspend|test|times|trap|type|typeset|ulimit|umask|unalias|unset|"
                                r"until|wait|while)\b"), self.keyword_format),
            (QRegularExpression(r"^\s*\#[^\n]*",QRegularExpression.MultilineOption), self.comment_format)
        ])

class CHighlighter(SyntaxHighlighterBase):
    def __init__(self, parent=None, theme_name="dark"):
        super().__init__(parent, theme_name=theme_name)

        self.highlight_rules.extend([
            (QRegularExpression(r"\b(?:asm|include|auto|bool|break|case|catch|char|class|const|"
                                r"const_cast|continue|default|delete|do|double|dynamic_cast|"
                                r"else|enum|explicit|export|extern|false|float|for|friend|goto|"
                                r"if|inline|int|long|mutable|namespace|new|operator|private|"
                                r"protected|public|register|reinterpret_cast|return|short|signed|"
                                r"sizeof|static|static_cast|struct|switch|template|this|throw|true|"
                                r"try|typedef|typeid|typename|union|unsigned|using|virtual|void|"
                                r"volatile|while)\b"), self.keyword_format),
            (QRegularExpression(r"^\s*\/\*[^\n]*\*\/|^\s*\/\/[^\n]*",QRegularExpression.MultilineOption), self.comment_format)
        ])

class CppHighlighter(SyntaxHighlighterBase):
    def __init__(self, parent=None, theme_name="dark"):
        super().__init__(parent, theme_name=theme_name)

        self.highlight_rules.extend([
            (QRegularExpression(r"\b(?:asm|auto|bool|break|case|catch|char|class|const|const_cast|"
                                r"continue|default|delete|do|double|dynamic_cast|else|enum|"
                                r"explicit|export|extern|false|float|for|friend|goto|if|inline|int|"
                                r"long|mutable|namespace|new|operator|private|protected|public|"
                                r"register|reinterpret_cast|return|short|signed|sizeof|static|"
                                r"static_cast|struct|switch|template|this|throw|true|try|typedef|"
                                r"typeid|typename|union|unsigned|using|virtual|void|volatile|while)\b"),
             self.keyword_format),
            (QRegularExpression(r"^\s*\/\/[^\n]*",QRegularExpression.MultilineOption), self.comment_format)  # 单行注释
        ])

class SQLHighlighter(SyntaxHighlighterBase):
    def __init__(self, parent=None, theme_name="dark"):
        super().__init__(parent, theme_name=theme_name)

        self.highlight_rules.extend([
            (QRegularExpression(r"\b(?:SELECT|FROM|WHERE|INSERT|INTO|VALUES|UPDATE|DELETE|"
                                r"CREATE|TABLE|DROP|ALTER|ORDER|BY|GROUP|HAVING|INNER|JOIN|LEFT|"
                                r"RIGHT|OUTER|UNION|ALL|AND|OR|NOT|AS|ON|NULL|TRUE|FALSE|SUM|COUNT|AVG)\b"),self.keyword_format),
            (QRegularExpression(r"^\s*(?:--[^\n]*|\/\*[^\n]*\*\/|\#[^\n]*)",QRegularExpression.MultilineOption), self.comment_format)
        ])

class JavaHighlighter(SyntaxHighlighterBase):
    def __init__(self, parent=None, theme_name="dark"):
        super().__init__(parent, theme_name=theme_name)

        self.highlight_rules.extend([
            (QRegularExpression(r"\b(?:abstract|assert|boolean|break|byte|case|catch|char|class|"
                                r"continue|default|do|double|else|enum|extends|final|finally|float|"
                                r"for|if|implements|import|instanceof|int|interface|long|native|new|"
                                r"null|package|private|protected|public|return|short|static|strictfp|"
                                r"super|switch|synchronized|this|throw|throws|transient|try|void|"
                                r"volatile|while)\b"), self.keyword_format),
            (QRegularExpression(r"^\s*(?:\/\*[^\n]*\*\/|\/\/[^\n]*)",QRegularExpression.MultilineOption), self.comment_format)
        ])

class PerlHighlighter(SyntaxHighlighterBase):
    def __init__(self, parent=None, theme_name="dark"):  # 添加 theme_name 参数
        super().__init__(parent, theme_name=theme_name)  # 传递 theme_name 参数

        # 定义Perl的关键字、操作符、字符串和注释的正则表达式
        self.highlight_rules.extend([
            # Perl关键字，这里只列出了一小部分示例
            (QRegularExpression(r"\b(?:use|my|foreach|while|if|elsif|else|unless|for|next|last|redo|do|sub|return|print|die)\b"),
             self.keyword_format),
            # 单行注释和多行注释
            (QRegularExpression(r"^\s*(?:\/\*[^\n]*\*\/|\#[^\n]*)"), self.comment_format),  # 单行注释
        ])

class XMLHighlighter(SyntaxHighlighterBase):
    def __init__(self, parent=None, theme_name="dark"):
        super().__init__(parent, theme_name=theme_name)

        self.highlight_rules.extend( [
            (QRegularExpression(r"(?:\<\??\w+\s*|\s*\<\/\w+\>)"), self.keyword_format),
            (QRegularExpression(r"^\s*\<\!\-\-[^\n]*?\-\-\>",QRegularExpression.MultilineOption), self.comment_format)
        ])

class HTMLHighlighter(SyntaxHighlighterBase):
    def __init__(self, parent=None, theme_name="dark"):
        super().__init__(parent, theme_name=theme_name)

        # 定义新的高亮规则
        self.highlight_rules.extend([
            # 关键字：在标签中查找
            (QRegularExpression(r"(?<=\<|/)\b(?:<!DOCTYPE|html|head|title|body|style|link|script|div|span|p|a|img|ul|ol|li|table|tr|td|th|form|input|button|select|option|textarea|fieldset|legend|header|footer|section|article|nav|aside|main|figure|figcaption|h1|h2|h3|h4|h5|h6|strong|em|u|s|strike|br)\b(?=\s|\/|\>)"), self.keyword_format),
            (QRegularExpression(r"^\s*\<\!\-\-[^\n]*\-\-\>",QRegularExpression.MultilineOption), self.comment_format)
        ])

class CssHighlighter(SyntaxHighlighterBase):
    def __init__(self, parent=None, theme_name="dark"):
        super().__init__(parent, theme_name=theme_name)

        self.highlight_rules.extend([
            (QRegularExpression(r"^\s*\.*[\w\d_%/\\-]+\s*(?=\{)",QRegularExpression.MultilineOption),self.keyword_format),
            # 注释：以 /* 开头，以 */ 结尾的注释
            (QRegularExpression(r"^\s*(?:/\*\*/|\/\/[^\n]*)",QRegularExpression.MultilineOption), self.comment_format)
        ])

class JavaScriptHighlighter(SyntaxHighlighterBase):
    def __init__(self, parent=None, theme_name="dark"):
        super().__init__(parent, theme_name=theme_name)

        self.highlight_rules.extend([
            (QRegularExpression(r"\b(?:break|case|catch|class|const|continue|debugger|default|delete|"
                                r"do|else|export|extends|false|finally|for|function|if|import|in|"
                                r"instanceof|new|null|return|super|switch|this|throw|true|try|typeof|"
                                r"var|void|while|with|yield)\b"), self.keyword_format),
            (QRegularExpression(r"^\s*(?:\/\*[^\n]*\*\/|\/\/[^\n]*)",QRegularExpression.MultilineOption), self.comment_format)
        ])

class HighlighterFactory:
    @staticmethod
    def create_highlighter(file_extension, theme_name="dark"):
        highlighters = {
            ".py": PythonHighlighter,
            ".bat": BatchHighlighter,
            ".c": CHighlighter,
            ".sql": SQLHighlighter,
            ".java": JavaHighlighter,
            ".pl": PerlHighlighter,
            ".xml": XMLHighlighter,
            ".js": JavaScriptHighlighter,
            ".kt": KotlinHighlighter,
            ".sh": BashHighlighter,
            ".html": HTMLHighlighter,
            ".css": CssHighlighter,
            ".cpp": CppHighlighter
        }

        highlighter_class = highlighters.get(file_extension)
        if highlighter_class:
            return highlighter_class(theme_name=theme_name)
        else:
            return None

class FindReplaceDialog(QDialog, Ui_replace_window):
    def __init__(self, text_edit, parent=None):
        super().__init__(parent)
        self.text_edit = text_edit
        self.setupUi(self)

        self.regex = None
        self.original_text = None
        self.loop_count = 0

        self.findnext_btn.clicked.connect(self.find_next)
        self.replace_btn.clicked.connect(self.replace)
        self.allreplace_btn.clicked.connect(self.replace_all)
        self.cancel_btn.clicked.connect(self.close_dialog)

        self.search_text.textChanged.connect(self.on_search_text_changed)
        self.search_text.setFocus()

        # 为搜索文本框和替换文本框安装事件过滤器
        self.search_text.installEventFilter(self)
        self.replacewith_text.installEventFilter(self)

        # 设置初始焦点
        self.search_text.setFocus()

        self.search_timer = QTimer()  # 定义定时器
        self.search_timer.setInterval(200)  # 设置定时器间隔为500毫秒
        self.search_timer.setSingleShot(True)  # 设置为单次触发
        self.search_timer.timeout.connect(self.update_search)

        # 如果有选中的文本，则将其填充到查找对话框的搜索框中
        selected_text = self.text_edit.textCursor().selectedText()
        if selected_text:
            self.search_text.setText(selected_text)
        self.show()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            if obj == self.search_text:
                self.replacewith_text.setFocus()
                return True
            elif obj == self.replacewith_text:
                self.matchcase_check.setFocus()
                return True
        return super().eventFilter(obj, event)

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

    def update_search(self):
        self.find_matches()

    def find_matches(self):
        self.update_regex()
        cursor = self.text_edit.textCursor()
        plain_text = self.text_edit.toPlainText()

        match_iter = self.regex.globalMatch(plain_text)

        while match_iter.hasNext():
            match = match_iter.next()
            match_start = match.capturedStart()
            match_end = match.capturedEnd()

            cursor.setPosition(match_start)
            cursor.setPosition(match_end, QTextCursor.KeepAnchor)
            self.text_edit.setTextCursor(cursor)
            self.text_edit.centerCursor()  # 居中显示光标所在位置
            return

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
                        self.text_edit.centerCursor()  # 居中显示光标所在位置
                        return
                    else:
                        if self.loop_count == 0:
                            QApplication.instance().beep()
                            cursor.setPosition(len(plain_text))
                            self.text_edit.setTextCursor(cursor)
                            self.text_edit.centerCursor()  # 居中显示光标所在位置
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
                    self.text_edit.centerCursor()  # 居中显示光标所在位置
                    return

        if direction == -1:
            if last_match:
                cursor.setPosition(last_match.capturedStart())
                cursor.setPosition(last_match.capturedEnd(), QTextCursor.KeepAnchor)
                self.text_edit.setTextCursor(cursor)
                self.text_edit.centerCursor()  # 居中显示光标所在位置
            else:
                if self.loop_count == 0:
                    QApplication.instance().beep()
                    cursor.setPosition(len(plain_text))
                    self.text_edit.setTextCursor(cursor)
                    self.text_edit.centerCursor()  # 居中显示光标所在位置
                    return
                else:
                    self.loop_count = 0
                    return self.find_next()  # 继续从头搜索
        else:
            if self.loop_count == 0:
                QApplication.instance().beep()
                cursor.setPosition(0)
                self.text_edit.setTextCursor(cursor)
                self.text_edit.centerCursor()  # 居中显示光标所在位置
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

    def on_search_text_changed(self):
        self.search_timer.start()  # 当搜索文本框内容改变时启动定时器

class SelectionReplaceDialog(QDialog, Ui_replace_window):
    def __init__(self,text_edit, parent=None):
        super().__init__(parent)
        self.text_edit = text_edit
        self.setupUi(self)
        self.setWindowTitle(f" 选区替换")

        # 隐藏查找按钮和单个替换按钮
        self.findnext_btn.hide()
        self.replace_btn.hide()
        # self.multiline_check.hide()
        # 移除方向选择组
        self.direction_gbox.setParent(None)
        # 微调按钮位置，将全部替换按钮的位置和大小设置为与查找按钮相同
        self.allreplace_btn.setGeometry(self.findnext_btn.geometry())
        self.cancel_btn.setGeometry(QRect(400, 80, 101, 31))
        self.matchcase_check.setGeometry(QRect(300, 120, 81, 30))
        self.dotall_check.setGeometry(QRect(185, 120, 71, 30))
        self.multiline_check.setGeometry(QRect(50, 120, 111, 30))

        self.allreplace_btn.clicked.connect(self.replace_all)
        self.cancel_btn.clicked.connect(self.close_dialog)

        # 为搜索文本框和替换文本框安装事件过滤器
        self.search_text.installEventFilter(self)
        self.replacewith_text.installEventFilter(self)

        # 设置初始焦点
        self.search_text.setFocus()
        self.show()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            if obj == self.search_text:
                self.replacewith_text.setFocus()
                return True
            elif obj == self.replacewith_text:
                self.matchcase_check.setFocus()
                return True
        return super().eventFilter(obj, event)

    def replace_all(self):
        cursor = self.text_edit.textCursor()
        selected_text = self.text_edit.textCursor().selectedText()
        if selected_text:
            pattern = self.search_text.text()
            replacement = self.replacewith_text.text()

            matchcase = self.matchcase_check.isChecked()
            dotall = self.dotall_check.isChecked()
            multiline = self.multiline_check.isChecked()

            flags = 0
            if not matchcase:
                flags |= re.IGNORECASE
            if dotall:
                flags |= re.DOTALL

            cursor.beginEditBlock()
            # 获取选区的开始和结束位置
            selection_start = cursor.selectionStart()
            selection_end = cursor.selectionEnd()
            if multiline:
                lines = selected_text.splitlines()
                for i,line in enumerate(lines):
                    lines[i] = re.sub(pattern,replacement,line,flags=flags)
                new_text = "\n".join(lines)
            # 执行替换操作
            else:
                new_text = re.sub(pattern, replacement, selected_text, flags=flags)


            cursor.removeSelectedText()
            cursor.insertText(new_text)
            cursor.endEditBlock()
            # 重新设置选区
            cursor.setPosition(selection_start, QTextCursor.MoveAnchor)
            cursor.setPosition(selection_end, QTextCursor.KeepAnchor)
            self.text_edit.setTextCursor(cursor)

    def close_dialog(self):
        self.close()

class CustomColorDialog(QColorDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOption(QColorDialog.DontUseNativeDialog)  # 禁用原生对话框以自定义界面

        self.copy_html_button = QPushButton("复制HTML颜色", self)
        self.copy_rgb_button = QPushButton("复制RGB颜色", self)

        # 设置按钮宽度
        self.copy_rgb_button.setGeometry(135, 363, 100, 23)
        self.copy_html_button.setGeometry(245, 363, 100, 23)

        # 连接按钮信号
        self.copy_html_button.clicked.connect(self.copy_to_clipboard_html)
        self.copy_rgb_button.clicked.connect(self.copy_to_clipboard_rgb)

    def copy_to_clipboard_html(self):
        color = self.currentColor()
        html_color = color.name()
        pyperclip.copy(html_color)

    def copy_to_clipboard_rgb(self):
        color = self.currentColor()
        rgb_color = f"rgb({color.red()}, {color.green()}, {color.blue()})"
        pyperclip.copy(rgb_color)

class CommandDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("编辑命令")
        layout = QVBoxLayout(self)
        self.command_line_edit = QLineEdit(self)
        layout.addWidget(self.command_line_edit)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_command(self):
        return self.command_line_edit.text()

class ClipboardManager(QObject):
    clipboard_content_changed = Signal()

    def __init__(self, history_file):
        super().__init__()
        self.history_file = history_file
        self.history = []
        # 异步加载历史记录
        self.load_history_async()

    def load_history_async(self):
        threading.Thread(target=self.load_history).start()

        # 连接到剪贴板内容改变的信号槽
        QApplication.clipboard().dataChanged.connect(self.on_clipboard_change)

    @Slot()
    def on_clipboard_change(self):
        mime_data = QApplication.clipboard().mimeData()
        if mime_data.hasText():
            new_content = mime_data.text()
            # 保存剪贴板中的内容到历史记录
            self.add_to_history(new_content)
            # 不直接设置剪贴板的文本内容，而是只保存到历史记录
            self.clipboard_content_changed.emit()  # 发出信号

    def add_to_history(self, content):
        if content not in self.history:
            self.history.insert(0, content)
            self.save_history_async()

    def save_history_async(self):
        threading.Thread(target=self.save_history).start()

    def save_history(self):
        try:
            with codecs.open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=True)
        except Exception as e:
            print(f"Error saving history: {e}")

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with codecs.open(self.history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading history: {e}. History reset.")
                self.backup_history_file()
                self.history = []
        else:
            print("History file not found. A new one will be created.")

    def backup_history_file(self):
        backup_file = f"{self.history_file}.bak"
        try:
            shutil.copy2(self.history_file, backup_file)
            print(f"Backup created: {backup_file}")
        except Exception as e:
            print(f"Error creating backup: {e}")

class PasteDialog(QDialog):
    def __init__(self, clipboard_manager, parent=None):
        super().__init__(parent)
        self.clipboard_manager = clipboard_manager
        self.setWindowTitle("剪贴板历史记录")
        self.setFixedSize(380, 500)

        main_layout = QVBoxLayout(self)

        self.clipboard_list = QListWidget()
        self.clipboard_list.setMinimumHeight(200)
        self.clipboard_list.setUniformItemSizes(True)  # 设置每个条目大小相同
        main_layout.addWidget(self.clipboard_list)

        self.detail_label = QLabel("详细内容:")
        main_layout.addWidget(self.detail_label)

        self.detail_text = QPlainTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setMinimumHeight(100)
        font = QFont()
        font.setPointSize(12)  # 设置字体大小
        self.detail_text.setFont(font)  # 设置字体
        main_layout.addWidget(self.detail_text)

        button_layout = QHBoxLayout()
        self.paste_button = QPushButton("粘贴")
        self.paste_button.setFixedWidth(80)  # 设置按钮长度为80
        self.paste_button.clicked.connect(self.paste_selected)
        button_layout.addWidget(self.paste_button)

        self.cancel_button = QPushButton("取消")
        self.cancel_button.setFixedWidth(80)  # 设置按钮长度为80
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)

        self.clipboard_manager.clipboard_content_changed.connect(self.update_clipboard_list)
        self.clipboard_list.currentItemChanged.connect(self.update_detail_text)
        # 加载剪贴板记录
        self.populate_clipboard_list()

    def populate_clipboard_list(self):
        self.clipboard_list.clear()
        for idx, item in enumerate(self.clipboard_manager.history):
            # 移除所有空白字符
            item_stripped = item.strip()
            # 取前面30个字符显示
            item_display = item_stripped[:50] + "..." if len(item_stripped) > 50 else item_stripped
            item_display = f"{idx + 1}: {item_display}"  # 添加行号
            self.clipboard_list.addItem(item_display)

    def update_clipboard_list(self):
        self.populate_clipboard_list()

    def update_detail_text(self, current, previous):
        if current:
            self.detail_text.setPlainText(self.clipboard_manager.history[self.clipboard_list.currentRow()])

    def paste_selected(self):
        selected_row = self.clipboard_list.currentRow()
        if selected_row != -1:
            content = self.clipboard_manager.history[selected_row]
            clipboard = QApplication.clipboard()

            # 将内容粘贴到光标处
            self.parent().text_edit.textCursor().insertText(content)

            # 清空剪贴板的文本内容
            clipboard.clear()

class LoadRecentFilesWorker(QObject):
    recentFilesLoaded = Signal(list)

    def __init__(self, recent_files_path):
        super().__init__()
        self.recent_files_path = recent_files_path

    def run(self):
        try:
            with open(self.recent_files_path, 'r') as file:
                recent_files = json.load(file)
        except FileNotFoundError:
            recent_files = []
        self.recentFilesLoaded.emit(recent_files)

class CustomCommentDialog(QDialog):
    def __init__(self, current_comment_char="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("自定义注释符号")
        layout = QVBoxLayout()

        self.label = QLabel("请输入新的注释符号:", self)
        layout.addWidget(self.label)

        self.lineEdit = QLineEdit(current_comment_char, self)  # 这里设置默认值
        layout.addWidget(self.lineEdit)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def getCommentChar(self):
        return self.lineEdit.text().strip()

class Notepad(QMainWindow):
    syntax_highlight_toggled = Signal(bool)
    # 定义主题改变信号
    theme_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.app_name = "JQEdit"
        self.resize(800,600)
        # 用来记录文件编码，名字
        self.current_file_encoding = None
        # 记录当前文件名
        self.current_file_name = ""
        # 记录当前文件后缀，用于判断使用何种语法高亮
        self.current_file_extension = ""
        # 记录文件所在目录名，打开命令行时就可以切换到该目录
        self.desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
        self.work_dir = self.desktop_dir

        self.last_modified_time = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_file_modification)
        self.timer.start(2000)  # 每2秒检查一次

        self.highlighter = None
        self.theme_changed.connect(self.on_theme_changed)  # 连接主题改变信号到槽函数
        self.syntax_highlight_toggled.connect(self.toggle_syntax_highlight)

        # 读取settings.json文件
        self.settings_file = os.path.join(resource_path, "settings.json")
        self.immersive_mode = False  # 记录是否处于沉浸模式
        # 读取并设置启动窗口尺寸,主题字体等设置
        self.load_settings()

        # UI初始化，菜单栏以及编辑器，状态栏，各个子菜单，自定义的右键菜单
        self.setup_menu_and_actions()

        # 创建剪贴板管理器
        self.clipboard_manager = ClipboardManager(os.path.join(resource_path,"clipboard_list.json"))

        # 最近打开的文件列表
        self.action_connections = {}
        # 使用os模块读取路径只是为了pyinstaller打包成exe的时候不会报错
        self.recent_files_path = os.path.join(resource_path, "recent_files.json")
        # 这个数组跟命令行参数处理一定要等recent_files_menu初始化才能正常运行
        self.recent_files = []
        self.load_recent_files_thread = QThread()
        self.load_recent_files_worker = LoadRecentFilesWorker(self.recent_files_path)
        self.load_recent_files_worker.recentFilesLoaded.connect(self.handle_recent_files_loaded)
        self.load_recent_files_worker.moveToThread(self.load_recent_files_thread)
        self.load_recent_files_thread.started.connect(self.load_recent_files_worker.run)
        self.load_recent_files_thread.start()
        QGuiApplication.instance().aboutToQuit.connect(self.clean_up_on_exit)

        self._styles_cache = {}  # 用于缓存已加载的样式
        # 预加载基础主题
        self.apply_theme(self.theme)
        self.apply_wrap_status()  # 应用状态栏，自动换行设置

    def setup_menu_and_actions(self):
        # 初始化界面，依次添加菜单栏，text_edit，status_bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.text_edit = TextEditor(self)
        self.setCentralWidget(self.text_edit)

        # 添加底部状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

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

        # 添加最近打开的文件子菜单
        self.recent_files_menu = self.file_menu.addMenu("最近打开")
        # 添加清空记录的菜单项
        self.clear_recent_files_action = QAction("清空记录", self)
        self.clear_recent_files_action.triggered.connect(self.clear_recent_files)
        self.recent_files_menu.addAction(self.clear_recent_files_action)

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

        self.word_menu = self.edit_menu.addMenu("单词")
        self.delete_word_right_action = QAction("右删单词", self)
        self.delete_word_right_action.setShortcut(QKeySequence("Alt+D"))
        self.delete_word_right_action.triggered.connect(self.delete_word_right)
        self.word_menu.addAction(self.delete_word_right_action)

        self.delete_word_left_action = QAction("左删单词", self)
        self.delete_word_left_action.setShortcut(QKeySequence("Alt+Del"))
        self.delete_word_left_action.triggered.connect(self.delete_word_left)
        self.word_menu.addAction(self.delete_word_left_action)

        self.move_word_right_action = QAction("前进一个单词", self)
        self.move_word_right_action.setShortcut(QKeySequence("Alt+F"))
        self.move_word_right_action.triggered.connect(self.move_word_right)
        self.word_menu.addAction(self.move_word_right_action)

        self.move_word_left_action = QAction("后退一个单词", self)
        self.move_word_left_action.setShortcut(QKeySequence("Alt+B"))
        self.move_word_left_action.triggered.connect(self.move_word_left)
        self.word_menu.addAction(self.move_word_left_action)
        self.edit_menu.addMenu(self.word_menu)

        self.case_menu = self.edit_menu.addMenu("大小写")
        self.to_uppercase_action = QAction("转换成大写", self)
        self.to_uppercase_action.triggered.connect(self.to_uppercase)
        self.case_menu.addAction(self.to_uppercase_action)

        self.to_lowercase_action = QAction("转换成小写", self)
        self.to_lowercase_action.triggered.connect(self.to_lowercase)
        self.case_menu.addAction(self.to_lowercase_action)

        self.capitalize_action = QAction("首字母大写", self)
        self.capitalize_action.triggered.connect(self.capitalize_words)
        self.case_menu.addAction(self.capitalize_action)

        self.toggle_case_action = QAction("大小写互换", self)
        self.toggle_case_action.triggered.connect(self.toggle_case)
        self.case_menu.addAction(self.toggle_case_action)
        self.edit_menu.addMenu(self.case_menu)


        self.line_menu = self.edit_menu.addMenu("行")
        self.emptyline_action = QAction("清空行", self)
        self.emptyline_action.setShortcut("Ctrl+K")
        self.emptyline_action.triggered.connect(self.empty_line)
        self.line_menu.addAction(self.emptyline_action)

        self.copyline_action = QAction("复制行", self)
        self.copyline_action.setShortcut("Alt+C")
        self.copyline_action.triggered.connect(self.copy_line)
        self.line_menu.addAction(self.copyline_action)

        self.del_line_action = QAction("删除行", self)
        self.del_line_action.setShortcut("Ctrl+Del")
        self.del_line_action.triggered.connect(self.delete_line)
        self.line_menu.addAction(self.del_line_action)
        self.edit_menu.addMenu(self.line_menu)

        self.comment_action = QAction("切换注释", self)
        self.comment_action.setShortcut("Ctrl+/")
        self.comment_action.triggered.connect(self.comment_selected_text)
        self.edit_menu.addAction(self.comment_action)

        self.custom_comment_char_aciton = QAction("自定义注释符号", self)
        self.custom_comment_char_aciton.triggered.connect(self.set_custom_comment_char)
        self.edit_menu.addAction(self.custom_comment_char_aciton)
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

        # 主题菜单, 将主题样式存入数组全部设为未选中，当用户选中哪一个，就把哪一个设为True
        # 也就是点击哪个主题，哪个主题样式前面就显示打勾
        self.theme_actions = []
        # 初始化动作时设置data属性
        self.intellijlight_theme_action = QAction("Intellij Light", self, checkable=True)
        self.intellijlight_theme_action.setData("intellijlight")  # 设置data
        self.intellijlight_theme_action.triggered.connect(lambda: self.apply_theme("intellijlight"))
        self.theme_menu.addAction(self.intellijlight_theme_action)
        self.theme_actions.append(self.intellijlight_theme_action)

        self.dark_theme_action = QAction("Dark", self, checkable=True)
        self.dark_theme_action.setData("dark")  # 设置data
        self.dark_theme_action.triggered.connect(lambda: self.apply_theme("dark"))
        self.theme_menu.addAction(self.dark_theme_action)
        self.theme_actions.append(self.dark_theme_action)

        self.gerrylight_theme_action = QAction("Gerry Light", self, checkable=True)
        self.gerrylight_theme_action.setData("gerrylight")  # 设置data
        self.gerrylight_theme_action.triggered.connect(lambda: self.apply_theme("gerrylight"))
        self.theme_menu.addAction(self.gerrylight_theme_action)
        self.theme_actions.append(self.gerrylight_theme_action)

        self.xcode_theme_action = QAction("Xcode", self, checkable=True)
        self.xcode_theme_action.setData("xcode")  # 设置data
        self.xcode_theme_action.triggered.connect(lambda: self.apply_theme("xcode"))
        self.theme_menu.addAction(self.xcode_theme_action)
        self.theme_actions.append(self.xcode_theme_action)

        self.font_action = QAction("字体(&Z)", self)
        self.font_action.setShortcut("Alt+Z")
        self.font_action.triggered.connect(self.modify_font)
        self.theme_menu.addAction(self.font_action)

        #添加一个操作来切换行号的可见性
        self.line_numbers_action = QAction("行号", self, checkable=True)
        self.line_numbers_action.setChecked(self.show_line_numbers)
        self.line_numbers_action.triggered.connect(self.toggle_line_numbers)
        self.theme_menu.addAction(self.line_numbers_action)

        self.syntax_highlight_action = QAction("语法高亮", self, checkable=True)
        self.syntax_highlight_action.setChecked(self.syntax_highlight_enabled)
        self.syntax_highlight_action.triggered.connect(self.toggle_syntax_highlight)
        self.theme_menu.addAction(self.syntax_highlight_action)

        # 将语法高亮动作添加到主题菜单
        self.theme_menu.addAction(self.syntax_highlight_action)
        self.wrap_action = QAction("自动换行(&W)", self, checkable=True)
        self.wrap_action.setChecked(self.wrap_line_on)
        self.wrap_action.setShortcut("Alt+W")
        self.wrap_action.triggered.connect(self.wrap_line_toggle)
        self.theme_menu.addAction(self.wrap_action)

        self.statusbar_action = QAction("状态栏(&L)", self, checkable=True)
        self.statusbar_action.setChecked(self.statusbar_shown)
        self.statusbar_action.setShortcut("Alt+L")
        self.statusbar_action.triggered.connect(self.statusbar_toggle)
        self.theme_menu.addAction(self.statusbar_action)
        # 设置启动窗口尺寸
        self.set_startup_size_action = QAction("设置启动窗口尺寸", self)
        self.set_startup_size_action.triggered.connect(self.show_startup_size_dialog)
        self.theme_menu.addAction(self.set_startup_size_action)
        # 沉浸模式
        self.immersive_mode_action = QAction("沉浸模式", self, checkable=True)
        self.immersive_mode_action.setChecked(self.immersive_mode)
        self.immersive_mode_action.triggered.connect(self.toggle_immersive_mode)
        self.immersive_mode_action.setShortcut("F12")
        self.theme_menu.addAction(self.immersive_mode_action)

        # 主窗口部分
        self.replace_action = QAction("查找/替换(&Z)", self)
        self.replace_action.triggered.connect(self.display_replace)
        self.find_menu.addAction(self.replace_action)

        self.selection_replace_action = QAction("选区替换(&R)", self)
        self.selection_replace_action.triggered.connect(self.show_replace_dialog)
        self.find_menu.addAction(self.selection_replace_action)

        encodings = {
            "gb18030": "中文（GB18030）",
            "utf-8": "UTF-8",
            "iso-8859-1": "西欧语系（ISO-8859-1）",
            "ascii": "ASCII码",
            "euc_jisx0213": "日文（EUC-JISX0213）",
            "euc_kr": "韩文（EUC-KR）",
            "cp866": "俄文（Windows-866）",
            "cp1258": "越南语（Windows-1258）",
            "cp1254": "土耳其语（Windows-1254）",
            "tis-620":"泰文（TIS-620）",
            "cp1257":"波罗的语（Windows-1257）",
            "cp1256":"阿拉伯语（Windows-1256）",
            "cp1255":"希伯来文（Windows-1255）",
            "cp1253":"希腊语（Windows-1253）",
            "utf-32-le": "UTF-32 (小端序)",
            "utf-32-be": "UTF-32 (大端序)",
            "utf-16le": "UTF-16 (小端序)",
            "utf-16be": "UTF-16 (大端序)",
        }

        for code_name, chinese_name in encodings.items():
            self.encoding_submenu = QMenu(chinese_name, self.bianma_menu)
            self.bianma_menu.addMenu(self.encoding_submenu)

            self.to_sava_as = QAction(f"以该编码另存", self)
            self.encoding_submenu.addAction(self.to_sava_as)
            self.to_sava_as.triggered.connect(partial(self.use_code_save, encoding=code_name))

            self.to_open = QAction(f"以该编码重新加载", self)
            self.to_open.triggered.connect(partial(self.re_open, coding=code_name))
            self.encoding_submenu.addAction(self.to_open)

        self.run_script_action = QAction("运行")
        self.run_script_action.triggered.connect(self.run_script)
        self.tool_menu.addAction(self.run_script_action)

        self.edit_cmd_action = QAction("编辑命令", self)
        self.edit_cmd_action.triggered.connect(self.edit_command)
        self.tool_menu.addAction(self.edit_cmd_action)

        self.cmd_action = QAction("仅打开命令行")
        self.cmd_action.triggered.connect(self.open_terminal)
        self.tool_menu.addAction(self.cmd_action)

        self.paste_history_action = QAction("剪贴板")
        self.paste_history_action.triggered.connect(self.show_paste_dialog)
        self.tool_menu.addAction(self.paste_history_action)

        self.color_picker_action = QAction("取色器")
        self.color_picker_action.triggered.connect(self.pick_color)
        self.tool_menu.addAction(self.color_picker_action)

        self.about_action = QAction("关于")
        self.about_action.triggered.connect(self.about_info)
        self.tool_menu.addAction(self.about_action)

        self.help_action = QAction("帮助")
        self.help_action.triggered.connect(self.help_info)
        self.tool_menu.addAction(self.help_action)

    def set_custom_comment_char(self):
        dialog = CustomCommentDialog(current_comment_char=self.custom_comment_char, parent=self)
        if dialog.exec() == QDialog.Accepted:
            new_comment_char = dialog.getCommentChar()
            if new_comment_char:  # 确保用户输入不为空
                self.custom_comment_char = new_comment_char
                self.save_settings()
            else:
                QMessageBox.warning(self, "警告", "注释符号不能为空！")

    def handle_recent_files_loaded(self, recent_files):
        self.recent_files = recent_files
        self.update_recent_files_menu()

    def clean_up_on_exit(self):
        self.load_recent_files_thread.quit()  # 请求线程退出
        self.load_recent_files_thread.wait()  # 请求线程退出

    def on_theme_changed(self, new_theme):
        if self.syntax_highlight_enabled:
            self.reload_highlighter(new_theme, self.current_file_extension)

    def reload_highlighter(self, new_theme, file_extension):
        if self.highlighter:
            self.highlighter.deleteLater()
            self.highlighter = None

        if not self.syntax_highlight_enabled:
            return

        highlighter = HighlighterFactory.create_highlighter(file_extension, new_theme)
        if highlighter:
            self.highlighter = highlighter
            self.highlighter.setDocument(self.text_edit.document())

    def toggle_syntax_highlight(self, enable=None):
        if enable is None:
            # 如果没有传递enable参数，则表示从动作中切换状态
            self.syntax_highlight_enabled = not self.syntax_highlight_enabled
            self.syntax_highlight_action.setChecked(self.syntax_highlight_enabled)
        else:
            # 如果传递了enable参数，则根据参数值设置状态
            self.syntax_highlight_enabled = enable

        if self.syntax_highlight_enabled:
            self.reload_highlighter(self.theme, self.current_file_extension)
        else:
            if self.highlighter:
                self.highlighter.deleteLater()
                self.highlighter = None
        self.save_settings()

    def toggle_line_numbers(self, checked):
        self.text_edit.update_line_number_display(checked)

    def check_file_modification(self):
        if self.current_file_name:
            current_time = QFileInfo(self.current_file_name).lastModified().toMSecsSinceEpoch()
            if current_time != self.last_modified_time:
                self.last_modified_time = current_time
                response = QMessageBox.question(self, "提示", "文件内容发生变化，是否加载？",
                                                QMessageBox.Yes | QMessageBox.No)
                if response == QMessageBox.Yes:
                    self.read_file(self.current_file_name)  # 重新加载文件
                else:
                    self.text_edit.document().setModified(True)  # 标记文档已修改

    def show_replace_dialog(self):
        selected_text = self.text_edit.textCursor().selectedText()
        if selected_text:
            selection_replace_dialog = SelectionReplaceDialog(self.text_edit, self)
        else:
            QMessageBox.warning(self, "错误", "先选中文本才能替换！")
            pass

    def toggle_immersive_mode(self):
        if not self.immersive_mode:
            self.immersive_mode = True
            self.showFullScreen()  # 进入全屏模式
            self.text_edit.showFullScreen()  # 让 QPlainTextEdit 占据整个屏幕
            self.menuBar().hide()
            self.immersive_mode_action.setChecked(True)  # 更新菜单项状态
            self.toggle_comment_shortcut = QShortcut(QKeySequence("Ctrl+/"), self)
            self.toggle_comment_shortcut.activated.connect(self.comment_selected_text)
            self.toggle_comment_shortcut.setEnabled(True)

            self.del_line_shortcut = QShortcut(QKeySequence("Ctrl+Del"), self)
            self.del_line_shortcut.activated.connect(self.delete_line)
            self.del_line_shortcut.setEnabled(True)

            self.empty_line_shortcut = QShortcut(QKeySequence("Ctrl+K"), self)
            self.empty_line_shortcut.activated.connect(self.empty_line)
            self.empty_line_shortcut.setEnabled(True)

            self.copy_line_shortcut = QShortcut(QKeySequence("Alt+C"), self)
            self.copy_line_shortcut.activated.connect(self.copy_line)
            self.copy_line_shortcut.setEnabled(True)

            self.delete_word_right_shortcut = QShortcut(QKeySequence("Alt+D"), self)
            self.delete_word_right_shortcut.activated.connect(self.delete_word_right)
            self.delete_word_right_shortcut.setEnabled(True)

            self.delete_word_left_shortcut = QShortcut(QKeySequence("Alt+Del"), self)
            self.delete_word_left_shortcut.activated.connect(self.delete_word_left)
            self.delete_word_left_shortcut.setEnabled(True)

            self.move_word_right_shortcut = QShortcut(QKeySequence("Alt+F"), self)
            self.move_word_right_shortcut.activated.connect(self.move_word_right)
            self.move_word_right_shortcut.setEnabled(True)

            self.move_word_left_shortcut = QShortcut(QKeySequence("Alt+B"), self)
            self.move_word_left_shortcut.activated.connect(self.move_word_left)
            self.move_word_left_shortcut.setEnabled(True)

        else:
            self.showNormal()  # 退出全屏模式
            self.immersive_mode = False
            self.menuBar().show()
            self.immersive_mode_action.setChecked(False)  # 更新菜单项状态
            self.toggle_comment_shortcut.setEnabled(False)
            self.del_line_shortcut.setEnabled(False)
            self.empty_line_shortcut.setEnabled(False)
            self.copy_line_shortcut.setEnabled(False)
            self.delete_word_right_shortcut.setEnabled(False)
            self.delete_word_left_shortcut.setEnabled(False)
            self.move_word_right_shortcut.setEnabled(False)
            self.move_word_left_shortcut.setEnabled(False)


    # 点击关闭按钮时提示要不要保存（重写closeEvent）
    def closeEvent(self, event):
        if self.tip_to_save():
            event.accept()  # 用户选择保存或确定不保存，继续关闭
        else:
            event.ignore()  # 用户选择取消保存，不关闭窗口

    def show_paste_dialog(self):
        # 按需创建PasteDialog实例
        self.paste_dialog = PasteDialog(self.clipboard_manager, parent=self)
        self.paste_dialog.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F12:
            self.toggle_immersive_mode()
        # 处理组合键 Ctrl+F
        if event.key() == Qt.Key_F and event.modifiers() & Qt.ControlModifier:
            self.display_replace()
            event.accept()
            return
        # 处理组合键 Ctrl+G
        if event.key() == Qt.Key_G and event.modifiers() & Qt.ControlModifier:
            line_number, ok = QInputDialog.getInt(self, "跳转到行", "请输入行号:")
            if ok and line_number > 0:
                self.jump_to_line(line_number - 1)  # 行号从1开始计数，但QTextCursor从0开始
            event.accept()
            return
        # 默认情况下，调用父类的事件处理函数
        super().keyPressEvent(event)

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
        try:
            with codecs.open(file_name, "w", encoding=self.current_file_encoding) as outfile:
                text = self.text_edit.toPlainText()
                outfile.write(text)
                # 更新最后修改时间
            self.text_edit.document().setModified(False)
            self.last_modified_time = QFileInfo(file_name).lastModified().toMSecsSinceEpoch()

            return True
        except IOError as e:
            QMessageBox.warning(self, self.app_name, f"文件 {file_name} 保存失败:\n{e}")
        except UnicodeEncodeError as e:
            # 如果编码错误，尝试使用UTF-8重新保存
            try:
                with codecs.open(file_name, "w", encoding="utf-8") as outfile:
                    text = self.text_edit.toPlainText()
                    outfile.write(text)
                self.text_edit.document().setModified(False)
                # 更新最后修改时间
                self.last_modified_time = QFileInfo(file_name).lastModified().toMSecsSinceEpoch()
                return True
            except Exception as e:
                QMessageBox.warning(self, self.app_name, f"编码错误，文件 {file_name} 保存失败:\n{e}")
        except Exception as e:
            QMessageBox.warning(self, self.app_name, f"文件 {file_name} 保存时发生未知错误:\n{e}")
        return False

    def read_file(self, filename):
        filename = os.path.normpath(filename)
        # 关闭语法高亮
        if self.highlighter:
            self.highlighter.deleteLater()
            self.highlighter = None
        if not filename:
            return
        try:
            lines,position = self.read_100_lines(filename,100)
            encoding_info = chardet.detect(b"".join(lines))
            if encoding_info is None:
                encoding = "utf-8"
            else:
                encoding = encoding_info.get("encoding", "utf-8")
                if not encoding:
                    encoding = "utf-8"
                if encoding.upper() in ["GB2312", "GBK"]:
                    encoding = "GB18030"

            initial_content = b"".join(lines).decode(encoding,"ignore")
            self.text_edit.setPlainText(initial_content.rstrip())
            self.setWindowTitle(f"{self.app_name} - {encoding.upper()} - {filename}")
            # 记录当前文件名,编码,以及当前目录
            self.current_file_name = filename
            self.current_file_encoding = encoding
            self.work_dir = os.path.dirname(os.path.abspath(filename))
            # 将打开记录添加到最近打开
            self.add_recent_file(filename)
            self.last_modified_time = QFileInfo(filename).lastModified().toMSecsSinceEpoch()

            # 使用文件后缀判断使用何种语言高亮
            self.current_file_extension = os.path.splitext(filename)[1]
            if self.syntax_highlight_enabled:
                self.reload_highlighter(self.theme, self.current_file_extension)
            self.start_file_loader(filename, encoding,position)

        except FileNotFoundError:
            QMessageBox.warning(self, "错误", "文件未找到，请检查路径是否正确！")
        except PermissionError:
            QMessageBox.warning(self, "错误", "没有足够的权限打开文件！")
        except UnicodeDecodeError:
            QMessageBox.warning(self, "错误", "文件编码无法识别，请尝试手动选择编码！")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"打开文件时发生错误（很可能不支持该文件类型）:{e}")

    def start_file_loader(self, filename, encoding,position):
        # 启动文件加载线程
        self.file_loader = FileLoader(filename, encoding,position)
        self.file_loader.contentLoaded.connect(self.append_content)
        self.file_loader.start()

    def append_content(self, chunk):
        self.text_edit.appendPlainText(chunk)
        self.text_edit.document().setModified(False)
        self.text_edit.update_total_lines()

    def read_100_lines(self, filename, num_lines):
        lines = []
        position = 0
        with open(filename, 'rb') as f:
            for _ in range(num_lines):
                line = f.readline()
                if not line:
                    break
                lines.append(line)
            position = f.tell()  # 在循环外获取位置
        return lines,position

    def add_recent_file(self, file_path):
        # 添加最近打开的文件路径到列表中
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        # 如果超过十个文件，则移除列表中最早打开的文件
        if len(self.recent_files) > 20:
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
            if os.path.exists(file_path):
                action = QAction(file_path, self)
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

    def apply_wrap_status(self):
        if self.wrap_line_on:
            self.text_edit.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        else:
            self.text_edit.setLineWrapMode(QPlainTextEdit.NoWrap)

        if self.statusbar_shown:
            self.status_bar.show()
        else:
            self.status_bar.hide()

    def apply_theme(self, theme):
        # 只勾选用户选择的主题
        for action in self.theme_actions:
            action.setChecked(action.data() == theme)

        if theme in self._styles_cache:
            self.setStyleSheet(self._styles_cache[theme])
        else:
            qss_file = QFile(os.path.join(resource_path,f"{theme}_style.qss"))
            if qss_file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(qss_file)
                self._styles_cache[theme] = stream.readAll()
                qss_file.close()
                self.setStyleSheet(self._styles_cache[theme])
            else:
                print(f"Failed to open QSS file for theme {theme}.")
        self.theme = theme
        self.theme_changed.emit(theme)
        self.save_settings()

    def load_settings(self):
        try:
            # 读取现有的设置
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {}  # 如果文件不存在，创建一个空字典

        # 更新字体设置
        font_data = settings.get("font", {})
        self.font = QFont(font_data.get("font_family", "Microsoft YaHei UI"), font_data.get("point_size", 12))
        self.font.setBold(font_data.get("bold", False))
        self.font.setItalic(font_data.get("italic", False))
        self.font.setUnderline(font_data.get("underline", False))
        self.font.setStrikeOut(font_data.get("strikeOut", False))

        # 更新其他设置
        self.theme = settings.get("theme", "intellijlight")
        self.syntax_highlight_enabled = settings.get("syntax_on", False)
        self.custom_command = settings.get("custom_command", "python $1")
        self.custom_comment_char = settings.get("custom_comment_char","#")
        self.wrap_line_on = settings.get("wrap_line_on", True)
        self.statusbar_shown = settings.get("statusbar_shown", True)
        self.show_line_numbers = settings.get("show_line_numbers", True)

        # 读取并应用窗口大小设置
        startup_size = settings.get("startup_size", {})
        width = startup_size.get("width", 800)
        height = startup_size.get("height", 600)
        is_maximized = startup_size.get("start_maximized", False)
        if is_maximized:
            self.showMaximized()
        else:
            self.resize(int(width), int(height))

    def save_settings(self):
        try:
            # 读取现有的设置
            with open(self.settings_file, "r") as f:
                existing_settings = json.load(f)
        except FileNotFoundError:
            existing_settings = {}  # 如果文件不存在，创建一个空字典

        # 更新现有设置
        existing_settings.update({
            "font":{"font_family": self.font.family(),"point_size": self.font.pointSize(),"bold": self.font.bold(),"italic": self.font.italic(),"underline": self.font.underline(),"strikeOut": self.font.strikeOut()},
            "theme": self.theme,
            "wrap_line_on": self.wrap_line_on,
            "statusbar_shown": self.statusbar_shown,
            "startup_size": {"width": self.width(), "height": self.height(), "start_maximized": self.isMaximized()},
            "show_line_numbers": self.show_line_numbers,
            "syntax_on": self.syntax_highlight_enabled,
            "custom_command": self.custom_command,
            "custom_comment_char":self.custom_comment_char
        })

        # 保存更新后的设置到文件
        with open(self.settings_file, "w") as f:
            json.dump(existing_settings, f, indent=4)

    def jump_to_line(self, line_number):
        # 获取文档对象
        doc = self.text_edit.document()
        # 查找指定行号对应的文本块
        block = doc.findBlockByLineNumber(line_number)
        if block.isValid():
            # 创建 QTextCursor 对象
            cursor = QTextCursor(block)
            # 移动到块的开始位置
            cursor.movePosition(QTextCursor.StartOfBlock)
            # 将光标设置到文本编辑器中
            self.text_edit.setTextCursor(cursor)
            # 确保光标所在的行是可见的
            self.text_edit.ensureCursorVisible()

    def is_cursor_at_empty_line_start(self):
        cursor = self.text_edit.textCursor()
        # 获取光标所在位置的文本块
        block = cursor.block()
        # 检查光标是否位于行首且该行是否为空行（去除前后空白字符后）
        return cursor.atBlockStart() and not block.text().strip()

    @Slot()
    def show_startup_size_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("设置启动窗口尺寸")

        width_label = QLabel("宽度:", dialog)
        width_edit = QLineEdit(dialog)
        width_edit.setValidator(QIntValidator())
        height_label = QLabel("高度:", dialog)
        height_edit = QLineEdit(dialog)
        height_edit.setValidator(QIntValidator())

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
        layout.addWidget(button_ok,alignment=Qt.AlignCenter)

        dialog.setLayout(layout)
        # 读取先前保存的窗口尺寸信息并显示在对话框中
        startup_size = self.read_startup_size()
        width_edit.setText(str(startup_size["width"]))
        height_edit.setText(str(startup_size["height"]))
        maximize_checkbox.setChecked(startup_size["start_maximized"])
        dialog.exec()

    def on_maximize_checkbox_changed(self, state, width_edit, height_edit):
        # 根据复选框的状态启用或禁用宽度和高度编辑框
        width_edit.setEnabled(not state)
        height_edit.setEnabled(not state)

    # 在save_startup_size方法中
    def save_startup_size(self, dialog, width, height, is_maximized):
        try:
            width = int(width)
            height = int(height)
        except ValueError:
            QMessageBox.critical(self, "错误", "请输入有效的数字", QMessageBox.Ok)
            return

        # 如果用户选择了最大化，则设置窗口尺寸为屏幕尺寸，并记录最大化状态
        if is_maximized:
            self.showMaximized()
        else:
            self.resize(width, height)

        # 保存启动窗口尺寸及最大化状态到 settings.json
        with open(self.settings_file, 'r+') as f:
            settings = json.load(f)
            settings["startup_size"] = {"width": width, "height": height, "start_maximized": is_maximized}
            f.seek(0)  # 将文件指针移到文件开头
            json.dump(settings, f, indent=4)
            f.truncate()  # 截断文件，删除多余的内容
        dialog.close()

    def read_startup_size(self):
        try:
            # 从 settings.json 文件读取启动窗口尺寸及最大化状态
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                startup_size = settings.get("startup_size", {})
                width = startup_size.get("width", 800)
                height = startup_size.get("height", 600)
                is_maximized = startup_size.get("start_maximized", False)
                if is_maximized:
                    self.showMaximized()
                else:
                    self.resize(int(width), int(height))

                return {"width": int(width), "height": int(height), "start_maximized": is_maximized}
        except (FileNotFoundError, ValueError):
            # json 文件不存在，或者值为空，默认使用 800x600 的尺寸
            self.resize(800, 600)

    @Slot()
    def help_info(self):
        help_txt = r"""<ol>
       <li><span style='font-size:14px'>匹配中文：[\u4e00-\u9fff]+ ,查找框三个选项对应Perl正则中的/i,/m,/s开关)。</span></li>
       <li><span style='font-size:14px'>鼠标选中想要的文字，按CTRL-F就可以搜索了.按Ctrl-G 可以跳转行号类似PyCharmIDE中的查找</span></li>
       <li><span style='font-size:14px'>取色器，点击PICK SCREEN COLOR 拾取颜色，那个英文暂时没法汉化</span></li>
       <li><span style='font-size:14px'>默认高亮的语言有:Java,Javascript,Kotlin,Perl,Python,Bat,Bash,Xml，C,C++,修改关键字颜色在程序目录下的resources/syntax_highlighter_file.json，修改文本区域颜色在主题对应的qss文件中修改。</span></li>
       <li><span style='font-size:14px'>自定义命令行，$1 表示当前文件名。</span></li>
       <li><span style='font-size:14px'>设置自动保存在settings.json中</span></li>
       <li><span style='font-size:14px'>清空剪贴板，需要打开resources目录下的clipboard_list.json,删除所有内容，然后在输入法的英文状态下输入“ [] ”（就是数组的符号）,保存为UTF-8编码就可以了.另外按CTRL-SHIFT-V也可以弹出剪贴板窗口</span></li>
    </ol>"""

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
        self.find_replace_dialog = FindReplaceDialog(self.text_edit, self)

    def edit_command(self):
        dialog = CommandDialog(self)
        dialog.command_line_edit.setText(self.custom_command)  # 设置输入框中的默认值
        if dialog.exec():
            self.custom_command = dialog.get_command()
            self.save_settings()  # 保存用户自定义命令到json文件中

    def run_script(self):
        try:
            # 如果self.work_dir不为空，切换到相应的目录
            if self.work_dir:
                os.chdir(self.work_dir)
            # 对于Windows系统
            custom_command = self.custom_command.replace("$1", self.current_file_name)
            cmd_command = f'start cmd /K {custom_command}'
            subprocess.Popen(cmd_command, shell=True)
        except Exception as e:
            QMessageBox.warning(self, "发生错误", str(e))

    @Slot()
    def open_terminal(self):
        try:
            # 如果self.work_dir不为空，切换到相应的目录
            if self.work_dir:
                os.chdir(self.work_dir)
            # 对于Windows系统
            cmd_command = f'start cmd /K cd /D "{self.work_dir}"'
            subprocess.Popen(cmd_command, shell=True)
        except Exception as e:
            QMessageBox.warning(self, "发生错误", str(e))

    @Slot()
    def use_code_save(self, encoding, *args):
        default_filename = self.current_file_name if self.current_file_name else self.text_edit.untitled_name
        filename, _ = QFileDialog.getSaveFileName(None, "保存文件", default_filename,
                                                  "所有文件类型(*.*);;文本文件 (*.txt)")
        # 如果用户取消保存操作，直接返回
        if not filename:
            return
        # 获取文件名输入框并选中文本
        filename_lineedit = QApplication.focusWidget()
        if isinstance(filename_lineedit, QLineEdit):
            filename_lineedit.selectAll()

        try:
            with open(filename, "w", encoding=encoding) as w:
                w.write(self.text_edit.toPlainText())
            # 更新最后修改时间
            self.last_modified_time = QFileInfo(filename).lastModified().toMSecsSinceEpoch()
            # 更新窗口标题以显示保存成功
            QMessageBox.information(self, "提示",
                                f"文件{filename}已经使用 {encoding.upper()} 编码另存至指定位置！")

            # 如果用户选择覆盖当前打开的文件，则更新窗口标题(编辑器内容没必要更新)
            if filename == self.current_file_name:
                self.current_file_name = filename
                self.current_file_encoding = encoding
                self.setWindowTitle(f"{self.app_name} - {encoding.upper()} - {filename}")

        except Exception as e:
            # 在这里处理异常，例如通过日志记录或更新窗口标题来显示错误信息
            print(f"保存文件时出错：{e}")

    @Slot()
    def re_open(self, coding, *args):
        # 指定编码加载文件
        try:
            with open(self.current_file_name, "r", encoding=coding,errors="ignore") as f:
                content = f.read()
            self.text_edit.setPlainText(content)
            self.current_file_encoding = coding
            self.last_modified_time = QFileInfo(self.current_file_name).lastModified().toMSecsSinceEpoch()
            self.setWindowTitle(self.app_name + " - " + coding.upper() + " - " + self.current_file_name)
        except FileNotFoundError:
            QMessageBox.warning(self, "错误", "还没打开文件！")

    @Slot()
    def open_dialog(self):
        if self.tip_to_save():
            filename, _ = QFileDialog.getOpenFileName(self, "打开", "",
                                                      "*.txt *.py *.xml *.html *.json *.qss *.c *.java *.sql *.pl *.kt *.sh *.cpp *.ini *.bat;;所有文件(*.*)")
            self.read_file(filename)

    # 根据当前是否打开文件来决定是直接保存，还是另存至其他位置（）
    @Slot()
    def save(self):
        encoding = self.current_file_encoding.upper()
        if self.text_edit.document().isModified():  # 检查文档是否被修改过
            if self.current_file_name:
                saved = self.save_file(self.current_file_name)
                if saved:
                    self.setWindowTitle(f"{self.app_name} - {encoding} - {self.current_file_name} - 保存成功")
            else:
                saved_file = self.save_as()
                if saved_file:
                    self.setWindowTitle(f"{self.app_name} - {encoding} - {self.current_file_name} - 保存成功")
        else:
            print("文档未修改，无需保存")

    @Slot()
    def save_as(self):
        default_filename = self.current_file_name if self.current_file_name else self.text_edit.untitled_name
        filename, _ = QFileDialog.getSaveFileName(None, "保存文件", default_filename,
                                                  "所有文件类型(*.*);;文本文件 (*.txt)")
        # 如果用户取消保存操作，直接返回 None
        if not filename:
            return None

        # 获取文件名输入框并选中文本
        filename_lineedit = QApplication.focusWidget()
        if isinstance(filename_lineedit, QLineEdit):
            filename_lineedit.selectAll()

        saved = self.save_file(filename)
        if saved:
            self.current_file_name = filename
            return True
        else:
            return False

    @Slot()
    def new_file(self):
        if self.tip_to_save():
            self.text_edit.clear()
            self.current_file_name=""
            self.work_dir = self.desktop_dir
            self.setWindowTitle(f"{self.app_name} - [{self.text_edit.untitled_name}]")

    @Slot()
    def modify_font(self):
        # 选择字体
        ok, font = QFontDialog.getFont()
        if not ok: return
        self.text_edit.setFont(font)
        self.font = font  # 更新字体
        self.save_settings()  # 保存字体设置到json

    @Slot()
    def wrap_line_toggle(self):
        self.wrap_line_on = self.wrap_action.isChecked()
        self.apply_wrap_status()
        self.save_settings()

    @Slot()
    def statusbar_toggle(self):
        self.statusbar_shown = self.statusbar_action.isChecked()
        self.apply_wrap_status()
        self.save_settings()

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

    def comment_selected_text(self, ):
        cursor = self.text_edit.textCursor()
        has_selection = cursor.hasSelection()

        if has_selection:
            selection_start = cursor.selectionStart()
            selection_end = cursor.selectionEnd()
            cursor.setPosition(selection_start)
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.setPosition(selection_end, QTextCursor.KeepAnchor)
            selected_text = cursor.selectedText()
            lines = selected_text.splitlines()

            comment_delta = 0
            # 修正后的逻辑，确保既能添加又能移除注释，并准确计算移除的空格
            has_added_count = 0  # 初始化添加#成功的计数器
            chars_replaced = 0
            # 使用传统for循环进行处理并计数
            for i, line in enumerate(lines):
                if line.startswith(self.custom_comment_char):
                    lines[i] = line[len(self.custom_comment_char):]
                    comment_delta = -len(self.custom_comment_char)
                    has_added_count -=1
                else:
                    lines[i] = self.custom_comment_char + line
                    comment_delta = len(self.custom_comment_char)
                    has_added_count += 1
            commented_text = "\n".join(lines)
            cursor.removeSelectedText()
            cursor.insertText(commented_text)

            # 更精确的计算新选区结束位置，考虑所有变化
            new_selection_end = selection_end + has_added_count * len(self.custom_comment_char)

            cursor.setPosition(selection_start + comment_delta)
            cursor.setPosition(new_selection_end, QTextCursor.KeepAnchor)
            self.text_edit.setTextCursor(cursor)
        else:
            # 若无选区，注释或取消注释当前行
            cursor.movePosition(QTextCursor.StartOfLine)
            if cursor.block().text().startswith(self.custom_comment_char):
                cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, len(self.custom_comment_char))
                cursor.removeSelectedText()
            else:
                cursor.insertText(f"{self.custom_comment_char}")

            self.text_edit.setTextCursor(cursor)

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

    def delete_word_right(self):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.NextWord, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()

    def delete_word_left(self):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.PreviousWord, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()

    def move_word_right(self):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.NextWord)
        self.text_edit.setTextCursor(cursor)

    def move_word_left(self):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.PreviousWord)
        self.text_edit.setTextCursor(cursor)

    def to_uppercase(self):
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            cursor.insertText(cursor.selectedText().upper())
        else:
            QMessageBox.warning(self, "错误", "先选中文本才能转换！")
            pass

    def to_lowercase(self):
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            cursor.insertText(cursor.selectedText().lower())
        else:
            QMessageBox.warning(self, "错误", "先选中文本才能转换！")
            pass

    def capitalize_words(self):
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            text_to_capitalize = cursor.selectedText()
            capitalized_text = text_to_capitalize.title()
            cursor.insertText(capitalized_text)
        else:
            QMessageBox.warning(self, "错误", "请先选中文本以便转换每个单词的首字母为大写！")

    def toggle_case(self):
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            toggled_text = ''.join(c.lower() if c.isupper() else c.upper() for c in selected_text)
            cursor.insertText(toggled_text)
        else:
            QMessageBox.warning(self, "错误", "先选中文本才能转换！")
            pass


    @Slot()
    def select_all(self):
        self.text_edit.selectAll()

    @Slot()
    def pick_color(self):
        dialog = CustomColorDialog()
        dialog.show()  # 使用show()方法显示非模态对话框
        if dialog.exec():
            selected_color = dialog.currentColor()

#======================================================================================
def get_file_argument():
    if len(sys.argv) > 1:
        return os.path.abspath(sys.argv[1])
    else:
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    resource_path = os.path.join(sys._MEIPASS if hasattr(sys, '_MEIPASS') else current_directory, 'resources')

    translator = QTranslator()
    translator_path = os.path.join(resource_path, f"qt_zh_CN.qm")
    translator.load(translator_path)
    app.installTranslator(translator)

    icon_path = os.path.join(resource_path, "JQEdit.png")
    app.setWindowIcon(QIcon(icon_path))

    JQEdit = Notepad()
    filename = get_file_argument()
    if filename:
        JQEdit.read_file(filename)
    JQEdit.show()
    sys.exit(app.exec())
