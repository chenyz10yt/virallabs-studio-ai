import os, sys, re, json

app_path = "c:/Users/Admin/Desktop/chenyz.app/panel_stream/app.py"

with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add TIKTOK_KEY_FILE and TIKTOK_SERVER_FILE
if "TIKTOK_KEY_FILE" not in code:
    code = code.replace(
        "TWITCH_KEY_FILE = os.path.join(BASE_DIR, 'twitch_key.txt')",
        "TWITCH_KEY_FILE = os.path.join(BASE_DIR, 'twitch_key.txt')\nTIKTOK_KEY_FILE = os.path.join(BASE_DIR, 'tiktok_key.txt')\nTIKTOK_SERVER_FILE = os.path.join(BASE_DIR, 'tiktok_server.txt')"
    )

# 2. Add tiktok to DEFAULT_STATE
if "'tiktok_key'" not in code:
    code = code.replace(
        "'facebook_key': '', 'twitch_key': '',",
        "'facebook_key': '', 'twitch_key': '', 'tiktok_key': '', 'tiktok_server': 'rtmp://push-rtmp-l01-va.tiktokcdn.com/live/', 'control_url': 'http://172.64.219:5000/control',"
    )
    code = code.replace(
        "'multistream_targets': {'youtube': True, 'facebook': False, 'twitch': False},",
        "'multistream_targets': {'youtube': True, 'facebook': False, 'twitch': False, 'tiktok': False},"
    )

# 3. Add tiktok to load_state
if "(TIKTOK_KEY_FILE, 'tiktok_key')" not in code:
    code = code.replace(
        "(TWITCH_KEY_FILE, 'twitch_key')",
        "(TWITCH_KEY_FILE, 'twitch_key'), (TIKTOK_KEY_FILE, 'tiktok_key'), (TIKTOK_SERVER_FILE, 'tiktok_server')"
    )

# 4. Add tiktok to save_state
if "'tiktok_key'" not in code:
    code = code.replace(
        "'facebook_key', 'twitch_key', 'accumulated_minutes'",
        "'facebook_key', 'twitch_key', 'tiktok_key', 'tiktok_server', 'control_url', 'accumulated_minutes'"
    )
    code = code.replace(
        "(TWITCH_KEY_FILE, SERVER_STATE.get('twitch_key'))",
        "(TWITCH_KEY_FILE, SERVER_STATE.get('twitch_key')),\n            (TIKTOK_KEY_FILE, SERVER_STATE.get('tiktok_key')),\n            (TIKTOK_SERVER_FILE, SERVER_STATE.get('tiktok_server'))"
    )

# 5. Add tiktok endpoint to get_platform_endpoint
if "elif plat == 'tiktok':" not in code:
    target_needle = "elif plat == 'twitch': return f'rtmp://live.twitch.tv/app/{k}'"
    tiktok_handler = (
        "elif plat == 'twitch': return f'rtmp://live.twitch.tv/app/{k}'\n"
        "    elif plat == 'tiktok':\n"
        "        if k.startswith('rtmp://') or k.startswith('rtmps://'): return k\n"
        "        srv = (SERVER_STATE.get('tiktok_server', '') or '').strip() or 'rtmp://push-rtmp-l01-va.tiktokcdn.com/live/'\n"
        "        if not srv.endswith('/'): srv += '/'\n"
        "        return f'{srv}{k}'"
    )
    code = code.replace(target_needle, tiktok_handler)

# 6. Add tiktok to stream_worker loop and targets
if "('tiktok', 'tiktok_key')" not in code:
    code = code.replace(
        "[('youtube', 'stream_key'), ('facebook', 'facebook_key'), ('twitch', 'twitch_key')]",
        "[('youtube', 'stream_key'), ('facebook', 'facebook_key'), ('twitch', 'twitch_key'), ('tiktok', 'tiktok_key')]"
    )
    code = code.replace(
        "k_val = SERVER_STATE.get('stream_key' if plat == 'youtube' else ('facebook_key' if plat == 'facebook' else 'twitch_key'))",
        "k_val = SERVER_STATE.get('stream_key' if plat == 'youtube' else ('facebook_key' if plat == 'facebook' else ('twitch_key' if plat == 'twitch' else 'tiktok_key')))"
    )

