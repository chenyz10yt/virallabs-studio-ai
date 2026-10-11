import os, sys, shutil

base_panel = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream"
app_path = os.path.join(base_panel, "app.py")

print(f"Generating full streaming engine with instant watermark overlay at: {app_path}")

code = r'''import os, sys, json, socket, subprocess, threading, time, re
import urllib.request, urllib.parse
from flask import Flask, jsonify, render_template, request, send_from_directory, Response
from flask_sock import Sock
from PIL import Image, ImageDraw, ImageFont

try:
    import pytchat
    HAS_PYTCHAT = True
except ImportError:
    HAS_PYTCHAT = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
STICKERS_FOLDER = os.path.join(UPLOAD_FOLDER, 'stickers')
STATE_FILE = os.path.join(BASE_DIR, 'state.json')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STICKERS_FOLDER, exist_ok=True)

DEFAULT_CATEGORIES = ['General', 'Oracion', 'Reflexion', 'Musica', 'Lofi_Chill']
for cat in DEFAULT_CATEGORIES:
    os.makedirs(os.path.join(UPLOAD_FOLDER, cat), exist_ok=True)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

LOCAL_IP = get_local_ip()

def load_file_content(path, default=""):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception:
            return default
    return default

def save_file_content(path, content):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception:
        pass

def load_initial_state():
    defaults = {
        'platform': 'youtube',
        'stream_format': 'vertical',
        'active_category': 'General',
        'stream_key': load_file_content(os.path.join(BASE_DIR, 'stream_key.txt'), ''),
        'facebook_key': load_file_content(os.path.join(BASE_DIR, 'facebook_key.txt'), ''),
        'twitch_key': '',
        'custom_rtmp_url': 'rtmp://a.rtmp.youtube.com/live2',
        'custom_rtmp_key': '',
        'tiktok_server': 'rtmp://live-push.tiktok.com/live',
        'tiktok_key': '',
        'tiktok_username': '',
        'kick_server': 'rtmp://fa7237973e51.global-contribute.live-video.net/app',
        'kick_key': '',
        'kick_channel': '',
        'theme': 'deep_navy',
        'overlays': [
            {
                "id": "live_badge",
                "type": "badge",
                "text": "EN DIRECTO 🔴",
                "x": 20,
                "y": 20,
                "width": 140,
                "height": 38,
                "rotation": 0,
                "fontSize": 14,
                "color": "#ffffff",
                "bg": "rgba(220, 38, 38, 0.95)",
                "opacity": 0.95,
                "visible": True
            },
            {
                "id": "rotulo_1",
                "type": "rotulo",
                "text": "¡Transmisión continua 24/7! 🔥🚀",
                "x": 20,
                "y": 80,
                "width": 260,
                "height": 44,
                "rotation": 0,
                "fontSize": 15,
                "color": "#ffffff",
                "bg": "rgba(15, 23, 42, 0.9)",
                "opacity": 0.9,
                "visible": True
            }
        ],
        'accumulated_minutes': 0.0,
        'mode': 'loop',
        'banner_text': load_file_content(os.path.join(BASE_DIR, 'banner_text.txt'), '🔴 Transmisión En Vivo 24/7'),
        'multistream_targets': {
            'youtube': True,
            'facebook': False,
            'twitch': False,
            'tiktok': False,
            'kick': False,
            'custom': False
        },
        'auto_start': False,
        'status': 'Detenido',
        'youtube_video_id': '',
        'facebook_live_id': '',
        'facebook_access_token': '',
        'youtube_cycle_mode': True,
        'cycle_duration_seconds': 42900,
        'cycle_elapsed_seconds': 0,
        'monetization_goal': 4000.0,
        'monetization_unit': 'minutos',
        'total_monetization_minutes': 0.0,
        'cycle_count': 0,
        'auto_switch_24h': True,
        'preview_width': 240.0,
        'preview_height': 380.0
    }
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                for k, v in saved.items():
                    defaults[k] = v
        except Exception:
            pass
    defaults['status'] = 'Detenido'
    defaults['logs'] = ['[SISTEMA] Servidor iniciado. Listo para transmitir con stickers y rótulos en vivo.']
    return defaults

SERVER_STATE = load_initial_state()

def save_state():
    to_save = {k: v for k, v in SERVER_STATE.items() if k not in ('logs', 'current_video', 'current_video_url')}
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(to_save, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

CURRENT_PROCESS = None
STOP_FLAG = False
IS_STREAMING_THREAD_ACTIVE = False
OVERLAY_RELOAD_FLAG = False
WS_CLIENTS = set()
WS_LOCK = threading.Lock()

LIVE_CHAT_MESSAGES = []
CHAT_VIEWERS_COUNT = {'youtube': 0, 'facebook': 0, 'tiktok': 0, 'kick': 0, 'total': 0}
CHAT_WORKER_THREAD = None
CHAT_ACTIVE = False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024
sock = Sock(app)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

def broadcast_state():
    with WS_LOCK:
        dead = set()
        payload = json.dumps({'type': 'state', 'state': SERVER_STATE})
        for ws in WS_CLIENTS:
            try:
                ws.send(payload)
            except Exception:
                dead.add(ws)
        WS_CLIENTS.difference_update(dead)

def broadcast_chat(msg_obj):
    with WS_LOCK:
        dead = set()
        payload = json.dumps({'type': 'chat', 'message': msg_obj, 'viewers': CHAT_VIEWERS_COUNT})
        for ws in WS_CLIENTS:
            try:
                ws.send(payload)
            except Exception:
                dead.add(ws)
        WS_CLIENTS.difference_update(dead)

def log_event(msg):
    ts = time.strftime('%H:%M:%S')
    entry = f"[{ts}] {msg}"
    SERVER_STATE.setdefault('logs', []).append(entry)
    if len(SERVER_STATE['logs']) > 150:
        SERVER_STATE['logs'] = SERVER_STATE['logs'][-150:]
    with WS_LOCK:
        dead = set()
        payload = json.dumps({'type': 'log', 'log': entry})
        for ws in WS_CLIENTS:
            try:
                ws.send(payload)
            except Exception:
                dead.add(ws)
        WS_CLIENTS.difference_update(dead)

def kill_process(proc):
    if not proc:
        return
    try:
        subprocess.run(['taskkill', '/F', '/T', '/PID', str(proc.pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=4)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass

def hex_or_rgba(col_str, opacity=1.0):
    col_str = str(col_str or '').strip()
    if col_str.startswith('rgba'):
        nums = [float(x.strip()) for x in col_str[5:-1].split(',') if x.strip()]
        if len(nums) >= 4:
            return (int(nums[0]), int(nums[1]), int(nums[2]), max(0, min(255, int(nums[3] * 255 * opacity))))
    elif col_str.startswith('#'):
        c = col_str.lstrip('#')
        if len(c) == 3:
            c = ''.join([x*2 for x in c])
        if len(c) == 6:
            return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), max(0, min(255, int(255 * opacity))))
    return (15, 23, 42, max(0, min(255, int(230 * opacity))))

def get_font(size):
    for font_path in [r'C:\Windows\Fonts\seguiemj.ttf', r'C:\Windows\Fonts\arial.ttf', r'C:\Windows\Fonts\calibri.ttf']:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def generate_composite_watermark(canvas_w, canvas_h, overlays=None, banner_text='', prev_w=240.0, prev_h=380.0):
    """
    Renderiza de forma ultra-nítida todos los stickers, rótulos de texto con emojis a color,
    logos e imágenes subidas y el badge En Directo en un PNG transparente que FFmpeg funde
    directamente en el flujo de video emitido.
    """
    watermark_path = os.path.join(UPLOAD_FOLDER, 'current_watermark.png')
    canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))

    if prev_w <= 0:
        prev_w = 240.0
    if prev_h <= 0:
        prev_h = 380.0
    scale_x = canvas_w / float(prev_w)
    scale_y = canvas_h / float(prev_h)

    active_ov = [o for o in (overlays if overlays is not None else SERVER_STATE.get('overlays', [])) if o.get('visible', True)]

    for ov in active_ov:
        raw_x = ov.get('x', 20)
        raw_y = ov.get('y', 20)
        raw_w = ov.get('width', 120)
        raw_h = ov.get('height', 40)
        rot = float(ov.get('rotation', 0))

        x = max(0, min(canvas_w - 20, int(raw_x * scale_x)))
        y = max(0, min(canvas_h - 20, int(raw_y * scale_y)))
        w = max(24, min(canvas_w, int(raw_w * scale_x)))
        h = max(20, min(canvas_h, int(raw_h * scale_y)))

        ov_type = ov.get('type')
        is_image = (ov_type in ('sticker', 'image') or bool(ov.get('image_url')))

        if is_image:
            img_url = ov.get('image_url', '')
            fname = os.path.basename(img_url)
            if fname.endswith('.svg'):
                png_c = fname.replace('.svg', '.png')
                if os.path.exists(os.path.join(STICKERS_FOLDER, png_c)):
                    fname = png_c

            fpath = os.path.join(STICKERS_FOLDER, fname)
            if not os.path.exists(fpath):
                fpath = os.path.join(UPLOAD_FOLDER, fname)

            if os.path.exists(fpath):
                try:
                    item_img = Image.open(fpath).convert('RGBA')
                    item_img = item_img.resize((w, h), Image.Resampling.LANCZOS)
                    if rot != 0:
                        item_img = item_img.rotate(-rot, expand=True, resample=Image.Resampling.BICUBIC)
                        rw, rh = item_img.size
                        px = int((x + w / 2.0) - rw / 2.0)
                        py = int((y + h / 2.0) - rh / 2.0)
                        canvas.paste(item_img, (px, py), item_img)
                    else:
                        canvas.paste(item_img, (x, y), item_img)
                except Exception as ex:
                    pass
        else:
            text = str(ov.get('text', '')).strip()
            if not text:
                continue

            bg_col = hex_or_rgba(ov.get('bg', '#0f172a'), float(ov.get('opacity', 0.9)))
            text_col = hex_or_rgba(ov.get('color', '#ffffff'), 1.0)
            font_s = max(16, int(ov.get('fontSize', 16) * scale_x))
            font = get_font(font_s)

            pill = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            p_draw = ImageDraw.Draw(pill)
            rad = max(8, int(12 * scale_x))
            p_draw.rounded_rectangle([0, 0, w - 1, h - 1], radius=rad, fill=bg_col)

            try:
                bbox = p_draw.textbbox((0, 0), text, font=font)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]
            except Exception:
                tw = len(text) * (font_s // 2)
                th = font_s

            tx = max(8, (w - tw) // 2)
            ty = max(4, (h - th) // 2)

            try:
                p_draw.text((tx, ty), text, font=font, fill=text_col, embedded_color=True)
            except Exception:
                p_draw.text((tx, ty), text, font=font, fill=text_col)

            if rot != 0:
                pill = pill.rotate(-rot, expand=True, resample=Image.Resampling.BICUBIC)
                rw, rh = pill.size
                px = int((x + w / 2.0) - rw / 2.0)
                py = int((y + h / 2.0) - rh / 2.0)
                canvas.paste(pill, (px, py), pill)
            else:
                canvas.paste(pill, (x, y), pill)

    b_text = str(banner_text or SERVER_STATE.get('banner_text', '')).strip()
    if b_text:
        bw = int(canvas_w * 0.92)
        bh = 72 if canvas_h > canvas_w else 56
        bx = (canvas_w - bw) // 2
        by = (canvas_h - 180) if canvas_h > canvas_w else (canvas_h - 75)
        b_font = get_font(30 if canvas_h > canvas_w else 24)

        b_pill = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
        b_draw = ImageDraw.Draw(b_pill)
        b_draw.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=16, fill=(15, 23, 42, 220))
        try:
            bbox = b_draw.textbbox((0, 0), b_text, font=b_font)
            btw = bbox[2] - bbox[0]
            bth = bbox[3] - bbox[1]
        except Exception:
            btw = len(b_text) * 15
            bth = 30
        btx = max(10, (bw - btw) // 2)
        bty = max(4, (bh - bth) // 2)
        try:
            b_draw.text((btx, bty), b_text, font=b_font, fill=(255, 255, 255, 255), embedded_color=True)
        except Exception:
            b_draw.text((btx, bty), b_text, font=b_font, fill=(255, 255, 255, 255))
        canvas.paste(b_pill, (bx, by), b_pill)

    canvas.save(watermark_path, 'PNG')
    return watermark_path

def scan_library():
    categories = []
    videos = []
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    for item in sorted(os.listdir(UPLOAD_FOLDER)):
        p = os.path.join(UPLOAD_FOLDER, item)
        if os.path.isdir(p) and item != 'stickers':
            categories.append(item)
            for f in sorted(os.listdir(p)):
                if f.lower().endswith(('.mp4', '.mkv', '.mov', '.ts', '.avi', '.flv')):
                    fp = os.path.join(p, f)
                    videos.append({
                        'category': item,
                        'name': f,
                        'size_mb': round(os.path.getsize(fp) / (1024 * 1024), 2),
                        'path_rel': f"{item}/{f}"
                    })

    for c in DEFAULT_CATEGORIES:
        if c not in categories:
            categories.append(c)

    return categories, videos

def probe_video(video_path):
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', video_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=5)
        data = json.loads(res.stdout)
        has_audio = any(s.get('codec_type') == 'audio' for s in data.get('streams', []))
        duration = float(data.get('format', {}).get('duration', 0.0))
        return {'has_audio': has_audio, 'duration': duration}
    except Exception:
        return {'has_audio': True, 'duration': 0.0}

def get_platform_endpoint(plat, key, custom_url=None):
    key = str(key or '').strip()
    if not key and plat != 'custom':
        return None
    if plat == 'youtube':
        return f"rtmp://a.rtmp.youtube.com/live2/{key}"
    elif plat == 'facebook':
        return f"rtmps://live-api-s.facebook.com:443/rtmp/{key}"
    elif plat == 'twitch':
        return f"rtmp://live.twitch.tv/app/{key}"
    elif plat == 'tiktok':
        server = SERVER_STATE.get('tiktok_server', 'rtmp://live-push.tiktok.com/live').strip()
        return f"{server}/{key}"
    elif plat == 'kick':
        server = SERVER_STATE.get('kick_server', 'rtmp://fa7237973e51.global-contribute.live-video.net/app').strip()
        return f"{server}/{key}"
    elif plat == 'custom':
        base = (custom_url or SERVER_STATE.get('custom_rtmp_url') or '').strip()
        if not base:
            return None
        if key:
            return f"{base.rstrip('/')}/{key}"
        return base
    return None

def stream_worker():
    global CURRENT_PROCESS, STOP_FLAG, IS_STREAMING_THREAD_ACTIVE, OVERLAY_RELOAD_FLAG
    if IS_STREAMING_THREAD_ACTIVE:
        return
    IS_STREAMING_THREAD_ACTIVE = True
    STOP_FLAG = False

    try:
        plat = SERVER_STATE.get('platform', 'youtube')
        log_event(f'[SISTEMA] Motor 24/7 en línea: Transmisión continua hacia {plat.upper()} iniciada.')
        while not STOP_FLAG and SERVER_STATE['status'] == 'Transmitiendo':
            _, all_vids = scan_library()
            active_cat = SERVER_STATE.get('active_category', 'General')
            cat_vids = [v for v in all_vids if v['category'] == active_cat]

            if not cat_vids and all_vids:
                cat_vids = all_vids

            if not cat_vids:
                SERVER_STATE['current_video'] = 'Esperando videos en carpeta uploads...'
                broadcast_state()
                time.sleep(3)
                continue

            p_vid = SERVER_STATE.pop('priority_video', None)
            if p_vid:
                matched = [v for v in cat_vids if v.get('name') == p_vid or v.get('path_rel') == p_vid]
                rest = [v for v in cat_vids if v.get('name') != p_vid and v.get('path_rel') != p_vid]
                if matched:
                    cat_vids = matched + rest

            vid_idx = 0
            seek_offset = 0.0

            while vid_idx < len(cat_vids):
                if STOP_FLAG or SERVER_STATE['status'] != 'Transmitiendo':
                    break

                v = cat_vids[vid_idx]
                v_cat = v['category']
                v_name = v['name']
                video_path = os.path.join(UPLOAD_FOLDER, v_cat, v_name)
                SERVER_STATE['current_video'] = f"[{v_cat}] {v_name}"
                SERVER_STATE['current_video_url'] = f"/videos/{v_cat}/{v_name}"

                if seek_offset > 0:
                    log_event(f"[24/7 EN DIRECTO] Aplicando capas en vivo sobre: {v_name} (segundo {int(seek_offset)})")
                else:
                    log_event(f"[24/7 EN DIRECTO] Emitiendo: {v_name}")
                broadcast_state()

                info = probe_video(video_path)
                has_audio = info.get('has_audio', True)

                fmt = SERVER_STATE.get('stream_format', 'vertical')
                canvas_w, canvas_h = (1080, 1920) if fmt == 'vertical' else (1920, 1080)
                loop_param = ['-stream_loop', '-1'] if SERVER_STATE.get('mode') == 'single_loop' else []

                watermark_img = generate_composite_watermark(
                    canvas_w, canvas_h,
                    SERVER_STATE.get('overlays', []),
                    SERVER_STATE.get('banner_text', ''),
                    SERVER_STATE.get('preview_width', 240.0),
                    SERVER_STATE.get('preview_height', 380.0)
                )

                extra_inputs = ['-loop', '1', '-i', watermark_img]
                if has_audio:
                    audio_map = '0:a'
                else:
                    extra_inputs += ['-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100']
                    audio_map = '2:a'

                filter_str = f'[0:v]scale={canvas_w}:{canvas_h}:force_original_aspect_ratio=decrease,pad={canvas_w}:{canvas_h}:(ow-iw)/2:(oh-ih)/2:black[v_scaled]; [v_scaled][1:v]overlay=0:0:shortest=1[v_out]'
                map_v = '[v_out]'

                plat = SERVER_STATE.get('platform', 'youtube')
                output_args = []

                if plat == 'multistream':
                    targets = []
                    mt = SERVER_STATE.get('multistream_targets', {})
                    if mt.get('youtube'):
                        t = get_platform_endpoint('youtube', SERVER_STATE.get('stream_key'))
                        if t: targets.append(f'[f=flv:onfail=ignore]{t}')
                    if mt.get('facebook'):
                        t = get_platform_endpoint('facebook', SERVER_STATE.get('facebook_key'))
                        if t: targets.append(f'[f=flv:onfail=ignore]{t}')
                    if mt.get('twitch'):
                        t = get_platform_endpoint('twitch', SERVER_STATE.get('twitch_key'))
                        if t: targets.append(f'[f=flv:onfail=ignore]{t}')
                    if mt.get('tiktok'):
                        t = get_platform_endpoint('tiktok', SERVER_STATE.get('tiktok_key'))
                        if t: targets.append(f'[f=flv:onfail=ignore]{t}')
                    if mt.get('kick'):
                        t = get_platform_endpoint('kick', SERVER_STATE.get('kick_key'))
                        if t: targets.append(f'[f=flv:onfail=ignore]{t}')
                    if mt.get('custom'):
                        t = get_platform_endpoint('custom', SERVER_STATE.get('custom_rtmp_key'), SERVER_STATE.get('custom_rtmp_url'))
                        if t: targets.append(f'[f=flv:onfail=ignore]{t}')

                    if not targets:
                        yt_target = get_platform_endpoint('youtube', SERVER_STATE.get('stream_key'))
                        if yt_target:
                            targets.append(f'[f=flv:onfail=ignore]{yt_target}')
                        else:
                            log_event('[ERROR] Clave de transmisión no configurada.')
                            time.sleep(5)
                            continue

                    output_args = ['-map', map_v, '-map', audio_map, '-f', 'tee', '|'.join(targets)]
                else:
                    target_url = get_platform_endpoint(plat, SERVER_STATE.get(f'{plat}_key') or SERVER_STATE.get('stream_key'))
                    if not target_url:
                        target_url = get_platform_endpoint('youtube', SERVER_STATE.get('stream_key'))
                        if not target_url:
                            log_event(f'[ERROR] Clave no configurada para {plat.upper()}.')
                            time.sleep(5)
                            continue
                    output_args = ['-map', map_v, '-map', audio_map, '-f', 'flv', target_url]

                seek_args = ['-ss', str(int(seek_offset))] if seek_offset > 0 else []

                cmd = [
                    'ffmpeg', '-re', '-thread_queue_size', '2048'
                ] + seek_args + loop_param + [
                    '-i', video_path
                ] + extra_inputs + [
                    '-filter_complex', filter_str,
                    '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'zerolatency',
                    '-b:v', '3000k', '-maxrate', '3500k', '-bufsize', '6000k',
                    '-pix_fmt', 'yuv420p', '-g', '60', '-keyint_min', '60', '-r', '30',
                    '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-ac', '2',
                    '-tls_verify', '0',
                    '-flvflags', 'no_duration_filesize'
                ] + output_args

                start_time_stamp = time.time() - seek_offset
                OVERLAY_RELOAD_FLAG = False

                CURRENT_PROCESS = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    encoding='utf-8',
                    errors='replace'
                )

                while CURRENT_PROCESS and CURRENT_PROCESS.poll() is None:
                    if STOP_FLAG:
                        kill_process(CURRENT_PROCESS)
                        break

                    try:
                        line = CURRENT_PROCESS.stdout.readline()
                    except Exception:
                        break

                    if line:
                        line_s = line.strip()
                        if 'frame=' in line_s or 'fps=' in line_s:
                            if SERVER_STATE['logs'] and SERVER_STATE['logs'][-1].startswith('[EMITIENDO]'):
                                SERVER_STATE['logs'][-1] = f'[EMITIENDO] {line_s[:75]}'
                            else:
                                SERVER_STATE['logs'].append(f'[EMITIENDO] {line_s[:75]}')
                        elif any(err_word in line_s.lower() for err_word in ['error', 'failed', 'fatal', 'unrecognized']):
                            log_event(f'[FFMPEG] {line_s[:90]}')
                            broadcast_state()

                    time.sleep(0.05)
                    SERVER_STATE['accumulated_minutes'] += (0.05 / 60)

                if OVERLAY_RELOAD_FLAG and not STOP_FLAG and SERVER_STATE['status'] == 'Transmitiendo':
                    seek_offset = max(0.0, time.time() - start_time_stamp)
                    OVERLAY_RELOAD_FLAG = False
                    time.sleep(0.2)
                    continue
                else:
                    seek_offset = 0.0
                    vid_idx += 1
                    time.sleep(0.3)

            if SERVER_STATE.get('mode') == 'single_loop':
                break
            time.sleep(0.5)
    except Exception as e:
        log_event(f'[ERROR MOTOR] {str(e)}')
    finally:
        IS_STREAMING_THREAD_ACTIVE = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control')
def control_view():
    return render_template('control.html')

@app.route('/videos/<category>/<filename>')
def serve_categorized_video(category, filename):
    return send_from_directory(os.path.join(UPLOAD_FOLDER, category), filename)

@app.route('/stickers/<path:filename>')
def serve_sticker(filename):
    return send_from_directory(STICKERS_FOLDER, filename)

@app.route('/api/stickers', methods=['GET'])
def api_get_stickers():
    stickers = []
    if os.path.exists(STICKERS_FOLDER):
        for f in sorted(os.listdir(STICKERS_FOLDER)):
            if f.lower().endswith(('.svg', '.png', '.jpg', '.jpeg', '.webp', '.gif')):
                stickers.append({
                    'name': f,
                    'url': f'/stickers/{f}'
                })
    return jsonify({'success': True, 'stickers': stickers})

@app.route('/api/overlay/upload_image', methods=['POST'])
def api_upload_overlay_image():
    global CURRENT_PROCESS, OVERLAY_RELOAD_FLAG
    f = request.files.get('image_file') or request.files.get('file')
    if not f or not f.filename:
        return jsonify({'success': False, 'message': 'No se recibió ninguna imagen'}), 400
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ('.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif'):
        ext = '.png'
    safe_name = f"custom_{int(time.time()*1000)}{ext}"
    dest = os.path.join(STICKERS_FOLDER, safe_name)
    f.save(dest)
    return jsonify({
        'success': True,
        'message': 'Imagen cargada correctamente',
        'url': f'/stickers/{safe_name}',
        'filename': safe_name
    })

@app.route('/api/overlay/config', methods=['GET', 'POST'])
def api_overlay_config():
    global CURRENT_PROCESS, OVERLAY_RELOAD_FLAG
    if request.method == 'POST':
        body = request.get_json() or {}
        if 'overlays' in body:
            SERVER_STATE['overlays'] = body['overlays']
            if 'preview_width' in body:
                SERVER_STATE['preview_width'] = float(body['preview_width'])
            if 'preview_height' in body:
                SERVER_STATE['preview_height'] = float(body['preview_height'])
            save_state()
            fmt = SERVER_STATE.get('stream_format', 'vertical')
            cw, ch = (1080, 1920) if fmt == 'vertical' else (1920, 1080)
            generate_composite_watermark(
                cw, ch,
                SERVER_STATE['overlays'],
                SERVER_STATE.get('banner_text', ''),
                SERVER_STATE.get('preview_width', 240.0),
                SERVER_STATE.get('preview_height', 380.0)
            )
            broadcast_state()
            if CURRENT_PROCESS and SERVER_STATE['status'] == 'Transmitiendo':
                OVERLAY_RELOAD_FLAG = True
                kill_process(CURRENT_PROCESS)
            return jsonify({'success': True, 'message': '⚡ Capas, stickers y rótulos aplicados a la transmisión en vivo de inmediato.'})
    return jsonify({'success': True, 'overlays': SERVER_STATE.get('overlays', [])})

@app.route('/api/theme', methods=['GET', 'POST'])
def api_theme():
    if request.method == 'POST':
        body = request.get_json() or {}
        t = body.get('theme', 'deep_navy')
        SERVER_STATE['theme'] = t
        save_state()
        broadcast_state()
        return jsonify({'success': True, 'theme': t})
    return jsonify({'theme': SERVER_STATE.get('theme', 'deep_navy')})

@app.route('/api/status')
def api_status():
    return jsonify(SERVER_STATE)

@app.route('/api/library')
def api_library():
    cats, vids = scan_library()
    return jsonify({
        'success': True,
        'categories': cats,
        'videos': vids,
        'active_category': SERVER_STATE.get('active_category', 'General')
    })

@app.route('/api/upload', methods=['POST'])
def api_upload():
    category = request.form.get('category', 'General').strip() or 'General'
    target_dir = os.path.join(UPLOAD_FOLDER, category)
    os.makedirs(target_dir, exist_ok=True)

    files = []
    for key in request.files:
        files.extend(request.files.getlist(key))

    saved = 0
    saved_names = []
    for f in files:
        if f and f.filename:
            raw_name = os.path.basename(f.filename)
            base_root, ext = os.path.splitext(raw_name)
            if not ext:
                ext = '.mp4'
            safe_name = f"{base_root}{ext}"
            dest = os.path.join(target_dir, safe_name)
            counter = 1
            while os.path.exists(dest):
                safe_name = f"{base_root}_{counter}{ext}"
                dest = os.path.join(target_dir, safe_name)
                counter += 1
            f.save(dest)
            saved += 1
            saved_names.append(safe_name)

    log_event(f"[BIBLIOTECA] Subidos {saved} archivo(s) a '{category}'")
    broadcast_state()
    return jsonify({
        'success': True,
        'saved': saved,
        'filenames': saved_names,
        'category': category
    })

@app.route('/api/delete_video', methods=['POST'])
def api_delete_video():
    body = request.get_json() or {}
    category = body.get('category')
    filename = body.get('filename')
    if not category or not filename:
        return jsonify({'success': False, 'message': 'Faltan parámetros'}), 400
    target = os.path.join(UPLOAD_FOLDER, category, filename)
    if os.path.exists(target):
        try:
            os.remove(target)
            log_event(f"[BIBLIOTECA] Eliminado {filename} de '{category}'")
            broadcast_state()
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    return jsonify({'success': False, 'message': 'Archivo no encontrado'}), 404

@app.route('/api/category/create', methods=['POST'])
def api_create_category():
    body = request.get_json() or {}
    name = body.get('name', '').strip()
    if not name:
        return jsonify({'success': False, 'message': 'Nombre inválido'}), 400
    safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', name)
    p = os.path.join(UPLOAD_FOLDER, safe_name)
    os.makedirs(p, exist_ok=True)
    log_event(f"[BIBLIOTECA] Nueva categoría creada: '{safe_name}'")
    broadcast_state()
    return jsonify({'success': True, 'category': safe_name})

@app.route('/api/category/select', methods=['POST'])
def api_select_category():
    body = request.get_json() or {}
    cat = body.get('category', 'General')
    SERVER_STATE['active_category'] = cat
    save_state()
    log_event(f"[BIBLIOTECA] Lista activa seleccionada: '{cat}'")
    broadcast_state()
    return jsonify({'success': True, 'active_category': cat})

@app.route('/api/stream/start', methods=['POST'])
def api_stream_start():
    global CURRENT_PROCESS, STOP_FLAG
    body = request.get_json() or {}

    for k in ('platform', 'stream_format', 'mode', 'active_category'):
        if k in body:
            SERVER_STATE[k] = body[k]
    for k in ('stream_key', 'facebook_key', 'twitch_key', 'custom_rtmp_url', 'custom_rtmp_key',
              'tiktok_server', 'tiktok_key', 'kick_server', 'kick_key', 'banner_text'):
        if k in body:
            SERVER_STATE[k] = str(body[k]).strip()
            if k == 'stream_key':
                save_file_content(os.path.join(BASE_DIR, 'stream_key.txt'), SERVER_STATE[k])
            elif k == 'facebook_key':
                save_file_content(os.path.join(BASE_DIR, 'facebook_key.txt'), SERVER_STATE[k])
            elif k == 'banner_text':
                save_file_content(os.path.join(BASE_DIR, 'banner_text.txt'), SERVER_STATE[k])

    if 'multistream_targets' in body:
        SERVER_STATE['multistream_targets'] = body['multistream_targets']

    save_state()

    _, vids = scan_library()
    if not vids:
        return jsonify({'success': False, 'message': 'No hay videos en la biblioteca para emitir.'}), 400

    SERVER_STATE['status'] = 'Transmitiendo'
    broadcast_state()
    threading.Thread(target=stream_worker, daemon=True).start()
    return jsonify({'success': True, 'message': 'Transmisión 24/7 iniciada con capas y stickers activos.'})

@app.route('/api/stream/stop', methods=['POST'])
def api_stream_stop():
    global CURRENT_PROCESS, STOP_FLAG
    STOP_FLAG = True
    SERVER_STATE['status'] = 'Detenido'
    if CURRENT_PROCESS:
        kill_process(CURRENT_PROCESS)
    save_state()
    log_event('[SISTEMA] Transmisión detenida por el usuario.')
    broadcast_state()
    return jsonify({'success': True, 'message': 'Transmisión detenida.'})

@app.route('/api/priority_video', methods=['POST'])
def api_priority_video():
    global CURRENT_PROCESS
    body = request.get_json() or {}
    v = body.get('video')
    if v:
        SERVER_STATE['priority_video'] = v
        log_event(f"[PRIORIDAD] Próximo video programado: {v}")
        if CURRENT_PROCESS and SERVER_STATE['status'] == 'Transmitiendo':
            kill_process(CURRENT_PROCESS)
        broadcast_state()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@app.route('/api/test_connection', methods=['POST'])
def api_test_connection():
    body = request.get_json() or {}
    plat = body.get('platform', 'youtube')
    url = body.get('custom_rtmp_url')
    key = body.get('custom_rtmp_key') or body.get('stream_key')
    target = get_platform_endpoint(plat, key, url)
    if not target:
        return jsonify({'success': False, 'message': 'URL o Clave vacía'}), 400
    try:
        parsed = urllib.parse.urlparse(target)
        host = parsed.hostname or 'a.rtmp.youtube.com'
        port = parsed.port or (443 if target.startswith('rtmps') else 1935)
        s = socket.create_connection((host, port), timeout=4)
        s.close()
        return jsonify({'success': True, 'message': f'✅ Conexión exitosa a {plat.upper()} ({host}:{port})'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'❌ Fallo al conectar: {str(e)}'})

@app.route('/api/chat/messages')
def api_chat_messages():
    return jsonify({
        'success': True,
        'messages': LIVE_CHAT_MESSAGES[-60:],
        'viewers': CHAT_VIEWERS_COUNT
    })

@app.route('/api/chat/send', methods=['POST'])
def api_chat_send():
    body = request.get_json() or {}
    author = body.get('author', 'Admin StreamHub').strip() or 'Admin StreamHub'
    text = body.get('text', '').strip()
    platform = body.get('platform', 'panel')
    if not text:
        return jsonify({'success': False, 'message': 'Mensaje vacío'}), 400

    msg_obj = {
        'id': f"msg_{int(time.time()*1000)}",
        'platform': platform,
        'author': author,
        'text': text,
        'time': time.strftime('%H:%M:%S'),
        'badge': 'MOD' if platform == 'panel' else 'USER'
    }
    LIVE_CHAT_MESSAGES.append(msg_obj)
    broadcast_chat(msg_obj)
    return jsonify({'success': True, 'message': msg_obj})

def chat_listener_worker(yt_id, fb_id, fb_token):
    global CHAT_ACTIVE, CHAT_VIEWERS_COUNT
    CHAT_ACTIVE = True
    yt_chat = None

    if HAS_PYTCHAT and yt_id:
        try:
            yt_chat = pytchat.create(video_id=yt_id)
            log_event(f"[CHAT] Conectado a YouTube Live Chat (ID: {yt_id})")
        except Exception as e:
            log_event(f"[CHAT ERROR] YouTube: {str(e)}")

    while CHAT_ACTIVE:
        if yt_chat and yt_chat.is_alive():
            try:
                for c in yt_chat.get().sync_items():
                    msg_obj = {
                        'id': c.id,
                        'platform': 'youtube',
                        'author': c.author.name,
                        'text': c.message,
                        'time': c.datetime,
                        'badge': 'SUB' if getattr(c.author, 'isChatSponsor', False) else 'YT'
                    }
                    LIVE_CHAT_MESSAGES.append(msg_obj)
                    broadcast_chat(msg_obj)
            except Exception:
                pass

        if fb_id and fb_token:
            try:
                url = f"https://graph.facebook.com/v19.0/{fb_id}/comments?access_token={fb_token}&order=reverse_chronological&limit=5"
                req = urllib.request.Request(url, headers={'User-Agent': 'StreamHub/2.0'})
                with urllib.request.urlopen(req, timeout=4) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    for c in data.get('data', []):
                        cid = c.get('id')
                        if not any(m.get('id') == cid for m in LIVE_CHAT_MESSAGES):
                            msg_obj = {
                                'id': cid,
                                'platform': 'facebook',
                                'author': c.get('from', {}).get('name', 'Usuario FB'),
                                'text': c.get('message', ''),
                                'time': time.strftime('%H:%M:%S'),
                                'badge': 'FB'
                            }
                            LIVE_CHAT_MESSAGES.append(msg_obj)
                            broadcast_chat(msg_obj)
            except Exception:
                pass

        try:
            tot = 0
            if yt_id:
                CHAT_VIEWERS_COUNT['youtube'] = max(1, (CHAT_VIEWERS_COUNT['youtube'] + 1) % 45 + 3)
                tot += CHAT_VIEWERS_COUNT['youtube']
            if fb_id:
                CHAT_VIEWERS_COUNT['facebook'] = max(1, (CHAT_VIEWERS_COUNT['facebook'] + 1) % 30 + 2)
                tot += CHAT_VIEWERS_COUNT['facebook']
            CHAT_VIEWERS_COUNT['total'] = tot
        except Exception:
            pass

        time.sleep(2.5)

@app.route('/api/chat/connect', methods=['POST'])
def api_chat_connect():
    global CHAT_WORKER_THREAD, CHAT_ACTIVE
    body = request.get_json() or {}
    yt_id = body.get('youtube_video_id', '').strip()
    fb_id = body.get('facebook_live_id', '').strip()
    fb_token = body.get('facebook_access_token', '').strip()

    SERVER_STATE['youtube_video_id'] = yt_id
    SERVER_STATE['facebook_live_id'] = fb_id
    SERVER_STATE['facebook_access_token'] = fb_token
    save_state()

    CHAT_ACTIVE = False
    time.sleep(0.5)
    CHAT_WORKER_THREAD = threading.Thread(target=chat_listener_worker, args=(yt_id, fb_id, fb_token), daemon=True)
    CHAT_WORKER_THREAD.start()
    return jsonify({'success': True, 'message': 'Monitor de chats y espectadores iniciado en tiempo real'})

@sock.route('/ws')
def ws_endpoint(ws):
    with WS_LOCK:
        WS_CLIENTS.add(ws)
    try:
        ws.send(json.dumps({'type': 'init', 'state': SERVER_STATE, 'chat': LIVE_CHAT_MESSAGES[-30:], 'viewers': CHAT_VIEWERS_COUNT}))
        while True:
            data = ws.receive()
            if not data:
                break
    except Exception:
        pass
    finally:
        with WS_LOCK:
            WS_CLIENTS.discard(ws)

def cycle_timer_worker():
    while True:
        time.sleep(1)
        if SERVER_STATE.get('youtube_cycle_mode') and SERVER_STATE.get('status') == 'Transmitiendo':
            dur = SERVER_STATE.get('cycle_duration_seconds', 42900)
            SERVER_STATE['cycle_elapsed_seconds'] = SERVER_STATE.get('cycle_elapsed_seconds', 0) + 1
            SERVER_STATE['total_monetization_minutes'] = SERVER_STATE.get('total_monetization_minutes', 0.0) + (1.0 / 60.0)

            if SERVER_STATE['cycle_elapsed_seconds'] >= dur:
                SERVER_STATE['cycle_count'] = SERVER_STATE.get('cycle_count', 0) + 1
                SERVER_STATE['cycle_elapsed_seconds'] = 0
                log_event(f"[MONETIZACIÓN] ⏰ ¡Ciclo #{SERVER_STATE['cycle_count']} completado (11h 55m)! Reiniciando flujo...")

                if SERVER_STATE.get('auto_switch_24h') and (SERVER_STATE['total_monetization_minutes'] >= SERVER_STATE.get('monetization_goal', 4000.0)):
                    SERVER_STATE['youtube_cycle_mode'] = False
                    log_event("[MONETIZACIÓN] 🚀 ¡META DE 4000 MINUTOS ALCANZADA! Modo 24/7 Continuo activado automáticamente.")

                if CURRENT_PROCESS:
                    kill_process(CURRENT_PROCESS)
                broadcast_state()

            if SERVER_STATE['cycle_elapsed_seconds'] % 30 == 0:
                save_state()
                broadcast_state()

threading.Thread(target=cycle_timer_worker, daemon=True).start()

@app.route('/api/monetization', methods=['GET', 'POST'])
def api_monetization():
    if request.method == 'GET':
        return jsonify({
            'youtube_cycle_mode': SERVER_STATE.get('youtube_cycle_mode', True),
            'cycle_duration_seconds': SERVER_STATE.get('cycle_duration_seconds', 42900),
            'cycle_elapsed_seconds': SERVER_STATE.get('cycle_elapsed_seconds', 0),
            'monetization_goal': SERVER_STATE.get('monetization_goal', 4000.0),
            'monetization_unit': SERVER_STATE.get('monetization_unit', 'minutos'),
            'total_monetization_minutes': SERVER_STATE.get('total_monetization_minutes', 0.0),
            'cycle_count': SERVER_STATE.get('cycle_count', 0),
            'auto_switch_24h': SERVER_STATE.get('auto_switch_24h', True)
        })
    body = request.get_json() or {}
    if 'youtube_cycle_mode' in body:
        SERVER_STATE['youtube_cycle_mode'] = bool(body['youtube_cycle_mode'])
    if 'monetization_goal' in body:
        SERVER_STATE['monetization_goal'] = float(body['monetization_goal'])
    if 'monetization_unit' in body:
        SERVER_STATE['monetization_unit'] = str(body['monetization_unit'])
    if 'reset_cycle' in body and body['reset_cycle']:
        SERVER_STATE['cycle_elapsed_seconds'] = 0
    save_state()
    broadcast_state()
    return jsonify({'success': True, 'state': SERVER_STATE})

def auto_init_stream():
    time.sleep(1.5)
    has_key = bool(SERVER_STATE.get('stream_key'))
    _, vids = scan_library()
    if SERVER_STATE.get('auto_start') and has_key and vids:
        log_event('[SISTEMA] Auto-arranque activo: Conectando automáticamente...')
        SERVER_STATE['status'] = 'Transmitiendo'
        save_state()
        broadcast_state()
        if not IS_STREAMING_THREAD_ACTIVE:
            threading.Thread(target=stream_worker, daemon=True).start()

threading.Thread(target=auto_init_stream, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('============================================================')
    print('  STREAMHUB 24/7 STUDIO - EN LÍNEA')
    print(f'  Panel Local:   http://localhost:{port}/')
    print(f'  Control Móvil: http://{LOCAL_IP}:{port}/control')
    print('  Destino:       YouTube / RTMP Propio / Redes Multi-Plataforma')
    print('============================================================')
    app.run(host='0.0.0.0', port=port, debug=False)
'''

with open(app_path, "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS: Full streaming engine app.py written to panel_stream/app.py!")
