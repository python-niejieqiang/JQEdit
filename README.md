 **JQEdit** 
使用Pyside6编写。作为Windows记事本的替代品，具有基本的读取、写入和保存功能，支持正则表达式查找替换、切换主题，自动保存用户设置，选区替换、行号显示，行号跳转，选区缩进（功能不是很完善）以及语法关键字高亮等功能。此外，JQEdit还具有处理各国编码的能力（我没用过，准确性有待验证），并提供剪贴板功能以及调用命令行的功能。

JQEdit的源代码遵循GPLv3协议发布。 GPLv3协议内容自行搜索，我就不粘贴了。
JQEdit.py为主程序
replace_window_ui.py为查找替换框代码

其他py文件为辅助工具，与记事本程序无关联
.iss为innosetup打包脚本，build_exe.bat则是一键打包

 **JQEdit** 
is developed using Pyside6. As a replacement for Windows Notepad, it features basic functionalities such as reading, writing, and saving files. It also supports regular expression find and replace, theme switching, automatic saving of user settings, selection replace, line numbering, line jumping, selection indentation (although this feature is not very robust), as well as syntax keyword highlighting. Additionally, JQEdit claims to have the ability to handle various encoding formats (accuracy to be verified as I have not personally tested it), and provides clipboard functionality along with the ability to invoke the command line.

The source code of JQEdit is released under the GPLv3 license. You can search for the content of the GPLv3 license on your own; I won't paste it here.

JQEdit.py is the main program file.
replace_window_ui.py is the code for the find and replace dialog box.

Other .py files are auxiliary tools unrelated to the notepad program.
.iss is the Inno Setup packaging script, and build_exe.bat is a one-click packaging tool.