# Viral Labs Studio Apex & OmniPublish Pro v1.0.0 (Build 102)

> **Suite Definitiva de CreaciÃ³n, AnimaciÃ³n, EdiciÃ³n, Billetera y PublicaciÃ³n Multiplataforma con Inteligencia Artificial.**
> DiseÃ±ada para Creadores de Contenido, Emprendedores y Canales Automatizados de YouTube Shorts, TikTok, Instagram Reels y Facebook Watch.

---

## Acceso RÃ¡pido y Descargas

- **Descargar APK para Android:** [ViralLabs_Studio_AI.apk](https://raw.githubusercontent.com/chenyz10yt/virallabs-studio-ai/main/ViralLabs_Studio_AI.apk)
- **Probar VersiÃ³n Web en GitHub Pages:** [ViralLabs OmniPublish Web](https://chenyz10yt.github.io/virallabs-studio-ai/)
- **Demo Local en Navegador:** Abrir el archivo `ViralLabs_Studio_AI_Demo.html` con doble clic o acceder a `http://localhost:5000/`.

---

## ðŸŒŸ Novedades de la VersiÃ³n 1.0.0 Build 102 (Free Image Canvas & Real Execution Suite)

### 1. ðŸ–¼ï¸ Capa de Imagen de Movimiento Libre en el Lienzo (Mouse en PC + Touch en MÃ³vil)
- **Movimiento IdÃ©ntico a la Capa de Texto:** Ahora la imagen del lienzo se puede mover, desplazar y reubicar con total libertad en los ejes X e Y, tal cual como se mueve el texto sobre el lienzo.
- **Selector de Capa Activa:** Botones rÃ¡pidos `[ ðŸ”¤ Mover Texto ]`, `[ ðŸ–¼ï¸ Mover Imagen ]` y `[ âœ‚ï¸ Recortar Libre ]`, ademÃ¡s de detecciÃ³n automÃ¡tica al hacer clic sobre la foto o sobre la caja de texto.
- **Ajustes de TransformaciÃ³n en Tiempo Real:**
  - **Zoom / Escala Continua:** Del $20\%$ al $300\%$ con control deslizante y visualizaciÃ³n de porcentaje.
  - **RotaciÃ³n Angular Completa:** De $-180^\circ$ a $+180^\circ$ para encuadres dinÃ¡micos, diagonales y tomas estilizadas.
  - **Lectura NumÃ©rica de Coordenadas:** Panel con monitor `X: ...px | Y: ...px` en vivo.
  - **BotÃ³n "Centrar PosiciÃ³n":** Centra la imagen y restablece el encuadre en 1 solo clic.

---

### 2. âœ‚ï¸ Motor de Recorte Interactivo y FijaciÃ³n Real en Lienzo (Crop Engine Pro)
- **Caja de Recorte con 8 Tiradores Interactivos:** 4 tiradores circulares en las esquinas y 4 barras en los bordes para redimensionar el recuadro a cualquier dimensiÃ³n deseada, con arrastre del cuerpo central para reubicar la ventana de recorte.
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

### 3. ðŸŽ¬ Auto-Clipper con ExportaciÃ³n Real de Videos y ConexiÃ³n al Planificador
- **Descargas Reales de Video (MP4 / WebM):** Reemplazo de toasts simulados por un motor de grabaciÃ³n en tiempo real con `MediaRecorder` y Web Audio API que sintetiza y descarga el archivo de video animado con barras de energÃ­a y medidor viral.
- **IntegraciÃ³n Directa con el Planificador:** El botÃ³n de calendario aÃ±ade automÃ¡ticamente el clip a la cola de publicaciones programadas de `omniState.tasks`, guardÃ¡ndolo en `localStorage` y actualizando el tablero Kanban.

---

### 4. ðŸ‘¤ Avatar Hiperrealista 8K con GrabaciÃ³n Real y Reproductor Interactivo
- **SÃ­ntesis y GrabaciÃ³n en Video Vivo:** La funciÃ³n genera una animaciÃ³n con sincronizaciÃ³n labial segÃºn el guion, graba el flujo con `MediaRecorder` y lo incrusta en un reproductor de video `<video controls loop autoplay>` interactivo.
- **Descargas Directas:** Botones para descargar el archivo de video generado en formato MP4 (Universal) o MOV (Apple).

---

### 5. ðŸŽ¨ ExportaciÃ³n HD Pixel-Perfect (Canvas 2D)
- El botÃ³n de descarga genera un archivo PNG en resoluciÃ³n nativa ($1920\times 1080$, $1080\times 1920$, $1080\times 1080$ o $1080\times 1350$) integrando la imagen recortada y rotada junto con las tipografÃ­as Google Fonts, borde (*stroke*) y opacidades exactas.

---

## ðŸš€ Arquitectura TÃ©cnica y Estructura

- `app/index.html`: NÃºcleo de la aplicaciÃ³n optimizada para WebView de Android y navegadores modernos.
- `ViralLabs_Studio_AI_Demo.html`: VersiÃ³n demo offline/online lista para usar en navegadores de escritorio.
- `index.html`: Enrutador y versiÃ³n para GitHub Pages.
- `version.json` / `app/version.json`: Metadatos de compilaciÃ³n (v1.0.0 Build 102).