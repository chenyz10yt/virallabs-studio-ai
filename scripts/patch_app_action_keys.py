import os

for target_dir in ["c:/Users/Admin/Desktop/chenyz.app/panel_stream", "c:/Users/Admin/Desktop/chenyz.app/web y app"]:
    app_file = os.path.join(target_dir, "app.py")
    if not os.path.exists(app_file):
        continue
    with open(app_file, "r", encoding="utf-8") as f:
        code = f.read()

    # In handle_control_action
    code = code.replace(
        "for k in ['platform', 'stream_key', 'facebook_key', 'twitch_key', 'active_category', 'format', 'stream_format']:",
        "for k in ['platform', 'stream_key', 'facebook_key', 'twitch_key', 'tiktok_key', 'tiktok_server', 'control_url', 'active_category', 'format', 'stream_format']:"
    )

    code = code.replace(
        "for k in ['stream_key', 'facebook_key', 'twitch_key', 'platform']:",
        "for k in ['stream_key', 'facebook_key', 'twitch_key', 'tiktok_key', 'tiktok_server', 'control_url', 'platform']:"
    )

    # In api_status
    code = code.replace(
        "d['local_ip'] = LOCAL_IP\n        d['has_overlay']",
        "d['local_ip'] = LOCAL_IP\n        d['control_url'] = SERVER_STATE.get('control_url', 'http://172.64.219:5000/control')\n        d['available_ips'] = ['172.64.219', '10.243.28.219', '26.210.81.134', LOCAL_IP, 'localhost']\n        d['has_overlay']"
    )

    # In broadcast_state
    code = code.replace(
        "data['local_ip'] = LOCAL_IP\n    data['panel_connected_devices']",
        "data['local_ip'] = LOCAL_IP\n    data['control_url'] = SERVER_STATE.get('control_url', 'http://172.64.219:5000/control')\n    data['available_ips'] = ['172.64.219', '10.243.28.219', '26.210.81.134', LOCAL_IP, 'localhost']\n    data['panel_connected_devices']"
    )

    with open(app_file, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Patched {app_file}")
