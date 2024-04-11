@echo off
python -m venv venv
call venv\Scripts\activate
pyinstaller -D -w --icon="resources\JQEdit.ico" --add-data="resources\*;resources" JQEdit.py