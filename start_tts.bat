@echo off
title Arcade TTS Server
cd /d %~dp0
call venv\Scripts\activate
echo ============================================================
echo                    ARCADE TTS SERVER
echo ============================================================
echo.
echo Starting server...
echo Press Ctrl+C to stop
echo.
python tts_server.py
pause
