import urllib.request

req = urllib.request.Request("http://localhost:5000/", headers={"Cache-Control": "no-cache", "Pragma": "no-cache"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')
    print("Fetched size:", len(html))
    print("Has STREAMHUB 24/7 STUDIO:", "STREAMHUB 24/7 STUDIO" in html)
    print("Has switchOverlaySubTab:", "switchOverlaySubTab" in html)
