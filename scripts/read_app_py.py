import os, sys

sys.stdout.reconfigure(encoding='utf-8')

app_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\app.py"
with open(app_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"app.py has {len(lines)} lines")
for i, l in enumerate(lines[:60]):
    print(f"{i+1:3d}: {l.rstrip()}")
