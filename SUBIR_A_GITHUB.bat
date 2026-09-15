@echo off
title Viral Labs - Conector Automatico con GitHub (@chenyz10yt)
echo =========================================================
echo   VIRAL LABS STUDIO AI - SUBIDA AUTOMATICA A GITHUB
echo   Usuario destino: https://github.com/chenyz10yt
echo =========================================================
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\subir_github.ps1"
pause
