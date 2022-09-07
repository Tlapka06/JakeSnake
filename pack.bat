@echo off
pyinstaller -y snake.py
copy README.md build\snake\