import os, shutil

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dst_dir = os.path.abspath(os.path.join(src_dir, '..', 'panel_stream'))

print(f"Fuente (web y app): {src_dir}")
print(f"Destino (panel_stream): {dst_dir}")

# Archivos principales a sincronizar hacia panel_stream
files_to_sync = [
    'app.py',
    'index.html',
    'control.html',
    'templates/index.html',
    'templates/control.html',
    'Iniciar_Servidor.bat',
    'Iniciar_Transmision_Automatica_YouTube.bat'
]

for fname in files_to_sync:
    src_file = os.path.join(src_dir, fname)
    if os.path.exists(src_file):
        dst_file = os.path.join(dst_dir, fname)
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        shutil.copy2(src_file, dst_file)
        print(f"Copied {fname} -> {dst_file}")

# Listar todos los archivos clave en panel_stream
print("\n--- ARCHIVOS CLAVE EN C:\\Users\\Admin\\Desktop\\chenyz.app\\panel_stream ---")
for root, dirs, files in os.walk(dst_dir):
    rel = os.path.relpath(root, dst_dir)
    if rel in ('.', 'templates', 'uploads', 'uploads\\stickers'):
        for f in files:
            if f.endswith(('.bat', '.py', '.html', '.json', '.txt', '.svg')):
                p = os.path.join(root, f)
                s = os.path.getsize(p)
                print(f"  [{rel}] {f} ({s} bytes)")
