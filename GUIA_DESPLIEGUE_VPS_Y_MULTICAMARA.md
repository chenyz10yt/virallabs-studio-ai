# 🚀 Guía Rápida: Despliegue 24/7 en VPS + Segundo Ángulo desde Celular

Con esta configuración, tu transmisión funcionará de forma ininterrumpida las 24 horas del día, los 7 días de la semana, sin necesidad de tener tu computadora encendida. Además, podrás controlar todo desde tu celular o PC y conectar otro celular como segundo ángulo en vivo.

---

## 1. Despliegue en el Servidor VPS (Nube)

Puedes usar cualquier VPS con **Ubuntu 20.04 / 22.04 / 24.04** o **Debian** (Contabo, DigitalOcean, Hetzner, AWS, etc.).

### Paso 1: Subir la carpeta `panel_stream` a tu VPS
Desde tu computadora, puedes subir la carpeta usando SCP o FileZilla:
```bash
scp -r panel_stream root@IP_DE_TU_VPS:~/panel_stream
```
O entrar por SSH a tu servidor:
```bash
ssh root@IP_DE_TU_VPS
```

### Paso 2: Ejecutar el instalador automático
Dentro de la carpeta del proyecto en tu VPS, ejecuta:
```bash
cd ~/panel_stream
sudo bash install.sh
```
El instalador:
- Instala Python, FFmpeg y dependencias.
- Abre los puertos **5000** (Web) y **1935** (RTMP) en el firewall.
- Crea el servicio continuo `systemd` que se reinicia solo si el servidor sufre un corte de luz.
- Deja el panel activo en `http://IP_DE_TU_VPS:5000`.

---

## 2. Control Remoto desde tu PC o Celular

1. Abre en el navegador de tu celular o computadora:
   ```
   http://IP_DE_TU_VPS:5000
   ```
2. Verás el panel con la etiqueta verde **"Servidor VPS Conectado 🟢"**.
3. Pega tu **Clave de emisión de YouTube Studio** y sube tus videos.
4. Presiona **▶ Iniciar Directo**.

---

## 3. Transmisión Multi-Ángulo desde otro Celular

El sistema incluye una interfaz web nativa para conectar un segundo celular como cámara en vivo sin necesidad de instalar aplicaciones:

### Método A: Directo desde el navegador del celular (Sin instalar apps)
1. En tu segundo celular, abre la dirección:
   ```
   http://IP_DE_TU_VPS:5000/camara
   ```
2. Acepta el permiso de cámara del navegador.
3. Presiona el botón rojo **🔴 INICIAR TRANSMISIÓN ÁNGULO 2**.
4. En el panel de control (en tu PC o celular principal), selecciona el modo de transmisión:
   - **🪟 Multicámara PiP**: El video grabado en pantalla completa y el celular en una esquina superior.
   - **📱 Pantalla Dividida (50/50)**: Mitad izquierda video grabado, mitad derecha cámara del celular.
   - **🔴 Conmutar 100% al Celular**: Pasa la transmisión completa al celular en vivo y vuelve al bucle con un clic.

### Método B: Usando apps de transmisión móvil (Larix Broadcaster / Prism Live)
Si prefieres usar una app profesional de cámara en tu celular:
- Configura la salida RTMP en la app hacia:
  `rtmp://IP_DE_TU_VPS:1935/live/celular`

---

## 4. Clave de Transmisión de YouTube

En **YouTube Studio** (studio.youtube.com -> *Emitir en directo*):
- **URL de emisión**: `rtmp://a.rtmp.youtube.com/live2`
- **Clave de emisión**: `xxxx-xxxx-xxxx-xxxx-xxxx` (copia este valor).

Puedes ingresar en el panel:
- Solo la clave: `xxxx-xxxx-xxxx-xxxx-xxxx`
- O la URL completa: `rtmp://a.rtmp.youtube.com/live2/xxxx-xxxx-xxxx-xxxx-xxxx`
