@echo off
rem Builds "RIPPS2 Media Studio.exe" in dist\ (pip install pyinstaller first)
cd /d "%~dp0"
python -m PyInstaller --noconfirm --onefile --windowed --name "RIPPS2 Media Studio" --add-data "fonts;fonts" --exclude-module scipy --exclude-module tkinter --exclude-module matplotlib studio.py
