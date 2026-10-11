@echo off
title StreamHub - Empaquetar para VPS
cd /d "%~dp0"
echo ========================================================
echo   CREANDO ARCHIVO ZIP PARA SUBIR AL VPS
echo ========================================================
echo.
powershell -Command "Compress-Archive -Path app.py, requirements.txt, install.sh, start.sh, config.json, stream_key.txt, templates, docker-compose.yml, Dockerfile, GUIA_DESPLIEGUE_VPS_Y_MULTICAMARA.md -DestinationPath panel_stream_vps.zip -Force"
echo.
echo [OK] Archivo 'panel_stream_vps.zip' listo para subir a tu servidor.
timeout /t 3 >nul
exit /b 0
