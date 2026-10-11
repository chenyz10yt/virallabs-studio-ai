@echo off
chcp 65001 >nul
title StreamHub 24/7 Studio - Servidor Local
cd /d "%~dp0"

set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"
set "PATH=%~dp0bin;C:\ffmpeg\bin;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;%PATH%"

echo ========================================================
echo   STREAMHUB 24/7 STUDIO - INICIANDO SERVIDOR LOCAL
echo ========================================================
echo.

REM 1. Sincronizar plantillas y carpetas
if not exist "templates" mkdir templates
copy /y "index.html" "templates\index.html" >nul
if exist "control.html" copy /y "control.html" "templates\control.html" >nul
if not exist "uploads" mkdir uploads

REM 2. Buscar ejecutable de Python
set "PYTHON_EXE="

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if defined PYTHON_EXE goto :found_python

where python >nul 2>nul
if %errorlevel% equ 0 set "PYTHON_EXE=python"
if defined PYTHON_EXE goto :found_python

where py >nul 2>nul
if %errorlevel% equ 0 set "PYTHON_EXE=py"
if defined PYTHON_EXE goto :found_python

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if defined PYTHON_EXE goto :found_python

if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if defined PYTHON_EXE goto :found_python

if exist "C:\Python311\python.exe" set "PYTHON_EXE=C:\Python311\python.exe"
if defined PYTHON_EXE goto :found_python

if exist "C:\Python312\python.exe" set "PYTHON_EXE=C:\Python312\python.exe"
if defined PYTHON_EXE goto :found_python

if exist "C:\Python310\python.exe" set "PYTHON_EXE=C:\Python310\python.exe"
if defined PYTHON_EXE goto :found_python

if exist "C:\Program Files\Python311\python.exe" set "PYTHON_EXE=C:\Program Files\Python311\python.exe"
if defined PYTHON_EXE goto :found_python

if exist "C:\Program Files\Python312\python.exe" set "PYTHON_EXE=C:\Program Files\Python312\python.exe"
if defined PYTHON_EXE goto :found_python

REM 3. Si no se encontro Python, iniciar servidor de contingencia
echo [AVISO] Python no esta en las rutas estandar.
echo Iniciando servidor de contingencia en PowerShell...
powershell -ExecutionPolicy Bypass -File "%~dp0server_local.ps1"
pause
exit /b 0

:found_python
echo [OK] Python detectado: %PYTHON_EXE%
echo Verificando dependencias [Flask]...
"%PYTHON_EXE%" -m pip install -q flask flask-sock pytchat

echo.
echo ========================================================
echo   Servidor Backend Activo en http://localhost:5000/
echo   Presiona Ctrl+C para detener el servidor
echo ========================================================
echo.

REM Abrir navegador automaticamente tras 2 segundos
start /b cmd /c "ping -n 3 127.0.0.1 >nul && start http://localhost:5000"

"%PYTHON_EXE%" app.py
pause
exit /b 0
