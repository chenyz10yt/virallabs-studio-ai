@echo off
chcp 65001 >nul
title StreamHub 24/7 Studio - Windows Launcher
cd /d "%~dp0"

set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"
set "PATH=%~dp0bin;C:\ffmpeg\bin;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;%PATH%"

echo =========================================================
echo   STREAMHUB 24/7 STUDIO - INICIANDO PANEL (WINDOWS)
echo =========================================================
echo.

if not exist "templates" mkdir templates
copy /y "index.html" "templates\index.html" >nul
if not exist "uploads" mkdir uploads

set "PYTHON_EXE="
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not defined PYTHON_EXE (
    where python >nul 2>nul
    if %errorlevel% equ 0 set "PYTHON_EXE=python"
)
if not defined PYTHON_EXE (
    where py >nul 2>nul
    if %errorlevel% equ 0 set "PYTHON_EXE=py"
)

if not defined PYTHON_EXE (
    echo [ERROR] No se encontro Python instalado.
    echo Ejecutando servidor de contingencia...
    powershell -ExecutionPolicy Bypass -File "%~dp0server_local.ps1"
    pause
    exit /b 0
)

echo [OK] Python: %PYTHON_EXE%
"%PYTHON_EXE%" -m pip install -q flask

start /b cmd /c "ping -n 3 127.0.0.1 >nul && start http://localhost:5000"

"%PYTHON_EXE%" app.py
pause
exit /b 0
