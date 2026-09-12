# Viral Labs Studio Apex & OmniPublish Pro v1.0.0 (Build 103)

> **Suite Definitiva de CreaciÃ³n, AnimaciÃ³n, EdiciÃ³n, Billetera, Auto-ActualizaciÃ³n e InstalaciÃ³n In-App y PublicaciÃ³n Multiplataforma con Inteligencia Artificial.**
> DiseÃ±ada para Creadores de Contenido, Emprendedores y Canales Automatizados de YouTube Shorts, TikTok, Instagram Reels y Facebook Watch.

---

## Acceso RÃ¡pido y Descargas

- **Descargar APK para Android:** [ViralLabs_Studio_AI.apk](https://raw.githubusercontent.com/chenyz10yt/virallabs-studio-ai/main/ViralLabs_Studio_AI.apk)
- **Probar VersiÃ³n Web en GitHub Pages:** [ViralLabs OmniPublish Web](https://chenyz10yt.github.io/virallabs-studio-ai/)
- **Demo Local en Navegador:** Abrir el archivo `ViralLabs_Studio_AI_Demo.html` con doble clic o acceder a `http://localhost:5000/`.

---

## ðŸš€ Novedades de la VersiÃ³n 1.0.0 Build 103 (In-App Auto-Updater & Auto-Installer Suite)

### 1. ðŸ”„ Sistema de Auto-ActualizaciÃ³n e InstalaciÃ³n AutomÃ¡tica In-App (OTA)
- **DetecciÃ³n AutomÃ¡tica de Publicaciones:** Al subir cambios o publicar una nueva versiÃ³n en el servidor o repositorio, la aplicaciÃ³n detecta automÃ¡ticamente la nueva compilaciÃ³n (`Build 103` o superior) comparando `version.json` con mitigaciÃ³n de cachÃ© HTTP (`?nocache=timestamp`).
- **Modal Interactivo de ActualizaciÃ³n:** Muestra la versiÃ³n actual versus la nueva versiÃ³n oficial, el nombre del release, la fecha de publicaciÃ³n y el registro completo de novedades (*changelog*).
- **Modo AutomÃ¡tico Silencioso (1-Clic):** Casilla de verificaciÃ³n *"Descargar e instalar siempre de forma automÃ¡tica al publicar"*. Cuando estÃ¡ activa, la app descarga e inicia la instalaciÃ³n de forma transparente sin interrumpir al usuario.
- **Barra de Progreso y Descarga en Tiempo Real:** Monitor visual en vivo con cÃ¡lculo exacto de megabytes transferidos (`MB / MB`) y porcentaje del $0\%$ al $100\%$ mediante `ReadableStream` y `Blob`.
- **InstalaciÃ³n Directa en Dispositivo:**
  - **En Android:** EjecuciÃ³n del instalador de paquetes de Android (`application/vnd.android.package-archive` MIME), activando la ventana del sistema operativo para actualizar la app de inmediato sin pasar por exploradores de archivos.
  - **En Web / PWA:** NotificaciÃ³n y recarga en caliente del Service Worker (`SKIP_WAITING`), purga de cachÃ©s obsoletas y recarga instantÃ¡nea de la aplicaciÃ³n.
- **ComprobaciÃ³n PeriÃ³dica y Manual:**
  - BotÃ³n directo *"Actualizar"* con icono de nube en la cabecera principal.
  - Distintivo de versiÃ³n interactivo con animaciÃ³n pulsante al haber una actualizaciÃ³n disponible.
  - Tarjeta de *"Estado del Sistema & Actualizaciones OTA"* dentro del Perfil de Creador.
  - Temporizador en segundo plano cada 3 minutos, al reconectar a internet (`online`) y al volver a la pestaÃ±a (`visibilitychange`).

---

### 2. ðŸ–¼ï¸ Capa de Imagen de Movimiento Libre en el Lienzo (Mouse en PC + Touch en MÃ³vil)
- **Movimiento IdÃ©ntico a la Capa de Texto:** La imagen del lienzo se puede mover, desplazar y reubicar con total libertad en los ejes X e Y, tal cual como se mueve el texto sobre el lienzo.
- **Selector de Capa Activa:** Botones rÃ¡pidos `[ ðŸ”¤ Mover Texto ]`, `[ ðŸ–¼ï¸ Mover Imagen ]` y `[ âœ‚ï¸ Recortar Libre ]`, ademÃ¡s de detecciÃ³n automÃ¡tica al hacer clic sobre la foto o sobre la caja de texto.
- **Ajustes de TransformaciÃ³n en Tiempo Real:**
  - **Zoom / Escala Continua:** Del $20\%$ al $300\%$ con control deslizante y visualizaciÃ³n de porcentaje.
  - **RotaciÃ³n Angular Completa:** De $-180^\circ$ a $+180^\circ$ para encuadres dinÃ¡micos, diagonales y tomas estilizadas.
  - **Lectura NumÃ©rica de Coordenadas:** Panel con monitor `X: ...px | Y: ...px` en vivo.
  - **BotÃ³n "Centrar PosiciÃ³n":** Centra la imagen y restablece el encuadre en 1 solo clic.

---

### 3. âœ‚ï¸ Motor de Recorte Interactivo y FijaciÃ³n Real en Lienzo (Crop Engine Pro)
- **Caja de Recorte con 8 Tiradores Interactivos:** 4 tiradores circulares en las esquinas y 4 barras en los bordes para redimensionar el recuadro a cualquier dimensiÃ³n deseada.
- **LÃ­neas GuÃ­a CinemÃ¡ticas (Regla de los Tercios):** CuadrÃ­cula de 9 sectores para composiciÃ³n visual fotogrÃ¡fica profesional.
- **Presets de ProporciÃ³n Oficiales:**
  - `Libre`: Recorte rectangular personalizado sin restricciones.
  - `16:9 YT`: YouTube estÃ¡ndar horizontal y banners de canal.
  - `9:16 Shorts`: TikTok, YouTube Shorts e Instagram Reels vertical.
  - `1:1 Post`: Publicaciones cuadradas de feed.
  - `4:5 Feed`: Formato vertical Ã³ptimo para Instagram y Facebook.
- **EjecuciÃ³n Real del Recorte en Lienzo HTML5:** Al pulsar **"Fijar y Aplicar Recorte"**, la aplicaciÃ³n extrae la porciÃ³n seleccionada de los pÃ­xeles originales, genera una nueva imagen de alta resoluciÃ³n y la fija en el lienzo.
- **BotÃ³n "Deshacer Recorte / Restaurar Original":** Permite revertir a la imagen original sin pÃ©rdida de calidad en cualquier momento.

---

### 4. ðŸŽ¬ Auto-Clipper con ExportaciÃ³n Real de Videos y ConexiÃ³n al Planificador
- **Descargas Reales de Video (MP4 / WebM):** Motor de grabaciÃ³n en tiempo real con `MediaRecorder` y Web Audio API que sintetiza y descarga el archivo de video animado con barras de energÃ­a y medidor viral.
- **IntegraciÃ³n Directa con el Planificador:** El botÃ³n de calendario aÃ±ade automÃ¡ticamente el clip a la cola de publicaciones programadas de `omniState.tasks`, guardÃ¡ndolo en `localStorage` y actualizando el tablero Kanban.

---

### 5. ðŸ‘¤ Avatar Hiperrealista 8K con GrabaciÃ³n Real y Reproductor Interactivo
- **SÃ­ntesis y GrabaciÃ³n en Video Vivo:** La funciÃ³n genera una animaciÃ³n con sincronizaciÃ³n labial segÃºn el guion, graba el flujo con `MediaRecorder` y lo incrusta en un reproductor de video `<video controls loop autoplay>` interactivo.
- **Descargas Directas:** Botones para descargar el archivo de video generado en formato MP4 (Universal) o MOV (Apple).

---

### 6. ðŸŽ¨ ExportaciÃ³n HD Pixel-Perfect (Canvas 2D)
- El botÃ³n de descarga genera un archivo PNG en resoluciÃ³n nativa ($1920\times 1080$, $1080\times 1920$, $1080\times 1080$ o $1080\times 1350$) integrando la imagen recortada y rotada junto con las tipografÃ­as Google Fonts, borde (*stroke*) y opacidades exactas.

---

## ðŸš€ Arquitectura TÃ©cnica y Estructura

- `app/index.html`: NÃºcleo de la aplicaciÃ³n con motor Auto-Updater OTA, lienzo de capas interactivas y herramientas completas.
- `ViralLabs_Studio_AI_Demo.html`: VersiÃ³n demo lista para usar en navegadores de escritorio.
- `index.html`: Enrutador y versiÃ³n para GitHub Pages.
- `version.json` / `app/version.json`: Metadatos oficiales de compilaciÃ³n (v1.0.0 Build 103).
- `android_config/AndroidManifest.xml`: Permisos nativos de Android para instalaciÃ³n de paquetes APK (`REQUEST_INSTALL_PACKAGES`, `DOWNLOAD_WITHOUT_NOTIFICATION`).