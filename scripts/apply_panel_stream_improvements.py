import os, sys, re, json, shutil

print("Starting panel_stream improvements script...")

panel_dir = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream"
app_root = r"C:\Users\Admin\Desktop\chenyz.app"

# ==============================================================================
# 1. COPIAR Y ASEGURAR EL LOGO ORIGINAL NARANJA
# ==============================================================================
logo_src = os.path.join(app_root, "logo.png")
if os.path.exists(logo_src):
    for dst in [
        os.path.join(panel_dir, "logo.png"),
        os.path.join(panel_dir, "static", "logo.png"),
        os.path.join(panel_dir, "uploads", "stickers", "logo_naranja.png"),
    ]:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(logo_src, dst)
        print(f"Logo copiado a: {dst} ({os.path.getsize(dst)} bytes)")

# ==============================================================================
# 2. ACTUALIZAR APP.PY EN PANEL_STREAM
# ==============================================================================
app_py_path = os.path.join(panel_dir, "app.py")
with open(app_py_path, "r", encoding="utf-8") as f:
    app_code = f.read()

# 2.1 Asegurar imports de PIL
if "from PIL import" not in app_code:
    app_code = app_code.replace(
        "from flask import Flask",
        "from PIL import Image, ImageDraw, ImageFont\nfrom flask import Flask"
    )

# 2.2 Asegurar STICKERS_FOLDER
if "STICKERS_FOLDER =" not in app_code:
    app_code = app_code.replace(
        "RECORDINGS_FOLDER = os.path.join(BASE_DIR, 'recordings')",
        "RECORDINGS_FOLDER = os.path.join(BASE_DIR, 'recordings')\nSTICKERS_FOLDER = os.path.join(UPLOAD_FOLDER, 'stickers')\nos.makedirs(STICKERS_FOLDER, exist_ok=True)"
    )

# 2.3 Insertar motor de renderizado de overlays con PIL si no existe
if "def render_composite_overlay(" not in app_code:
    renderer_snippet = '''
def parse_hex_or_rgba(col_str, default_alpha=1.0):
    if not col_str:
        return (0, 0, 0, int(255 * default_alpha))
    col_str = str(col_str).strip().lower()
    if col_str.startswith('rgba('):
        m = re.findall(r'[\\d\\.]+', col_str)
        if len(m) >= 4:
            return (int(float(m[0])), int(float(m[1])), int(float(m[2])), int(float(m[3]) * 255))
    if col_str.startswith('rgb('):
        m = re.findall(r'[\\d\\.]+', col_str)
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

def render_composite_overlay(overlays=None, stream_format='vertical'):
    """Renderiza con nitidez todos los stickers, logos y rótulos en stream_overlay.png"""
    try:
        canvas_w, canvas_h = (1080, 1920) if stream_format == 'vertical' else (1920, 1080)
        canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
        active_ovs = overlays if overlays is not None else SERVER_STATE.get('overlays', [])
        visible_ovs = [o for o in active_ovs if o.get('visible', True)]
        
        if not visible_ovs:
            if os.path.exists(OVERLAY_IMAGE_FILE):
                try: os.remove(OVERLAY_IMAGE_FILE)
                except Exception: pass
            SERVER_STATE['has_overlay'] = False
            return ""

        prev_w = 240.0 if stream_format == 'vertical' else 420.0
        prev_h = 380.0 if stream_format == 'vertical' else 240.0
        scale_x = canvas_w / float(prev_w)
        scale_y = canvas_h / float(prev_h)

        for ov in visible_ovs:
            raw_x = ov.get('x', 20)
            raw_y = ov.get('y', 20)
            raw_w = ov.get('width', 100)
            raw_h = ov.get('height', 50)
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
                if not os.path.exists(fpath):
                    fpath = os.path.join(BASE_DIR, fname)

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
                    except Exception: pass
            else:
                text = str(ov.get('text', '')).strip()
                if not text: continue
                bg_col = parse_hex_or_rgba(ov.get('bg', '#0f172a'), float(ov.get('opacity', 0.9)))
                text_col = parse_hex_or_rgba(ov.get('color', '#ffffff'), 1.0)
                font_s = max(16, int(ov.get('fontSize', 16) * scale_x))
                try:
                    font = ImageFont.truetype('arial.ttf', font_s)
                except Exception:
                    font = ImageFont.load_default()

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

        canvas.save(OVERLAY_IMAGE_FILE, 'PNG')
        SERVER_STATE['has_overlay'] = True
        return OVERLAY_IMAGE_FILE
    except Exception as e:
        log_event(f"[ERROR RENDERIZANDO OVERLAY] {str(e)}")
        return ""
'''
    app_code = app_code.replace("def build_filter(", renderer_snippet + "\ndef build_filter(")

