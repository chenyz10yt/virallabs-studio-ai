@echo off
title Viral Labs - Servidor Local HTTP
echo =========================================================
echo   VIRAL LABS - SERVIDOR HTTP NATIVO ONLINE
echo =========================================================
echo Iniciando servidor en http://localhost:8080/ ...
start "" "http://localhost:8080/"
powershell -ExecutionPolicy Bypass -File "%~dp0server.ps1"
pause
