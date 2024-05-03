# altgraph
# chardet                  
# pefile                   
# pip                      
# pyinstaller              
# pyinstaller-hooks-contrib
# pyperclip                
# PySide6                  
# PySide6_Addons           
# PySide6_Essentials       
# pywin32-ctypes           
# setuptools               
# shiboken6
    
    
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