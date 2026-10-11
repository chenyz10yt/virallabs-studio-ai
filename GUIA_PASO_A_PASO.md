# 🎬 StreamHub 24/7 Studio — Guía de Emisión Real (YouTube, Facebook & Celular QR)

Bienvenido a la versión definitiva de **StreamHub 24/7 Studio**. Este sistema está diseñado para que puedas hacer tu **primera transmisión real en directo** hacia **YouTube Live**, **Facebook Live** o **ambas plataformas simultáneamente (Dual Stream)** directamente desde un servidor en la nube (VPS) sin depender de OBS ni tener que dejar encendida tu computadora personal.

---

## 🌟 Novedades y Herramientas del Creador

1. **Selector Multiplataforma**:
   - 🔴 **YouTube Live**: Transmite en bucle 24/7 con bloques automáticos que guardan tus directos como videos en tu canal.
   - 🔵 **Facebook Live**: Transmite a páginas o perfiles de Facebook con el códec H.264 y fotogramas clave de 2 segundos requeridos por Facebook.
   - 🟣 **Transmisión Dual (YouTube + Facebook)**: Emite a ambas plataformas a la vez mediante multiplexación inteligente (`-f tee`) sin duplicar el consumo de CPU.
   - ⚙️ **RTMP Personalizado**: Para emitir en Twitch, Kick o servidores propios.
2. **Botón "🧪 Probar Conexión (5s)"**:
   - Realiza un test de handshake de 5 segundos contra YouTube o Facebook antes de emitir. Te confirma si tu clave es válida y si los servidores están listos, eliminando la incertidumbre de no saber por qué no arranca la transmisión.
3. **Conexión Celular por Código QR (Sin Cables ni Apps)**:
   - **📷 Cámara Móvil (Ángulo 2)**: Escanea el QR con la cámara de tu celular (iPhone o Android) para transmitir video en directo desde tu teléfono hacia el servidor.
   - **🎮 Control Remoto de Bolsillo**: Escanea el QR para controlar todo el estudio (iniciar/detener, cambiar de video, cambiar escenas) desde tu celular acostado en la cama o el sillón.
4. **Consola del Director (Live Switcher)**:
   - Botones con indicadores luminosos LED para conmutar escenas al instante:
     - `🎬 Video Principal (Bucle)`: Transmite el video del servidor en bucle continuo.
     - `🪟 Multicámara PiP`: Muestra el video de fondo y la cámara de tu celular en la esquina superior derecha (ideal para reaccionar).
     - `📱 Pantalla Dividida (50/50)`: Mitad video del servidor y mitad cámara de celular.
     - `🔴 Celular 100% en Vivo`: Pone la cámara de tu celular a pantalla completa.
     - `⏸ Pantalla de Pausa`: Placa "En breve volvemos..." con audio/silencio para pausar sin que YouTube o Facebook corten tu directo.
5. **Rótulo Dinámico de Texto en Pantalla**:
   - Escribe mensajes en tiempo real (ej: *"¡Suscríbete y activa la campana! 🔔"*) y actualízalos al instante con el botón `⚡ Actualizar Rótulo`.
6. **Subida de Videos Pesados**:
   - Arrastra videos de 500 MB a 10 GB directamente al servidor con barra de progreso real en porcentaje.
7. **Meta de 4.000 Minutos**:
   - Bloques automáticos de 11h 55m para canales nuevos (garantiza archivo VOD en YouTube) y desbloqueo del modo 24 Horas ininterrumpidas.

---

## 🚀 Paso 1: Poner en Marcha el Panel en tu Servidor VPS Linux

*(Si ya ejecutaste `sudo bash install.sh` en tu servidor, salta directamente al Paso 2).*

Conéctate a tu servidor Linux (Ubuntu 20.04/22.04/24.04 o Debian) vía SSH:
```bash
ssh root@TU_IP_DEL_SERVIDOR
```

Entra a la carpeta del proyecto y ejecuta el instalador automatizado:
```bash
cd ~/panel_stream
sudo bash install.sh
```

El instalador instalará FFmpeg, Python, creará el servicio 24/7 y te dará el enlace:
```
http://TU_IP_PUBLICA:5000
```
Abre ese enlace en el navegador de tu computadora o teléfono.

---

## 🔑 Paso 2: Cómo Obtener las Claves Correctas (¡Evita el error común!)

> [!CAUTION]
> **Error Muy Común**: La dirección `rtmp://a.rtmp.youtube.com/live2` es la **URL del Servidor**, NO es tu clave de emisión privada. Si pegas solo esa URL, YouTube rechazará la transmisión.

