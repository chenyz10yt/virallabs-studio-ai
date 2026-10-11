import re, sys, os

sys.stdout.reconfigure(encoding='utf-8')

for label, p in [
    ("panel_stream/templates/index.html", r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\templates\index.html"),
    ("panel_stream/index.html", r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\index.html"),
    ("web y app/index.html", r"C:\Users\Admin\Desktop\chenyz.app\web y app\index.html"),
]:
    if not os.path.exists(p):
        print(f"{label}: NOT FOUND")
        continue
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()
    print(f"=== {label} (size: {len(html)} chars) ===")
    titles = re.findall(r'<div class="card-title">(.*?)</div>', html, re.DOTALL)
    print(f"Total card-titles: {len(titles)}")
    for i, t in enumerate(titles):
        clean_t = re.sub(r'<[^>]+>', '', t).strip().replace('\n', ' ')
        clean_t = ' '.join(clean_t.split())
        print(f"  Card {i+1}: {clean_t[:65]}")

