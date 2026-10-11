import re

with open(r'C:\Users\Admin\Desktop\chenyz.app\panel_stream\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find('<script>')
script_content = text[s:]

functions = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', script_content)
print(f"Total functions in script: {len(functions)}")
for i, fn in enumerate(functions):
    print(f"{i+1}. {fn}")
