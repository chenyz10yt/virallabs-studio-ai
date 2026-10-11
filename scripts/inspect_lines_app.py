import os, sys

sys.stdout.reconfigure(encoding='utf-8')

app_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\app.py"
with open(app_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for j in range(880, 920):
    print(f"{j+1:3d}: {lines[j].rstrip()}")
