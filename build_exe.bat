@echo off
python -m venv venv
call venv\Scripts\activate
::pyinstaller -D -w --icon="resources\JQEdit.ico" --add-data="resources\*;resources" JQEdit.py
pyinstaller --clean JQEdit.spec
Compil32 /cc inno_setup.iss