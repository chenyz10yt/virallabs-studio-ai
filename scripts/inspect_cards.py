import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\Admin\Desktop\chenyz.app\web y app\index.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, l in enumerate(lines[850:1320]):
    line_no = 851 + idx
    s = l.strip()
    if 'TARJETA' in s or 'class="grid"' in s or 'class="col' in s or 'card-title' in s or 'ffmpeg' in s.lower() or 'playlist' in s.lower():
        print(f'{line_no}: {s[:90]}')



