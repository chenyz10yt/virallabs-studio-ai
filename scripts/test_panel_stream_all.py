import os, sys, json, io, shutil

panel_dir = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream"
sys.path.insert(0, panel_dir)

import app as ps_app

client = ps_app.app.test_client()
print("Initialized Flask test_client for panel_stream app")

# TEST 1: Logo route
print("\n--- TEST 1: Logo Naranja ---")
res = client.get('/logo.png')
print("Status code for /logo.png:", res.status_code)
assert res.status_code == 200, "Failed to serve /logo.png"
print("Logo content length:", len(res.data), "bytes")
assert len(res.data) > 1000, "Logo data too small"
print("✅ Test 1 Passed: Logo servido correctamente con HTTP 200.")

# TEST 2: Stickers List
print("\n--- TEST 2: Listado de Stickers del Proyecto ---")
res = client.get('/api/stickers')
assert res.status_code == 200
data = json.loads(res.data.decode('utf-8'))
stickers = data.get('stickers', [])
print(f"Total stickers encontrados en el proyecto: {len(stickers)}")
stk_names = [s['name'] for s in stickers]
print("Ejemplos de stickers disponibles:", stk_names[:5])
assert len(stickers) > 0, "No stickers found"
assert any('logo' in s['name'].lower() or 'logo' in s['filename'].lower() for s in stickers), "Logo sticker missing in gallery"
print("✅ Test 2 Passed: Stickers y logo listados y disponibles en el proyecto.")

