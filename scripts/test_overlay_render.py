import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import render_composite_overlay, SERVER_STATE, OVERLAY_IMAGE_FILE
from PIL import Image

print("--- TEST DE RENDERIZADO COMPOSITE OVERLAY MULTIEJE LIBRE ---")

test_overlays = [
    {
        "id": "stk_test_1",
        "type": "sticker",
        "name": "fire.svg",
        "image_url": "/stickers/fire.svg",
        "x": 30,
        "y": 40,
        "width": 100,
        "height": 100,
        "rotation": 45,
        "opacity": 0.85,
        "flip_h": True,
        "flip_v": False,
        "visible": True
    },
    {
        "id": "rot_test_2",
        "type": "rotulo",
        "name": "Rótulo Libre",
        "text": "🔴 TRANSMISIÓN 24/7 EN VIVO",
        "x": 40,
        "y": 200,
        "width": 220,
        "height": 50,
        "rotation": -15,
        "color": "#ffffff",
        "bg": "#ef4444",
        "fontSize": 18,
        "opacity": 0.9,
        "flip_h": False,
        "flip_v": False,
        "visible": True
    },
    {
        "id": "logo_test_3",
        "type": "logo",
        "name": "Logo",
        "image_url": "/logo.png",
        "x": 10,
        "y": 10,
        "width": 60,
        "height": 60,
        "rotation": 0,
        "opacity": 1.0,
        "flip_h": False,
        "flip_v": False,
        "visible": True
    }
]

# Probar en formato vertical (1080x1920)
res_v = render_composite_overlay(test_overlays, stream_format='vertical', preview_width=240, preview_height=380)
print("Vertical render result:", res_v)
if os.path.exists(OVERLAY_IMAGE_FILE):
    im = Image.open(OVERLAY_IMAGE_FILE)
    print(f"Vertical overlay image created successfully: size={im.size}, mode={im.mode}")
    assert im.size == (1080, 1920), "Size mismatch for vertical"

# Probar en formato horizontal (1920x1080)
res_h = render_composite_overlay(test_overlays, stream_format='horizontal', preview_width=420, preview_height=240)
print("Horizontal render result:", res_h)
if os.path.exists(OVERLAY_IMAGE_FILE):
    im = Image.open(OVERLAY_IMAGE_FILE)
    print(f"Horizontal overlay image created successfully: size={im.size}, mode={im.mode}")
    assert im.size == (1920, 1080), "Size mismatch for horizontal"

print("✅ TODOS LOS TESTS DE RENDERIZADO LIBRE MULTIEJE PASARON CON ÉXITO!")
