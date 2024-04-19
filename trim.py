import time
import os
from concurrent.futures import ThreadPoolExecutor

# 统计程序运行时间
start_time = time.time()


def search_files(directory, files_to_keep):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path not in files_to_keep and os.path.isfile(file_path):
                os.remove(file_path)
                # print("即将被删除：", file_path)
            else:
                pass


def search_in_thread(directory, files_to_keep, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for subdir in os.listdir(directory):
            subdir_path = os.path.join(directory, subdir)
            if os.path.isdir(subdir_path):
                future = executor.submit(search_files, subdir_path, files_to_keep)
                futures.append(future)

        # 等待所有任务完成
        for future in futures:
            future.result()


# 使用相对路径指定目标目录
src = "dist\\JQEdit"  # 目标目录相对于当前工作目录
max_workers = 5  # 设置最大工作线程数

# 存储需要保留的文件路径
files_to_keep = [
    "dist\\JQEdit\\_internal\\base_library.zip",
    "dist\\JQEdit\\_internal\\python3.dll",
    "dist\\JQEdit\\_internal\\python311.dll",
    "dist\\JQEdit\\_internal\\PySide6\\pyside6.abi3.dll",
    "dist\\JQEdit\\_internal\\PySide6\\Qt6Core.dll",
    "dist\\JQEdit\\_internal\\PySide6\\Qt6Gui.dll",
    "dist\\JQEdit\\_internal\\PySide6\\Qt6Widgets.dll",
    "dist\\JQEdit\\_internal\\PySide6\\QtCore.pyd",
    "dist\\JQEdit\\_internal\\PySide6\\QtGui.pyd",
    "dist\\JQEdit\\_internal\\PySide6\\QtWidgets.pyd",
    "dist\\JQEdit\\_internal\\PySide6\\plugins\\platforms\\qwindows.dll",
    "dist\\JQEdit\\_internal\\PySide6\\plugins\\styles\\qmodernwindowsstyle.dll",
    "dist\\JQEdit\\_internal\\resources\\JetBrainsMono-Regular-2.ttf",
    "dist\\JQEdit\\_internal\\resources\\JQEdit.ico",
    "dist\\JQEdit\\_internal\\resources\\JQEdit.png",
    "dist\\JQEdit\\_internal\\resources\\qt_zh_CN.qm",
    "dist\\JQEdit\\_internal\\resources\\recent_files.json",
    "dist\\JQEdit\\_internal\\resources\\settings.json",
    "dist\\JQEdit\\_internal\\resources\\widgets.qm",
    "dist\\JQEdit\\_internal\\resources\\window_size.json",
    "dist\\JQEdit\\_internal\\shiboken6\\Shiboken.pyd",
    "dist\\JQEdit\\_internal\\shiboken6\\shiboken6.abi3.dll",
    "dist\\JQEdit\\_internal\\PySide6\\plugins\\styles\\qwindowsvistastyle.dll"
    # 添加其他文件路径...
]

search_in_thread(src, files_to_keep, max_workers)
end_time = time.time()

print("程序运行时间:", end_time - start_time)
