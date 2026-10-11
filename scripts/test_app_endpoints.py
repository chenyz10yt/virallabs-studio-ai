import re, urllib.request, json, sys

sys.stdout.reconfigure(encoding='utf-8')

app_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\app.py"
with open(app_path, "r", encoding="utf-8") as f:
    app_code = f.read()

# Extract all routes in app.py
routes = re.findall(r'@app\.route\(["\']([^"\']+)["\'](?:,\s*methods=\[([^\]]+)\])?\)', app_code)
print(f"Total routes defined in app.py: {len(routes)}")
for r, m in routes:
    methods = m.replace('"', '').replace("'", '').strip() if m else 'GET'
    print(f"  {methods:15} {r}")

print("\n=== PROBANDO ENDPOINTS GET ACTIVOS EN http://localhost:5000 ===")
test_get_endpoints = [
    "/",
    "/control",
    "/api/status",
    "/stickers/subscribe.png",
    "/stickers/like.png",
]

for ep in test_get_endpoints:
    try:
        url = f"http://localhost:5000{ep}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            print(f"✅ {ep}: HTTP {resp.status} ({len(data)} bytes)")
    except Exception as e:
        print(f"❌ {ep}: ERROR -> {e}")
