import re, os, json, urllib.request

html_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=== 1. VERIFICACIÓN DE IDs EN EL DOM ===")
# Extract getElementById calls
get_id_matches = set(re.findall(r'document\.getElementById\([\'"]([^\'"]+)[\'"]\)', content))
missing_ids = []
present_ids = []

for elem_id in sorted(get_id_matches):
    # Check if id="elem_id" exists in HTML
    pattern = rf'id=[\'"]{re.escape(elem_id)}[\'"]'
    if re.search(pattern, content):
        present_ids.append(elem_id)
    else:
        missing_ids.append(elem_id)

print(f"Total IDs solicitados por JavaScript: {len(get_id_matches)}")
print(f"IDs encontrados y vinculados en el DOM: {len(present_ids)}")
if missing_ids:
    print(f"⚠️ IDs no encontrados ({len(missing_ids)}): {missing_ids}")
else:
    print("✅ 100% DE LOS IDs REQUERIDOS ESTÁN PRESENTES EN EL DOM!")

print("\n=== 2. VERIFICACIÓN DE SUB-PESTAÑAS ===")
overlay_tabs = ["stickers", "rotulos", "layers"]
for t in overlay_tabs:
    btn = f'data-tab="{t}"' in content
    pane = f'id="overlay_pane_{t}"' in content
    print(f"Sub-pestaña Overlay '{t}': Botón={btn}, Panel={pane}")

comm_tabs = ["chat", "monetization"]
for t in comm_tabs:
    btn = f'data-tab="{t}"' in content
    pane = f'id="community_pane_{t}"' in content
    print(f"Sub-pestaña Comunidad '{t}': Botón={btn}, Panel={pane}")

print("\n=== 3. VERIFICACIÓN DE TEMAS ===")
themes = ["cyber_dark", "twitch_purple", "yt_crimson", "kick_matrix", "oled_black", "sunset_gold", "titanium_light"]
for th in themes:
    css_match = f'[data-theme="{th}"]' in content or th == "cyber_dark"
    opt_match = f'value="{th}"' in content
    print(f"Tema '{th}': CSS={css_match}, Selector Option={opt_match}")

print("\n=== 4. VERIFICACIÓN DE ENDPOINTS DEL SERVIDOR ===")
endpoints = [
    ("GET /", "http://localhost:5000/"),
    ("GET /control", "http://localhost:5000/control"),
    ("GET /api/status", "http://localhost:5000/api/status"),
    ("GET /api/stickers", "http://localhost:5000/api/stickers"),
    ("GET /stickers/subscribe.png", "http://localhost:5000/stickers/subscribe.png")
]

for label, url in endpoints:
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"✅ {label}: HTTP {resp.status}")
    except Exception as e:
        print(f"❌ {label}: ERROR {e}")

print("\n=== 5. VERIFICACIÓN DE ESTRUCTURA Y UNIFORMIDAD ===")
has_card_grid = 'class="grid"' in content
has_left_col = '<!-- TARJETA 1:' in content and '<!-- TARJETA 2:' in content and '<!-- TARJETA 3:' in content
has_right_col = '<!-- TARJETA 4:' in content and '<!-- TARJETA 5:' in content and '<!-- TARJETA 6:' in content
print(f"Grid unificado en 2 columnas: {has_card_grid}")
print(f"Columna Izquierda (3 tarjetas estructuradas): {has_left_col}")
print(f"Columna Derecha (3 tarjetas estructuradas): {has_right_col}")