### Para transmitir en 🔴 YouTube Live:
1. Entra a [YouTube Studio](https://studio.youtube.com).
2. En la esquina superior derecha, haz clic en **Emitir en directo** (icono rojo de emisión).
3. En la pestaña **Emitir** (menú de la izquierda), baja a la sección **Configuración de la emisión**.
4. Verás dos campos:
   - *URL de la emisión*: `rtmp://a.rtmp.youtube.com/live2` (El panel ya la conoce, no necesitas copiarla).
   - *Clave de emisión*: Haz clic en **Copiar** (tiene el formato: `xxxx-xxxx-xxxx-xxxx-xxxx`).
5. En el panel StreamHub, selecciona la pestaña **🔴 YouTube Live** y pega tu clave.

### Para transmitir en 🔵 Facebook Live:
1. Entra a [Facebook Live Producer](https://www.facebook.com/live/producer).
2. Selecciona transmitir desde tu perfil o página de Facebook.
3. Elige la opción **Software de streaming**.
4. En la sección de configuración de stream, copia la **Clave de stream** (ejemplo: `FB-123456789...`).
5. En el panel StreamHub, selecciona la pestaña **🔵 Facebook Live** y pega la clave.

### Para transmitir en 🟣 Modo Dual (YouTube + Facebook a la vez):
1. Selecciona la pestaña **🟣 Dual (YT + FB)**.
2. Pega tu clave de YouTube en el primer campo.
3. Pega tu clave de Facebook Live en el segundo campo.

---

## 🧪 Paso 3: Probar la Conexión Antes de Emitir

Antes de darle al botón de iniciar directo, haz clic en:
👉 **`🧪 Probar Conexión con los Servidores`**

- El panel enviará un paquete sintético de prueba de 5 segundos hacia YouTube/Facebook.
- Si ves el aviso verde:
  `✅ ¡Conexión con [PLATAFORMA] Exitosa! Tu clave y los servidores responden correctamente.`
  **¡Tu clave es 100% correcta y ya puedes emitir sin riesgo a fallar!**
- Si ves un aviso rojo, te explicará exactamente el problema (ej: *"Clave rechazada: revisa si tu directo está activo en YouTube/Facebook"*).

---

## 📱 Paso 4: Cómo Conectar tu Celular por Código QR

1. En la parte superior del panel, haz clic en el botón:
   👉 **`📱 Conectar Celular / QR`**
2. Aparecerá una ventana con dos opciones:
   - **📷 Cámara Secundaria**: Muestra un código QR apuntando a `http://TU_IP:5000/camara`.
   - **🎮 Control Remoto**: Muestra un código QR apuntando a `http://TU_IP:5000`.
3. **Para usar tu celular como cámara**:
   - Abre la aplicación de cámara de tu celular (iPhone o Android).
   - Apunta al código QR de la pantalla y pulsa el enlace amarillo que aparece.
   - En tu celular, pulsa **"Permitir cámara y micrófono"**.
   - Verás tu cámara en vivo en la pantalla del celular.
   - Toca el gran botón rojo: **`🔴 INICIAR TRANSMISIÓN ÁNGULO 2`**.
   - ¡Listo! En el panel de control verás que la etiqueta cambia a:
     `🟢 Celular Conectado (Ángulo 2 Activo)`

---

## 🎛️ Paso 5: Cómo Usar la Consola de Dirección (Conmutar Escenas)

Una vez que tu directo esté transmitiendo, puedes cambiar de escena con solo un clic en la botonera táctil:

| Botón de Escena | Qué hace en tu transmisión |
|---|---|
| **🎬 Video Bucle** | Muestra únicamente el video subido al servidor en ciclo continuo 24/7. |
| **🪟 Multi PiP** | Video principal de fondo + la cámara de tu celular en la esquina superior derecha (ideal para hablar o reaccionar). |
| **📱 Dividida** | Pantalla dividida 50/50: a la izquierda tu video y a la derecha tu celular. |
| **🔴 Celular Vivo** | La cámara de tu teléfono ocupa el 100% de la pantalla del directo. |
| **⏸️ En Breve** | Muestra una placa elegante de espera con fondo oscuro para cuando necesites pausar sin cortar la señal. |

*El indicador LED verde se encenderá sobre la escena que está saliendo al aire en ese momento.*

---

## 🔴 Paso 6: Arrancar tu Primera Transmisión Real

1. Arrastra al menos un video (MP4) en la zona de subida **"Biblioteca de Videos en Servidor"**.
2. Selecciona la plataforma (YouTube, Facebook o Dual).
3. Pulsa el gran botón verde:
   👉 **`🔴 INICIAR TRANSMISIÓN EN DIRECTO`**
4. En 10 a 15 segundos, entra a tu panel de YouTube Studio o Facebook Live:
   - Verás el estado en verde: **"Conexión excelente"**.
   - Haz clic en **Transmitir en directo** en YouTube Studio / Facebook si tienes configurado inicio manual, ¡y estarás al aire para todo el mundo!

---

## 🛠️ Comandos de Control en el Servidor VPS

Puedes apagar tu computadora personal; la transmisión continuará en el servidor 24/7. Si en algún momento necesitas gestionar el servicio desde la consola SSH de tu servidor:

```bash
# Ver estado del servicio
sudo systemctl status panel_stream

# Ver logs de emisión de FFmpeg en tiempo real
sudo journalctl -u panel_stream -f

# Reiniciar el panel
sudo systemctl restart panel_stream

# Detener el panel
sudo systemctl stop panel_stream
```
