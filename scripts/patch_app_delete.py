import os, sys, re, time
sys.stdout.reconfigure(encoding='utf-8')


app_path = r'c:\Users\Admin\Desktop\chenyz.app\panel_stream\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r"@app\.route\('/api/recordings/delete/<filename>', methods=\['POST'\]\)[\s\S]*?return jsonify\(\{'success': False\}\), 404"

replacement = """@app.route('/api/recordings/delete/<filename>', methods=['POST'])
def api_delete_recording(filename):
    file_path = os.path.join(RECORDINGS_FOLDER, filename)
    if os.path.exists(file_path):
        import gc
        last_err = None
        for attempt in range(5):
            try:
                gc.collect()
                os.remove(file_path)
                log_event_history('RECORDING_DELETE', f"Grabación eliminada: {filename}")
                return jsonify({'success': True})
            except Exception as e:
                last_err = e
                time.sleep(0.15)
        return jsonify({'success': False, 'message': str(last_err)}), 500
    return jsonify({'success': False}), 404"""

new_code = re.sub(pattern, replacement, code, count=1)
if new_code != code:
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(new_code)
    print("✅ Patch applied successfully to panel_stream/app.py")
else:
    print("❌ Pattern not matched")
