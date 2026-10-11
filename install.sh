#!/usr/bin/env bash
# =============================================================================
# INSTALADOR AUTOMATIZADO - PANEL DE STREAMING YOUTUBE 24/7 (UBUNTU / DEBIAN)
# =============================================================================

set -e

echo ""
echo "=================================================================="
echo "  🚀 INSTALANDO PANEL DE CONTROL STREAMING 24/7 (YOUTUBE LIVE)"
echo "=================================================================="
echo ""

# 1. Verificar permisos de superusuario
if [ "$EUID" -ne 0 ]; then
  echo "❌ Por favor ejecuta este instalador con sudo: sudo bash install.sh"
  exit 1
fi

CURRENT_DIR=$(pwd)
APP_USER=$(logname 2>/dev/null || echo $SUDO_USER)
if [ -z "$APP_USER" ]; then
    APP_USER="root"
fi

echo "📦 1. Actualizando repositorios e instalando paquetes del sistema..."
apt-get update -y
apt-get install -y python3 python3-pip python3-venv ffmpeg screen curl ufw

echo "📂 2. Creando directorios y entorno virtual..."
mkdir -p "$CURRENT_DIR/uploads"

if [ ! -d "$CURRENT_DIR/venv" ]; then
    python3 -m venv "$CURRENT_DIR/venv"
fi

echo "📦 3. Instalando dependencias de Python..."
"$CURRENT_DIR/venv/bin/pip" install --upgrade pip
"$CURRENT_DIR/venv/bin/pip" install -r "$CURRENT_DIR/requirements.txt"

# Ajustar permisos para el usuario
chown -R "$APP_USER:$APP_USER" "$CURRENT_DIR"

echo "🛡️  4. Configurando puertos (5000 Web, 1935 RTMP) en el Firewall (UFW)..."
if command -v ufw >/dev/null 2>&1; then
    ufw allow 5000/tcp comment 'Panel de Streaming 24/7' || true
    ufw allow 1935/tcp comment 'RTMP Streaming Celular' || true
fi

echo "⚙️  5. Creando servicio automático en segundo plano (Systemd 24/7)..."
SERVICE_FILE="/etc/systemd/system/panel_stream.service"

cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=Panel de Control Streaming YouTube 24/7
After=network.target

[Service]
Type=simple
User=$APP_USER
WorkingDirectory=$CURRENT_DIR
ExecStart=$CURRENT_DIR/venv/bin/python3 $CURRENT_DIR/app.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable panel_stream.service
systemctl restart panel_stream.service

# Obtener IP Pública
PUBLIC_IP=$(curl -s https://api.ipify.org || curl -s https://ifconfig.me || echo "TU_IP_DEL_SERVIDOR")

echo ""
echo "=================================================================="
echo "  🎉 ¡INSTALACIÓN COMPLETADA CON ÉXITO!"
echo "=================================================================="
echo ""
echo "  El panel ya está corriendo 24/7 en segundo plano y se reiniciará"
echo "  automáticamente si el servidor se apaga o reinicia."
echo ""
echo "  👉 Accede desde cualquier navegador (PC o celular):"
echo "     http://${PUBLIC_IP}:5000"
echo ""
echo "  Comandos útiles para gestionar tu panel:"
echo "  - Ver estado del servicio: sudo systemctl status panel_stream"
echo "  - Ver logs en vivo:        sudo journalctl -u panel_stream -f"
echo "  - Reiniciar panel:         sudo systemctl restart panel_stream"
echo "  - Detener panel:           sudo systemctl stop panel_stream"
echo ""
echo "=================================================================="
