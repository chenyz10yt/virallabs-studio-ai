import re, sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\templates\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

targets = ['autoSaveBannerText', 'popoutChat']

for idx, line in enumerate(lines):
    for t in targets:
        if t in line:
            print(f"Line {idx+1} [{t}]: {line.strip()}")

