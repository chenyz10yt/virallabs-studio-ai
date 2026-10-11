import os, sys, json, subprocess
sys.stdout.reconfigure(encoding='utf-8')

panel_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream"
if panel_path not in sys.path:
    sys.path.insert(0, panel_path)

import app as stream_app
from app import app, RECORDINGS_FOLDER, compile_recording_session

client = app.test_client()

print("=== LIFECYCLE TEST: GENERACIÓN DE FRAGMENTOS Y COMPILACIÓN ===")

# Create a test session
test_session_id = "test_20261009_120000"
test_session_dir = os.path.join(RECORDINGS_FOLDER, test_session_id)
os.makedirs(test_session_dir, exist_ok=True)

# Generate a small 1-second .ts video chunk using lavfi and ffmpeg
test_ts_file = os.path.join(test_session_dir, "chunk_0001.ts")
cmd = [
    'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=640x360:r=30',
    '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
    '-t', '1',
    '-c:v', 'libx264', '-preset', 'ultrafast',
    '-c:a', 'aac',
    '-f', 'mpegts', test_ts_file
]
p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if p.returncode == 0 and os.path.exists(test_ts_file):
    print("✅ Fragmento .ts de prueba generado con éxito")
else:
    print("⚠️ No se pudo generar fragmento con ffmpeg:", p.stderr.decode('utf-8', errors='ignore')[:200])

# Set active session
stream_app.CURRENT_RECORDING_SESSION = test_session_id

# Test compile
print("\n--- Compilando sesión vía API ---")
res = client.post('/api/recordings/compile')
print("Status:", res.status_code)
comp_data = res.get_json()
print("Data:", comp_data)
assert res.status_code == 200
assert comp_data.get('success') is True
output_filename = comp_data.get('filename')
print(f"✅ Video compilado con éxito: {output_filename}")

# Test listing
print("\n--- Verificando lista de grabaciones ---")
res_list = client.get('/api/recordings')
list_data = res_list.get_json()
print("Grabaciones encontradas:", len(list_data.get('recordings', [])))
assert any(r['filename'] == output_filename for r in list_data.get('recordings', []))
print("✅ Grabación visible en /api/recordings")

# Test download route
print("\n--- Verificando descarga del video ---")
res_dl = client.get(f'/recordings/download/{output_filename}')
print(f"Status descarga: {res_dl.status_code}, Bytes recibidos: {len(res_dl.data)}")
assert res_dl.status_code == 200
assert len(res_dl.data) > 0
res_dl.close()
print("✅ Descarga de video MP4 exitosa")

# Test deletion route
print("\n--- Eliminando archivo de prueba ---")
res_del = client.post(f'/api/recordings/delete/{output_filename}')
print("Status eliminación:", res_del.status_code)
assert res_del.status_code == 200
assert not os.path.exists(os.path.join(RECORDINGS_FOLDER, output_filename))
print("✅ Grabación eliminada correctamente")

# Clean up test session directory
shutil_rm = False
try:
    import shutil
    shutil.rmtree(test_session_dir, ignore_errors=True)
    shutil_rm = True
except Exception: pass
print(f"Carpeta temporal de prueba limpiada: {shutil_rm}")

stream_app.CURRENT_RECORDING_SESSION = None

print("\n🎉 ¡LIFECYCLE DE GRABACIÓN MAESTRA VERIFICADO AL 100% CON ÉXITO TOTAL!")
