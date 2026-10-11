import os, sys, json, socket, subprocess, threading, time, re, base64, shutil
import urllib.request, urllib.parse
from flask import Flask, jsonify, render_template, request, send_from_directory, Response, send_file
from flask_sock import Sock
from PIL import Image, ImageDraw, ImageFont

try:
    import pytchat
    HAS_PYTCHAT = True
except ImportError:
    HAS_PYTCHAT = False

if sys.platform == 'win32':
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024
sock = Sock(app)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_DIR = os.path.join(BASE_DIR, 'bin')
if os.path.exists(BIN_DIR) and BIN_DIR not in os.environ.get('PATH', ''):
    os.environ['PATH'] = BIN_DIR + os.path.pathsep + os.environ.get('PATH', '')

# ESTRUCTURA DE CARPETAS FÍSICAS EN DISCO
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
PLAYLISTS_FOLDER = os.path.join(BASE_DIR, 'playlists')
PREVIEWS_FOLDER = os.path.join(BASE_DIR, 'previews')
RECORDINGS_FOLDER = os.path.join(BASE_DIR, 'recordings')
STICKERS_FOLDER = os.path.join(UPLOAD_FOLDER, 'stickers')
STATE_FILE = os.path.join(BASE_DIR, 'state.json')
STREAM_KEY_FILE = os.path.join(BASE_DIR, 'stream_key.txt')
FACEBOOK_KEY_FILE = os.path.join(BASE_DIR, 'facebook_key.txt')
TWITCH_KEY_FILE = os.path.join(BASE_DIR, 'twitch_key.txt')
TIKTOK_KEY_FILE = os.path.join(BASE_DIR, 'tiktok_key.txt')
TIKTOK_SERVER_FILE = os.path.join(BASE_DIR, 'tiktok_server.txt')
OVERLAY_IMAGE_FILE = os.path.join(BASE_DIR, 'stream_overlay.png')
OVERLAY_CONFIG_FILE = os.path.join(BASE_DIR, 'overlay_config.json')
HISTORY_FILE = os.path.join(BASE_DIR, 'events_history.json')

for d in [UPLOAD_FOLDER, PLAYLISTS_FOLDER, PREVIEWS_FOLDER, RECORDINGS_FOLDER, STICKERS_FOLDER]:
    os.makedirs(d, exist_ok=True)

DEFAULT_CATEGORIES = ['General', 'Oracion', 'Reflexion', 'Musica', 'Lofi_Chill']
for cat in DEFAULT_CATEGORIES:
    os.makedirs(os.path.join(UPLOAD_FOLDER, cat), exist_ok=True)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

LOCAL_IP = get_local_ip()
PROBE_CACHE = {}

def log_event_history(action_type, description, metadata=None):
    entry = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'type': action_type,
        'description': description,
        'metadata': metadata or {}
    }
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except Exception:
            history = []
    history.insert(0, entry)
    if len(history) > 300:
        history = history[:300]
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass

def probe_video(filepath):
    try:
        mtime = os.path.getmtime(filepath)
        if filepath in PROBE_CACHE and PROBE_CACHE[filepath].get('mtime') == mtime:
            return PROBE_CACHE[filepath]['info']
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'stream=codec_type,width,height,duration:format=duration',
            '-of', 'json', filepath
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=8)
        data = json.loads(res.stdout)
        streams = data.get('streams', [])
        video_stream = next((s for s in streams if s.get('codec_type') == 'video'), {})
        has_audio = any(s.get('codec_type') == 'audio' for s in streams)
        w = int(video_stream.get('width', 1080))
        h = int(video_stream.get('height', 1920))
        dur_val = video_stream.get('duration') or data.get('format', {}).get('duration', 0.0)
        try:
            dur = float(dur_val)
        except Exception:
            dur = 0.0
        info = {
            'width': w, 'height': h, 'duration': dur,
            'orientation': 'vertical' if h > w else 'horizontal',
            'has_audio': has_audio
        }
        PROBE_CACHE[filepath] = {'mtime': mtime, 'info': info}
        return info
    except Exception:
        return {'width': 1080, 'height': 1920, 'duration': 0.0, 'orientation': 'vertical', 'has_audio': True}

def scan_library():
    categories, videos = [], []
    if os.path.exists(UPLOAD_FOLDER):
        for entry in os.listdir(UPLOAD_FOLDER):
            cat_path = os.path.join(UPLOAD_FOLDER, entry)
            if os.path.isdir(cat_path):
                categories.append(entry)
                for f in sorted(os.listdir(cat_path)):
                    if f.lower().endswith(('.mp4', '.mkv', '.mov', '.webm', '.avi', '.ts')):
                        p = os.path.join(cat_path, f)
                        try:
                            s = os.path.getsize(p)
                            info = probe_video(p)
                            videos.append({
                                'name': f, 'category': entry, 'path_rel': f'{entry}/{f}',
                                'size_bytes': s, 'size_formatted': f'{(s / (1024*1024)):.1f} MB',
                                'url': f'/videos/{entry}/{f}',
                                'width': info['width'], 'height': info['height'],
                                'duration': info['duration'], 'orientation': info['orientation'],
                                'has_audio': info.get('has_audio', True)
                            })
                        except Exception:
                            pass
    return sorted(categories), videos

DEFAULT_STATE = {
    'status': 'Transmitiendo', 'platform': 'youtube', 'stream_format': 'vertical',
    'active_category': 'General', 'stream_key': 'du9h-3ajm-9e6b-gj2c-5emj',
    'facebook_key': '', 'twitch_key': '', 'tiktok_key': '', 'tiktok_server': 'rtmp://push-rtmp-l01-va.tiktokcdn.com/live/', 'control_url': 'http://172.64.219:5000/control',
    'current_video': 'Iniciando transmisión...',
    'current_video_url': '', 'preview_video_url': '', 'preview_video_name': '',
    'banner_text': '', 'accumulated_minutes': 0.0, 'mode': 'playlist',
    'multistream_targets': {'youtube': True, 'facebook': False, 'twitch': False, 'tiktok': False},
    'auto_start': True, 'logs': [f'[SISTEMA] Servidor activo en http://{LOCAL_IP}:5000'],
    'youtube_video_id': '', 'facebook_live_id': '', 'facebook_access_token': '',
    'youtube_cycle_mode': True, 'cycle_duration_seconds': 42900, 'cycle_elapsed_seconds': 0,
    'monetization_goal': 4000, 'monetization_unit': 'minutos', 'total_monetization_minutes': 0.0,
    'cycle_count': 1, 'auto_switch_24h': True, 'live_viewers': 0, 'peak_viewers': 0,
    'panel_connected_devices': 1, 'chat_messages': [],
    'youtube_chat_active': False, 'facebook_chat_active': False,
    'has_overlay': False, 'overlays': [], 'current_session_id': ''
}

