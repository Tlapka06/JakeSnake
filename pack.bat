@echo off
pyinstaller -y jakesnake.py
copy README.md build\jakesnake\