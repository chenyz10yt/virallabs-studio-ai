@echo off
chcp 65001 >nul
title Studio de Transmisión 24/7 - StreamHub
color 0A

cd /d "%~dp0..\panel_stream"
set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"

if not exist "%PYTHON_EXE%" (
    for %%P in (python.exe py.exe) do (
        where %%P >nul 2>nul
        if not defined PYTHON_EXE if %errorlevel% equ 0 set "PYTHON_EXE=%%P"
    )
)

powershell -NoProfile -Command "try { $client = New-Object System.Net.Sockets.TcpClient; $client.Connect('127.0.0.1', 5000); $client.Close(); exit 0 } catch { exit 1 }"
if %ERRORLEVEL% NEQ 0 (
    start /min "StreamHub 24/7 Engine" "%PYTHON_EXE%" app.py
    timeout /t 3 /nobreak >nul
)

start "" "http://localhost:5000/"
exit
