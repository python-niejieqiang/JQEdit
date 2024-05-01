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

    profiler = cProfile.Profile()
    profiler.enable()
    # 如果有参数就传给记事本打开（这样打包成exe双击txt就能被记事本打开），否则创建空窗口
    if Notepad._instance is None:
        JQEdit = Notepad()
    else:
        JQEdit = Notepad._instance

        # Get filename from command line argument and open the file
    filename = get_file_argument()
    if filename:
        JQEdit.read_file_in_thread(filename)
    JQEdit.show()

    profiler.disable()
    profiler.print_stats(sort='cumulative')
    sys.exit(app.exec())