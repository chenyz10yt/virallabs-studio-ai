@echo off
title Viral Labs - Fanpage Oficial
echo ===================================================
echo   VIRAL LABS - FANPAGE OFICIAL DE LA COMUNIDAD
echo ===================================================

:: Comprobar si el servidor ya esta activo en el puerto 8080
powershell -NoProfile -Command "try { $client = New-Object System.Net.Sockets.TcpClient; $client.Connect('127.0.0.1', 8080); $client.Close(); exit 0 } catch { exit 1 }"
if %ERRORLEVEL% NEQ 0 (
    echo Iniciando servidor local en segundo plano...
    start /min powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File "%~dp0server.ps1"
    timeout /t 2 /nobreak >nul
)

echo Abriendo Fanpage publica conectada con el Studio...
start "" "http://localhost:8080/fanpage.html"
exit