# 2.4 Asegurar escape de chunk_file para muxer tee en Windows
chunk_plain = "targets.append(f\"[f=mpegts:onfail=ignore]{chunk_file}\")"
chunk_escaped = "esc_chunk = chunk_file.replace('\\\\', '/').replace(':', r'\\:')\n                targets.append(f\"[f=mpegts:onfail=ignore]{esc_chunk}\")"
if chunk_plain in app_code:
    app_code = app_code.replace(chunk_plain, chunk_escaped)

# 2.5 Mejorar compile_recording_session para filtrar archivos > 0 bytes
compile_old = "ts_files = sorted([f for f in os.listdir(session_dir) if f.endswith('.ts')])"
compile_new = "ts_files = sorted([f for f in os.listdir(session_dir) if f.endswith('.ts') and os.path.getsize(os.path.join(session_dir, f)) > 0])"
if compile_old in app_code:
    app_code = app_code.replace(compile_old, compile_new)

# 2.6 Mejorar api_overlay_upload_image para aceptar 'image_file', 'file' o 'image'
upload_old = "f = request.files.get('file') or request.files.get('image')"
upload_new = "f = request.files.get('image_file') or request.files.get('file') or request.files.get('image')"
if upload_old in app_code:
    app_code = app_code.replace(upload_old, upload_new)

# 2.7 Actualizar api_overlay_config para invocar render_composite_overlay y refrescar en vivo
old_overlay_config_post = """    if request.method == 'POST':
        body = request.get_json() or {}
        try:
            with open(OVERLAY_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(body, f, indent=2)
            log_event('🎨 [OVERLAY] Capas y stickers guardados.')
            log_event_history('OVERLAY_CONFIG', 'Configuración de stickers/rótulos actualizada')
            broadcast_state()
            return jsonify({'success': True, 'message': 'Configuración de overlay guardada'})"""

new_overlay_config_post = """    if request.method == 'POST':
        body = request.get_json() or {}
        try:
            with open(OVERLAY_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(body, f, indent=2)
            ovs = body.get('overlays', [])
            SERVER_STATE['overlays'] = ovs
            render_composite_overlay(ovs, SERVER_STATE.get('stream_format', 'vertical'))
            log_event(f'🎨 [OVERLAY] {len(ovs)} capa(s)/sticker(s) aplicadas a la transmisión.')
            log_event_history('OVERLAY_CONFIG', f'Configuración de stickers/rótulos actualizada ({len(ovs)} capas)')
            
            global CURRENT_PROCESS
            if CURRENT_PROCESS and SERVER_STATE.get('status') == 'Transmitiendo':
                kill_process(CURRENT_PROCESS)

            broadcast_state()
            return jsonify({'success': True, 'message': 'Capas aplicadas a la transmisión en vivo'})"""

if old_overlay_config_post in app_code:
    app_code = app_code.replace(old_overlay_config_post, new_overlay_config_post)

# 2.8 En api_overlay_config GET, retornar overlays desde SERVER_STATE si existen
old_overlay_config_get = "return jsonify({'overlays': []})"
new_overlay_config_get = "return jsonify({'overlays': SERVER_STATE.get('overlays', [])})"
if old_overlay_config_get in app_code:
    app_code = app_code.replace(old_overlay_config_get, new_overlay_config_get)

# 2.9 Agregar ruta /logo.png y /api/stickers/delete/<filename>
if "@app.route('/logo.png')" not in app_code:
    extra_routes = """
@app.route('/logo.png')
def serve_main_logo():
    for p in [BASE_DIR, os.path.join(BASE_DIR, 'static'), os.path.dirname(BASE_DIR)]:
        cand = os.path.join(p, 'logo.png')
        if os.path.exists(cand):
            return send_from_directory(p, 'logo.png')
    return jsonify({'error': 'Logo no encontrado'}), 404

@app.route('/api/stickers/delete/<path:filename>', methods=['POST'])
def api_delete_sticker(filename):
    safe_fn = os.path.basename(filename)
    stickers_dir = os.path.join(UPLOAD_FOLDER, 'stickers')
    fp = os.path.join(stickers_dir, safe_fn)
    if os.path.exists(fp):
        try:
            os.remove(fp)
            log_event_history('STICKER_DELETE', f"Sticker eliminado: {safe_fn}")
            return jsonify({'success': True, 'message': 'Sticker eliminado'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    return jsonify({'success': False, 'message': 'Archivo no encontrado'}), 404
"""
    app_code = app_code.replace("@app.route('/')", extra_routes + "\n@app.route('/')")