def load_state():
    for f_path, key in [
        (STREAM_KEY_FILE, 'stream_key'), (FACEBOOK_KEY_FILE, 'facebook_key'),
        (TWITCH_KEY_FILE, 'twitch_key'), (TIKTOK_KEY_FILE, 'tiktok_key'), (TIKTOK_SERVER_FILE, 'tiktok_server')
    ]:
        if os.path.exists(f_path):
            try:
                with open(f_path, 'r', encoding='utf-8') as kf:
                    val = kf.read().strip()
                    if val: DEFAULT_STATE[key] = val
            except Exception: pass

    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                DEFAULT_STATE.update(saved)
        except Exception: pass

    if os.path.exists(OVERLAY_CONFIG_FILE):
        try:
            with open(OVERLAY_CONFIG_FILE, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
                DEFAULT_STATE['overlays'] = cfg.get('overlays', [])
                if 'preview_width' in cfg: DEFAULT_STATE['overlay_preview_width'] = float(cfg['preview_width'])
                if 'preview_height' in cfg: DEFAULT_STATE['overlay_preview_height'] = float(cfg['preview_height'])
        except Exception:
            DEFAULT_STATE['overlays'] = []

    DEFAULT_STATE['has_overlay'] = (os.path.exists(OVERLAY_IMAGE_FILE) and os.path.getsize(OVERLAY_IMAGE_FILE) > 0)
    return DEFAULT_STATE

SERVER_STATE = load_state()

def save_state():
    try:
        keys_to_save = [
            'platform', 'stream_format', 'active_category', 'stream_key',
            'facebook_key', 'twitch_key', 'accumulated_minutes', 'mode',
            'banner_text', 'multistream_targets', 'auto_start', 'status',
            'youtube_video_id', 'facebook_live_id', 'facebook_access_token', 'youtube_cycle_mode',
            'cycle_duration_seconds', 'cycle_elapsed_seconds', 'monetization_goal',
            'monetization_unit', 'total_monetization_minutes', 'cycle_count', 'auto_switch_24h',
            'preview_video_url', 'preview_video_name', 'current_video_url', 'has_overlay',
            'current_session_id'
        ]
        data = {k: SERVER_STATE[k] for k in keys_to_save if k in SERVER_STATE}
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        panel_stream_state = os.path.abspath(os.path.join(BASE_DIR, '..', 'panel_stream', 'state.json'))
        if os.path.exists(os.path.dirname(panel_stream_state)):
            try:
                with open(panel_stream_state, 'w', encoding='utf-8') as psf:
                    json.dump(data, psf, indent=2)
            except Exception: pass

        for f_path, val in [
            (STREAM_KEY_FILE, SERVER_STATE.get('stream_key')),
            (FACEBOOK_KEY_FILE, SERVER_STATE.get('facebook_key')),
            (TWITCH_KEY_FILE, SERVER_STATE.get('twitch_key'))
        ]:
            if val:
                with open(f_path, 'w', encoding='utf-8') as kf:
                    kf.write(val.strip())
    except Exception: pass

CURRENT_PROCESS = None
STOP_FLAG = False
CONNECTED_CLIENTS = set()
IS_STREAMING_THREAD_ACTIVE = False
CURRENT_RECORDING_SESSION = None

def kill_process(proc):
    if not proc: return
    try:
        proc.terminate()
        proc.wait(timeout=2)
    except Exception:
        try: proc.kill()
        except Exception: pass

def log_event(msg):
    t = time.strftime('%H:%M:%S')
    SERVER_STATE['logs'].append(f'[{t}] {msg}')
    if len(SERVER_STATE['logs']) > 100: SERVER_STATE['logs'].pop(0)

def broadcast_state():
    cats, vids = scan_library()
    data = dict(SERVER_STATE)
    data['categories'] = cats
    data['videos'] = vids
    data['local_ip'] = LOCAL_IP
    data['control_url'] = SERVER_STATE.get('control_url', 'http://172.64.219:5000/control')
    data['available_ips'] = ['172.64.219', '10.243.28.219', '26.210.81.134', LOCAL_IP, 'localhost']
    data['panel_connected_devices'] = max(1, len(CONNECTED_CLIENTS))
    data['has_overlay'] = (os.path.exists(OVERLAY_IMAGE_FILE) and os.path.getsize(OVERLAY_IMAGE_FILE) > 0)
    data['current_session_id'] = CURRENT_RECORDING_SESSION or ''
    data['overlays'] = SERVER_STATE.get('overlays', [])
    msg = json.dumps({'type': 'state_update', 'state': data})
    for c in list(CONNECTED_CLIENTS):
        try: c.send(msg)
        except Exception: CONNECTED_CLIENTS.discard(c)

def broadcast_chat(chat_item):
    msg = json.dumps({'type': 'chat_message', 'message': chat_item})
    for c in list(CONNECTED_CLIENTS):
        try: c.send(msg)
        except Exception: pass

def parse_hex_or_rgba(col_str, default_alpha=1.0):
    if not col_str:
        return (0, 0, 0, int(255 * default_alpha))
    col_str = str(col_str).strip().lower()
    if col_str.startswith('rgba('):
        m = re.findall(r'[\d\.]+', col_str)
        if len(m) >= 4:
            return (int(float(m[0])), int(float(m[1])), int(float(m[2])), int(float(m[3]) * 255))
    if col_str.startswith('rgb('):
        m = re.findall(r'[\d\.]+', col_str)
        if len(m) >= 3:
            return (int(float(m[0])), int(float(m[1])), int(float(m[2])), int(255 * default_alpha))
    if col_str.startswith('#'):
        h = col_str.lstrip('#')
        if len(h) == 6:
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            return (r, g, b, int(255 * default_alpha))
        elif len(h) == 8:
            r, g, b, a = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16)
            return (r, g, b, a)
    if col_str == 'transparent':
        return (0, 0, 0, 0)
    return (15, 23, 42, int(255 * default_alpha))

