import urllib.request, json, sys

sys.stdout.reconfigure(encoding='utf-8')

def test_post(name, endpoint, payload):
    try:
        url = f"http://localhost:5000{endpoint}"
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            res_json = json.loads(resp.read().decode('utf-8'))
            print(f"✅ {name} ({endpoint}): HTTP {resp.status} -> {res_json.get('success', res_json)}")
            return res_json
    except Exception as e:
        print(f"❌ {name} ({endpoint}): ERROR -> {e}")
        return None

print("=== VERIFICANDO ENDPOINTS DE CONTROL Y TRANSMISIÓN ===")
# 1. Test Theme
test_post("Cambiar Tema", "/api/theme", {"theme": "cyber_dark"})

# 2. Test Control (skip, format, keys)
test_post("Control (Actualizar Estado)", "/api/control", {
    "platform": "youtube",
    "stream_format": "vertical",
    "stream_key": "du9h-3ajm-9e6b-gj2c-5emj"
})

# 3. Test Overlay Config
test_post("Configurar Overlays", "/api/overlay/config", {
    "overlays": [
        {
            "id": "live_badge",
            "type": "badge",
            "text": "EN DIRECTO 🔴",
            "x": 25, "y": 25, "width": 150, "height": 42,
            "fontSize": 15, "color": "#ffffff", "bg": "rgba(220, 38, 38, 0.95)",
            "opacity": 0.95, "rotation": 0, "visible": True
        },
        {
            "id": "rotulo_en_vivo",
            "type": "rotulo",
            "text": "🔥 ¡EN VIVO AHORA! Suscríbete y Comenta 🚀",
            "x": 7, "y": 330, "width": 227, "height": 42,
            "fontSize": 16, "color": "#ffffff", "bg": "rgba(15, 23, 42, 0.92)",
            "opacity": 0.92, "rotation": 0, "visible": True
        }
    ],
    "preview_width": 238.0,
    "preview_height": 378.0
})

# 4. Test Chat Send
test_post("Enviar Mensaje Chat", "/api/chat/send", {
    "platform": "youtube",
    "message": "Hola a todos desde StreamHub Studio"
})

# 5. Test Chat Connect
test_post("Conectar Chat", "/api/chat/connect", {
    "youtube_video_id": "test_video_id",
    "facebook_live_id": ""
})

# 6. Test Connection
test_post("Probar Conexión Plataforma", "/api/test_connection", {
    "platform": "youtube",
    "key": "du9h-3ajm-9e6b-gj2c-5emj"
})

# 7. Test Monetization
test_post("Guardar Meta Monetización", "/api/monetization", {
    "goal": 4000.0,
    "unit": "minutos"
})
