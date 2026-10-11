import os

p_root = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\index.html"
p_tpl = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\templates\index.html"

print("root index exists:", os.path.exists(p_root), "size:", os.path.getsize(p_root) if os.path.exists(p_root) else 0)
print("tpl index exists:", os.path.exists(p_tpl), "size:", os.path.getsize(p_tpl) if os.path.exists(p_tpl) else 0)

with open(p_tpl, 'r', encoding='utf-8') as f:
    tpl_text = f.read()

print("tpl has STREAMHUB:", "STREAMHUB 24/7 STUDIO" in tpl_text)
print("tpl has switchOverlaySubTab:", "switchOverlaySubTab" in tpl_text)
