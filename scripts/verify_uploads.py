import os

base_uploads = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\uploads"
categories = ["General", "Oracion", "Reflexion", "Musica", "Lofi_Chill"]

print("=== VERIFICACION DE VIDEOS Y LISTAS ===")
for cat in categories:
    cat_dir = os.path.join(base_uploads, cat)
    if os.path.exists(cat_dir):
        files = os.listdir(cat_dir)
        print(f"Lista '{cat}': {len(files)} videos presentes")
    else:
        print(f"Lista '{cat}': No existe el directorio")
