import re, sys

sys.stdout.reconfigure(encoding='utf-8')

ctrl_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\templates\control.html"
with open(ctrl_path, "r", encoding="utf-8") as f:
    html = f.read()

print("Control.html size:", len(html))

print("Control.html size:", len(html))

for m in re.finditer(r'<h[1-4][^>]*>(.*?)</h[1-4]>|<!--\s*([A-Z0-9_\s:\-]+)\s*-->', html):
    txt = m.group(1) or m.group(2)
    clean = re.sub(r'<[^>]+>', '', txt).strip()
    print("Section:", clean)



# Check script in control.html
script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if script_match:
    js = script_match.group(1)
    func_defs = set(re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', js))
    var_funcs = set(re.findall(r'(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*(?:function|\([^)]*\)\s*=>)', js))
    window_funcs = set(re.findall(r'window\.([a-zA-Z0-9_$]+)\s*=', js))
    all_funcs = func_defs | var_funcs | window_funcs
    print(f"Control.html defined functions: {len(all_funcs)}")
    
    handlers = re.findall(r'on(?:click|change|input|submit|mouseover|keyup|keydown)\s*=\s*["\']([^"\']+)["\']', html)
    called = set()
    for h in handlers:
        calls = re.findall(r'([a-zA-Z0-9_$]+)\s*\(', h)
        for c in calls:
            called.add(c)
    
    missing = [c for c in sorted(called) if c not in all_funcs and c not in ['alert', 'confirm', 'prompt', 'parseInt', 'parseFloat', 'showToast']]
    if missing:
        print("Control.html missing functions:", missing)
    else:
        print("✅ Control.html: All inline handler functions are defined!")

# Check getElementById in control.html
get_ids = set(re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)', html))
missing_ids = []
for gid in sorted(get_ids):
    if not re.search(rf'id=["\']{re.escape(gid)}["\']', html):
        missing_ids.append(gid)

if missing_ids:
    print(f"Control.html missing DOM IDs ({len(missing_ids)}):", missing_ids)
else:
    print("✅ Control.html: 100% of DOM IDs requested in JS exist in HTML!")