# 2.10 En load_state(), cargar overlays si overlay_config.json existe
if "DEFAULT_STATE['overlays']" not in app_code:
    app_code = app_code.replace(
        "DEFAULT_STATE['has_overlay'] = (os.path.exists(OVERLAY_IMAGE_FILE) and os.path.getsize(OVERLAY_IMAGE_FILE) > 0)",
        """if os.path.exists(OVERLAY_CONFIG_FILE):
        try:
            with open(OVERLAY_CONFIG_FILE, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
                DEFAULT_STATE['overlays'] = cfg.get('overlays', [])
        except Exception:
            DEFAULT_STATE['overlays'] = []
    else:
        DEFAULT_STATE['overlays'] = []
    DEFAULT_STATE['has_overlay'] = (os.path.exists(OVERLAY_IMAGE_FILE) and os.path.getsize(OVERLAY_IMAGE_FILE) > 0)"""
    )

# 2.11 En broadcast_state() y api_status(), enviar 'overlays'
if "data['overlays'] = SERVER_STATE.get('overlays', [])" not in app_code:
    app_code = app_code.replace(
        "data['current_session_id'] = CURRENT_RECORDING_SESSION or ''",
        "data['current_session_id'] = CURRENT_RECORDING_SESSION or ''\n    data['overlays'] = SERVER_STATE.get('overlays', [])"
    )

if "d['overlays'] = SERVER_STATE.get('overlays', [])" not in app_code:
    app_code = app_code.replace(
        "d['current_session_id'] = CURRENT_RECORDING_SESSION or ''\n    return jsonify(d)",
        "d['current_session_id'] = CURRENT_RECORDING_SESSION or ''\n    d['overlays'] = SERVER_STATE.get('overlays', [])\n    return jsonify(d)"
    )

with open(app_py_path, "w", encoding="utf-8") as f:
    f.write(app_code)
print("app.py actualizado con éxito.")

# ==============================================================================
# 3. ACTUALIZAR INDEX.HTML EN PANEL_STREAM Y TEMPLATES
# ==============================================================================
index_path = os.path.join(panel_dir, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index_html = f.read()

# 3.1 Marca / Logo con el color naranja original
brand_icon_old = '<div class="brand-icon">📡</div>'
brand_icon_new = '''<div class="brand-icon" style="background: linear-gradient(135deg, rgba(249, 115, 22, 0.22), rgba(234, 88, 12, 0.38)); border: 1px solid rgba(249, 115, 22, 0.55); box-shadow: 0 0 16px rgba(249, 115, 22, 0.4); border-radius: 12px; display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; overflow: hidden;">
                    <img src="/logo.png" style="width: 30px; height: 30px; object-fit: contain; border-radius: 6px;" alt="Logo" onerror="this.onerror=null; this.outerHTML='<span style=\\'font-size:24px; color:#f97316;\\'>📡</span>';">
                </div>'''

if brand_icon_old in index_html:
    index_html = index_html.replace(brand_icon_old, brand_icon_new)
    print("Logo original naranja integrado en index.html")

# 3.2 Dynamic Stickers Gallery Loader en index.html
if "async function loadStickersGallery()" not in index_html:
    sticker_logic = '''
        /* CARGA DINÁMICA DE STICKERS Y LOGOS DEL PROYECTO */
        async function loadStickersGallery() {
            try {
                const res = await fetch("/api/stickers");
                const data = await res.json();
                const cont = document.getElementById("stickersGallery");
                if (!cont || !data.stickers) return;

                cont.innerHTML = data.stickers.map(stk => {
                    const cleanName = stk.name.replace(/\\.[^/.]+$/, "").replace(/^custom_\\d+_/, "").replace(/_/g, " ");
                    const isCustom = stk.filename && stk.filename.startsWith("custom_");
                    return `
                        <div class="sticker-card" style="position: relative;" onclick="addStickerOverlay('${stk.url}', '${cleanName}')" title="Toca para agregar a la transmisión">
                            <img src="${stk.url}" alt="${cleanName}">
                            <span style="font-size: 10px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${cleanName}</span>
                            ${isCustom ? `
                                <button type="button" onclick="event.stopPropagation(); deleteCustomSticker('${stk.filename}')" 
                                    style="position: absolute; top: -4px; right: -4px; background: #ef4444; color: #fff; border: none; border-radius: 50%; width: 18px; height: 18px; font-size: 9px; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.4);" title="Eliminar sticker">✕</button>
                            ` : ''}
                        </div>
                    `;
                }).join("");
            } catch(e) {
                console.error("Error cargando galería de stickers:", e);
            }
        }

        async function deleteCustomSticker(filename) {
            if (!confirm(`¿Eliminar sticker permanentemente?`)) return;
            try {
                const res = await fetch(`/api/stickers/delete/${encodeURIComponent(filename)}`, { method: "POST" });
                const data = await res.json();
                if (data.success) {
                    showToast("Sticker eliminado");
                    loadStickersGallery();
                }
            } catch(e) {}
        }
    '''
    # Insert before handleOverlayImageUpload
    index_html = index_html.replace(
        "function handleOverlayImageUpload(e) {",
        sticker_logic + "\n        function handleOverlayImageUpload(e) {"
    )

    # In handleOverlayImageUpload, call loadStickersGallery() upon success
    index_html = index_html.replace(
        'showToast("✅ Logo aplicado y transmitido en vivo");',
        'showToast("✅ Logo aplicado y transmitido en vivo");\n                        loadStickersGallery();'
    )

    # In DOMContentLoaded, call loadStickersGallery() and fetch initial overlays
    index_html = index_html.replace(
        'setTimeout(refreshRecordingsList, 1500);',
        'setTimeout(refreshRecordingsList, 1500);\n            setTimeout(loadStickersGallery, 500);'
    )
    print("Lógica dinámica de stickers agregada a index.html")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index_html)

