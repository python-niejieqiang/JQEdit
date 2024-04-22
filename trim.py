import time
import os

# 统计程序运行时间
start_time = time.time()
# 使用相对路径指定目标目录
src = r"dist\JQEdit"  # 目标目录相对于当前工作目录

files_to_keep = [
    r"dist\JQEdit\base_library.zip",
    r"dist\JQEdit\JQEdit.exe",
    r"dist\JQEdit\python3.dll",
    r"dist\JQEdit\python38.dll",
    r"dist\JQEdit\PySide6\pyside6.abi3.dll",
    r"dist\JQEdit\PySide6\Qt6Core.dll",
    r"dist\JQEdit\PySide6\Qt6Gui.dll",
    r"dist\JQEdit\PySide6\Qt6Widgets.dll",
    r"dist\JQEdit\PySide6\QtCore.pyd",
    r"dist\JQEdit\PySide6\QtGui.pyd",
    r"dist\JQEdit\PySide6\QtWidgets.pyd",
    r"dist\JQEdit\PySide6\plugins\platforms\qwindows.dll",
    r"dist\JQEdit\PySide6\plugins\styles\qwindowsvistastyle.dll",
    r"dist\JQEdit\resources\JetBrainsMono-Regular-2.ttf",
    r"dist\JQEdit\resources\JQEdit.ico",
    r"dist\JQEdit\resources\JQEdit.png",
    r"dist\JQEdit\resources\qt_zh_CN.qm",
    r"dist\JQEdit\resources\recent_files.json",
    r"dist\JQEdit\resources\settings.json",
    r"dist\JQEdit\resources\widgets.qm",
    r"dist\JQEdit\shiboken6\Shiboken.pyd",
    r"dist\JQEdit\shiboken6\shiboken6.abi3.dll"
]
def find_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)

# 使用示例
for file_path in find_files(src):
    if file_path not in files_to_keep:
        # os.remove(file_path)
        print(file_path)
