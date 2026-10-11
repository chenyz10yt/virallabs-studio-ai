import sys, re

sys.stdout.reconfigure(encoding='utf-8')

for label, p in [
    ('index.html', r'c:\Users\Admin\Desktop\chenyz.app\web y app\index.html'),
    ('control.html', r'c:\Users\Admin\Desktop\chenyz.app\web y app\control.html')
]:
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Match action in JSON
    actions_json = set(re.findall(r'[\'"]action[\'"]\s*:\s*[\'"]([^\'"]+)[\'"]', text))
    # Match apiCall('...') or apiCall("...")
    actions_call = set(re.findall(r'apiCall\([\'"]([^\'"]+)[\'"]', text))
    
    all_actions = actions_json | actions_call
    print(f"=== {label} Actions ({len(all_actions)}) ===")
    for a in sorted(all_actions):
        print(f"  - {a}")
