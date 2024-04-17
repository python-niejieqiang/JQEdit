@echo off
python -m venv venv
call venv\Scripts\activate
pyinstaller --clean JQEdit.spec

:: 编译.iss脚本
Compil32 /cc inno_setup.iss
