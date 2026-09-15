# ⚡ Viral Labs Studio AI (v2.7) — Creator OS & Multi-Platform Engine

[![Version](https://img.shields.io/badge/version-2.7.0%20AI-6366f1.svg?style=for-the-badge)](https://github.com)
[![Status](https://img.shields.io/badge/status-Production%20Ready-10b981.svg?style=for-the-badge)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-3b82f6.svg?style=for-the-badge)](https://github.com)
[![Zero-Dependencies](https://img.shields.io/badge/dependencies-Zero%20(Pure%20Vanilla%20ES6)-ec4899.svg?style=for-the-badge)](https://github.com)

> **Viral Labs Studio** es la suite integral de producción, automatización, transmisión en vivo y publicación simultánea diseñada para creadores de contenido que buscan maximizar el alcance algorítmico, retención y monetización en **Facebook (Perfil & Fanpage), Instagram, TikTok, YouTube, Twitch, X y LinkedIn**.

---

## 🌟 Características Principales

### 1. ✍️ AI Content Studio & Diseñador de Portadas / Posts
- **Librería Tipográfica Viral (Google Fonts)**: Bebas Neue, Montserrat 900, Anton, Outfit 800, Permanent Marker, JetBrains Mono e Inter.
- **Efectos de Texto Avanzados**: Contornos y bordes con grosor milimétrico (0-30px), sombras profundas de alto relieve (0-50px), y **cajas de fondo resaltadas** configurables con padding y border-radius.
- **Paleta de Stickers & Emojis Virales**: Inserción inmediata de badges de alta retención (`🔥 100% VIRAL`, `🔴 EN VIVO`, `⚡ NUEVO`, `💎 PRO`, `🤫 SECRETO`, `😱 WOW`, etc.) y emojis de impacto.
- **Formatos y Relaciones de Aspecto Nativas**:
  - `16:9` Miniaturas de YouTube (1280x720)
  - `9:16` Shorts / TikTok / Reels (720x1280)
  - `1:1` Post Cuadrado (1080x1080)
  - `4:5` **Post Vertical para Feed de Facebook & Instagram (1080x1350)**
  - `Portada` Banners oficiales para Fanpage de Facebook & Cabecera de YouTube (1640x624)
- **Manipulador 360° Interactivo**: Arrastre libre de capas, 4 esquinas de redimensionamiento, knob de rotación angular con snap y efectos espejo (Horizontal y Vertical).
- **Exportador Ultra HD 4K Lossless**: Renderizado en canvas de 3840x2160 sin pérdida de calidad.
- **Enlace Directo**: Botón *🚀 Enviar a Planificador* para transferir el diseño automáticamente al área de publicación.

---

### 2. 📅 Planificador de Contenidos Multi-Red (Facebook Perfil vs Fanpage)
- **Selección Explícita de Destinos**:
  - 📘 **Facebook: Perfil Personal** (Muro personal / Amigos)
  - 🏢 **Facebook: Fanpage / Página de Creador** (Página pública con monetización)
  - 📸 **Instagram: Feed & Reels**
  - ⭕ **Instagram: Stories (24h)**
  - 🎵 **TikTok**
  - ▶️ **YouTube Shorts & Videos**
  - ✖️ **X (Twitter)**
  - 💼 **LinkedIn**
- **Tipos de Contenido**: Post Estándar / Imagen, Short / Reel Vertical, Video Horizontal y Carrusel.
- **Zona de Carga Drag & Drop**: Arrastra imágenes y videos directamente al compositor o impórtalos con un clic desde el Studio.
- **Contador Dinámico de Caracteres**: Indicador en vivo de límite de caracteres adaptado según la red activa (ej: 2,200 en Instagram/TikTok, 63,206 en Facebook, 5,000 en YouTube).
- **Simulador de Smartphone en Vivo**: Vistas previas fotorrealistas de cómo lucirá el post en **Facebook (con toggle Perfil / Fanpage)**, TikTok, Instagram y YouTube Shorts.
- **Heatmap de Horas Pico Algorítmicas**: Sugerencias de horarios de mayor viralidad calculadas según la ventana horaria del día.

---

### 3. 📡 Multistream Hub & Transmisión Simultánea
- **Grabador de Pantalla Nativo en HD**: Captura tu escritorio, ventanas o pestañas junto con audio del sistema y micrófono utilizando `MediaRecorder` nativo sin necesidad de plugins externos. Descarga automática en formato de video `.webm`.
- **Captura Instantánea (Snapshot)**: Toma capturas de pantalla instantáneas en resolución nativa desde el monitor de transmisión.
- **Conmutador de Escenas Estilo OBS**:
  - `🎨 Estudio Principal`: Gráficos y visualizador interactivo.
  - `📷 Cámara Web`: Entrada de cámara en pantalla completa.
  - `🖼️ Pantalla + PiP`: Compartir pantalla con recuadro Facecam en esquina inferior.
  - `🖥️ Solo Pantalla`: Captura limpia de escritorio.
  - `📱 Cámara Móvil`: Conexión de smartphone como cámara remota mediante WebRTC o IP Webcam.
- **Mezclador de Audio de 3 Canales**: Control de volumen individual para Master General, Micrófono y Audio de Sistema/PC, con función de silenciado rápido (*Mute All*).
- **Telemetría de Transmisión**: Monitoreo en vivo de bitrate de salida, FPS (60.0), pérdida de paquetes y carga de CPU, junto a vúmetro estéreo peak dB.
- **Chat Unificado Interactivo**: Agrupa comentarios en tiempo real de TikTok, YouTube, Facebook y Twitch con herramienta para fijar preguntas en pantalla en el Ticker (*Lower Third*).

---

### 4. ✂️ Auto-Clipper Viral & Subtítulos Karaoke
- Detección de picos de retención algorítmica y momentos de risas/hooks.
- Subtítulos dinámicos estilo MrBeast con animación karaoke y resaltado automático por palabras clave y emojis.
- Waveform interactivo con marcador de reproducción y exportación en 9:16.

---

### 5. 🎙️ Voice Lab & Licencia de Derechos de Autor
- Calibración acústica de voz para captura de frecuencia fundamental (F0), timbre y tono.
- Generador y firmador de **Certificado Legal de Derechos de Autor y Anti-Deepfake** (código de verificación único compatible con normativas de YouTube, TikTok y Meta).
- Síntesis de voz clonada con selector de inflexión emocional (*Viral, Misterio, Cinemático, Cercano*).

---

### 6. 🔐 Autenticación & Conectores OAuth Oficiales
- Autenticación híbrida: Inicio de sesión con **Google Workspace** o mediante correo electrónico.
- Gestor de Conexiones OAuth para APIs oficiales:
  - **Meta Graph API** (Facebook Perfil, Facebook Fanpages e Instagram Graph API)
  - **YouTube Studio API** (Publicación directa y YouTube Live RTMP)
  - **TikTok for Creators API**
  - **Twitch Interactive API**
- Billetera BYOK (*Bring Your Own Key*) para almacenar de forma cifrada claves de Google Gemini, OpenAI, Runway y ElevenLabs en el cliente.

---

### 7. 📈 Radar de Algoritmos & Calculadora de Monetización
- Análisis semántico de ganchos virales con puntuación radial (0-100) y sugerencias de mejora.
- Calculadora de ingresos por CPM, acuerdos de marca y suscripciones según nicho de mercado.

---

### 8. 🎙️ Teleprompter Pro Flotante 4K
- Modo espejo configurable para cristal divisor de teleprompter físico.
- Control de velocidad, tamaño de fuente y lectura guiada.

---

## 🚀 Inicio Rápido

No necesitas Node.js ni instalar paquetes adicionales (cero dependencias de npm).

### Opción 1: En Windows con un solo clic
Haz doble clic en el archivo:
```
Iniciar_ViralLabs.bat
```
Esto iniciará el servidor local nativo en PowerShell y abrirá automáticamente tu navegador en `http://localhost:8080/`.

### Opción 2: Mediante PowerShell
Ejecuta en tu terminal:
```powershell
powershell -ExecutionPolicy Bypass -File .\server.ps1
```
Abre tu navegador en `http://localhost:8080/`.

---

## 📂 Estructura del Proyecto

```
web y app/
│
├── index.html               # Aplicación principal Viral Labs Studio Suite
├── fanpage.html             # Fanpage pública optimizada para monetización
├── manifest.json            # Manifiesto PWA para instalación como app nativa
├── service-worker.js        # Service Worker para funcionamiento offline y caché
├── server.ps1               # Servidor HTTP ultraligero nativo en PowerShell
├── Iniciar_ViralLabs.bat    # Lanzador en un solo clic
│
├── css/
│   ├── main.css             # Variables, reseteo y layout global
│   ├── glassmorphism.css    # Efectos glassmorphism, botones y badges
│   ├── studio.css           # Editor de portadas, tipografías y stickers
│   ├── clipper.css          # Auto-clipper y subtítulos karaoke
│   ├── multistream.css      # Multistream hub, grabador y mezclador
│   ├── planner.css          # Planificador, destinos FB/IG y mockup
│   ├── radar.css            # Radar de algoritmos y métricas
│   └── visualstudio.css     # Manipulador 360° y gizmos de lienzo
│
├── js/
│   └── bundle.js            # Motor unificado modular (Storage, Studio, Multistream, Planner, etc.)
│
└── assets/                  # Logos, banners y demos de medios
```

---

## 📤 Cómo Subir este Proyecto a GitHub

Sigue estos sencillos pasos en tu terminal (PowerShell o Git Bash) dentro de esta carpeta:

```bash
# 1. Inicializar el repositorio Git
git init

# 2. Agregar todos los archivos al seguimiento
git add .

# 3. Crear el commit inicial con la versión completa
git commit -m "feat: Viral Labs v2.7 AI - Suite completa con generador de posts, grabador de pantalla y selector Facebook Perfil/Fanpage"

# 4. Renombrar la rama principal a main
git branch -M main

# 5. Conectar tu repositorio remoto de GitHub (reemplaza con tu URL de GitHub)
git remote add origin https://github.com/TU_USUARIO/viral-labs-studio.git

# 6. Subir tus cambios a GitHub
git push -u origin main
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Eres libre de usarlo, modificarlo y desplegarlo para proyectos comerciales y personales.
