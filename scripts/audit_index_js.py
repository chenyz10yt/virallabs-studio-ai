import re, sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\templates\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Extract script
script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if not script_match:
    print("ERROR: No script tag found")
    sys.exit(1)
js = script_match.group(1)

# Find all function declarations in JS
func_defs = set(re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', js))
var_funcs = set(re.findall(r'(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*(?:function|\([^)]*\)\s*=>)', js))
window_funcs = set(re.findall(r'window\.([a-zA-Z0-9_$]+)\s*=', js))
all_defined_funcs = func_defs | var_funcs | window_funcs

print(f"Total defined JS functions: {len(all_defined_funcs)}")

# 2. Extract all inline event handlers in HTML
handlers = re.findall(r'on(?:click|change|input|submit|mouseover|keyup|keydown)\s*=\s*["\']([^"\']+)["\']', html)
print(f"Total inline event handlers found: {len(handlers)}")

called_funcs = set()
for h in handlers:
    # Match function calls like foo() or foo(bar)
    calls = re.findall(r'([a-zA-Z0-9_$]+)\s*\(', h)
    for c in calls:
        called_funcs.add(c)

print(f"Unique functions called in HTML inline handlers: {len(called_funcs)}")
missing_funcs = []
for c in sorted(called_funcs):
    if c not in all_defined_funcs and c not in ['alert', 'confirm', 'prompt', 'parseInt', 'parseFloat', 'showToast']:
        missing_funcs.append(c)

if missing_funcs:
    print(f"⚠️ MISSING FUNCTIONS called in HTML ({len(missing_funcs)}):")
    for mf in missing_funcs:
        print(f"   - {mf}")
else:
    print("✅ All inline handler functions are defined in JavaScript!")

# 3. Check all API calls in JavaScript
api_calls = re.findall(r'fetch\s*\(\s*["\']([^"\']+)["\']', js)
api_calls += re.findall(r'fetch\s*\(\s*`([^`]+)`', js)
print(f"\nUnique API endpoints fetched in JS: {len(set(api_calls))}")
for ep in sorted(set(api_calls)):
    print(f"   - {ep}")

