import os, sys

sys.stdout.reconfigure(encoding='utf-8')

app_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\app.py"
with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

lines = code.splitlines()

for i, l in enumerate(lines):
    if '/api/chat/send' in l or 'chat/send' in l or 'api_control' in l:
        print(f"Line {i+1}: {l.strip()[:90]}")
        for j in range(max(0, i-2), min(len(lines), i+20)):
            print(f"  {j+1:3d}: {lines[j]}")
        print("="*40)
