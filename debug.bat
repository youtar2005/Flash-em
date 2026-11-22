@echo off
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 goto use_launcher
goto use_python

:use_launcher
py -3 localhost_server.py
goto finished

:use_python
pythonw localhost_server.py

:finished
exit
