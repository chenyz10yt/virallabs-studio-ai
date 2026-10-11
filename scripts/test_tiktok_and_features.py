import sys, os, json

sys.path.insert(0, "c:/Users/Admin/Desktop/chenyz.app/panel_stream")
import app

client = app.app.test_client()

print("\n--- TEST 1: Estado del Servidor & Control URL ---")
resp = client.get('/api/status')
assert resp.status_code == 200, f"Error {resp.status_code}"
data = resp.get_json()
print("control_url:", data.get('control_url'))
print("available_ips:", data.get('available_ips'))
assert data.get('control_url') == 'http://172.64.219:5000/control', "control_url mismatch"
print("tiktok_server en estado:", data.get('tiktok_server'))
print("✅ Test 1 Passed: control_url configurado con 'http://172.64.219:5000/control'")

print("\n--- TEST 2: Logo Naranja Original & Nombre ---")
resp_logo = client.get('/logo.png')
assert resp_logo.status_code == 200, f"Error logo: {resp_logo.status_code}"
assert len(resp_logo.data) > 10000, "Logo data too small"
print(f"Logo servido: {len(resp_logo.data)} bytes")
print("✅ Test 2 Passed: Logo naranja original servido correctamente con HTTP 200")

print("\n--- TEST 3: Stickers por Nichos ---")
resp_stk = client.get('/api/stickers')
assert resp_stk.status_code == 200
stk_data = resp_stk.get_json().get('stickers', [])
print(f"Total stickers en el proyecto: {len(stk_data)}")
sample_names = [s['name'] for s in stk_data[:8]]
print("Ejemplos de stickers:", sample_names)
assert len(stk_data) >= 20, "Faltan stickers en el proyecto"
print("✅ Test 3 Passed: Stickers por nichos disponibles y listados")

print("\n--- TEST 4: Configuración y Guardado de TikTok ---")
save_payload = {
    'action': 'save_keys',
    'platform': 'tiktok',
    'tiktok_key': 'stream-test-tiktok-key-12345',
    'tiktok_server': 'rtmp://push-rtmp-l01-va.tiktokcdn.com/live/',
    'control_url': 'http://172.64.219:5000/control'
}
resp_save = client.post('/api/control', json=save_payload)
assert resp_save.status_code == 200
status_after = client.get('/api/status').get_json()
assert status_after.get('tiktok_key') == 'stream-test-tiktok-key-12345', "tiktok_key not saved"
print("tiktok_key guardada correctamente:", status_after.get('tiktok_key'))
print("✅ Test 4 Passed: TikTok integrado y persistido en el servidor")

print("\n--- TEST 5: Previsualización de Overlay Transparente ---")
resp_ov = client.get('/stream_overlay.png')
assert resp_ov.status_code == 200
print(f"stream_overlay.png servido: {len(resp_ov.data)} bytes")
print("✅ Test 5 Passed: stream_overlay.png accesible en tiempo real")

print("\n--- TEST 6: Rutas HTML / y /control ---")
resp_index = client.get('/')
assert resp_index.status_code == 200
assert 'StreamHub 24/7 Studio' in resp_index.get_data(as_text=True)
assert '172.64.219:5000' in resp_index.get_data(as_text=True)
assert 'panelTiktok' in resp_index.get_data(as_text=True)

resp_ctrl = client.get('/control')
assert resp_ctrl.status_code == 200
assert 'StreamHub Mando' in resp_ctrl.get_data(as_text=True)
assert '172.64.219:5000' in resp_ctrl.get_data(as_text=True)
print("✅ Test 6 Passed: Ambas vistas HTML / y /control cargan con éxito e incluyen la URL solicitada")

print("\n=======================================================")
print("  TODAS LAS PRUEBAS DE TIKTOK, IP Y STICKERS PASARON")
print("=======================================================\n")
