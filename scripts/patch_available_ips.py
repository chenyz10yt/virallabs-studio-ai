import os

for target_dir in ['c:/Users/Admin/Desktop/chenyz.app/panel_stream', 'c:/Users/Admin/Desktop/chenyz.app/web y app']:
    app_file = os.path.join(target_dir, 'app.py')
    with open(app_file, 'r', encoding='utf-8') as f:
        txt = f.read()
    
    needle = "d['local_ip'] = LOCAL_IP\n    d['has_overlay']"
    repl = "d['local_ip'] = LOCAL_IP\n    d['control_url'] = SERVER_STATE.get('control_url', 'http://172.64.219:5000/control')\n    d['available_ips'] = ['172.64.219', '10.243.28.219', '26.210.81.134', LOCAL_IP, 'localhost']\n    d['has_overlay']"
    if needle in txt:
        txt = txt.replace(needle, repl)
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(txt)
        print("Updated available_ips in", app_file)
    else:
        print("Needle not found in", app_file)
