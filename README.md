# Viral Labs Studio Apex & OmniPublish Pro v1.0.0 (Build 101)

> **Suite Definitiva de CreaciÃ³n, AnimaciÃ³n, EdiciÃ³n, Billetera y PublicaciÃ³n Multiplataforma con Inteligencia Artificial.**
> DiseÃ±ada para Creadores de Contenido, Emprendedores y Canales Automatizados de YouTube Shorts, TikTok, Instagram Reels y Facebook Watch.

---

## Acceso RÃ¡pido y Descargas

- **Descargar APK para Android:** [ViralLabs_Studio_AI.apk](https://raw.githubusercontent.com/chenyz10yt/virallabs-studio-ai/main/ViralLabs_Studio_AI.apk)
- **Probar VersiÃ³n Web en GitHub Pages:** [ViralLabs OmniPublish Web](https://chenyz10yt.github.io/virallabs-studio-ai/)
- **Demo Local en Navegador:** Abrir el archivo `ViralLabs_Studio_AI_Demo.html` con doble clic o acceder a `http://localhost:5000/`.

---

## ðŸŒŸ Novedades de la VersiÃ³n 1.0.0 Build 101 (Creator Profile & Advanced Visual Canvas)

### 1. ðŸ‘¤ Sistema de Perfil de Creador en 1-Clic (`creatorProfileModal`)
- **Avatar / Logo Personalizable:** Toca el avatar en la esquina superior izquierda o en la ventana de ajustes para abrir directamente la galerÃ­a de tu celular o el explorador de archivos de la PC y colocar tu foto oficial (`profileAvatarUpload`).
- **ConfiguraciÃ³n de Marca:** Campos editables para tu nombre de creador (`Fabian Martinez`), nicho principal (`Hablemos Sin Filtro â€¢ Creator`) y enlace a redes sociales.
- **Persistencia Local AutomÃ¡tica:** Los datos y la foto quedan almacenados en la memoria del dispositivo (`localStorage`: `vl_profile_name`, `vl_profile_niche`, `vl_profile_url`, `vl_profile_avatar`), mostrÃ¡ndose en el encabezado principal cada vez que abres la app.

---

### 2. ðŸŽ¬ Manipulador y Recortador CinemÃ¡tico Pan & Crop Engine
- **Arrastre Libre con Clic Sostenido / Touch:** Puedes hacer clic sostenido con el ratÃ³n (en PC) o tocar y arrastrar con el dedo (en celular) sobre la imagen base en el lienzo interactivo para desplazarla en cualquier Ã¡ngulo (X, Y).
- **Control de Zoom y RotaciÃ³n:** Deslizadores continuos de escala (del $50\%$ al $250\%$) y rotaciÃ³n angular (de $-180^\circ$ a $+180^\circ$) para encuadres diagonales o tomas panorÃ¡micas.
- **Caja de SelecciÃ³n de Recorte (*Crop Box*):** Activa una guÃ­a visual sobre el lienzo para demarcar el Ã¡rea exacta que quedarÃ¡ enmarcada.
- **BotÃ³n "Fijar Recorte":** Bloquea la composiciÃ³n exacta en esas coordenadas del lienzo.
- **BotÃ³n "Centrar Foto / Reiniciar":** Restaura el encuadre de la foto al centro inmediatamente.

---

### 3. âœï¸ TipografÃ­a Profesional y LibrerÃ­a de Fuentes CinemÃ¡ticas
- **6 Fuentes Google Fonts de Alto Impacto Integradas:**
  - *Montserrat Black:* Titulares pesados y limpios para YouTube.
  - *Anton:* TipografÃ­a vertical de alto impacto para Reels y Shorts.
  - *Bebas Neue:* Estilo cinematogrÃ¡fico alargado.
  - *Outfit UltraBold:* GeometrÃ­a moderna de alta legibilidad en pantallas mÃ³viles.
  - *Syne Heavy:* EstÃ©tica futurista y editorial.
  - *Fira Code:* Estilo consola para temÃ¡ticas de tecnologÃ­a o misterio.
- **Control de Borde / Trazo del Texto (*Stroke Control*):**
  - Selector de color de borde independiente (`inputStrokeColor`).
  - Control deslizante para el grosor del contorno de 0 a 8 px (`rngStrokeWidth`).
- **Control de Opacidad Dual:**
  - Opacidad del texto regulable del $10\%$ al $100\%$.
  - Opacidad de la caja de fondo regulable del $0\%$ al $100\%$.

---

### 4. ðŸ” Sistema de AutenticaciÃ³n & Conexiones OAuth
- Proveedores: Google / YouTube OAuth, Meta / Facebook Login, Correo ElectrÃ³nico.
- Centro de conexiones OAuth para YouTube Studio, TikTok for Creators, Meta Business y Twitch.
- Gestor dinÃ¡mico de mÃºltiples PÃ¡ginas de Facebook sincronizado con OmniPublish 1-Clic.

---

### 5. ðŸª™ Billetera, Ledger de CrÃ©ditos y Modo BYOK Google AI Studio
- 2 videos de prueba gratis de bienvenida para nuevos creadores.
- **Modo BYOK (Bring Your Own Key):** Introduce tu clave de Google AI Studio (`AIzaSy...`) para renderizar de forma 100% ILIMITADA sin gastar crÃ©ditos de la billetera.
- Tienda de crÃ©ditos (Paquete Creator 10 videos por $4.99 USD, Paquete Pro 30 videos por $11.99 USD).

---

## ðŸ› ï¸ CÃ³mo Probar Localmente

1. Abre un navegador y dirÃ­gete a `http://localhost:5000/`.
2. En la cabecera:
   - Haz clic en tu **Avatar de Creador** para cambiar tu foto, nombre de marca o nicho.
   - Haz clic en **Billetera** (`ðŸª™ 2 CrÃ©ditos`) para consultar tu saldo o activar el Modo BYOK.
3. En la pestaÃ±a **OmniPublish 1-Clic -> Editor Visual Pro**:
   - Carga una foto base o usa la cinemÃ¡tica por defecto.
   - Haz clic sostenido con el ratÃ³n o desliza con el dedo para encuadrar la imagen libremente.
   - Ajusta el zoom ($50\% - 250\%$) y la rotaciÃ³n ($-180^\circ$ a $+180^\circ$).
   - Activa el **Ãrea de Recorte** y presiona **Fijar Recorte**.
   - Prueba las 6 tipografÃ­as (Montserrat, Anton, Bebas Neue, Outfit, Syne, Fira Code), ajusta el grosor y color del borde (*stroke*), y exporta en alta definiciÃ³n.