# TEST 3: Upload Sticker / Logo
print("\n--- TEST 3: Subida de Sticker / Logo Personalizado ---")
test_file_bytes = io.BytesIO(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x19IDATx\x9cc\xfc\xff\xff?\x03\x10\x04\x00\x00\xff\xff\x03\x00\x08\xfc\x02\xfe\xa7\x9d\x01\x12\x00\x00\x00\x00IEND\xaeB`\x82')
res = client.post('/api/overlay/upload_image', data={'image_file': (test_file_bytes, 'test_sticker_unit.png')}, content_type='multipart/form-data')
assert res.status_code == 200
up_data = json.loads(res.data.decode('utf-8'))
print("Upload response:", up_data)
assert up_data.get('success') is True
uploaded_filename = up_data.get('filename')
print("Uploaded sticker filename:", uploaded_filename)
print("✅ Test 3 Passed: Sticker subido y guardado en uploads/stickers/ con éxito.")

# TEST 4: Overlay Config & Pillow Renderer
print("\n--- TEST 4: Guardado de Stickers/Rótulos y Renderizado de stream_overlay.png ---")
test_overlays = [
    {
        "id": "stk_test_1",
        "type": "sticker",
        "text": "Sticker Test",
        "image_url": f"/stickers/{uploaded_filename}",
        "x": 60,
        "y": 100,
        "width": 80,
        "height": 80,
        "rotation": 0,
        "visible": True
    },
    {
        "id": "rotulo_test_1",
        "type": "rotulo",
        "text": "Transmisión en Vivo 24/7 🔥",
        "x": 30,
        "y": 200,
        "width": 260,
        "height": 50,
        "rotation": 0,
        "fontSize": 16,
        "color": "#ffffff",
        "bg": "rgba(15, 23, 42, 0.9)",
        "opacity": 0.9,
        "visible": True
    }
]

res = client.post('/api/overlay/config', json={'overlays': test_overlays, 'preview_width': 240, 'preview_height': 380})
assert res.status_code == 200
ov_res = json.loads(res.data.decode('utf-8'))
print("Overlay save response:", ov_res)
assert ov_res.get('success') is True

overlay_img_path = ps_app.OVERLAY_IMAGE_FILE
assert os.path.exists(overlay_img_path), "stream_overlay.png was not generated"
ov_size = os.path.getsize(overlay_img_path)
print("Generated stream_overlay.png size:", ov_size, "bytes")
assert ov_size > 1000, "stream_overlay.png is empty or too small"

# Verificar GET /api/overlay/config
res_get = client.get('/api/overlay/config')
assert res_get.status_code == 200
get_data = json.loads(res_get.data.decode('utf-8'))
assert len(get_data.get('overlays', [])) == 2
print("✅ Test 4 Passed: Configuración guardada y stream_overlay.png generado automáticamente por Pillow.")

# TEST 5: Recordings API & Compilation
print("\n--- TEST 5: Grabador Maestro de Transmisión & Descarga ---")
# Simular una sesión de grabación con 2 fragmentos .ts
test_session_id = "test_unit_session"
test_sess_dir = os.path.join(ps_app.RECORDINGS_FOLDER, test_session_id)
os.makedirs(test_sess_dir, exist_ok=True)

# Crear 2 fragmentos sintéticos de MPEG-TS para verificar concat
vid_sample = os.path.join(ps_app.UPLOAD_FOLDER, 'General', '1000002310.mp4')
import subprocess
for idx in [1, 2]:
    chunk_file = os.path.join(test_sess_dir, f"chunk_{idx:04d}.ts")
    esc = chunk_file.replace('\\', '/').replace(':', r'\:')
    cmd = [
        'ffmpeg', '-y', '-ss', str(idx), '-t', '1',
        '-i', vid_sample,
        '-map', '0:v', '-map', '0:a?',
        '-c:v', 'libx264', '-preset', 'ultrafast',
        '-c:a', 'aac',
        '-f', 'tee', f'[f=mpegts:onfail=ignore]{esc}'
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

ts_in_dir = [f for f in os.listdir(test_sess_dir) if f.endswith('.ts')]
print(f"Fragmentos .ts generados en {test_session_id}: {ts_in_dir}")
assert len(ts_in_dir) == 2, "Failed to create test ts chunks"

# Probar compilación del video maestro
ps_app.CURRENT_RECORDING_SESSION = test_session_id
ps_app.SERVER_STATE['status'] = 'Detenido'

res_compile = client.post('/api/recordings/compile')
assert res_compile.status_code == 200
comp_data = json.loads(res_compile.data.decode('utf-8'))
print("Compilation API response:", comp_data)
assert comp_data.get('success') is True
merged_fn = comp_data.get('filename')
print("Compiled video file:", merged_fn)

# Verificar GET /api/recordings
res_list = client.get('/api/recordings')
assert res_list.status_code == 200
list_data = json.loads(res_list.data.decode('utf-8'))
print("Recordings list response:", list_data)
assert any(r['filename'] == merged_fn for r in list_data.get('recordings', [])), "Compiled recording not found in recordings list"

# Verificar descarga del MP4
res_dl = client.get(f'/recordings/download/{merged_fn}')
assert res_dl.status_code == 200
print("Downloaded MP4 size:", len(res_dl.data), "bytes")
assert len(res_dl.data) > 100000, "Downloaded MP4 file too small"
res_dl.close()
import gc
gc.collect()

# Verificar eliminación de la grabación
res_del = client.post(f'/api/recordings/delete/{merged_fn}')
assert res_del.status_code == 200
del_data = json.loads(res_del.data.decode('utf-8'))
assert del_data.get('success') is True
print("Delete response:", del_data)
assert not os.path.exists(os.path.join(ps_app.RECORDINGS_FOLDER, merged_fn)), "File was not deleted"
print("✅ Test 5 Passed: Grabación, compilación rápida en 1 solo MP4, descarga y borrado funcionan al 100%.")

# TEST 6: Limpieza de sticker de prueba
res_del_stk = client.post(f'/api/stickers/delete/{uploaded_filename}')
assert res_del_stk.status_code == 200
# Limpiar carpeta de sesión de prueba
shutil.rmtree(test_sess_dir, ignore_errors=True)
print("✅ Test 6 Passed: Limpieza de archivos de prueba completada.")

print("\n=======================================================")
print("  TODAS LAS PRUEBAS UNITARIAS Y DE INTEGRACIÓN PASARON")
print("=======================================================")