def render_composite_overlay(overlays=None, stream_format='vertical', preview_width=None, preview_height=None):
    """Renderiza con máxima nitidez todos los stickers, logos y rótulos en stream_overlay.png con soporte libre 360°, espejo H/V, opacidad y texto libre"""
    try:
        canvas_w, canvas_h = (1080, 1920) if stream_format == 'vertical' else (1920, 1080)
        canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
        active_ovs = overlays if overlays is not None else SERVER_STATE.get('overlays', [])
        visible_ovs = [o for o in active_ovs if o.get('visible', True)]

        if not visible_ovs:
            SERVER_STATE['has_overlay'] = False
            if os.path.exists(OVERLAY_IMAGE_FILE):
                try: os.remove(OVERLAY_IMAGE_FILE)
                except Exception:
                    try:
                        blank = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
                        blank.save(OVERLAY_IMAGE_FILE, 'PNG')
                    except Exception: pass
            return ""

        pw = preview_width or SERVER_STATE.get('overlay_preview_width')
        ph = preview_height or SERVER_STATE.get('overlay_preview_height')
        prev_w = float(pw) if pw else (240.0 if stream_format == 'vertical' else 420.0)
        prev_h = float(ph) if ph else (380.0 if stream_format == 'vertical' else 240.0)
        if prev_w <= 0: prev_w = 240.0
        if prev_h <= 0: prev_h = 380.0

        scale_x = canvas_w / float(prev_w)
        scale_y = canvas_h / float(prev_h)

        for ov in visible_ovs:
            raw_x = float(ov.get('x', 20))
            raw_y = float(ov.get('y', 20))
            raw_w = float(ov.get('width', 100))
            raw_h = float(ov.get('height', 50))
            rot = float(ov.get('rotation', 0))
            flip_h = bool(ov.get('flip_h', False) or (float(ov.get('scaleX', 1)) < 0))
            flip_v = bool(ov.get('flip_v', False) or (float(ov.get('scaleY', 1)) < 0))
            opacity = max(0.0, min(1.0, float(ov.get('opacity', 1.0))))

            x = int(raw_x * scale_x)
            y = int(raw_y * scale_y)
            w = max(16, int(raw_w * scale_x))
            h = max(16, int(raw_h * scale_y))

            ov_type = ov.get('type')
            is_image = (ov_type in ('sticker', 'image', 'logo') or bool(ov.get('image_url')))

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
                if not os.path.exists(fpath):
                    fpath = os.path.join(BASE_DIR, fname)
                if not os.path.exists(fpath) and 'logo' in fname.lower():
                    cand_logo = os.path.join(BASE_DIR, 'logo.png')
                    if os.path.exists(cand_logo):
                        fpath = cand_logo

                if os.path.exists(fpath):
                    try:
                        item_img = Image.open(fpath).convert('RGBA')
                        item_img = item_img.resize((w, h), Image.Resampling.LANCZOS)

                        # Volteado horizontal / vertical
                        if flip_h:
                            item_img = item_img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                        if flip_v:
                            item_img = item_img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

                        # Opacidad del sticker / imagen
                        if opacity < 1.0:
                            r, g, b, a = item_img.split()
                            a = a.point(lambda p: int(p * opacity))
                            item_img = Image.merge('RGBA', (r, g, b, a))

                        # Rotación 360° en torno al centro
                        if rot != 0:
                            item_img = item_img.rotate(-rot, expand=True, resample=Image.Resampling.BICUBIC)
                            rw, rh = item_img.size
                            px = int((x + w / 2.0) - rw / 2.0)
                            py = int((y + h / 2.0) - rh / 2.0)
                            canvas.paste(item_img, (px, py), item_img)
                        else:
                            canvas.paste(item_img, (x, y), item_img)
                    except Exception: pass
            else:
                text = str(ov.get('text', '')).strip()
                if not text: continue
                bg_col = parse_hex_or_rgba(ov.get('bg', '#0f172a'), float(ov.get('bg_opacity', ov.get('opacity', 0.9))))
                text_col = parse_hex_or_rgba(ov.get('color', '#ffffff'), 1.0)
                font_s = max(14, int(float(ov.get('fontSize', 18)) * scale_x))
                try:
                    font = ImageFont.truetype('arial.ttf', font_s)
                except Exception:
                    try:
                        font = ImageFont.truetype('segoeui.ttf', font_s)
                    except Exception:
                        font = ImageFont.load_default()

                # Auto-ajuste de tamaño de fuente para que no se desborde si el usuario encogió el rótulo
                while font_s > 10:
                    try:
                        bbox = p_draw.textbbox((0, 0), text, font=font)
                        tw = bbox[2] - bbox[0]
                        th = bbox[3] - bbox[1]
                        if tw <= (w - 14) and th <= (h - 6):
                            break
                    except Exception:
                        break
                    font_s -= 2
                    try: font = ImageFont.truetype('arial.ttf', font_s)
                    except Exception: break

                pill = Image.new('RGBA', (w, h), (0, 0, 0, 0))
                p_draw = ImageDraw.Draw(pill)
                rad = max(4, int(float(ov.get('borderRadius', 12)) * scale_x))
                bg_raw = str(ov.get('bg', '#0f172a')).strip().lower()
                if bg_col[3] > 0 and bg_raw != 'transparent':
                    p_draw.rounded_rectangle([0, 0, w - 1, h - 1], radius=rad, fill=bg_col)

                border_col = ov.get('borderColor') or ov.get('border_color')
                if border_col:
                    b_col = parse_hex_or_rgba(border_col, 1.0)
                    p_draw.rounded_rectangle([0, 0, w - 1, h - 1], radius=rad, outline=b_col, width=max(1, int(2 * scale_x)))

                try:
                    bbox = p_draw.textbbox((0, 0), text, font=font)
                    tw = bbox[2] - bbox[0]
                    th = bbox[3] - bbox[1]
                except Exception:
                    tw = len(text) * (font_s // 2)
                    th = font_s

                tx = max(4, (w - tw) // 2)
                ty = max(2, (h - th) // 2)

                try:
                    p_draw.text((tx, ty), text, font=font, fill=text_col, embedded_color=True)
                except Exception:
                    p_draw.text((tx, ty), text, font=font, fill=text_col)

                if flip_h:
                    pill = pill.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                if flip_v:
                    pill = pill.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

                if opacity < 1.0:
                    r, g, b, a = pill.split()
                    a = a.point(lambda p: int(p * opacity))
                    pill = Image.merge('RGBA', (r, g, b, a))

                if rot != 0:
                    pill = pill.rotate(-rot, expand=True, resample=Image.Resampling.BICUBIC)
                    rw, rh = pill.size
                    px = int((x + w / 2.0) - rw / 2.0)
                    py = int((y + h / 2.0) - rh / 2.0)
                    canvas.paste(pill, (px, py), pill)
                else:
                    canvas.paste(pill, (x, y), pill)

        canvas.save(OVERLAY_IMAGE_FILE, 'PNG')
        SERVER_STATE['has_overlay'] = True
        return OVERLAY_IMAGE_FILE
    except Exception as e:
        log_event(f"[ERROR RENDERIZANDO OVERLAY] {str(e)}")
        return ""

def build_filter(banner, target_format, has_overlay=False, overlay_input_idx=1):
    is_vertical = (target_format == 'vertical')
    canvas_w, canvas_h = (1080, 1920) if is_vertical else (1920, 1080)
    parts = [f'[0:v]scale={canvas_w}:{canvas_h}:force_original_aspect_ratio=decrease,pad={canvas_w}:{canvas_h}:(ow-iw)/2:(oh-ih)/2:black[v_scaled]']
    curr_v = '[v_scaled]'

    if has_overlay:
        parts.append(f'[{overlay_input_idx}:v]scale={canvas_w}:{canvas_h}[v_ov_scaled]')
        parts.append(f'{curr_v}[v_ov_scaled]overlay=0:0:shortest=1[v_overlaid]')
        curr_v = '[v_overlaid]'

    # Si hay overlay interactivo activo, los rótulos se muestran exactamente como se diseñaron en el lienzo
    if banner and banner.strip() and not has_overlay:
        clean = banner.replace(':', '\\:').replace("'", '')
        font_s = 36 if is_vertical else 28
        y_pos = 'h-180' if is_vertical else 'h-60'
        parts.append(f"{curr_v}drawtext=text='{clean}':fontcolor=white:fontsize={font_s}:box=1:boxcolor=black@0.65:boxborderw=10:x=(w-text_w)/2:y={y_pos}[v_final]")
        curr_v = '[v_final]'

    return '; '.join(parts), curr_v

def get_platform_endpoint(plat, key):
    k = (key or '').strip()
    if not k: return ''
    if k.startswith('rtmp://') or k.startswith('rtmps://'): return k
    if plat == 'youtube': return f'rtmp://a.rtmp.youtube.com/live2/{k}'
    elif plat == 'facebook': return f'rtmps://live-api-s.facebook.com:443/rtmp/{k}'
    elif plat == 'twitch': return f'rtmp://live.twitch.tv/app/{k}'
    elif plat == 'tiktok':
        if k.startswith('rtmp://') or k.startswith('rtmps://'): return k
        srv = (SERVER_STATE.get('tiktok_server', '') or '').strip() or 'rtmp://push-rtmp-l01-va.tiktokcdn.com/live/'
        if not srv.endswith('/'): srv += '/'
        return f'{srv}{k}'
    return k

# COMPILADOR DE FRAGMENTOS EN 1 SOLO VIDEO MP4 MAESTRO (CONCAT DIRECTO)
def compile_recording_session(session_id):
    session_dir = os.path.join(RECORDINGS_FOLDER, session_id)
    if not os.path.exists(session_dir):
        return None
    
    ts_files = sorted([f for f in os.listdir(session_dir) if f.endswith('.ts') and os.path.getsize(os.path.join(session_dir, f)) > 0])
    if not ts_files:
        return None

    concat_list_file = os.path.join(session_dir, 'concat_list.txt')
    with open(concat_list_file, 'w', encoding='utf-8') as f:
        for ts in ts_files:
            abs_path = os.path.join(session_dir, ts).replace('\\', '/')
            f.write(f"file '{abs_path}'\n")

    output_filename = f"Transmision_{session_id}.mp4"
    output_path = os.path.join(RECORDINGS_FOLDER, output_filename)

    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', concat_list_file,
        '-c', 'copy', '-bsf:a', 'aac_adtstoasc',
        output_path
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            log_event_history('RECORDING_COMPILED', f"Video maestro generado con éxito: {output_filename}")
            return output_filename
    except Exception as e:
        log_event(f"[ERROR COMPILANDO GRABACIÓN] {str(e)}")
    return None

def stream_worker():
    global CURRENT_PROCESS, STOP_FLAG, IS_STREAMING_THREAD_ACTIVE, CURRENT_RECORDING_SESSION
    if IS_STREAMING_THREAD_ACTIVE: return
    IS_STREAMING_THREAD_ACTIVE = True
    STOP_FLAG = False

    CURRENT_RECORDING_SESSION = time.strftime('%Y%m%d_%H%M%S')
    session_dir = os.path.join(RECORDINGS_FOLDER, CURRENT_RECORDING_SESSION)
    os.makedirs(session_dir, exist_ok=True)
    chunk_index = 1

    try:
        log_event(f'[SISTEMA] Motor 24/7 en línea. Grabador activo en sesión: {CURRENT_RECORDING_SESSION}')
        log_event_history('STREAM_START', f'Emisión iniciada. Grabación activa: {CURRENT_RECORDING_SESSION}')
        while not STOP_FLAG and SERVER_STATE['status'] == 'Transmitiendo':
            _, all_vids = scan_library()
            active_cat = SERVER_STATE.get('active_category', 'General')
            cat_vids = [v for v in all_vids if v['category'] == active_cat] or all_vids

            if not cat_vids:
                SERVER_STATE['current_video'] = 'Esperando videos en carpeta uploads...'
                broadcast_state()
                time.sleep(3)
                continue

            p_vid = SERVER_STATE.pop('priority_video', None)
            if p_vid:
                matched = [v for v in cat_vids if v.get('name') == p_vid or v.get('path_rel') == p_vid]
                rest = [v for v in cat_vids if v.get('name') != p_vid and v.get('path_rel') != p_vid]
                if matched: cat_vids = matched + rest

            for v in cat_vids:
                if STOP_FLAG or SERVER_STATE['status'] != 'Transmitiendo': break

                v_cat, v_name = v['category'], v['name']
                video_path = os.path.join(UPLOAD_FOLDER, v_cat, v_name)
                SERVER_STATE['current_video'] = f"[{v_cat}] {v_name}"
                SERVER_STATE['current_video_url'] = f"/videos/{v_cat}/{v_name}"
                log_event(f"[24/7 EN DIRECTO] Emitiendo: {v_name}")
                broadcast_state()

                info = probe_video(video_path)
                has_audio = info.get('has_audio', True)
                fmt = SERVER_STATE.get('stream_format', 'vertical')

                has_overlay = (os.path.exists(OVERLAY_IMAGE_FILE) and os.path.getsize(OVERLAY_IMAGE_FILE) > 0)
                ffmpeg_inputs = []
                if SERVER_STATE.get('mode') == 'single_loop':
                    ffmpeg_inputs.extend(['-stream_loop', '-1'])
                ffmpeg_inputs.extend(['-i', video_path])

                current_input_idx = 1
                overlay_idx = None
                if has_overlay:
                    overlay_idx = current_input_idx
                    ffmpeg_inputs.extend(['-loop', '1', '-i', OVERLAY_IMAGE_FILE])
                    current_input_idx += 1

                if has_audio:
                    audio_map = '0:a'
                else:
                    null_idx = current_input_idx
                    ffmpeg_inputs.extend(['-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100'])
                    current_input_idx += 1
                    audio_map = f'{null_idx}:a'

                filter_str, map_v = build_filter(
                    SERVER_STATE.get('banner_text', ''), fmt,
                    has_overlay=has_overlay, overlay_input_idx=overlay_idx
                )

                # ARCHIVO DE GRABACIÓN DE ESTE FRAGMENTO (ESCAPE COMPATIBLE CON WINDOWS)
                chunk_file = os.path.join(session_dir, f"chunk_{chunk_index:04d}.ts")
                chunk_index += 1
                esc_chunk = chunk_file.replace('\\', '/').replace(':', r'\:')

                plat = SERVER_STATE.get('platform', 'youtube')
                targets = []

                if plat == 'multistream':
                    mt = SERVER_STATE.get('multistream_targets', {})
                    for p_name, key_name in [('youtube', 'stream_key'), ('facebook', 'facebook_key'), ('twitch', 'twitch_key'), ('tiktok', 'tiktok_key')]:
                        if mt.get(p_name):
                            t = get_platform_endpoint(p_name, SERVER_STATE.get(key_name))
                            if t: targets.append(f'[f=flv:onfail=ignore]{t}')
                    if not targets:
                        targets.append(f"[f=flv:onfail=ignore]{get_platform_endpoint('youtube', SERVER_STATE.get('stream_key'))}")
                else:
                    k_val = SERVER_STATE.get('stream_key' if plat == 'youtube' else ('facebook_key' if plat == 'facebook' else ('twitch_key' if plat == 'twitch' else 'tiktok_key')))
                    target_url = get_platform_endpoint(plat, k_val) or get_platform_endpoint('youtube', SERVER_STATE.get('stream_key'))
                    targets.append(f"[f=flv:onfail=ignore]{target_url}")

                targets.append(f"[f=mpegts:onfail=ignore]{esc_chunk}")
                output_args = ['-map', map_v, '-map', audio_map, '-f', 'tee', '|'.join(targets)]

                cmd = [
                    'ffmpeg', '-re', '-thread_queue_size', '2048'
                ] + ffmpeg_inputs + [
                    '-filter_complex', filter_str,
                    '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'zerolatency',
                    '-b:v', '3000k', '-maxrate', '3500k', '-bufsize', '6000k',
                    '-pix_fmt', 'yuv420p', '-g', '60', '-keyint_min', '60', '-r', '30',
                    '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-ac', '2',
                    '-tls_verify', '0', '-flvflags', 'no_duration_filesize'
                ] + output_args

                CURRENT_PROCESS = subprocess.Popen(
                    cmd, cwd=BASE_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    universal_newlines=True, encoding='utf-8', errors='replace'
                )

                while CURRENT_PROCESS and CURRENT_PROCESS.poll() is None:
                    if STOP_FLAG:
                        kill_process(CURRENT_PROCESS)
                        break
                    try:
                        line = CURRENT_PROCESS.stdout.readline()
                        if line and ('frame=' in line or 'fps=' in line):
                            if SERVER_STATE['logs'] and SERVER_STATE['logs'][-1].startswith('[EMITIENDO]'):
                                SERVER_STATE['logs'][-1] = f'[EMITIENDO] {line.strip()[:75]}'
                            else:
                                SERVER_STATE['logs'].append(f'[EMITIENDO] {line.strip()[:75]}')
                    except Exception: break
                    time.sleep(0.05)
                    SERVER_STATE['accumulated_minutes'] += (0.05 / 60)

                if CURRENT_PROCESS and CURRENT_PROCESS.poll() != 0 and not STOP_FLAG:
                    time.sleep(1)
    except Exception as e:
        log_event(f'[ERROR MOTOR] {str(e)}')
    finally:
        IS_STREAMING_THREAD_ACTIVE = False
        if CURRENT_RECORDING_SESSION:
            sess_to_compile = CURRENT_RECORDING_SESSION
            threading.Thread(target=lambda: compile_recording_session(sess_to_compile), daemon=True).start()

# =====================================================================
# RUTAS DE GRABACIÓN Y DESCARGA EN 1 SOLO VIDEO MP4
# =====================================================================
@app.route('/api/recordings', methods=['GET'])
def api_get_recordings():
    recordings = []
    if os.path.exists(RECORDINGS_FOLDER):
        for f in sorted(os.listdir(RECORDINGS_FOLDER), reverse=True):
            if f.endswith('.mp4'):
                fp = os.path.join(RECORDINGS_FOLDER, f)
                s = os.path.getsize(fp)
                recordings.append({
                    'filename': f,
                    'size_formatted': f'{(s / (1024*1024)):.1f} MB',
                    'date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(fp))),
                    'download_url': f'/recordings/download/{f}'
                })
    return jsonify({
        'recordings': recordings,
        'active_session': CURRENT_RECORDING_SESSION,
        'is_recording': bool(CURRENT_RECORDING_SESSION and SERVER_STATE.get('status') == 'Transmitiendo')
    })

@app.route('/api/recordings/compile', methods=['POST'])
def api_compile_recording():
    session_id = CURRENT_RECORDING_SESSION
    if not session_id:
        dirs = sorted([d for d in os.listdir(RECORDINGS_FOLDER) if os.path.isdir(os.path.join(RECORDINGS_FOLDER, d))], reverse=True)
        if dirs:
            session_id = dirs[0]
        else:
            return jsonify({'success': False, 'message': 'No hay grabaciones activas registradas'}), 404

    output_file = compile_recording_session(session_id)
    if output_file:
        return jsonify({
            'success': True,
            'message': '¡Video maestro generado con éxito!',
            'filename': output_file,
            'download_url': f'/recordings/download/{output_file}'
        })
    return jsonify({'success': False, 'message': 'Aún no hay fragmentos suficientes para compilar el video'}), 400

@app.route('/recordings/download/<filename>')
def download_recording_file(filename):
    file_path = os.path.join(RECORDINGS_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=filename)
    return jsonify({'error': 'Archivo de video no encontrado'}), 404

@app.route('/api/recordings/delete/<filename>', methods=['POST'])
def api_delete_recording(filename):
    file_path = os.path.join(RECORDINGS_FOLDER, filename)
    if os.path.exists(file_path):
        import gc
        for attempt in range(6):
            try:
                gc.collect()
                os.remove(file_path)
                log_event_history('RECORDING_DELETE', f"Grabación eliminada: {filename}")
                return jsonify({'success': True})
            except Exception:
                time.sleep(0.2)
        return jsonify({'success': False, 'message': 'Archivo en uso por otro proceso'}), 500
    return jsonify({'success': False}), 404

# =====================================================================
# RUTAS DE STICKERS, THEMES, IMÁGENES Y LOGOS
# =====================================================================
@app.route('/logo.png')
def serve_main_logo():
    for p in [BASE_DIR, os.path.join(BASE_DIR, 'static'), os.path.dirname(BASE_DIR)]:
        cand = os.path.join(p, 'logo.png')
        if os.path.exists(cand):
            return send_from_directory(p, 'logo.png')
    return jsonify({'error': 'Logo no encontrado'}), 404

@app.route('/stream_overlay.png')
def serve_stream_overlay():
    if os.path.exists(OVERLAY_IMAGE_FILE) and os.path.getsize(OVERLAY_IMAGE_FILE) > 0:
        resp = send_from_directory(BASE_DIR, 'stream_overlay.png')
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return resp
    # 1x1 transparent PNG
    transparent_1px = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc`\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82'
    return Response(transparent_1px, mimetype='image/png', headers={'Cache-Control': 'no-store'})

@app.route('/stickers/<path:filename>')
def serve_sticker(filename):
    return send_from_directory(STICKERS_FOLDER, filename)

@app.route('/api/stickers', methods=['GET'])
def api_get_stickers():
    files = []
    if os.path.exists(STICKERS_FOLDER):
        for f in sorted(os.listdir(STICKERS_FOLDER)):
            if f.lower().endswith(('.png', '.svg', '.jpg', '.jpeg', '.webp')):
                display_name = os.path.splitext(f)[0].replace('custom_', '').replace('_', ' ')
                files.append({'name': display_name, 'filename': f, 'url': f'/stickers/{f}'})
    return jsonify({'stickers': files})

@app.route('/api/stickers/delete/<path:filename>', methods=['POST'])
def api_delete_sticker(filename):
    safe_fn = os.path.basename(filename)
    fp = os.path.join(STICKERS_FOLDER, safe_fn)
    if os.path.exists(fp):
        try:
            os.remove(fp)
            log_event_history('STICKER_DELETE', f"Sticker eliminado: {safe_fn}")
            return jsonify({'success': True, 'message': 'Sticker eliminado'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    return jsonify({'success': False, 'message': 'Archivo no encontrado'}), 404

@app.route('/api/overlay/upload_image', methods=['POST'])
def api_overlay_upload_image():
    f = request.files.get('image_file') or request.files.get('file') or request.files.get('image')
    if not f or not f.filename:
        return jsonify({'success': False, 'message': 'No se recibió ningún archivo'}), 400
    raw_name = os.path.basename(f.filename)
    safe_base = re.sub(r'[^a-zA-Z0-9_\-.]', '_', raw_name)
    safe_name = f"custom_{int(time.time()*1000)}_{safe_base}"
    dest = os.path.join(STICKERS_FOLDER, safe_name)
    f.save(dest)
    log_event(f"🎨 [OVERLAY] Imagen cargada: {safe_name}")
    log_event_history('STICKER_UPLOAD', f"Sticker o logo subido: {safe_name}")
    return jsonify({
        'success': True,
        'filename': safe_name,
        'url': f'/stickers/{safe_name}',
        'message': 'Imagen guardada con éxito'
    })

@app.route('/api/overlay/config', methods=['GET', 'POST'])
def api_overlay_config():
    if request.method == 'POST':
        body = request.get_json() or {}
        try:
            with open(OVERLAY_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(body, f, indent=2)
            ovs = body.get('overlays', [])
            SERVER_STATE['overlays'] = ovs
            pw = body.get('preview_width')
            ph = body.get('preview_height')
            if pw: SERVER_STATE['overlay_preview_width'] = float(pw)
            if ph: SERVER_STATE['overlay_preview_height'] = float(ph)
            render_composite_overlay(
                ovs,
                SERVER_STATE.get('stream_format', 'vertical'),
                preview_width=pw,
                preview_height=ph
            )
            log_event(f'🎨 [OVERLAY] {len(ovs)} capa(s)/sticker(s) aplicadas a la transmisión.')
            log_event_history('OVERLAY_CONFIG', f'Configuración de stickers/rótulos actualizada ({len(ovs)} capas)')
            
            global CURRENT_PROCESS
            if CURRENT_PROCESS and SERVER_STATE.get('status') == 'Transmitiendo':
                kill_process(CURRENT_PROCESS)

            broadcast_state()
            return jsonify({'success': True, 'message': 'Capas aplicadas a la transmisión en vivo'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error guardando configuración: {str(e)}'}), 500
    else:
        if os.path.exists(OVERLAY_CONFIG_FILE):
            try:
                with open(OVERLAY_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return jsonify(json.load(f))
            except Exception: pass
        return jsonify({
            'overlays': SERVER_STATE.get('overlays', []),
            'preview_width': SERVER_STATE.get('overlay_preview_width', 240),
            'preview_height': SERVER_STATE.get('overlay_preview_height', 380)
        })

@app.route('/api/overlay/clear', methods=['POST'])
def api_clear_overlay():
    SERVER_STATE['has_overlay'] = False
    SERVER_STATE['overlays'] = []
    if os.path.exists(OVERLAY_CONFIG_FILE):
        try:
            with open(OVERLAY_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump({'overlays': []}, f)
        except Exception: pass

    global CURRENT_PROCESS
    if CURRENT_PROCESS and SERVER_STATE.get('status') == 'Transmitiendo':
        kill_process(CURRENT_PROCESS)
        time.sleep(0.3)

    if os.path.exists(OVERLAY_IMAGE_FILE):
        try: os.remove(OVERLAY_IMAGE_FILE)
        except Exception:
            try:
                canvas_w, canvas_h = (1080, 1920) if SERVER_STATE.get('stream_format') == 'vertical' else (1920, 1080)
                blank = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
                blank.save(OVERLAY_IMAGE_FILE, 'PNG')
            except Exception: pass

    log_event('🗑️ [OVERLAY] Overlay eliminado de la transmisión.')
    log_event_history('OVERLAY_CLEAR', 'Overlay eliminado del directo')
    broadcast_state()
    return jsonify({'success': True, 'message': 'Overlay eliminado.'})

@app.route('/api/overlay/get', methods=['GET'])
def api_get_overlay():
    if os.path.exists(OVERLAY_IMAGE_FILE):
        return send_from_directory(BASE_DIR, 'stream_overlay.png')
    return jsonify({'error': 'No overlay disponible'}), 404

@app.route('/api/github/publish', methods=['POST'])
def api_github_publish():
    body = request.get_json() or {}
    commit_msg = body.get('commit_message', 'StreamHub Studio - Publicación directa desde el panel')
    try:
        from scripts.publish_to_github import publish_all_to_github
        panel_dir = os.path.abspath(os.path.join(BASE_DIR, '..', 'panel_stream'))
        if os.path.exists(panel_dir):
            for fname in ['app.py', 'index.html', 'control.html', 'templates/index.html', 'templates/control.html']:
                sf = os.path.join(BASE_DIR, fname)
                df = os.path.join(panel_dir, fname)
                if os.path.exists(sf):
                    os.makedirs(os.path.dirname(df), exist_ok=True)
                    shutil.copy2(sf, df)
        res = publish_all_to_github(source_dir=panel_dir, commit_message=commit_msg)
        log_event_history('GITHUB_PUBLISH', res.get('message', 'Publicado en GitHub'))
        return jsonify(res)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error publicando: {str(e)}'}), 500

# =====================================================================
# CHAT MULTI-PLATAFORMA & AUDIENCIA EN TIEMPO REAL
# =====================================================================
YOUTUBE_CHAT_THREAD = None
YOUTUBE_CHAT_STOP = False
FACEBOOK_CHAT_THREAD = None
FACEBOOK_CHAT_STOP = False

def start_youtube_chat(video_id):
    global YOUTUBE_CHAT_THREAD, YOUTUBE_CHAT_STOP
    if not HAS_PYTCHAT or not video_id: return
    YOUTUBE_CHAT_STOP = True
    time.sleep(0.3)
    YOUTUBE_CHAT_STOP = False

    def chat_worker():
        global YOUTUBE_CHAT_STOP
        vid_clean = video_id.strip()
        m = re.search(r'(?:v=|\/live\/|\.be\/)([a-zA-Z0-9_-]{11})', vid_clean)
        if m: vid_clean = m.group(1)
        SERVER_STATE['youtube_video_id'] = vid_clean
        SERVER_STATE['youtube_chat_active'] = True
        save_state()
        broadcast_state()
        log_event(f'[CHAT YOUTUBE] Conectando a transmisión Live: {vid_clean}...')
        try:
            livechat = pytchat.create(video_id=vid_clean)
            while livechat.is_alive() and not YOUTUBE_CHAT_STOP:
                for c in livechat.get().sync_items():
                    chat_item = {
                        'id': f"yt_{int(time.time()*1000)}_{len(SERVER_STATE.get('chat_messages', []))}",
                        'platform': 'youtube',
                        'author': c.author.name,
                        'author_image': c.author.imageUrl or '',
                        'message': c.message,
                        'datetime': c.datetime,
                        'amount': getattr(c, 'amountString', '') or '',
                        'is_owner': False
                    }
                    SERVER_STATE.setdefault('chat_messages', [])
                    SERVER_STATE['chat_messages'].append(chat_item)
                    if len(SERVER_STATE['chat_messages']) > 150: SERVER_STATE['chat_messages'].pop(0)
                    broadcast_chat(chat_item)
                time.sleep(1.2)
        except Exception as e:
            log_event(f'[CHAT YOUTUBE] Error ({vid_clean}): {str(e)}')
        finally:
            SERVER_STATE['youtube_chat_active'] = False
            broadcast_state()

    YOUTUBE_CHAT_THREAD = threading.Thread(target=chat_worker, daemon=True)
    YOUTUBE_CHAT_THREAD.start()

def start_facebook_chat(fb_live_id, access_token=None):
    global FACEBOOK_CHAT_THREAD, FACEBOOK_CHAT_STOP
    if not fb_live_id: return
    FACEBOOK_CHAT_STOP = True
    time.sleep(0.3)
    FACEBOOK_CHAT_STOP = False

    def fb_worker():
        global FACEBOOK_CHAT_STOP
        clean_id = fb_live_id.strip()
        m = re.search(r'(?:videos\/|watch\/\?v=|live\/)([0-9]+)', clean_id)
        if m: clean_id = m.group(1)
        SERVER_STATE['facebook_live_id'] = clean_id
        SERVER_STATE['facebook_chat_active'] = True
        save_state()
        broadcast_state()
        log_event(f'[CHAT FACEBOOK] Monitoreando comentarios Live: {clean_id}')
        seen_comment_ids = set()
        while not FACEBOOK_CHAT_STOP:
            token = access_token or SERVER_STATE.get('facebook_access_token')
            if token and clean_id:
                try:
                    url = f"https://graph.facebook.com/v19.0/{clean_id}/comments?access_token={token}&order=reverse_chronological&limit=25"
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=5) as r:
                        res = json.loads(r.read().decode('utf-8'))
                        for c in reversed(res.get('data', [])):
                            cid = c.get('id')
                            if cid and cid not in seen_comment_ids:
                                seen_comment_ids.add(cid)
                                chat_item = {
                                    'id': f"fb_{cid}",
                                    'platform': 'facebook',
                                    'author': c.get('from', {}).get('name', 'Usuario Facebook'),
                                    'author_image': '',
                                    'message': c.get('message', ''),
                                    'datetime': time.strftime('%H:%M:%S'),
                                    'amount': '',
                                    'is_owner': False
                                }
                                SERVER_STATE.setdefault('chat_messages', [])
                                SERVER_STATE['chat_messages'].append(chat_item)
                                if len(SERVER_STATE['chat_messages']) > 150: SERVER_STATE['chat_messages'].pop(0)
                                broadcast_chat(chat_item)
                except Exception: pass
            time.sleep(4)

    FACEBOOK_CHAT_THREAD = threading.Thread(target=fb_worker, daemon=True)
    FACEBOOK_CHAT_THREAD.start()

def viewers_monitor():
    while True:
        try:
            yt_vid = SERVER_STATE.get('youtube_video_id')
            if yt_vid and SERVER_STATE.get('status') == 'Transmitiendo':
                url = f"https://www.youtube.com/watch?v={yt_vid}"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                try:
                    with urllib.request.urlopen(req, timeout=4) as r:
                        html = r.read().decode('utf-8', errors='ignore')
                        m = re.search(r'"viewCount":\{"runs":\[\{"text":"([\d.,]+)"\}', html)
                        if m:
                            v_cnt = int(m.group(1).replace(',', '').replace('.', ''))
                            SERVER_STATE['live_viewers'] = v_cnt
                            if v_cnt > SERVER_STATE.get('peak_viewers', 0):
                                SERVER_STATE['peak_viewers'] = v_cnt
                except Exception: pass
            SERVER_STATE['panel_connected_devices'] = max(1, len(CONNECTED_CLIENTS))
        except Exception: pass
        time.sleep(15)

threading.Thread(target=viewers_monitor, daemon=True).start()

def monetization_cycle_worker():
    global CURRENT_PROCESS, STOP_FLAG
    last_save = time.time()
    while True:
        time.sleep(1)
        if SERVER_STATE.get('status') == 'Transmitiendo':
            SERVER_STATE['cycle_elapsed_seconds'] = SERVER_STATE.get('cycle_elapsed_seconds', 0) + 1
            SERVER_STATE['total_monetization_minutes'] = SERVER_STATE.get('total_monetization_minutes', 0.0) + (1.0 / 60.0)
            SERVER_STATE['accumulated_minutes'] = SERVER_STATE.get('accumulated_minutes', 0.0) + (1.0 / 60.0)

            if time.time() - last_save > 30:
                save_state()
                last_save = time.time()

            is_yt = (SERVER_STATE.get('platform') == 'youtube' or SERVER_STATE.get('multistream_targets', {}).get('youtube'))
            if SERVER_STATE.get('youtube_cycle_mode') and is_yt:
                limit = SERVER_STATE.get('cycle_duration_seconds', 11 * 3600 + 55 * 60)
                elapsed = SERVER_STATE.get('cycle_elapsed_seconds', 0)
                if elapsed >= limit:
                    log_event(f"[MONETIZACIÓN YOUTUBE] Ciclo #{SERVER_STATE.get('cycle_count', 1)} alcanzado (11h 55m).")
                    log_event("[MONETIZACIÓN YOUTUBE] Pausando sesión por 15 segundos para procesar VOD en YouTube...")
                    STOP_FLAG = True
                    if CURRENT_PROCESS: kill_process(CURRENT_PROCESS)
                    time.sleep(15)
                    SERVER_STATE['cycle_count'] = SERVER_STATE.get('cycle_count', 1) + 1
                    SERVER_STATE['cycle_elapsed_seconds'] = 0

                    goal = SERVER_STATE.get('monetization_goal', 4000)
                    unit = SERVER_STATE.get('monetization_unit', 'minutos')
                    current_prog = SERVER_STATE.get('total_monetization_minutes', 0.0)
                    compare_prog = current_prog if unit == 'minutos' else (current_prog / 60.0)
                    if compare_prog >= goal:
                        if SERVER_STATE.get('auto_switch_24h', True):
                            SERVER_STATE['youtube_cycle_mode'] = False
                            log_event(f"[MONETIZACIÓN YOUTUBE] ¡META DE {goal} {unit.upper()} LOGRADA! Activando emisión continua 24/7.")

                    save_state()
                    broadcast_state()
                    if SERVER_STATE.get('status') == 'Transmitiendo':
                        STOP_FLAG = False
                        if not IS_STREAMING_THREAD_ACTIVE:
                            threading.Thread(target=stream_worker, daemon=True).start()

threading.Thread(target=monetization_cycle_worker, daemon=True).start()

# =====================================================================
# RUTAS PRINCIPALES DEL PANEL
# =====================================================================
@app.route('/')
def index(): return render_template('index.html')

@app.route('/control')
def control_view(): return render_template('control.html')

@app.route('/videos/<category>/<filename>')
def serve_categorized_video(category, filename):
    return send_from_directory(os.path.join(UPLOAD_FOLDER, category), filename)

@app.route('/api/status', methods=['GET'])
def api_status():
    cats, vids = scan_library()
    d = dict(SERVER_STATE)
    d['categories'] = cats
    d['videos'] = vids
    d['local_ip'] = LOCAL_IP
    d['control_url'] = SERVER_STATE.get('control_url', 'http://172.64.219:5000/control')
    d['available_ips'] = ['172.64.219', '10.243.28.219', '26.210.81.134', LOCAL_IP, 'localhost']
    d['has_overlay'] = (os.path.exists(OVERLAY_IMAGE_FILE) and os.path.getsize(OVERLAY_IMAGE_FILE) > 0)
    d['current_session_id'] = CURRENT_RECORDING_SESSION or ''
    d['overlays'] = SERVER_STATE.get('overlays', [])
    return jsonify(d)

@app.route('/api/test_connection', methods=['POST'])
def api_test_connection():
    body = request.get_json() or {}
    plat = body.get('platform', 'youtube')
    yt_key = body.get('stream_key', '').strip() or SERVER_STATE.get('stream_key', '')
    fb_key = body.get('facebook_key', '').strip() or SERVER_STATE.get('facebook_key', '')
    tw_key = body.get('twitch_key', '').strip() or SERVER_STATE.get('twitch_key', '')

    target = ''
    if plat == 'youtube': target = get_platform_endpoint('youtube', yt_key)
    elif plat == 'facebook': target = get_platform_endpoint('facebook', fb_key)
    elif plat == 'twitch': target = get_platform_endpoint('twitch', tw_key)
    elif plat == 'multistream':
        mt = body.get('multistream_targets', {})
        if mt.get('youtube') and yt_key: target = get_platform_endpoint('youtube', yt_key)
        elif mt.get('facebook') and fb_key: target = get_platform_endpoint('facebook', fb_key)
        elif mt.get('twitch') and tw_key: target = get_platform_endpoint('twitch', tw_key)

    if not target:
        return jsonify({'success': False, 'message': f'Falta ingresar la clave de {plat.upper()}.'})

    cmd = [
        'ffmpeg', '-y', '-t', '3',
        '-f', 'lavfi', '-i', 'color=c=black:s=640x360:r=30',
        '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency',
        '-c:a', 'aac', '-b:a', '64k',
        '-tls_verify', '0', '-f', 'flv', target
    ]

    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=8)
        ok = (proc.returncode == 0)
        log_event_history('TEST_CONNECTION', f"Prueba con {plat.upper()}: {'Exitosa' if ok else 'Fallida'}")
        if ok:
            return jsonify({'success': True, 'message': f'✅ Conexión con {plat.upper()} exitosa y lista para emitir.'})
        return jsonify({'success': False, 'message': f'⚠️ Clave rechazada o directo inactivo en {plat.upper()}.'})
    except subprocess.TimeoutExpired:
        return jsonify({'success': True, 'message': f'✅ Conexión con {plat.upper()} aceptada y fluida.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'❌ Error en prueba: {str(e)}'})

@app.route('/api/category/create', methods=['POST'])
def api_create_category():
    body = request.get_json() or {}
    name = body.get('name', '').strip()
    if name:
        os.makedirs(os.path.join(UPLOAD_FOLDER, name), exist_ok=True)
        log_event_history('CAT_CREATE', f"Nueva lista temática creada: {name}")
        broadcast_state()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

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
            if not ext: ext = '.mp4'
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
            log_event(f'[BIBLIOTECA] Video subido a [{category}]: {safe_name}')
            log_event_history('FILE_UPLOAD', f"Archivo subido: {safe_name} en [{category}]")

    if saved > 0:
        broadcast_state()
        return jsonify({
            'success': True,
            'message': f'¡{saved} video(s) subido(s) correctamente a [{category}]!',
            'files': saved_names
        })
    return jsonify({'success': False, 'message': 'No se recibieron archivos válidos.'}), 400

@app.route('/api/delete/<category>/<path:filename>', methods=['POST'])
def api_delete(category, filename):
    p = os.path.join(UPLOAD_FOLDER, category, filename)
    if os.path.exists(p):
        os.remove(p)
        log_event_history('FILE_DELETE', f"Archivo eliminado: {filename} de [{category}]")
        broadcast_state()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

def handle_control_action(act, body):
    global CURRENT_PROCESS, STOP_FLAG
    if act == 'start':
        STOP_FLAG = False
        SERVER_STATE['status'] = 'Transmitiendo'
        for k in ['platform', 'stream_key', 'facebook_key', 'twitch_key', 'tiktok_key', 'tiktok_server', 'control_url', 'active_category', 'format', 'stream_format']:
            if k in body: SERVER_STATE[k] = body[k]
        if 'multistream_targets' in body:
            SERVER_STATE['multistream_targets'] = body['multistream_targets']
        save_state()
        broadcast_state()
        log_event_history('STREAM_START', f"Transmisión iniciada hacia {SERVER_STATE['platform']}")
        if not IS_STREAMING_THREAD_ACTIVE:
            threading.Thread(target=stream_worker, daemon=True).start()
        return {'success': True, 'message': 'Emisión iniciada.'}

    elif act == 'stop':
        STOP_FLAG = True
        SERVER_STATE['status'] = 'Detenido'
        if CURRENT_PROCESS: kill_process(CURRENT_PROCESS)
        save_state()
        broadcast_state()
        log_event_history('STREAM_STOP', 'Transmisión detenida por el usuario')
        return {'success': True, 'message': 'Emisión detenida.'}

    elif act == 'skip':
        if CURRENT_PROCESS: kill_process(CURRENT_PROCESS)
        log_event_history('VIDEO_SKIP', 'Video saltado al siguiente')
        return {'success': True, 'message': 'Saltando al siguiente video...'}

    elif act == 'play_now':
        cat = body.get('category', 'General')
        name = body.get('name')
        SERVER_STATE['active_category'] = cat
        if name: SERVER_STATE['priority_video'] = name
        log_event_history('PLAY_NOW', f"Emitiendo de inmediato: {name} [{cat}]")
        if CURRENT_PROCESS and SERVER_STATE['status'] == 'Transmitiendo':
            kill_process(CURRENT_PROCESS)
        elif SERVER_STATE['status'] != 'Transmitiendo':
            SERVER_STATE['status'] = 'Transmitiendo'
            STOP_FLAG = False
            save_state()
            broadcast_state()
            if not IS_STREAMING_THREAD_ACTIVE:
                threading.Thread(target=stream_worker, daemon=True).start()
        save_state()
        broadcast_state()
        return {'success': True, 'message': f'Reproduciendo ahora: {name}'}

    elif act == 'set_category':
        SERVER_STATE['active_category'] = body.get('category', 'General')
        if CURRENT_PROCESS and SERVER_STATE['status'] == 'Transmitiendo':
            kill_process(CURRENT_PROCESS)
        save_state()
        broadcast_state()
        return {'success': True, 'message': f'Lista cambiada a: {SERVER_STATE["active_category"]}'}

    elif act == 'switch_format':
        SERVER_STATE['stream_format'] = body.get('format', 'vertical')
        log_event_history('FORMAT_SWITCH', f"Formato cambiado a: {SERVER_STATE['stream_format']}")
        render_composite_overlay(SERVER_STATE.get('overlays', []), SERVER_STATE['stream_format'])
        if CURRENT_PROCESS: kill_process(CURRENT_PROCESS)
        save_state()
        broadcast_state()
        return {'success': True, 'message': f'Formato: {SERVER_STATE["stream_format"]}'}

    elif act == 'toggle_cycle_mode':
        SERVER_STATE['youtube_cycle_mode'] = not SERVER_STATE.get('youtube_cycle_mode', True)
        save_state()
        broadcast_state()
        return {'success': True, 'message': f'Modo Ciclo 11:55: {"Activado" if SERVER_STATE["youtube_cycle_mode"] else "Desactivado (24/7)"}'}

    elif act == 'update_banner':
        SERVER_STATE['banner_text'] = body.get('banner_text', '')
        log_event_history('BANNER_UPDATE', f"Rótulo actualizado: {SERVER_STATE['banner_text']}")
        if CURRENT_PROCESS: kill_process(CURRENT_PROCESS)
        save_state()
        broadcast_state()
        return {'success': True, 'message': 'Rótulo actualizado.'}

    elif act == 'save_keys':
        for k in ['stream_key', 'facebook_key', 'twitch_key', 'tiktok_key', 'tiktok_server', 'control_url', 'platform']:
            if k in body: SERVER_STATE[k] = body[k]
        if 'multistream_targets' in body:
            SERVER_STATE['multistream_targets'] = body['multistream_targets']
        save_state()
        broadcast_state()
        log_event_history('KEYS_SAVE', 'Credenciales RTMP guardadas')
        return {'success': True, 'message': 'Claves guardadas con éxito.'}

    return {'success': True, 'message': 'Acción completada.'}

@app.route('/api/control', methods=['POST'])
def api_control():
    body = request.get_json() or {}
    return jsonify(handle_control_action(body.get('action'), body))

@app.route('/api/preview', methods=['POST'])
def api_preview():
    body = request.get_json() or {}
    cat, name = body.get('category', 'General'), body.get('name')
    if name:
        SERVER_STATE['preview_video_name'] = name
        SERVER_STATE['preview_video_url'] = f"/videos/{cat}/{name}"
        broadcast_state()
        return jsonify({'success': True, 'url': SERVER_STATE['preview_video_url'], 'name': name})
    return jsonify({'success': False, 'message': 'Falta nombre de video'}), 400

@app.route('/api/chat/send', methods=['POST'])
def api_chat_send():
    body = request.get_json() or {}
    platform = body.get('platform', 'youtube')
    message_text = body.get('message', '').strip()
    if not message_text:
        return jsonify({'success': False, 'message': 'Mensaje vacío'}), 400

    SERVER_STATE.setdefault('chat_messages', [])
    chat_item = {
        'id': f"send_{int(time.time()*1000)}",
        'platform': platform,
        'author': 'Canal (Tú)',
        'author_image': '',
        'message': message_text,
        'datetime': time.strftime('%H:%M:%S'),
        'amount': '',
        'is_owner': True
    }
    SERVER_STATE['chat_messages'].append(chat_item)
    if len(SERVER_STATE['chat_messages']) > 150: SERVER_STATE['chat_messages'].pop(0)
    broadcast_chat(chat_item)

    if platform == 'facebook':
        fb_id = SERVER_STATE.get('facebook_live_id')
        token = SERVER_STATE.get('facebook_access_token')
        if fb_id and token:
            def post_fb():
                try:
                    url = f"https://graph.facebook.com/v19.0/{fb_id}/comments"
                    data = urllib.parse.urlencode({'message': message_text, 'access_token': token}).encode('utf-8')
                    req = urllib.request.Request(url, data=data, method='POST')
                    urllib.request.urlopen(req, timeout=5)
                except Exception: pass
            threading.Thread(target=post_fb, daemon=True).start()

    return jsonify({'success': True, 'message': 'Mensaje enviado', 'item': chat_item})

@app.route('/api/chat/connect', methods=['POST'])
def api_chat_connect():
    body = request.get_json() or {}
    yt_vid = body.get('youtube_video_id', '').strip()
    fb_id = body.get('facebook_live_id', '').strip()
    fb_token = body.get('facebook_access_token', '').strip()

    if yt_vid:
        SERVER_STATE['youtube_video_id'] = yt_vid
        start_youtube_chat(yt_vid)
    if fb_id:
        SERVER_STATE['facebook_live_id'] = fb_id
        if fb_token: SERVER_STATE['facebook_access_token'] = fb_token
        start_facebook_chat(fb_id, fb_token)

    save_state()
    broadcast_state()
    return jsonify({
        'success': True,
        'youtube_active': SERVER_STATE.get('youtube_chat_active', False),
        'facebook_active': SERVER_STATE.get('facebook_chat_active', False)
    })

@app.route('/api/chat/webhook/facebook', methods=['GET', 'POST'])
def api_chat_webhook_facebook():
    if request.method == 'GET':
        return request.args.get('hub.challenge') or 'OK'
    body = request.get_json() or {}
    try:
        for entry in body.get('entry', []):
            for change in entry.get('changes', []):
                val = change.get('value', {})
                msg = val.get('message')
                sender = val.get('from', {}).get('name', 'Facebook Live')
                if msg:
                    chat_item = {
                        'id': f"fb_wh_{int(time.time()*1000)}",
                        'platform': 'facebook',
                        'author': sender,
                        'author_image': '',
                        'message': msg,
                        'datetime': time.strftime('%H:%M:%S'),
                        'amount': '',
                        'is_owner': False
                    }
                    SERVER_STATE.setdefault('chat_messages', [])
                    SERVER_STATE['chat_messages'].append(chat_item)
                    if len(SERVER_STATE['chat_messages']) > 150: SERVER_STATE['chat_messages'].pop(0)
                    broadcast_chat(chat_item)
    except Exception: pass
    return jsonify({'status': 'received'})

@app.route('/api/monetization/config', methods=['POST'])
def api_monetization_config():
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

@sock.route('/ws/sync')
def ws_sync(ws):
    CONNECTED_CLIENTS.add(ws)
    try:
        cats, vids = scan_library()
        d = dict(SERVER_STATE)
        d['categories'], d['videos'], d['local_ip'] = cats, vids, LOCAL_IP
        ws.send(json.dumps({'type': 'state_update', 'state': d}))
        while getattr(ws, 'connected', True):
            msg = ws.receive(timeout=10)
            if msg:
                try:
                    data = json.loads(msg)
                    if data.get('action'): handle_control_action(data['action'], data)
                except Exception: pass
            else:
                if getattr(ws, 'connected', True):
                    cats, vids = scan_library()
                    hb = dict(SERVER_STATE)
                    hb['categories'], hb['videos'], hb['local_ip'] = cats, vids, LOCAL_IP
                    ws.send(json.dumps({'type': 'state_update', 'state': hb}))
    except Exception: pass
    finally: CONNECTED_CLIENTS.discard(ws)

def auto_init_stream():
    time.sleep(2.0)
    plat = SERVER_STATE.get('platform', 'youtube')
    has_key = bool(
        SERVER_STATE.get('stream_key') or
        SERVER_STATE.get('facebook_key') or
        SERVER_STATE.get('tiktok_key') or
        SERVER_STATE.get('twitch_key')
    )
    _, vids = scan_library()
    if SERVER_STATE.get('auto_start', True) and has_key and vids:
        log_event(f'[SISTEMA] Auto-arranque activo: Transmisión continua 24/7 iniciada hacia {plat.upper()}.')
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
    print('============================================================')
    app.run(host='0.0.0.0', port=port, debug=False)
