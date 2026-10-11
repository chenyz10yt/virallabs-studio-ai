import os, sys

sys.stdout.reconfigure(encoding='utf-8')

app_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\app.py"
with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

print("Contains RECORDINGS_FOLDER:", "RECORDINGS_FOLDER" in code)
print("Contains compile_recording_session:", "compile_recording_session" in code)
print("Contains /api/recordings:", "/api/recordings" in code)
print("Contains CURRENT_RECORDING_SESSION:", "CURRENT_RECORDING_SESSION" in code)

# Let's search where /api/recordings is defined if present
for i, line in enumerate(code.splitlines()):
    if 'recordings' in line.lower() or 'compile' in line.lower():
        print(f"Line {i+1}: {line.strip()[:90]}")
