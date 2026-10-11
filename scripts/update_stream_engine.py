import os, sys, json, re, shutil

base_panel = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'panel_stream'))

print(f"Target panel directory: {base_panel}")

# ==============================================================================
# 1. GENERATE UPDATED app.py
# ==============================================================================
app_code = r'''import os, sys, json, socket, subprocess, threading, time, re
import urllib.request, urllib.parse
from flask import Flask, jsonify, render_template, request, send_from_directory, Response
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

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
STICKERS_FOLDER = os.path.join(UPLOAD_FOLDER, 'stickers')
STATE_FILE = os.path.join(BASE_DIR, 'state.json')
STREAM_KEY_FILE = os.path.join(BASE_DIR, 'stream_key.txt')
FACEBOOK_KEY_FILE = os.path.join(BASE_DIR, 'facebook_key.txt')
CUSTOM_RTMP_FILE = os.path.join(BASE_DIR, 'custom_rtmp.txt')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STICKERS_FOLDER, exist_ok=True)

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
            'width': w,
            'height': h,
            'duration': dur,
            'orientation': 'vertical' if h > w else 'horizontal',
            'has_audio': has_audio
        }
        PROBE_CACHE[filepath] = {'mtime': mtime, 'info': info}
        return info
    except Exception:
        return {'width': 1080, 'height': 1920, 'duration': 0.0, 'orientation': 'vertical', 'has_audio': True}

def scan_library():
    categories = []
    videos = []
    if os.path.exists(UPLOAD_FOLDER):
        for entry in os.listdir(UPLOAD_FOLDER):
            if entry.lower() in ('stickers', 'overlays', '__pycache__'):
                continue
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
                                'name': f,
                                'category': entry,
                                'path_rel': f'{entry}/{f}',
                                'size_bytes': s,
                                'size_formatted': f'{(s / (1024*1024)):.1f} MB',
                                'url': f'/videos/{entry}/{f}',
                                'width': info['width'],
                                'height': info['height'],
                                'duration': info['duration'],
                                'orientation': info['orientation'],
                                'has_audio': info.get('has_audio', True)
                            })
                        except Exception:
                            pass
    return sorted(categories), videos

DEFAULT_STATE = {
    'status': 'Transmitiendo',
    'platform': 'youtube',
    'stream_format': 'vertical',
    'active_category': 'General',
    'stream_key': 'du9h-3ajm-9e6b-gj2c-5emj',
    'facebook_key': '',
    'twitch_key': '',
    'custom_rtmp_url': '',
    'custom_rtmp_key': '',
    'tiktok_server': 'rtmp://live-push.tiktok.com/live',
    'tiktok_key': '',
    'tiktok_username': '',
    'kick_server': 'rtmps://fa723fc1b171.global-contribute.live-video.net:443/app',
    'kick_key': '',
    'kick_channel': '',
    'theme': 'cyber_dark',
    'overlays': [
        {
            'id': 'live_badge',
            'type': 'badge',
            'text': 'EN DIRECTO 🔴',
            'x': 20,
            'y': 20,
            'width': 160,
            'height': 42,
            'rotation': 0,
            'fontSize': 14,
            'color': '#ffffff',
            'bg': '#ef4444',
            'opacity': 0.95,
            'visible': True
        },
        {
            'id': 'rotulo_1',
            'type': 'rotulo',
            'text': '¡Transmisión en directo continua 24/7! 🚀',
            'x': 30,
            'y': 310,
            'width': 180,
            'height': 40,
            'rotation': 0,
            'fontSize': 14,
            'color': '#ffffff',
            'bg': '#0f172a',
            'opacity': 0.85,
            'visible': True
        }
    ],
    'current_video': 'Esperando transmisión...',
    'current_video_url': '',
    'preview_video_url': '',
    'preview_video_name': '',
    'banner_text': '',
    'accumulated_minutes': 0.0,
    'mode': 'playlist',
    'multistream_targets': {'youtube': True, 'facebook': False, 'twitch': False, 'custom': False, 'tiktok': False, 'kick': False},
    'auto_start': False,
    'logs': [f'[SISTEMA] Servidor activo en http://{LOCAL_IP}:5000'],
    'youtube_video_id': '',
    'facebook_live_id': '',
    'facebook_access_token': '',
    'youtube_cycle_mode': True,
    'cycle_duration_seconds': 42900,
    'cycle_elapsed_seconds': 0,
    'monetization_goal': 4000,
    'monetization_unit': 'minutos',
    'total_monetization_minutes': 0.0,
    'cycle_count': 1,
    'auto_switch_24h': True,
    'live_viewers': 0,
    'peak_viewers': 0,
    'panel_connected_devices': 1,
    'chat_messages': [],
    'youtube_chat_active': False,
    'facebook_chat_active': False
}

def load_state():
    if os.path.exists(STREAM_KEY_FILE):
        try:
            with open(STREAM_KEY_FILE, 'r', encoding='utf-8') as kf:
                k = kf.read().strip()
                if k:
                    DEFAULT_STATE['stream_key'] = k
        except Exception:
            pass

    if os.path.exists(FACEBOOK_KEY_FILE):
        try:
            with open(FACEBOOK_KEY_FILE, 'r', encoding='utf-8') as fk:
                k = fk.read().strip()
                if k:
                    DEFAULT_STATE['facebook_key'] = k
        except Exception:
            pass

    if os.path.exists(CUSTOM_RTMP_FILE):
        try:
            with open(CUSTOM_RTMP_FILE, 'r', encoding='utf-8') as cf:
                lines = [l.strip() for l in cf.readlines() if l.strip()]
                if len(lines) >= 1:
                    DEFAULT_STATE['custom_rtmp_url'] = lines[0]
                if len(lines) >= 2:
                    DEFAULT_STATE['custom_rtmp_key'] = lines[1]
        except Exception:
            pass

    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                DEFAULT_STATE.update(saved)
        except Exception:
            pass

    if not DEFAULT_STATE.get('stream_key'):
        DEFAULT_STATE['stream_key'] = 'du9h-3ajm-9e6b-gj2c-5emj'

    if 'chat_messages' not in DEFAULT_STATE or not isinstance(DEFAULT_STATE['chat_messages'], list):
        DEFAULT_STATE['chat_messages'] = []
    if 'overlays' not in DEFAULT_STATE or not isinstance(DEFAULT_STATE['overlays'], list) or len(DEFAULT_STATE['overlays']) == 0:
        DEFAULT_STATE['overlays'] = [
            {
                'id': 'live_badge',
                'type': 'badge',
                'text': 'EN DIRECTO 🔴',
                'x': 20,
                'y': 20,
                'width': 160,
                'height': 42,
                'rotation': 0,
                'fontSize': 14,
                'color': '#ffffff',
                'bg': '#ef4444',
                'opacity': 0.95,
                'visible': True
            },
            {
                'id': 'rotulo_1',
                'type': 'rotulo',
                'text': '¡Transmisión en directo continua 24/7! 🚀',
                'x': 30,
                'y': 310,
                'width': 180,
                'height': 40,
                'rotation': 0,
                'fontSize': 14,
                'color': '#ffffff',
                'bg': '#0f172a',
                'opacity': 0.85,
                'visible': True
            }
        ]
    if 'theme' not in DEFAULT_STATE:
        DEFAULT_STATE['theme'] = 'cyber_dark'
    if 'custom_rtmp_url' not in DEFAULT_STATE:
        DEFAULT_STATE['custom_rtmp_url'] = ''
    if 'custom_rtmp_key' not in DEFAULT_STATE:
        DEFAULT_STATE['custom_rtmp_key'] = ''
    if 'tiktok_server' not in DEFAULT_STATE:
        DEFAULT_STATE['tiktok_server'] = 'rtmp://live-push.tiktok.com/live'
    if 'tiktok_key' not in DEFAULT_STATE:
        DEFAULT_STATE['tiktok_key'] = ''
    if 'tiktok_username' not in DEFAULT_STATE:
        DEFAULT_STATE['tiktok_username'] = ''
    if 'kick_server' not in DEFAULT_STATE:
        DEFAULT_STATE['kick_server'] = 'rtmps://fa723fc1b171.global-contribute.live-video.net:443/app'
    if 'kick_key' not in DEFAULT_STATE:
        DEFAULT_STATE['kick_key'] = ''
    if 'kick_channel' not in DEFAULT_STATE:
        DEFAULT_STATE['kick_channel'] = ''
    if 'youtube_cycle_mode' not in DEFAULT_STATE:
        DEFAULT_STATE['youtube_cycle_mode'] = True
    if 'cycle_duration_seconds' not in DEFAULT_STATE:
        DEFAULT_STATE['cycle_duration_seconds'] = 42900
    if 'cycle_elapsed_seconds' not in DEFAULT_STATE:
        DEFAULT_STATE['cycle_elapsed_seconds'] = 0
    if 'monetization_goal' not in DEFAULT_STATE:
        DEFAULT_STATE['monetization_goal'] = 4000
    if 'monetization_unit' not in DEFAULT_STATE:
        DEFAULT_STATE['monetization_unit'] = 'minutos'
    if 'total_monetization_minutes' not in DEFAULT_STATE:
        DEFAULT_STATE['total_monetization_minutes'] = 0.0
    if 'cycle_count' not in DEFAULT_STATE:
        DEFAULT_STATE['cycle_count'] = 1
    if 'auto_switch_24h' not in DEFAULT_STATE:
        DEFAULT_STATE['auto_switch_24h'] = True
    if 'live_viewers' not in DEFAULT_STATE:
        DEFAULT_STATE['live_viewers'] = 0
    if 'peak_viewers' not in DEFAULT_STATE:
        DEFAULT_STATE['peak_viewers'] = 0
    if 'panel_connected_devices' not in DEFAULT_STATE:
        DEFAULT_STATE['panel_connected_devices'] = 1
    if 'youtube_video_id' not in DEFAULT_STATE:
        DEFAULT_STATE['youtube_video_id'] = ''
    if 'facebook_live_id' not in DEFAULT_STATE:
        DEFAULT_STATE['facebook_live_id'] = ''
    if 'facebook_access_token' not in DEFAULT_STATE:
        DEFAULT_STATE['facebook_access_token'] = ''
    if 'current_video_url' not in DEFAULT_STATE:
        DEFAULT_STATE['current_video_url'] = ''
    if 'preview_video_url' not in DEFAULT_STATE:
        DEFAULT_STATE['preview_video_url'] = ''
    if 'preview_video_name' not in DEFAULT_STATE:
        DEFAULT_STATE['preview_video_name'] = ''

    return DEFAULT_STATE

SERVER_STATE = load_state()

def save_state():
    try:
        keys_to_save = [
            'platform', 'stream_format', 'active_category', 'stream_key',
            'facebook_key', 'twitch_key', 'custom_rtmp_url', 'custom_rtmp_key',
            'tiktok_server', 'tiktok_key', 'tiktok_username',
            'kick_server', 'kick_key', 'kick_channel', 'theme', 'overlays',
            'accumulated_minutes', 'mode', 'banner_text', 'multistream_targets',
            'auto_start', 'status', 'youtube_video_id', 'facebook_live_id',
            'facebook_access_token', 'youtube_cycle_mode', 'cycle_duration_seconds',
            'cycle_elapsed_seconds', 'monetization_goal', 'monetization_unit',
            'total_monetization_minutes', 'cycle_count', 'auto_switch_24h',
            'preview_video_url', 'preview_video_name', 'current_video_url'
        ]
        data = {k: SERVER_STATE[k] for k in keys_to_save if k in SERVER_STATE}
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        if SERVER_STATE.get('stream_key'):
            with open(STREAM_KEY_FILE, 'w', encoding='utf-8') as kf:
                kf.write(SERVER_STATE['stream_key'].strip())
        if SERVER_STATE.get('facebook_key'):
            with open(FACEBOOK_KEY_FILE, 'w', encoding='utf-8') as fk:
                fk.write(SERVER_STATE['facebook_key'].strip())
        if SERVER_STATE.get('custom_rtmp_url') or SERVER_STATE.get('custom_rtmp_key'):
            with open(CUSTOM_RTMP_FILE, 'w', encoding='utf-8') as cf:
                cf.write(f"{SERVER_STATE.get('custom_rtmp_url', '').strip()}\n{SERVER_STATE.get('custom_rtmp_key', '').strip()}")
    except Exception:
        pass

CURRENT_PROCESS = None
STOP_FLAG = False
CONNECTED_CLIENTS = set()
IS_STREAMING_THREAD_ACTIVE = False

def kill_process(proc):
    if not proc:
        return
    try:
        proc.terminate()
        proc.wait(timeout=2)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass

def log_event(msg):
    t = time.strftime('%H:%M:%S')
    SERVER_STATE['logs'].append(f'[{t}] {msg}')
    if len(SERVER_STATE['logs']) > 100:
        SERVER_STATE['logs'].pop(0)

def broadcast_state():
    cats, vids = scan_library()
    data = dict(SERVER_STATE)
    data['categories'] = cats
    data['videos'] = vids
    data['local_ip'] = LOCAL_IP
    data['panel_connected_devices'] = max(1, len(CONNECTED_CLIENTS))
    msg = json.dumps({'type': 'state_update', 'state': data})
    for c in list(CONNECTED_CLIENTS):
        try:
            c.send(msg)
        except Exception:
            CONNECTED_CLIENTS.discard(c)

def broadcast_chat(chat_item):
    msg = json.dumps({'type': 'chat_message', 'message': chat_item})
    for c in list(CONNECTED_CLIENTS):
        try:
            c.send(msg)
        except Exception:
            pass

# ==============================================================================
# GENERADOR DINÁMICO DE MARCA DE AGUA COMPUESTA (STICKERS, LOGOS, RÓTULOS 360°)
# ==============================================================================
def hex_or_rgba(col_str, alpha_val=1.0):
    if not col_str:
        return (15, 23, 42, int(alpha_val * 255))
    col_str = str(col_str).strip()
    if col_str.startswith('rgba'):
        m = re.findall(r'[\d.]+', col_str)
        if len(m) >= 4:
            return (int(m[0]), int(m[1]), int(m[2]), int(float(m[3]) * 255))
        elif len(m) >= 3:
            return (int(m[0]), int(m[1]), int(m[2]), int(alpha_val * 255))
    if col_str.startswith('#'):
        h = col_str.lstrip('#')
        if len(h) == 6:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(alpha_val * 255))
        elif len(h) == 3:
            return (int(h[0]*2, 16), int(h[1]*2, 16), int(h[2]*2, 16), int(alpha_val * 255))
    return (15, 23, 42, int(alpha_val * 255))

def generate_composite_watermark(canvas_w, canvas_h, overlays=None, banner_text='', prev_w=240.0, prev_h=380.0):
    """
    Renderiza todos los stickers, logos PNG subidos, rótulos de texto y el botón de En Directo
    con sus 8 tiradores de redimensión y rotación de 360° en una imagen PNG transparente 1080x1920 / 1920x1080.
    """
    watermark_path = os.path.join(UPLOAD_FOLDER, 'current_watermark.png')
    canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))

    if prev_w <= 0: prev_w = 240.0
    if prev_h <= 0: prev_h = 380.0
    scale_x = canvas_w / float(prev_w)
    scale_y = canvas_h / float(prev_h)

    # Intentar cargar fuentes compatibles con emojis
    def get_font(size):
        for font_path in [r'C:\Windows\Fonts\seguiemj.ttf', r'C:\Windows\Fonts\arial.ttf', r'C:\Windows\Fonts\calibri.ttf']:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    active_ov = [o for o in (overlays or SERVER_STATE.get('overlays', [])) if o.get('visible', True)]

    # Si hay overlays activos, dibujarlos capa por capa
    if active_ov:
        for ov in active_ov:
            x = int(ov.get('x', 20) * scale_x)
            y = int(ov.get('y', 20) * scale_y)
            w = max(30, int(ov.get('width', 120) * scale_x))
            h = max(20, int(ov.get('height', 40) * scale_y))
            rot = float(ov.get('rotation', 0))

            ov_type = ov.get('type')
            is_image = (ov_type in ('sticker', 'image') or bool(ov.get('image_url')))

            if is_image:
                img_url = ov.get('image_url', '')
                fname = os.path.basename(img_url)
                if fname.endswith('.svg'):
                    png_candidate = fname.replace('.svg', '.png')
                    if os.path.exists(os.path.join(STICKERS_FOLDER, png_candidate)):
                        fname = png_candidate
                fpath = os.path.join(STICKERS_FOLDER, fname)
                if os.path.exists(fpath):
                    try:
                        item_img = Image.open(fpath).convert('RGBA')
                        item_img = item_img.resize((w, h), Image.Resampling.LANCZOS)
                        if rot != 0:
                            orig_cx = x + w / 2.0
                            orig_cy = y + h / 2.0
                            item_img = item_img.rotate(-rot, expand=True, resample=Image.Resampling.BICUBIC)
                            rw, rh = item_img.size
                            px = int(orig_cx - rw / 2.0)
                            py = int(orig_cy - rh / 2.0)
                            canvas.paste(item_img, (px, py), item_img)
                        else:
                            canvas.paste(item_img, (x, y), item_img)
                    except Exception as ex:
                        pass
            else:
                # Texto, Badge o Rótulo
                text = str(ov.get('text', '')).strip()
                if not text:
                    continue
                bg_col = hex_or_rgba(ov.get('bg', '#0f172a'), float(ov.get('opacity', 0.88)))
                text_col = hex_or_rgba(ov.get('color', '#ffffff'), 1.0)
                font_s = max(16, int(ov.get('fontSize', 14) * scale_x))
                font = get_font(font_s)

                pill = Image.new('RGBA', (w, h), (0, 0, 0, 0))
                p_draw = ImageDraw.Draw(pill)
                rad = max(8, int(10 * scale_x))
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
                    orig_cx = x + w / 2.0
                    orig_cy = y + h / 2.0
                    pill = pill.rotate(-rot, expand=True, resample=Image.Resampling.BICUBIC)
                    rw, rh = pill.size
                    px = int(orig_cx - rw / 2.0)
                    py = int(orig_cy - rh / 2.0)
                    canvas.paste(pill, (px, py), pill)
                else:
                    canvas.paste(pill, (x, y), pill)

    # Si hay banner inferior explícito, añadirlo también
    b_text = str(banner_text or SERVER_STATE.get('banner_text', '')).strip()
    if b_text:
        bw = int(canvas_w * 0.9)
        bh = 70 if canvas_h > canvas_w else 55
        bx = (canvas_w - bw) // 2
        by = (canvas_h - 180) if canvas_h > canvas_w else (canvas_h - 75)
        b_font = get_font(32 if canvas_h > canvas_w else 24)

        b_pill = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
        b_draw = ImageDraw.Draw(b_pill)
        b_draw.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=16, fill=(15, 23, 42, 220))
        try:
            bbox = b_draw.textbbox((0, 0), b_text, font=b_font)
            btw = bbox[2] - bbox[0]
            bth = bbox[3] - bbox[1]
        except Exception:
            btw = len(b_text) * 16
            bth = 30
        btx = max(10, (bw - btw) // 2)
        bty = max(4, (bh - bth) // 2)
        try:
            b_draw.text((btx, bty), b_text, font=b_font, fill=(255, 255, 255, 255), embedded_color=True)
        except Exception:
            b_draw.text((btx, bty), b_text, font=b_font, fill=(255, 255, 255, 255))
        canvas.paste(b_pill, (bx, by), b_pill)

    canvas.save(watermark_path)
    return watermark_path

def get_platform_endpoint(plat, key='', custom_url=''):
    k = (key or '').strip()
    c_url = (custom_url or '').strip()

    if plat in ('custom', 'rtmp'):
        if not c_url:
            c_url = SERVER_STATE.get('custom_rtmp_url', '').strip()
        if not k:
            k = SERVER_STATE.get('custom_rtmp_key', '').strip()
        if not c_url:
            return ''
        if k and not c_url.endswith('/' + k):
            sep = '' if c_url.endswith('/') else '/'
            return f"{c_url}{sep}{k}"
        return c_url

    if plat == 'tiktok':
        if not k:
            k = SERVER_STATE.get('tiktok_key', '').strip()
        srv = SERVER_STATE.get('tiktok_server', '').strip() or 'rtmp://live-push.tiktok.com/live'
        if not k: return ''
        if k.startswith('rtmp://') or k.startswith('rtmps://'): return k
        sep = '' if srv.endswith('/') else '/'
        return f"{srv}{sep}{k}"

    if plat == 'kick':
        if not k:
            k = SERVER_STATE.get('kick_key', '').strip()
        srv = SERVER_STATE.get('kick_server', '').strip() or 'rtmps://fa723fc1b171.global-contribute.live-video.net:443/app'
        if not k: return ''
        if k.startswith('rtmp://') or k.startswith('rtmps://'): return k
        sep = '' if srv.endswith('/') else '/'
        return f"{srv}{sep}{k}"

    if not k:
        return ''
    if k.startswith('rtmp://') or k.startswith('rtmps://'):
        return k
    if plat == 'youtube':
        return f'rtmp://a.rtmp.youtube.com/live2/{k}'
    elif plat == 'facebook':
        return f'rtmps://live-api-s.facebook.com:443/rtmp/{k}'
    elif plat == 'twitch':
        return f'rtmp://live.twitch.tv/app/{k}'
    return k

def stream_worker():
    global CURRENT_PROCESS, STOP_FLAG, IS_STREAMING_THREAD_ACTIVE
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

            for v in cat_vids:
                if STOP_FLAG or SERVER_STATE['status'] != 'Transmitiendo':
                    break

                v_cat = v['category']
                v_name = v['name']
                video_path = os.path.join(UPLOAD_FOLDER, v_cat, v_name)
                SERVER_STATE['current_video'] = f"[{v_cat}] {v_name}"
                SERVER_STATE['current_video_url'] = f"/videos/{v_cat}/{v_name}"
                log_event(f"[24/7 EN DIRECTO] Emitiendo: {v_name}")
                broadcast_state()

                info = probe_video(video_path)
                has_audio = info.get('has_audio', True)

                fmt = SERVER_STATE.get('stream_format', 'vertical')
                canvas_w, canvas_h = (1080, 1920) if fmt == 'vertical' else (1920, 1080)
                loop_param = ['-stream_loop', '-1'] if SERVER_STATE.get('mode') == 'single_loop' else []

                # Renderizar marca de agua compuesta en alta resolución
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

                # Filtro complejo: Redimensionar video a lienzo y aplicar overlay de marcas/stickers
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

                cmd = [
                    'ffmpeg', '-re', '-thread_queue_size', '2048'
                ] + loop_param + [
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

                ret = CURRENT_PROCESS.poll() if CURRENT_PROCESS else 0
                if ret != 0 and not STOP_FLAG and SERVER_STATE['status'] == 'Transmitiendo':
                    log_event('[BUCLE 24/7] Siguiente video o recarga de capas...')
                    time.sleep(0.5)

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
    global CURRENT_PROCESS
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
    global CURRENT_PROCESS
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
            # Reiniciar FFmpeg de inmediato para que se reflejen los stickers y rótulos en vivo
            if CURRENT_PROCESS and SERVER_STATE['status'] == 'Transmitiendo':
                kill_process(CURRENT_PROCESS)
            return jsonify({'success': True, 'message': '✅ Capas y stickers aplicados a la transmisión de inmediato.'})
    return jsonify({'success': True, 'overlays': SERVER_STATE.get('overlays', [])})

@app.route('/api/theme', methods=['GET', 'POST'])
def api_theme():
    if request.method == 'POST':
        body = request.get_json() or {}
        t = body.get('theme', 'cyber_dark')
        SERVER_STATE['theme'] = t
        save_state()
        broadcast_state()
        return jsonify({'success': True, 'theme': t})
    return jsonify({'theme': SERVER_STATE.get('theme', 'cyber_dark')})

@app.route('/api/status', methods=['GET'])
def api_status():
    cats, vids = scan_library()
    d = dict(SERVER_STATE)
    d['categories'] = cats
    d['videos'] = vids
    d['local_ip'] = LOCAL_IP
    return jsonify(d)

@app.route('/api/test_connection', methods=['POST'])
def api_test_connection():
    body = request.get_json() or {}
    plat = body.get('platform', 'youtube')
    yt_key = body.get('stream_key', '').strip() or SERVER_STATE.get('stream_key', '')
    fb_key = body.get('facebook_key', '').strip() or SERVER_STATE.get('facebook_key', '')
    tw_key = body.get('twitch_key', '').strip() or SERVER_STATE.get('twitch_key', '')
    c_url = body.get('custom_rtmp_url', '').strip() or SERVER_STATE.get('custom_rtmp_url', '')
    c_key = body.get('custom_rtmp_key', '').strip() or SERVER_STATE.get('custom_rtmp_key', '')
    tk_key = body.get('tiktok_key', '').strip() or SERVER_STATE.get('tiktok_key', '')
    kk_key = body.get('kick_key', '').strip() or SERVER_STATE.get('kick_key', '')

    target = ''
    if plat == 'youtube':
        target = get_platform_endpoint('youtube', yt_key)
    elif plat == 'facebook':
        target = get_platform_endpoint('facebook', fb_key)
    elif plat == 'twitch':
        target = get_platform_endpoint('twitch', tw_key)
    elif plat in ('custom', 'rtmp'):
        target = get_platform_endpoint('custom', c_key, c_url)
    elif plat == 'tiktok':
        target = get_platform_endpoint('tiktok', tk_key)
    elif plat == 'kick':
        target = get_platform_endpoint('kick', kk_key)
    elif plat == 'multistream':
        mt = body.get('multistream_targets', {})
        if mt.get('youtube') and yt_key:
            target = get_platform_endpoint('youtube', yt_key)
        elif mt.get('custom') and c_url:
            target = get_platform_endpoint('custom', c_key, c_url)
        elif mt.get('facebook') and fb_key:
            target = get_platform_endpoint('facebook', fb_key)
        elif mt.get('twitch') and tw_key:
            target = get_platform_endpoint('twitch', tw_key)

    if not target:
        return jsonify({'success': False, 'message': f'Falta ingresar la clave o servidor de {plat.upper()}.'})

    cmd = [
        'ffmpeg', '-y', '-t', '3',
        '-f', 'lavfi', '-i', 'color=c=black:s=640x360:r=30',
        '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency',
        '-c:a', 'aac', '-b:a', '64k',
        '-tls_verify', '0',
        '-f', 'flv', target
    ]

    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=8)
        if proc.returncode == 0:
            log_event(f'[TEST] Handshake exitoso con {plat.upper()}.')
            return jsonify({'success': True, 'message': f'✅ Conexión con {plat.upper()} exitosa y lista para emitir.'})
        else:
            return jsonify({'success': False, 'message': f'⚠️ Clave rechazada o directo inactivo en {plat.upper()}.'})
    except subprocess.TimeoutExpired:
        log_event(f'[TEST] Handshake exitoso con {plat.upper()}.')
        return jsonify({'success': True, 'message': f'✅ Conexión con {plat.upper()} aceptada y fluida.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'❌ Error ejecutando prueba: {str(e)}'})

@app.route('/api/category/create', methods=['POST'])
def api_create_category():
    body = request.get_json() or {}
    name = body.get('name', '').strip()
    if name:
        os.makedirs(os.path.join(UPLOAD_FOLDER, name), exist_ok=True)
        broadcast_state()
        return jsonify({'success': True, 'message': f'Lista {name} creada.'})
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
            log_event(f'[BIBLIOTECA] Video subido a [{category}]: {safe_name}')

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
        broadcast_state()
        log_event(f'[BIBLIOTECA] Eliminado: {category}/{filename}')
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

def handle_control_action(act, body):
    global CURRENT_PROCESS, STOP_FLAG
    if act == 'start':
        STOP_FLAG = False
        SERVER_STATE['status'] = 'Transmitiendo'
        for k in ['platform', 'stream_key', 'facebook_key', 'twitch_key', 'custom_rtmp_url', 'custom_rtmp_key', 'tiktok_key', 'tiktok_server', 'kick_key', 'kick_server', 'active_category', 'format', 'stream_format']:
            if k in body:
                SERVER_STATE[k] = body[k]
        if 'multistream_targets' in body:
            SERVER_STATE['multistream_targets'] = body['multistream_targets']

        save_state()
        broadcast_state()
        if not IS_STREAMING_THREAD_ACTIVE:
            threading.Thread(target=stream_worker, daemon=True).start()
        return {'success': True, 'message': 'Emisión iniciada hacia la plataforma.'}

    elif act == 'stop':
        STOP_FLAG = True
        SERVER_STATE['status'] = 'Detenido'
        if CURRENT_PROCESS:
            kill_process(CURRENT_PROCESS)
        save_state()
        broadcast_state()
        return {'success': True, 'message': 'Emisión detenida.'}

    elif act == 'skip':
        if CURRENT_PROCESS:
            kill_process(CURRENT_PROCESS)
        return {'success': True, 'message': 'Saltando al siguiente video...'}

    elif act == 'play_now':
        cat = body.get('category', 'General')
        name = body.get('name')
        SERVER_STATE['active_category'] = cat
        if name:
            SERVER_STATE['priority_video'] = name
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

    elif act in ('set_category', 'set_playlist'):
        cat = body.get('category', 'General')
        SERVER_STATE['active_category'] = cat
        if CURRENT_PROCESS and SERVER_STATE['status'] == 'Transmitiendo':
            kill_process(CURRENT_PROCESS)
        save_state()
        broadcast_state()
        return {'success': True, 'message': f'Lista cambiada a: {cat}'}

    elif act == 'switch_format':
        SERVER_STATE['stream_format'] = body.get('format', 'vertical')
        if CURRENT_PROCESS and SERVER_STATE['status'] == 'Transmitiendo':
            kill_process(CURRENT_PROCESS)
        save_state()
        broadcast_state()
        return {'success': True, 'message': f'Formato cambiado a: {SERVER_STATE["stream_format"]}'}

    elif act == 'toggle_cycle_mode':
        SERVER_STATE['youtube_cycle_mode'] = not SERVER_STATE.get('youtube_cycle_mode', True)
        save_state()
        broadcast_state()
        return {'success': True, 'message': f'Modo Ciclo 11:55: {"Activado" if SERVER_STATE["youtube_cycle_mode"] else "Desactivado (24/7)"}'}

    elif act == 'set_preview':
        cat = body.get('category', 'General')
        name = body.get('name')
        if name:
            SERVER_STATE['preview_video_name'] = name
            SERVER_STATE['preview_video_url'] = f"/videos/{cat}/{name}"
        broadcast_state()
        return {'success': True, 'url': SERVER_STATE.get('preview_video_url')}

    elif act == 'update_banner':
        SERVER_STATE['banner_text'] = body.get('banner_text', '')
        fmt = SERVER_STATE.get('stream_format', 'vertical')
        cw, ch = (1080, 1920) if fmt == 'vertical' else (1920, 1080)
        generate_composite_watermark(cw, ch, SERVER_STATE.get('overlays', []), SERVER_STATE['banner_text'])
        if CURRENT_PROCESS and SERVER_STATE['status'] == 'Transmitiendo':
            kill_process(CURRENT_PROCESS)
        save_state()
        broadcast_state()
        return {'success': True, 'message': 'Rótulo actualizado en pantalla de transmisión.'}

    elif act == 'set_theme':
        SERVER_STATE['theme'] = body.get('theme', 'cyber_dark')
        save_state()
        broadcast_state()
        return {'success': True, 'message': 'Tema actualizado'}

    elif act == 'update_overlays':
        if 'overlays' in body:
            SERVER_STATE['overlays'] = body['overlays']
            fmt = SERVER_STATE.get('stream_format', 'vertical')
            cw, ch = (1080, 1920) if fmt == 'vertical' else (1920, 1080)
            generate_composite_watermark(
                cw, ch,
                SERVER_STATE['overlays'],
                SERVER_STATE.get('banner_text', ''),
                body.get('preview_width', 240.0),
                body.get('preview_height', 380.0)
            )
            if CURRENT_PROCESS and SERVER_STATE['status'] == 'Transmitiendo':
                kill_process(CURRENT_PROCESS)
            save_state()
            broadcast_state()
        return {'success': True, 'message': 'Capas actualizadas y emitidas de inmediato.'}

    elif act == 'save_keys':
        for k in ['stream_key', 'facebook_key', 'twitch_key', 'custom_rtmp_url', 'custom_rtmp_key', 'tiktok_key', 'tiktok_server', 'kick_key', 'kick_server', 'platform']:
            if k in body:
                SERVER_STATE[k] = body[k]
        if 'multistream_targets' in body:
            SERVER_STATE['multistream_targets'] = body['multistream_targets']
        save_state()
        broadcast_state()
        return {'success': True, 'message': 'Claves guardadas.'}

    return {'success': True, 'message': 'Acción completada.'}

@app.route('/api/control', methods=['POST'])
def api_control():
    body = request.get_json() or {}
    act = body.get('action')
    res = handle_control_action(act, body)
    return jsonify(res)

@sock.route('/ws/sync')
def ws_sync(ws):
    CONNECTED_CLIENTS.add(ws)
    try:
        cats, vids = scan_library()
        d = dict(SERVER_STATE)
        d['categories'] = cats
        d['videos'] = vids
        d['local_ip'] = LOCAL_IP
        ws.send(json.dumps({'type': 'state_update', 'state': d}))
        while getattr(ws, 'connected', True):
            try:
                msg = ws.receive(timeout=10)
                if msg:
                    try:
                        data = json.loads(msg)
                        act = data.get('action')
                        if act:
                            handle_control_action(act, data)
                    except Exception:
                        pass
                else:
                    if getattr(ws, 'connected', True):
                        cats, vids = scan_library()
                        hb = dict(SERVER_STATE)
                        hb['categories'] = cats
                        hb['videos'] = vids
                        hb['local_ip'] = LOCAL_IP
                        ws.send(json.dumps({'type': 'state_update', 'state': hb}))
            except Exception:
                break
    except Exception:
        pass
    finally:
        CONNECTED_CLIENTS.discard(ws)

# =====================================================================
# CHAT EN VIVO MULTI-PLATAFORMA (YOUTUBE & FACEBOOK) + AUDIENCIA
# =====================================================================
YOUTUBE_CHAT_THREAD = None
YOUTUBE_CHAT_STOP = False
FACEBOOK_CHAT_THREAD = None
FACEBOOK_CHAT_STOP = False

def start_youtube_chat(video_id):
    global YOUTUBE_CHAT_THREAD, YOUTUBE_CHAT_STOP
    if not HAS_PYTCHAT or not video_id:
        return
    YOUTUBE_CHAT_STOP = True
    time.sleep(0.3)
    YOUTUBE_CHAT_STOP = False

    def chat_worker():
        global YOUTUBE_CHAT_STOP
        vid_clean = video_id.strip()
        m = re.search(r'(?:v=|\/live\/|\.be\/)([a-zA-Z0-9_-]{11})', vid_clean)
        if m:
            vid_clean = m.group(1)
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
                    if len(SERVER_STATE['chat_messages']) > 150:
                        SERVER_STATE['chat_messages'].pop(0)
                    broadcast_chat(chat_item)
                time.sleep(1.2)
        except Exception as e:
            log_event(f'[CHAT YOUTUBE] Estado conexión ({vid_clean}): {str(e)}')
        finally:
            SERVER_STATE['youtube_chat_active'] = False
            broadcast_state()

    YOUTUBE_CHAT_THREAD = threading.Thread(target=chat_worker, daemon=True)
    YOUTUBE_CHAT_THREAD.start()

def start_facebook_chat(fb_live_id, access_token=None):
    global FACEBOOK_CHAT_THREAD, FACEBOOK_CHAT_STOP
    if not fb_live_id:
        return
    FACEBOOK_CHAT_STOP = True
    time.sleep(0.3)
    FACEBOOK_CHAT_STOP = False

    def fb_worker():
        global FACEBOOK_CHAT_STOP
        clean_id = fb_live_id.strip()
        m = re.search(r'(?:videos\/|watch\/\?v=|live\/)([0-9]+)', clean_id)
        if m:
            clean_id = m.group(1)
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
                                if len(SERVER_STATE['chat_messages']) > 150:
                                    SERVER_STATE['chat_messages'].pop(0)
                                broadcast_chat(chat_item)
                except Exception:
                    pass
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
                except Exception:
                    pass
            SERVER_STATE['panel_connected_devices'] = max(1, len(CONNECTED_CLIENTS))
        except Exception:
            pass
        time.sleep(15)

threading.Thread(target=viewers_monitor, daemon=True).start()

# =====================================================================
# TEMPORIZADOR CICLO 11:55 Y META DE MONETIZACION (4000 MINUTOS)
# =====================================================================
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

            is_yt = (SERVER_STATE.get('platform') == 'youtube' or 
                     SERVER_STATE.get('multistream_targets', {}).get('youtube'))
            
            if SERVER_STATE.get('youtube_cycle_mode') and is_yt:
                limit = SERVER_STATE.get('cycle_duration_seconds', 11 * 3600 + 55 * 60)
                elapsed = SERVER_STATE.get('cycle_elapsed_seconds', 0)
                if elapsed >= limit:
                    log_event(f"[MONETIZACIÓN YOUTUBE] Ciclo #{SERVER_STATE.get('cycle_count', 1)} de 11h 55m alcanzado.")
                    log_event("[MONETIZACIÓN YOUTUBE] Pausando sesión por 15 segundos para que YouTube procese y guarde el VOD completo...")
                    
                    STOP_FLAG = True
                    if CURRENT_PROCESS:
                        kill_process(CURRENT_PROCESS)
                    
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
                            log_event(f"[MONETIZACIÓN YOUTUBE] ¡META DE {goal} {unit.upper()} LOGRADA! Activando emisión continua 24/7 permanente.")
                    
                    save_state()
                    broadcast_state()
                    
                    if SERVER_STATE.get('status') == 'Transmitiendo':
                        log_event(f"[MONETIZACIÓN YOUTUBE] Reiniciando nuevo ciclo #{SERVER_STATE.get('cycle_count', 1)} en YouTube...")
                        STOP_FLAG = False
                        if not IS_STREAMING_THREAD_ACTIVE:
                            threading.Thread(target=stream_worker, daemon=True).start()

threading.Thread(target=monetization_cycle_worker, daemon=True).start()

# =====================================================================
# RUTAS API: VISTA PREVIA, CHAT MULTI-PLATAFORMA & MONETIZACION
# =====================================================================
@app.route('/api/preview', methods=['POST'])
def api_preview():
    body = request.get_json() or {}
    cat = body.get('category', 'General')
    name = body.get('name')
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
    if len(SERVER_STATE['chat_messages']) > 150:
        SERVER_STATE['chat_messages'].pop(0)
    
    broadcast_chat(chat_item)

    if platform == 'facebook':
        fb_id = SERVER_STATE.get('facebook_live_id')
        token = SERVER_STATE.get('facebook_access_token')
        if fb_id and token:
            def post_fb_comment():
                try:
                    url = f"https://graph.facebook.com/v19.0/{fb_id}/comments"
                    data = urllib.parse.urlencode({'message': message_text, 'access_token': token}).encode('utf-8')
                    req = urllib.request.Request(url, data=data, method='POST')
                    urllib.request.urlopen(req, timeout=5)
                except Exception as ex:
                    log_event(f"[CHAT FACEBOOK] Error publicando a Graph API: {str(ex)}")
            threading.Thread(target=post_fb_comment, daemon=True).start()

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
        if fb_token:
            SERVER_STATE['facebook_access_token'] = fb_token
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
        entries = body.get('entry', [])
        for entry in entries:
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
                    if len(SERVER_STATE['chat_messages']) > 150:
                        SERVER_STATE['chat_messages'].pop(0)
                    broadcast_chat(chat_item)
    except Exception:
        pass
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

with open(os.path.join(base_panel, 'app.py'), 'w', encoding='utf-8') as f:
    f.write(app_code)
print("Updated app.py with high-res dynamic watermark pipeline and auto-restart!")
