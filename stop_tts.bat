@echo off
title Stop Arcade TTS Server
echo ============================================================
echo               STOPPING ARCADE TTS SERVER
echo ============================================================
echo.

:: Find and kill Python processes running tts_server.py
for /f "tokens=2" %%a in ('wmic process where "commandline like '%%tts_server.py%%'" get processid /format:list ^| find "="') do (
    echo Killing process ID: %%a
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo Server stopped.
timeout /t 3