# 7. Add tiktok to api_test_connection
if "elif plat == 'tiktok':" not in code:
    code = code.replace(
        "tw_key = body.get('twitch_key', '').strip() or SERVER_STATE.get('twitch_key', '')",
        "tw_key = body.get('twitch_key', '').strip() or SERVER_STATE.get('twitch_key', '')\n    tk_key = body.get('tiktok_key', '').strip() or SERVER_STATE.get('tiktok_key', '')"
    )
    code = code.replace(
        "elif plat == 'twitch': target = get_platform_endpoint('twitch', tw_key)",
        "elif plat == 'twitch': target = get_platform_endpoint('twitch', tw_key)\n    elif plat == 'tiktok': target = get_platform_endpoint('tiktok', tk_key)"
    )
    code = code.replace(
        "elif mt.get('twitch') and tw_key: target = get_platform_endpoint('twitch', tw_key)",
        "elif mt.get('twitch') and tw_key: target = get_platform_endpoint('twitch', tw_key)\n        elif mt.get('tiktok') and tk_key: target = get_platform_endpoint('tiktok', tk_key)"
    )

# 8. Add tiktok and control_url to handle_control_action
if "'tiktok_key'" not in code:
    code = code.replace(
        "for k in ['stream_key', 'facebook_key', 'twitch_key', 'platform']:",
        "for k in ['stream_key', 'facebook_key', 'twitch_key', 'tiktok_key', 'tiktok_server', 'control_url', 'platform']:"
    )
    code = code.replace(
        "for k in ['platform', 'stream_key', 'facebook_key', 'twitch_key', 'active_category', 'format', 'stream_format']:",
        "for k in ['platform', 'stream_key', 'facebook_key', 'twitch_key', 'tiktok_key', 'tiktok_server', 'control_url', 'active_category', 'format', 'stream_format']:"
    )

# 9. Add route to serve stream_overlay.png directly with no-cache
if "@app.route('/stream_overlay.png')" not in code:
    overlay_route = (
        "@app.route('/stream_overlay.png')\n"
        "def serve_stream_overlay():\n"
        "    if os.path.exists(OVERLAY_IMAGE_FILE) and os.path.getsize(OVERLAY_IMAGE_FILE) > 0:\n"
        "        resp = send_from_directory(BASE_DIR, 'stream_overlay.png')\n"
        "        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'\n"
        "        return resp\n"
        "    # 1x1 transparent PNG\n"
        "    transparent_1px = b'\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x01\\x08\\x06\\x00\\x00\\x00\\x1f\\x15c4\\x00\\x00\\x00\\rIDATx\\x9cc`\\x00\\x00\\x00\\x02\\x00\\x01H\\xaf\\xa4q\\x00\\x00\\x00\\x00IEND\\xaeB`\\x82'\n"
        "    return Response(transparent_1px, mimetype='image/png', headers={'Cache-Control': 'no-store'})\n"
    )
    code = code.replace("@app.route('/stickers/<path:filename>')", overlay_route + "\n@app.route('/stickers/<path:filename>')")

# 10. Update api_status to include available_ips and control_url
if "'control_url'" not in code:
    code = code.replace(
        "d['local_ip'] = LOCAL_IP\n    return jsonify(d)",
        "d['local_ip'] = LOCAL_IP\n    d['control_url'] = SERVER_STATE.get('control_url', 'http://172.64.219:5000/control')\n    d['available_ips'] = ['172.64.219', '10.243.28.219', '26.210.81.134', LOCAL_IP, 'localhost']\n    return jsonify(d)"
    )
    code = code.replace(
        "data['local_ip'] = LOCAL_IP\n    data['panel_connected_devices'] = max(1, len(CONNECTED_CLIENTS))",
        "data['local_ip'] = LOCAL_IP\n    data['control_url'] = SERVER_STATE.get('control_url', 'http://172.64.219:5000/control')\n    data['available_ips'] = ['172.64.219', '10.243.28.219', '26.210.81.134', LOCAL_IP, 'localhost']\n    data['panel_connected_devices'] = max(1, len(CONNECTED_CLIENTS))"
    )

with open(app_path, "w", encoding="utf-8") as f:
    f.write(code)

print("panel_stream/app.py actualizado con TikTok y control_url.")
