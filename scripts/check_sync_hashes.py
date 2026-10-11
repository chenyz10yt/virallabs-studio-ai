import os, hashlib

def get_hash(path):
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

files_to_check = [
    ("panel_stream/index.html", r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\index.html"),
    ("panel_stream/templates/index.html", r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\templates\index.html"),
    ("web y app/index.html", r"c:\Users\Admin\Desktop\chenyz.app\web y app\index.html"),
    ("panel_stream/templates/control.html", r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\templates\control.html"),
    ("web y app/control.html", r"c:\Users\Admin\Desktop\chenyz.app\web y app\control.html"),
]

for label, p in files_to_check:
    h = get_hash(p)
    size = os.path.getsize(p) if os.path.exists(p) else 0
    print(f"{label}: size={size}, md5={h}")