# Copiar a templates/index.html
templates_index = os.path.join(panel_dir, "templates", "index.html")
os.makedirs(os.path.dirname(templates_index), exist_ok=True)
shutil.copy2(index_path, templates_index)
print("index.html y templates/index.html sincronizados con éxito.")

# ==============================================================================
# 4. ACTUALIZAR CONTROL.HTML EN PANEL_STREAM Y TEMPLATES
# ==============================================================================
control_path = os.path.join(panel_dir, "control.html")
with open(control_path, "r", encoding="utf-8") as f:
    ctrl_html = f.read()

# 4.1 Marca / Logo naranja en control.html
ctrl_brand_old = '<span class="brand-icon">📡</span>'
ctrl_brand_new = '''<span class="brand-icon" style="background: linear-gradient(135deg, rgba(249, 115, 22, 0.25), rgba(234, 88, 12, 0.45)); border: 1px solid rgba(249, 115, 22, 0.6); box-shadow: 0 0 12px rgba(249, 115, 22, 0.4); border-radius: 8px; width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center; vertical-align: middle; margin-right: 6px; overflow: hidden;">
                <img src="/logo.png" style="width: 22px; height: 22px; object-fit: contain; border-radius: 4px;" alt="Logo" onerror="this.onerror=null; this.outerHTML='<span style=\\'font-size:18px; color:#f97316;\\'>📡</span>';">
            </span>'''

if ctrl_brand_old in ctrl_html:
    ctrl_html = ctrl_html.replace(ctrl_brand_old, ctrl_brand_new)
    print("Logo naranja integrado en control.html")

