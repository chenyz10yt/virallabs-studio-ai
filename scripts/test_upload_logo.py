import urllib.request, io, json
from PIL import Image

dummy = Image.new('RGBA', (120, 120), (56, 189, 248, 240))
buf = io.BytesIO()
dummy.save(buf, 'PNG')
img_bytes = buf.getvalue()

boundary = 'boundary123456789'
body = bytearray()
body.extend(b'--boundary123456789\r\n')
body.extend(b'Content-Disposition: form-data; name="image_file"; filename="mi_logo_canal.png"\r\n')
body.extend(b'Content-Type: image/png\r\n\r\n')
body.extend(img_bytes)
body.extend(b'\r\n--boundary123456789--\r\n')

req = urllib.request.Request(
    'http://localhost:5000/api/overlay/upload_image',
    data=bytes(body),
    headers={'Content-Type': 'multipart/form-data; boundary=boundary123456789'}
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print('Upload result:', data)
