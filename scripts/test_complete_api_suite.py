import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')

panel_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream"
if panel_path not in sys.path:
    sys.path.insert(0, panel_path)

from app import app

client = app.test_client()

print("=== 1. VERIFICANDO RUTAS BÁSICAS GET ===")
for ep in ['/', '/control', '/api/status', '/api/stickers', '/api/recordings', '/api/playlists', '/api/history', '/api/library/tree']:
    res = client.get(ep)
    print(f"GET {ep:25}: Status {res.status_code}")
    assert res.status_code == 200

print("\n=== 2. VERIFICANDO ACCIONES DE CONTROL POST /api/control ===")
control_tests = [
    {"action": "start", "platform": "youtube", "format": "vertical"},
    {"action": "stop"},
    {"action": "skip"},
    {"action": "switch_format", "format": "horizontal"},
    {"action": "switch_format", "format": "vertical"},
    {"action": "update_banner", "banner_text": "🔴 EN VIVO TEST 24/7"},
    {"action": "set_category", "category": "General"},
    {"action": "toggle_cycle_mode"},
    {"action": "toggle_mode", "mode": "playlist"},
    {"action": "save_keys", "platform": "youtube", "stream_key": "du9h-3ajm-9e6b-gj2c-5emj"}
]
for payload in control_tests:
    res = client.post('/api/control', json=payload)
    print(f"POST /api/control [{payload['action']:18}]: Status {res.status_code} -> {res.get_json().get('message')}")
    assert res.status_code == 200
    assert res.get_json().get('success') is True

print("\n=== 3. VERIFICANDO THEME POST /api/theme ===")
res_th = client.post('/api/theme', json={'theme': 'twitch_purple'})
print(f"POST /api/theme: Status {res_th.status_code} -> {res_th.get_json()}")
assert res_th.status_code == 200

print("\n=== 4. VERIFICANDO CHAT EN VIVO ===")
res_conn = client.post('/api/chat/connect', json={'youtube_video_id': 'dQw4w9WgXcQ', 'facebook_live_id': ''})
print(f"POST /api/chat/connect: Status {res_conn.status_code} -> {res_conn.get_json()}")
assert res_conn.status_code == 200

res_msg = client.post('/api/chat/send', json={'platform': 'all', 'message': '¡Bienvenidos a la transmisión en vivo!'})
print(f"POST /api/chat/send: Status {res_msg.status_code} -> {res_msg.get_json()}")
assert res_msg.status_code == 200

print("\n=== 5. VERIFICANDO PRUEBA DE CONEXIÓN A PLATAFORMAS ===")
res_test = client.post('/api/test_connection', json={'platform': 'youtube', 'stream_key': 'test-fake-key'})
print(f"POST /api/test_connection: Status {res_test.status_code} -> {res_test.get_json().get('message')}")
assert res_test.status_code == 200

print("\n=== 6. VERIFICANDO GRABACIÓN MAESTRA ===")
res_rec = client.get('/api/recordings')
print(f"GET /api/recordings: Status {res_rec.status_code} -> {res_rec.get_json().get('is_recording')}")
assert res_rec.status_code == 200

print("\n🎉 ¡EL 100% DE LOS ENDPOINTS Y ACCIONES RESPONDIERON CORRECTAMENTE (STATUS 200)! 🎉")
