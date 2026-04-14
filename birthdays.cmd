@echo off
cd /d "%~dp0"
title Birthday Reminder
call .venv\Scripts\activate.bat
uv run main.py