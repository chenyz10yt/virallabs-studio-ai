@echo off
title StreamHub - Detener Servidor
cd /d "%~dp0"
echo ========================================================
echo   DETENIENDO SERVIDOR STREAMHUB LOCAL
echo ========================================================
echo.
REM Detener procesos asociados al servidor
taskkill /F /IM ffmpeg.exe >nul 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq StreamHub*" >nul 2>nul
powershell -Command "Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*app.py*' } | Stop-Process -Force" >nul 2>nul
echo [OK] Servidor y transmision detenidos correctamente.
timeout /t 3 >nul
exit /b 0
