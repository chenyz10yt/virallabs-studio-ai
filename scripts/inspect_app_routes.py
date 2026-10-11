import os

app_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\app.py"
with open(app_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if any(k in line for k in ['def index', 'route("/")', "route('/')", 'template_folder', 'render_template', 'send_from_directory']):
        print(f"Line {idx+1}: {line.strip()}")