# 4.2 Dynamic Stickers Gallery y Capas Activas en control.html
if "async function loadMobileStickers()" not in ctrl_html:
    mobile_stickers_script = '''
        /* CARGA DINÁMICA DE STICKERS EN EL CELULAR */
        async function loadMobileStickers() {
            try {
                const res = await fetch("/api/stickers");
                const data = await res.json();
                const cont = document.querySelector(".stickers-scroll-m");
                if (!cont || !data.stickers) return;

                cont.innerHTML = data.stickers.map(stk => {
                    const cleanName = stk.name.replace(/\\.[^/.]+$/, "").replace(/^custom_\\d+_/, "").replace(/_/g, " ");
                    return `
                        <div class="sticker-card-m" onclick="addStickerMobile('${stk.url}', '${cleanName}')" title="Toca para emitir en directo">
                            <img src="${stk.url}" alt="${cleanName}">
                            <span style="font-size: 10px; color: var(--text-muted); display: block; max-width: 65px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${cleanName}</span>
                        </div>
                    `;
                }).join("");
            } catch(e) {}
        }

        async function refreshMobileActiveOverlays() {
            try {
                const res = await fetch("/api/overlay/config");
                const data = await res.json();
                const cont = document.getElementById("mobileActiveLayersList");
                if (!cont) return;

                const ovs = (data.overlays || []).filter(o => o.visible !== false);
                if (!ovs.length) {
                    cont.innerHTML = '<span style="font-size: 11px; color: var(--text-muted); padding: 4px 8px;">No hay capas activas en pantalla.</span>';
                    return;
                }

                cont.innerHTML = ovs.map(o => `
                    <div style="display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 20px; font-size: 11px; color: #fff;">
                        <span>${o.type === 'rotulo' ? '✍️' : (o.type === 'badge' ? '🔴' : '🎨')} ${o.text || 'Capa'}</span>
                        <button type="button" onclick="removeOverlayMobile('${o.id}')" style="background: none; border: none; color: #f87171; font-weight: bold; cursor: pointer; padding: 0 2px;">✕</button>
                    </div>
                `).join("");
            } catch(e) {}
        }

        async function removeOverlayMobile(id) {
            try {
                const res = await fetch("/api/overlay/config");
                const d = await res.json();
                const filtered = (d.overlays || []).filter(o => o.id !== id);
                await fetch("/api/overlay/config", {
                    method: "POST", headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ overlays: filtered })
                });
                if (typeof notify === "function") notify("Capa eliminada");
                refreshMobileActiveOverlays();
            } catch(e) {}
        }
    '''

    ctrl_html = ctrl_html.replace(
        "function addStickerMobile(url, name) {",
        mobile_stickers_script + "\n        function addStickerMobile(url, name) {"
    )

    # In addStickerMobile and addRotuloMobile, call refreshMobileActiveOverlays()
    ctrl_html = ctrl_html.replace(
        '.then(() => notify(`Sticker \'${name}\' agregado`));',
        '.then(() => { notify(`Sticker \'${name}\' agregado`); refreshMobileActiveOverlays(); });'
    )
    ctrl_html = ctrl_html.replace(
        '.then(() => notify("Rótulo agregado a la transmisión"));',
        '.then(() => { notify("Rótulo agregado a la transmisión"); refreshMobileActiveOverlays(); });'
    )

    # In handleMobileLogoUpload, refresh stickers & layers
    ctrl_html = ctrl_html.replace(
        'if (typeof notify === "function") notify("✅ Logo aplicado y transmitido en vivo");',
        'if (typeof notify === "function") notify("✅ Logo aplicado y transmitido en vivo");\n                        loadMobileStickers();\n                        refreshMobileActiveOverlays();'
    )

    # In DOMContentLoaded, call loadMobileStickers() and refreshMobileActiveOverlays()
    ctrl_html = ctrl_html.replace(
        "setTimeout(refreshRecordingsList, 1500);",
        "setTimeout(refreshRecordingsList, 1500);\n        setTimeout(loadMobileStickers, 500);\n        setTimeout(refreshMobileActiveOverlays, 800);"
    )

    # Add mobileActiveLayersList container inside STICKERS Y RÓTULOS card
    target_card_end = '<!-- RTMP PROPIO Y MULTI-REDES DESDE EL CELULAR -->'
    layers_markup = '''    <!-- CAPAS ACTIVAS EN PANTALLA (CONTROL MÓVIL) -->
    <div style="margin-top: 10px; padding: 10px; background: rgba(0,0,0,0.25); border-radius: 8px;">
        <span style="font-size: 10px; font-weight: 800; color: var(--text-muted); text-transform: uppercase; display: block; margin-bottom: 6px;">
            Capas Transmitiendo en Vivo:
        </span>
        <div id="mobileActiveLayersList" style="display: flex; flex-wrap: wrap; gap: 6px;">
            <span style="font-size: 11px; color: var(--text-muted); padding: 4px;">Cargando capas...</span>
        </div>
    </div>
'''
    ctrl_html = ctrl_html.replace(target_card_end, layers_markup + "\n    " + target_card_end)
    print("Controles móviles dinámicos agregados a control.html")

with open(control_path, "w", encoding="utf-8") as f:
    f.write(ctrl_html)

# Copiar a templates/control.html
templates_ctrl = os.path.join(panel_dir, "templates", "control.html")
os.makedirs(os.path.dirname(templates_ctrl), exist_ok=True)
shutil.copy2(control_path, templates_ctrl)
print("control.html y templates/control.html sincronizados con éxito.")

print("All improvements applied successfully!")
