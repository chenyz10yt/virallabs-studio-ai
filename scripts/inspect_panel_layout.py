import re

with open(r'C:\Users\Admin\Desktop\chenyz.app\panel_stream\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def safe_p(s):
    return str(s).encode('ascii', 'backslashreplace').decode('ascii')

print("=== GRID / LAYOUT STRUCTURE ===")
for m in re.finditer(r'<div class=["\'](?:grid|card|card-title|header|nav-tabs)["\'][^>]*>', text):
    start = m.start()
    snippet = text[start:start+120].replace('\n', ' ')
    print(safe_p(snippet))

print("\n=== THEMES IN CSS ===")
themes = set(re.findall(r'body\.theme-([a-zA-Z0-9_\-]+)', text))
print('Themes found:', sorted(list(themes)))

print("\n=== MAJOR SECTION HEADINGS ===")
for m in re.finditer(r'<h[1-4][^>]*>(.*?)</h[1-4]>|<div class=["\']card-title["\'][^>]*>(.*?)</div>', text):
    title = m.group(1) or m.group(2)
    clean = re.sub(r'<[^>]+>', '', title).strip()
    if clean:
        print("  -", safe_p(clean))
