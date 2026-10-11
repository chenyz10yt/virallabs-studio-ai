import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')

panel_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream"
if panel_path not in sys.path:
    sys.path.insert(0, panel_path)

# Import app from panel_stream/app.py
from app import app, RECORDINGS_FOLDER, compile_recording_session

client = app.test_client()

print("=== 1. TEST GET /api/recordings ===")
res = client.get('/api/recordings')
print(f"Status: {res.status_code}")
data = res.get_json()
print("Response JSON:", json.dumps(data, indent=2))
assert res.status_code == 200
assert 'recordings' in data
assert 'active_session' in data
assert 'is_recording' in data
print("✅ GET /api/recordings PASSED")

print("\n=== 2. TEST POST /api/recordings/compile (cuando no hay fragmentos) ===")
res_compile = client.post('/api/recordings/compile')
print(f"Status: {res_compile.status_code}")
compile_data = res_compile.get_json()
print("Response JSON:", compile_data)
# Status will be 400 or 404 because there are no chunks yet, which is expected
assert res_compile.status_code in [400, 404]
print("✅ POST /api/recordings/compile handled properly")

print("\n=== 3. TEST GET / ===")
res_index = client.get('/')
print(f"Status: {res_index.status_code}")
assert res_index.status_code == 200
html_index = res_index.get_data(as_text=True)
for item in ['btnCompileNow', 'recordingLiveStatusBadge', 'recordingsFileList', 'refreshRecordingsList', 'compileAndDownloadMasterRecording']:
    assert item in html_index, f"Falta {item} en /"
print("✅ GET / contains all Master Recording elements!")

print("\n=== 4. TEST GET /control ===")
res_ctrl = client.get('/control')
print(f"Status: {res_ctrl.status_code}")
assert res_ctrl.status_code == 200
html_ctrl = res_ctrl.get_data(as_text=True)
for item in ['btnCompileNow', 'recordingLiveStatusBadge', 'recordingsFileList', 'refreshRecordingsList', 'compileAndDownloadMasterRecording']:
    assert item in html_ctrl, f"Falta {item} en /control"
print("✅ GET /control contains all Master Recording elements!")

print("\n🎉 ¡TODOS LOS TESTS DE GRABACIÓN MAESTRA PASARON EXITOSAMENTE!")
