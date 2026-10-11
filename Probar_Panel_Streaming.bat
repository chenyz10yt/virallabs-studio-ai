@echo off
title StreamHub 24/7 Studio - Entorno de Pruebas
echo ========================================================
echo   STREAMHUB 24/7 STUDIO - ENTORNO DE PRUEBAS LOCAL
echo ========================================================
echo Abriendo el panel interactivo en tu navegador...
start "" "%~dp0index.html"
echo.
echo Listo. Ya puedes probar la subida de videos, la emision simulada,
echo el monitor de retorno y los controles en tu navegador.
echo ========================================================
timeout /t 3 >nul
exit
