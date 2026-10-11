import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

app_path = r'c:\Users\Admin\Desktop\chenyz.app\panel_stream\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Asegurar STICKERS_FOLDER
if 'STICKERS_FOLDER' not in code:
    code = code.replace(
        "RECORDINGS_FOLDER = os.path.join(BASE_DIR, 'recordings')",
        "RECORDINGS_FOLDER = os.path.join(BASE_DIR, 'recordings')\nSTICKERS_FOLDER = os.path.join(UPLOAD_FOLDER, 'stickers')\nos.makedirs(STICKERS_FOLDER, exist_ok=True)"
    )
    print("STICKERS_FOLDER configurado")

# 2. Rutas adicionales de stickers, theme, overlay image upload y chat
extra_routes = '''
# =====================================================================
# RUTAS DE STICKERS, THEMES, IMÁGENES Y CHAT EN VIVO
# =====================================================================
@app.route('/stickers/<path:filename>')
def serve_sticker(filename):
    stickers_dir = os.path.join(UPLOAD_FOLDER, 'stickers')
    os.makedirs(stickers_dir, exist_ok=True)
    return send_from_directory(stickers_dir, filename)

@app.route('/api/stickers', methods=['GET'])
def api_get_stickers():
    stickers_dir = os.path.join(UPLOAD_FOLDER, 'stickers')
    os.makedirs(stickers_dir, exist_ok=True)
    files = []
    for f in sorted(os.listdir(stickers_dir)):
        if f.lower().endswith(('.png', '.svg', '.jpg', '.jpeg', '.webp')):
            files.append({'name': f, 'url': f'/stickers/{f}'})
    return jsonify({'stickers': files})

@app.route('/api/overlay/upload_image', methods=['POST'])
def api_overlay_upload_image():
    f = request.files.get('file') or request.files.get('image')
    if not f or not f.filename:
        return jsonify({'success': False, 'message': 'No se recibió ningún archivo'}), 400
    stickers_dir = os.path.join(UPLOAD_FOLDER, 'stickers')
    os.makedirs(stickers_dir, exist_ok=True)
    safe_name = f"custom_{int(time.time()*1000)}_{os.path.basename(f.filename)}"
    dest = os.path.join(stickers_dir, safe_name)
    f.save(dest)
    log_event(f"🎨 [OVERLAY] Imagen cargada: {safe_name}")
    return jsonify({
        'success': True,
        'filename': safe_name,
        'url': f'/stickers/{safe_name}',
        'message': 'Imagen guardada con éxito'
    })

@app.route('/api/theme', methods=['POST'])
def api_theme():
    body = request.get_json() or {}
    th = body.get('theme', 'cyber_dark')
    SERVER_STATE['theme'] = th
    save_state()
    broadcast_state()
    return jsonify({'success': True, 'theme': th})

PYTCHAT_THREAD = None
PYTCHAT_ACTIVE_ID = None

def pytchat_listener(video_id):
    global PYTCHAT_ACTIVE_ID
    if not HAS_PYTCHAT: return
    try:
        chat = pytchat.create(video_id=video_id)
        while chat.is_alive() and PYTCHAT_ACTIVE_ID == video_id:
            for c in chat.get().sync_items():
                item = {
                    'id': f"yt_{int(time.time()*1000)}_{getattr(c, 'id', '')}",
                    'platform': 'youtube',
                    'author': c.author.name,
                    'message': c.message,
                    'time': time.strftime('%H:%M:%S'),
                    'avatar': getattr(c.author, 'imageUrl', '')
                }
                SERVER_STATE['chat_messages'].append(item)
                if len(SERVER_STATE['chat_messages']) > 150:
                    SERVER_STATE['chat_messages'].pop(0)
                broadcast_chat(item)
            time.sleep(1)
    except Exception as e:
        log_event(f"[CHAT YT] {str(e)}")

@app.route('/api/chat/connect', methods=['POST'])
def api_chat_connect():
    global PYTCHAT_THREAD, PYTCHAT_ACTIVE_ID
    body = request.get_json() or {}
    yt_id = (body.get('youtube_video_id') or '').strip()
    fb_id = (body.get('facebook_live_id') or '').strip()

    if yt_id:
        m = re.search(r'(?:v=|\/live\/|\.be\/)([a-zA-Z0-9_-]{11})', yt_id)
        if m: yt_id = m.group(1)
        SERVER_STATE['youtube_video_id'] = yt_id

    if fb_id:
        SERVER_STATE['facebook_live_id'] = fb_id

    save_state()
    broadcast_state()

    if yt_id and HAS_PYTCHAT and yt_id != PYTCHAT_ACTIVE_ID:
        PYTCHAT_ACTIVE_ID = yt_id
        PYTCHAT_THREAD = threading.Thread(target=pytchat_listener, args=(yt_id,), daemon=True)
        PYTCHAT_THREAD.start()
        log_event(f"💬 [CHAT] Conectado a chat de YouTube ID: {yt_id}")

    return jsonify({'success': True, 'youtube_video_id': yt_id, 'facebook_live_id': fb_id})

@app.route('/api/chat/send', methods=['POST'])
def api_chat_send():
    body = request.get_json() or {}
    plat = body.get('platform', 'all')
    msg = (body.get('message') or '').strip()
    author = body.get('author', '👑 Moderador')
    if not msg:
        return jsonify({'success': False, 'message': 'Mensaje vacío'}), 400

    item = {
        'id': f"mod_{int(time.time()*1000)}",
        'platform': plat,
        'author': author,
        'message': msg,
        'time': time.strftime('%H:%M:%S'),
        'badge': 'MOD',
        'is_mod': True,
        'is_owner': True
    }
    SERVER_STATE['chat_messages'].append(item)
    if len(SERVER_STATE['chat_messages']) > 150:
        SERVER_STATE['chat_messages'].pop(0)
    broadcast_chat(item)
    log_event(f"💬 [{author}] {msg}")
    return jsonify({'success': True, 'item': item})
'''

