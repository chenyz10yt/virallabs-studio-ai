import os, sys

sys.stdout.reconfigure(encoding='utf-8')

app_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\app.py"
with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

lines = code.splitlines()

def print_section(start_kw, end_kw=None, num_lines=35):
    for i, l in enumerate(lines):
        if start_kw in l:
            print(f"=== FOUND {start_kw} at line {i+1} ===")
            for j in range(i, min(len(lines), i + num_lines)):
                print(f"{j+1:3d}: {lines[j]}")
            print("="*40)
            break

print_section("def api_control():")
print_section("def handle_control_action(")
print_section("def api_chat_send():")
print_section("def api_test_connection():")
