# Viral Labs Studio Apex & OmniPublish Pro v1.0.0 (Beta Oficial)

> **Suite Definitiva de CreaciÃ³n, AnimaciÃ³n, EdiciÃ³n, Billetera y PublicaciÃ³n Multiplataforma con Inteligencia Artificial.**
> DiseÃ±ada para Creadores de Contenido, Emprendedores y Canales Automatizados de YouTube Shorts, TikTok, Instagram Reels y Facebook Watch.

---

## Acceso RÃ¡pido y Descargas

- **Descargar APK para Android:** [ViralLabs_Studio_AI.apk](https://raw.githubusercontent.com/chenyz10yt/virallabs-studio-ai/main/ViralLabs_Studio_AI.apk)
- **Probar VersiÃ³n Web en GitHub Pages:** [ViralLabs OmniPublish Web](https://chenyz10yt.github.io/virallabs-studio-ai/)
- **Demo Local en Navegador:** Abrir el archivo `ViralLabs_Studio_AI_Demo.html` con doble clic o acceder a `http://localhost:5000/`.

---

## ðŸŒŸ Novedades de la VersiÃ³n 1.0.0 Apex (Monetized & Auth Edition)

### 1. ðŸ” Sistema de AutenticaciÃ³n de Creadores (Viral Labs Auth Suite)
- Modal dedicado de inicio de sesiÃ³n y registro de cuentas.
- Soporte para **Google / YouTube OAuth**, **Meta / Facebook Login**, y autenticaciÃ³n vÃ­a **Correo ElectrÃ³nico y ContraseÃ±a**.
- SesiÃ³n persistente almacenada de forma segura en `localStorage` (`vl_user_profile`), lista para integraciÃ³n con Firebase / Supabase Auth.
- Indicador de perfil y avatar de usuario en la barra superior (Header) con visualizaciÃ³n de nombre, iniciales y proveedor.

---

### 2. ðŸª™ Billetera y Ledger de CrÃ©ditos (Wallet & Credits Engine)
- **2 Videos Gratuitos de Bienvenida:** Todo nuevo usuario o creador recibe 2 crÃ©ditos iniciales para renderizar videos 8K completos de prueba (guion 4 fases, locuciÃ³n TTS en vivo, karaoke oro, audio binaural 528Hz/432Hz y miniatura).
- **âš¡ Modo BYOK ("Bring Your Own Key" - Google AI Studio):**
  - Permite ingresar una API Key personal de Google AI Studio (`AIzaSy...`).
  - Al activar este modo, **el consumo de crÃ©ditos se desactiva por completo (0 crÃ©ditos gastados)**, permitiendo generaciones 100% ilimitadas.
  - Indicador de estado en tiempo real en la cabecera: `âš¡ BYOK Ilimitado`.
  - BotÃ³n para probar la conectividad y latencia con Gemini 2.5 e Imagen 3.
- **Tienda de Recargas Integrada (Stripe / Google Play Billing / PayPal):**
  - **Paquete Creator:** 10 videos completos por $4.99 USD ($0.50/video).
  - **Paquete Pro Studio:** 30 videos completos por $11.99 USD ($0.40/video - Ahorro del 20%).
- **Ledger de Transacciones:** Historial transparente que registra fecha, concepto, crÃ©ditos aÃ±adidos o deducidos y saldo resultante.

---

### 3. ðŸŒ Centro de ConexiÃ³n OAuth de Plataformas & PÃ¡ginas
- Modal interactivo de configuraciÃ³n y gestiÃ³n OAuth para:
  - **ðŸ”´ YouTube Studio:** VisualizaciÃ³n de canal conectado, nÃºmero de suscriptores, avatar y scopes de subida (`youtube.upload`, `userinfo.profile`).
  - **ðŸ”µ Meta (Facebook & Instagram):**
    - **Gestor DinÃ¡mico de PÃ¡ginas de Facebook:** Permite listar, seleccionar la pÃ¡gina principal y vincular nuevas pÃ¡ginas administradas con su nombre e ID.
    - SincronizaciÃ³n automÃ¡tica con la tarjeta de Facebook en **OmniPublish 1-Clic**.
    - ConexiÃ³n de cuenta profesional de Instagram con publicaciÃ³n directa.
  - **âš« TikTok for Creators:** Permisos de Content Posting API (`video.upload`, `video.publish`, `user.info.basic`).
  - **ðŸŸ£ Twitch & Kick:** Monitoreo en vivo y clÃ­pper automÃ¡tico.
- **Generador de URLs de AutorizaciÃ³n OAuth Oficiales:** Permite configurar Client ID / App ID y generar o copiar la URL oficial con redirecciÃ³n hacia la app.

---

### 4. ðŸš€ OmniPublish Multi-Publisher Engine (Disparo SimultÃ¡neo en 1 Clic)
- EnvÃ­o simultÃ¡neo o individual a YouTube, Facebook, Instagram y TikTok.
- Soporte para capÃ­tulos automÃ¡ticos en YouTube (timestamps), First Comment con hashtags en Instagram, selector dinÃ¡mico de PÃ¡ginas de Facebook y controles de privacidad en TikTok.

---

### 5. ðŸŽ¨ Canvas Pro de EdiciÃ³n Visual & Transformaciones Totales
- Formatos: 16:9, 9:16, 4:5 y 1:1.
- Zoom de imagen base (50% a 200%), rotaciÃ³n libre (-180Â° a 180Â°) y herramienta de recorte (Crop tool).
- Control de opacidad dual (fondo de 10% a 100%, caja de texto de 0% a 100%).
- Capas de texto multitÃ¡ctiles independientes (PC ratÃ³n y mÃ³vil touch).
- ExportaciÃ³n directa a PNG de alta definiciÃ³n.

---

### 6. ðŸ“… Planificador Multi-Horario (Multi-Task Scheduler)
- Cola de tareas visual con horarios simultÃ¡neos o escalonados.
- BotÃ³n de subida forzada inmediata ("Subir Ya").
- ExportaciÃ³n completa en JSON.

---

## ðŸ› ï¸ CÃ³mo Probar Localmente

1. Abre un navegador y dirÃ­gete a `http://localhost:5000/`.
2. En la cabecera verÃ¡s:
   - Tu botÃ³n de **Billetera** (`ðŸª™ 2 CrÃ©ditos`). PÃºlsalo para ver el ledger, recargar o ingresar tu API Key en Modo BYOK.
   - Tu botÃ³n de **Perfil de Creador**. PÃºlsalo para iniciar sesiÃ³n con Google, Facebook o Correo.
3. Ve a la pestaÃ±a **Conexiones** para gestionar tus canales, autorizar permisos OAuth y vincular pÃ¡ginas de Facebook.
4. Ve a la pestaÃ±a **Auto-Video 8K**, selecciona un nicho (ej: Espiritualidad o Finanzas) y pulsa **Generar Video 8K**. Observa cÃ³mo se ejecuta al pie de la letra y cÃ³mo tu billetera o clave BYOK gestiona los crÃ©ditos de forma transparente.