if '/api/chat/send' not in code:
    code = code.replace(
        "@app.route('/previews/<path:filename>')",
        extra_routes + "\n@app.route('/previews/<path:filename>')"
    )
    print("Rutas añadidas: /stickers, /api/stickers, /api/overlay/upload_image, /api/theme, /api/chat/connect, /api/chat/send")

# 3. Mejorar handle_control_action para soportar set_category, toggle_cycle_mode, set_playlist, toggle_mode
extra_actions = '''    elif act == 'set_category':
        cat = body.get('category', 'General')
        SERVER_STATE['active_category'] = cat
        save_state()
        broadcast_state()
        log_event_history('CAT_SWITCH', f"Categoría activa: {cat}")
        return {'success': True, 'message': f'Categoría: {cat}'}

    elif act == 'toggle_cycle_mode':
        SERVER_STATE['youtube_cycle_mode'] = not SERVER_STATE.get('youtube_cycle_mode', True)
        save_state()
        broadcast_state()
        state_str = "Activo" if SERVER_STATE['youtube_cycle_mode'] else "Inactivo"
        log_event_history('CYCLE_MODE', f"Modo ciclo 11h 55m: {state_str}")
        return {'success': True, 'cycle_mode': SERVER_STATE['youtube_cycle_mode'], 'message': f'Modo ciclo: {state_str}'}

    elif act == 'set_playlist':
        vids = body.get('videos', [])
        SERVER_STATE['playlist'] = vids
        broadcast_state()
        return {'success': True, 'message': 'Lista cargada'}

    elif act == 'toggle_mode':
        m = body.get('mode')
        if m:
            SERVER_STATE['mode'] = m
        else:
            SERVER_STATE['mode'] = 'single_loop' if SERVER_STATE.get('mode') == 'playlist' else 'playlist'
        save_state()
        broadcast_state()
        return {'success': True, 'mode': SERVER_STATE['mode'], 'message': f'Modo: {SERVER_STATE["mode"]}'}
'''

if "elif act == 'set_category':" not in code:
    code = code.replace(
        "    return {'success': True, 'message': 'Acción completada.'}",
        extra_actions + "\n    return {'success': True, 'message': 'Acción completada.'}"
    )
    print("Acciones de control añadidas: set_category, toggle_cycle_mode, set_playlist, toggle_mode")

# 4. En handle_control_action 'start', asegurar que se capturen todas las claves y campos
code = code.replace(
    "['platform', 'stream_key', 'facebook_key', 'twitch_key', 'active_category', 'format', 'stream_format']",
    "['platform', 'stream_key', 'facebook_key', 'twitch_key', 'custom_rtmp_url', 'custom_rtmp_key', 'tiktok_key', 'kick_key', 'active_category', 'format', 'stream_format', 'multistream_targets']"
)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ panel_stream/app.py actualizado exitosamente!")
