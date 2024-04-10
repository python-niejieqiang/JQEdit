from functools import partial

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QPlainTextEdit,
                               QMenu, QMenuBar, QStatusBar)

class UI_main_window(object):
    def setupUI(self):
        self.app_name = "JQEdit"
        self.setWindowTitle(self.app_name)
        # 设置窗口的最小尺寸
        self.resize(800, 600)

        # 初始化界面，依次添加菜单栏，text_edit，status_bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.text_edit = QPlainTextEdit()
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

        # 文件菜单
        # 添加最近打开的文件子菜单
        self.recent_files_menu = self.file_menu.addMenu("最近打开")
        # 添加清空记录的菜单项
        self.clear_recent_files_action = QAction("清空记录", self)
        self.recent_files_menu.addAction(self.clear_recent_files_action)

        self.new_file_action = QAction("新建(&N)", self)
        self.new_file_action.setShortcut("Ctrl+N")
        self.file_menu.addAction(self.new_file_action)

        self.open_action = QAction("打开(&O)", self)
        self.open_action.setShortcut("Ctrl+O")
        self.file_menu.addAction(self.open_action)

        self.save_action = QAction("保存(&S)", self)
        self.save_action.setShortcut("Ctrl+S")
        self.file_menu.addAction(self.save_action)

        self.save_as_action = QAction("另存(&A)", self)
        self.save_as_action.setShortcut("Alt+S")
        self.file_menu.addAction(self.save_as_action)

        self.exit_action = QAction("退出(&X)", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.file_menu.addAction(self.exit_action)

        # 编辑 菜单
        self.undo_action = QAction("撤销(&U)", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.edit_menu.addAction(self.undo_action)

        self.redo_action = QAction("重做(&Y)", self)
        self.redo_action.setShortcut("Ctrl+Y")
        self.edit_menu.addAction(self.redo_action)
        # 添加菜单分割线
        self.edit_menu.addSeparator()

        self.emptyline_action = QAction(self.tr("清空行(&M)"), self)
        self.emptyline_action.setShortcut("Ctrl+K")
        self.edit_menu.addAction(self.emptyline_action)

        self.copyline_action = QAction(self.tr("复制行(&H)"), self)
        self.copyline_action.setShortcut("Ctrl+R")
        self.edit_menu.addAction(self.copyline_action)

        self.del_line_action = QAction(self.tr("删除行(&D)"), self)
        self.del_line_action.setShortcut("Alt+D")
        self.edit_menu.addAction(self.del_line_action)

        self.comment_action = QAction(self.tr("切换注释(&S)"), self)
        self.comment_action.setShortcut("Ctrl+/")
        self.edit_menu.addAction(self.comment_action)

        self.edit_menu.addSeparator()

        self.cut_action = QAction("剪切(&T)", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.edit_menu.addAction(self.cut_action)

        self.copy_action = QAction("复制(&C)", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.edit_menu.addAction(self.copy_action)

        self.paste_action = QAction("粘贴(&P)", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.edit_menu.addAction(self.paste_action)

        self.delete_action = QAction("删除(&D)", self)
        self.delete_action.setShortcut("Backspace")
        self.edit_menu.addAction(self.delete_action)

        self.selectall_action = QAction("全选(&A)", self)
        self.selectall_action.setShortcut("Ctrl+A")
        self.edit_menu.addAction(self.selectall_action)

        self.edit_menu.addSeparator()

        self.date_action = QAction("日期(&Y)", self)
        self.date_action.setShortcut("F6")
        self.edit_menu.addAction(self.date_action)

        # 主题菜单
        # 将主题样式存入数组全部设为未选中，当用户选中哪一个，就把哪一个设为True
        # 也就是点击哪个主题，哪个主题样式前面就显示打勾
        self.theme_actions = []
        self.def_theme_action = QAction("windows默认", self, checkable=True)
        self.def_theme_action.triggered.connect(self.set_default_style)
        self.theme_menu.addAction(self.def_theme_action)
        self.theme_actions.append(self.def_theme_action)

        self.dark_theme_action = QAction("Dark", self, checkable=True)
        self.dark_theme_action.triggered.connect(self.set_dark_style)
        self.theme_menu.addAction(self.dark_theme_action)
        self.theme_actions.append(self.dark_theme_action)

        self.light_theme_action = QAction("light", self, checkable=True)
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

        # 设置启动窗口尺寸
        self.set_startup_size_action = QAction("设置启动窗口尺寸", self)
        self.set_startup_size_action.triggered.connect(self.show_startup_size_dialog)
        self.theme_menu.addAction(self.set_startup_size_action)

        # 主窗口部分
        self.replace_action = QAction("查找/替换(&Z)", self)
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
            self.to_sava_as.triggered.connect(partial(self.use_code_save, cod=code_name))
            self.to_open = QAction("以该编码重新加载", self)
            self.to_open.triggered.connect(partial(self.re_open, coding=code_name))
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