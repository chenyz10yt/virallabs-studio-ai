import urllib.request

req = urllib.request.Request("http://localhost:5000/control", headers={"Cache-Control": "no-cache"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')
    print("Control fetched size:", len(html))
    print("Has StreamHub:", "StreamHub" in html)
    print("Has theme-select-m:", "theme-select-m" in html)
