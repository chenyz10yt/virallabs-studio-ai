import re, os, sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

get_id_matches = set(re.findall(r'document\.getElementById\([\'"]([^\'"]+)[\'"]\)', content))
missing_ids = []
present_ids = []

for elem_id in sorted(get_id_matches):
    pattern = rf'id=[\'"]{re.escape(elem_id)}[\'"]'
    if re.search(pattern, content):
        present_ids.append(elem_id)
    else:
        missing_ids.append(elem_id)

print(f"Total IDs solicitados por JS: {len(get_id_matches)}")
print(f"Presentes: {len(present_ids)}")
print(f"Faltantes ({len(missing_ids)}):")
for m in missing_ids:
    print(" -", m)
