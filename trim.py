import time
import os

# 统计程序运行时间
start_time = time.time()
# 使用相对路径指定目标目录
src = r"dist\JQEdit"  # 目标目录相对于当前工作目录

files_to_keep = [
    r"dist\JQEdit\_internal\base_library.zip",
    r"dist\JQEdit\_internal\ujson.cp312-win_amd64.pyd",
    r"dist\JQEdit\_internal\python3.dll",
    r"dist\JQEdit\_internal\python312.dll",
    r"dist\JQEdit\_internal\PySide6\pyside6.abi3.dll",
    r"dist\JQEdit\_internal\PySide6\Qt6Core.dll",
    r"dist\JQEdit\_internal\PySide6\Qt6Gui.dll",
    r"dist\JQEdit\_internal\PySide6\Qt6Widgets.dll",
    r"dist\JQEdit\_internal\PySide6\QtCore.pyd",
    r"dist\JQEdit\_internal\PySide6\QtGui.pyd",
    r"dist\JQEdit\_internal\PySide6\QtWidgets.pyd",
    r"dist\JQEdit\_internal\PySide6\plugins\platforms\qwindows.dll",
    r"dist\JQEdit\_internal\PySide6\plugins\styles\qwindowsvistastyle.dll",
    r"dist\JQEdit\_internal\resources\JetBrainsMono-Regular-2.ttf",
    r"dist\JQEdit\_internal\resources\JQEdit.ico",
    r"dist\JQEdit\_internal\resources\clipboard_list.json",
    r"dist\JQEdit\_internal\resources\dacula_darker_style.qss",
    r"dist\JQEdit\_internal\resources\dark_style.qss",
    r"dist\JQEdit\_internal\resources\gerrylight_style.qss",
    r"dist\JQEdit\_internal\resources\grovbox_soft_style.qss",
    r"dist\JQEdit\_internal\resources\intellijlight_style.qss",
    r"dist\JQEdit\_internal\resources\nature_green_style.qss",
    r"dist\JQEdit\_internal\resources\syntax_highlighter_file.json",
    r"dist\JQEdit\_internal\resources\xcode_style.qss",
    r"dist\JQEdit\_internal\resources\JQEdit.png",
    r"dist\JQEdit\_internal\resources\qt_zh_CN.qm",
    r"dist\JQEdit\_internal\resources\recent_files.json",
    r"dist\JQEdit\_internal\resources\settings.json",
    r"dist\JQEdit\_internal\resources\widgets.qm",
    r"dist\JQEdit\_internal\shiboken6\Shiboken.pyd",
    r"dist\JQEdit\_internal\shiboken6\shiboken6.abi3.dll",
    r"dist\JQEdit\JQEdit.exe",
    r"dist\JQEdit\_internal\_ctypes.pyd",
    r"dist\JQEdit\_internal\libffi-8.dll"
]
def find_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)

# 使用示例
for file_path in find_files(src):
    if file_path not in files_to_keep:
        os.remove(file_path)
        #print(file_path)
