import urllib.request, json

# 1. Fetch current overlays
with urllib.request.urlopen('http://localhost:5000/api/status') as resp:
    state = json.loads(resp.read().decode('utf-8'))
    ovs = state.get('overlays', [])

# 2. Add uploaded logo
ovs.append({
    'id': 'logo_test_1',
    'type': 'image',
    'text': 'Mi Logo Personalizado',
    'image_url': '/stickers/custom_1791493497325.png',
    'x': 50,
    'y': 240,
    'width': 120,
    'height': 120,
    'rotation': 15,
    'visible': True
})

req = urllib.request.Request(
    'http://localhost:5000/api/overlay/config',
    data=json.dumps({'overlays': ovs, 'preview_width': 320.0, 'preview_height': 500.0}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print('Add logo response success:', data.get('success'))
