import os

def build_control_html():
    return r'''<!DOCTYPE html>
<html lang="es" data-theme="cyber_dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="theme-color" content="#030712">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>StreamHub - Mando Remoto 24/7 & Monetización</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #030712;
            --bg-surface: #0a101f;
            --bg-card: rgba(15, 23, 42, 0.92);
            --border: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(56, 189, 248, 0.4);
            --primary: #0284c7;
            --primary-glow: #38bdf8;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        /* 7 TEMAS MOVIL */
        [data-theme="twitch_purple"] {
            --bg-base: #0b0416;
            --bg-surface: #17092c;
            --bg-card: rgba(26, 14, 46, 0.92);
            --border: rgba(192, 132, 252, 0.15);
            --border-glow: rgba(192, 132, 252, 0.45);
            --primary: #9333ea;
            --primary-glow: #c084fc;
        }

        [data-theme="yt_crimson"] {
            --bg-base: #0e0507;
            --bg-surface: #1f0a0e;
            --bg-card: rgba(36, 14, 19, 0.92);
            --border: rgba(239, 68, 68, 0.15);
            --border-glow: rgba(239, 68, 68, 0.45);
            --primary: #dc2626;
            --primary-glow: #f87171;
        }

        [data-theme="kick_matrix"] {
            --bg-base: #040d07;
            --bg-surface: #0a1f11;
            --bg-card: rgba(12, 33, 19, 0.92);
            --border: rgba(16, 185, 129, 0.18);
            --border-glow: rgba(16, 185, 129, 0.5);
            --primary: #059669;
            --primary-glow: #34d399;
        }

        [data-theme="oled_black"] {
            --bg-base: #000000;
            --bg-surface: #0a0a0a;
            --bg-card: rgba(18, 18, 18, 0.95);
            --border: rgba(255, 255, 255, 0.12);
            --border-glow: rgba(255, 255, 255, 0.35);
            --primary: #2563eb;
            --primary-glow: #60a5fa;
        }

        [data-theme="sunset_gold"] {
            --bg-base: #0f0a05;
            --bg-surface: #1c1308;
            --bg-card: rgba(33, 22, 12, 0.92);
            --border: rgba(245, 158, 11, 0.18);
            --border-glow: rgba(245, 158, 11, 0.5);
            --primary: #d97706;
            --primary-glow: #fbbf24;
        }

        [data-theme="titanium_light"] {
            --bg-base: #f1f5f9;
            --bg-surface: #e2e8f0;
            --bg-card: rgba(255, 255, 255, 0.95);
            --border: rgba(0, 0, 0, 0.1);
            --border-glow: rgba(2, 132, 199, 0.35);
            --primary: #0284c7;
            --primary-glow: #0284c7;
            --text-main: #0f172a;
            --text-muted: #64748b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background: var(--bg-base);
            color: var(--text-main);
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            min-height: 100vh;
            padding: calc(env(safe-area-inset-top, 12px) + 8px) 14px calc(env(safe-area-inset-bottom, 20px) + 40px);
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-width: 540px;
            margin: 0 auto;
            transition: background 0.3s ease, color 0.3s ease;
        }

        /* CABECERA */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
            gap: 8px;
            flex-wrap: wrap;
        }

        .header-brand {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .brand-icon {
            font-size: 22px;
            filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.5));
        }

        .header-brand h1 {
            font-size: 16px;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -0.3px;
        }

        .status-pill-group {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .net-status {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 4px 8px;
            border-radius: 999px;
            font-size: 10px;
            font-weight: 700;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border);
            color: var(--text-muted);
            transition: all 0.3s ease;
        }

        .net-status.online {
            background: rgba(16, 185, 129, 0.15);
            border-color: rgba(16, 185, 129, 0.35);
            color: #34d399;
        }

        .net-status.offline {
            background: rgba(239, 68, 68, 0.15);
            border-color: rgba(239, 68, 68, 0.35);
            color: #f87171;
        }

        .pulse-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: currentColor;
            box-shadow: 0 0 8px currentColor;
            animation: pulse-dot 1.8s infinite;
        }

        @keyframes pulse-dot {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.3); opacity: 0.6; }
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 5px 10px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 800;
            background: rgba(148, 163, 184, 0.15);
            color: #94a3b8;
            border: 1px solid rgba(148, 163, 184, 0.25);
        }

        .status-badge.live {
            background: rgba(239, 68, 68, 0.2);
            color: #f87171;
            border-color: rgba(239, 68, 68, 0.5);
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.4);
        }

        .theme-select-m {
            background: var(--bg-surface); color: var(--text-main); border: 1px solid var(--border);
            border-radius: 8px; padding: 4px 8px; font-size: 10px; font-weight: 700; outline: none;
        }

        /* TARJETAS */
        .card {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 14px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }

        .card-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            font-weight: 800;
            color: var(--text-muted);
            letter-spacing: 0.4px;
            margin-bottom: 10px;
            text-transform: uppercase;
        }

        /* VIDEO ACTUAL */
        .current-video-box {
            background: rgba(3, 7, 18, 0.7);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 12px;
            padding: 10px 12px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .current-video-title {
            font-size: 13px;
            font-weight: 700;
            color: #fff;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            flex: 1;
        }

        /* TELEMETRIA */
        .telemetry-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 6px;
        }

        .tele-box {
            background: rgba(3, 7, 18, 0.6);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 8px 4px;
            text-align: center;
        }

        .tele-label {
            font-size: 9px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 700;
        }

        .tele-val {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 700;
            color: var(--primary-glow);
            margin-top: 2px;
        }

        /* MONETIZACION Y CICLO 11:55 */
        .mono-card {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.12), rgba(2, 132, 199, 0.1));
            border: 1px solid rgba(239, 68, 68, 0.35);
        }

        .mono-timer-display {
            font-family: 'JetBrains Mono', monospace;
            font-size: 20px;
            font-weight: 800;
            color: #f87171;
            letter-spacing: 0.5px;
        }

        .progress-track {
            height: 8px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 999px;
            overflow: hidden;
            margin: 6px 0;
        }

        .progress-bar-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #ef4444, #f97316, #10b981);
            border-radius: 999px;
            transition: width 0.3s ease;
        }

        /* BOTONES DE CONTROL */
        .btn-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }

        .btn {
            appearance: none;
            border: none;
            border-radius: 12px;
            padding: 13px 12px;
            font-size: 13px;
            font-weight: 800;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 7px;
            transition: all 0.18s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            touch-action: manipulation;
        }

        .btn:active { transform: scale(0.96); }

        .btn-start {
            grid-column: span 2;
            background: linear-gradient(135deg, #059669, #10b981);
            color: #fff;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.4);
            font-size: 14px;
            padding: 15px;
        }

        .btn-stop {
            grid-column: span 2;
            background: linear-gradient(135deg, #dc2626, #ef4444);
            color: #fff;
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
            font-size: 14px;
            padding: 15px;
        }

        .btn-action {
            background: rgba(30, 41, 59, 0.9);
            color: #f8fafc;
            border: 1px solid rgba(255, 255, 255, 0.12);
        }

        .btn-fmt {
            background: rgba(2, 132, 199, 0.18);
            color: var(--primary-glow);
            border: 1px solid rgba(56, 189, 248, 0.35);
        }

        /* SUBIDA */
        .upload-dropzone {
            border: 2px dashed rgba(56, 189, 248, 0.45);
            background: rgba(2, 132, 199, 0.08);
            border-radius: 14px;
            padding: 18px 14px;
            text-align: center;
            cursor: pointer;
        }

        .upload-dropzone:active {
            background: rgba(2, 132, 199, 0.16);
            transform: scale(0.98);
        }

        .upload-icon { font-size: 30px; margin-bottom: 4px; }
        .upload-title { font-size: 14px; font-weight: 800; color: #fff; }
        .upload-sub { font-size: 11px; color: var(--text-muted); margin-top: 3px; }

        .progress-wrap {
            margin-top: 10px; display: none; background: rgba(3, 7, 18, 0.7);
            border-radius: 10px; padding: 10px; border: 1px solid rgba(56, 189, 248, 0.3);
        }

        /* CHAT MOVIL */
        .chat-box-mobile {
            height: 200px; overflow-y: auto; display: flex; flex-direction: column;
            gap: 6px; padding: 8px; background: rgba(3, 7, 18, 0.7); border-radius: 10px;
            border: 1px solid var(--border); margin-bottom: 8px;
        }

        .chat-msg-m {
            font-size: 11px; line-height: 1.35; padding: 5px 8px;
            border-radius: 6px; background: rgba(255, 255, 255, 0.03);
        }

        .cat-scroll {
            display: flex; gap: 6px; overflow-x: auto; padding-bottom: 6px;
            scrollbar-width: none; -webkit-overflow-scrolling: touch;
        }
        .cat-scroll::-webkit-scrollbar { display: none; }

        .btn-cat {
            appearance: none; border: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.05); color: var(--text-muted);
            padding: 6px 12px; border-radius: 999px; font-size: 12px; font-weight: 700;
            white-space: nowrap; cursor: pointer;
        }
        .btn-cat.active {
            background: rgba(2, 132, 199, 0.25); border-color: var(--primary-glow);
            color: var(--primary-glow);
        }

        .playlist { list-style: none; display: flex; flex-direction: column; gap: 6px; max-height: 240px; overflow-y: auto; margin-top: 8px; }
        .playlist-item {
            display: flex; align-items: center; justify-content: space-between;
            background: rgba(3, 7, 18, 0.6); border: 1px solid var(--border);
            border-radius: 10px; padding: 8px 10px; gap: 8px;
        }

        .video-meta { display: flex; align-items: center; gap: 8px; overflow: hidden; flex: 1; }
        .video-name { font-size: 12px; font-weight: 700; color: #f8fafc; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

        .btn-icon-sm {
            background: rgba(255, 255, 255, 0.06); border: 1px solid var(--border);
            color: #fff; padding: 5px 8px; border-radius: 8px; font-size: 11px;
            cursor: pointer; display: inline-flex; align-items: center; gap: 4px;
        }
        .btn-icon-sm.play { color: #34d399; border-color: rgba(16, 185, 129, 0.3); }
        .btn-icon-sm.del { color: #f87171; border-color: rgba(239, 68, 68, 0.3); }

        .input-text {
            width: 100%; background: rgba(15, 23, 42, 0.9); border: 1px solid var(--border);
            border-radius: 10px; padding: 10px 12px; color: #fff; font-size: 13px; outline: none;
        }

        .stickers-scroll-m {
            display: flex; gap: 6px; overflow-x: auto; padding: 6px 2px;
            scrollbar-width: none;
        }
        .stickers-scroll-m::-webkit-scrollbar { display: none; }
        .sticker-card-m {
            background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border);
            border-radius: 8px; padding: 6px; cursor: pointer; text-align: center;
            min-width: 54px; flex-shrink: 0;
        }
        .sticker-card-m img { width: 28px; height: 28px; object-fit: contain; margin: 0 auto 2px; display: block; }
        .sticker-card-m span { font-size: 9px; font-weight: 700; color: var(--text-muted); }

        .toast {
            position: fixed; top: 18px; left: 50%; transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.96); border: 1px solid #38bdf8;
            color: #fff; padding: 10px 20px; border-radius: 999px; font-size: 12px;
            font-weight: 700; opacity: 0; pointer-events: none; transition: all 0.25s ease;
            z-index: 1000; box-shadow: 0 10px 30px rgba(0,0,0,0.8); text-align: center; max-width: 90vw;
        }
        .toast.show { opacity: 1; transform: translate(-50%, 4px); }
    </style>
</head>
<body>
    <!-- CABECERA -->
    <div class="header">
        <div class="header-brand">
            <span class="brand-icon">📡</span>
            <h1>StreamHub Mando</h1>
        </div>
        <div class="status-pill-group">
            <select id="mobileThemeSelector" class="theme-select-m" onchange="changeTheme(this.value)">
                <option value="cyber_dark">🌌 Cyber Dark</option>
                <option value="twitch_purple">🟣 Twitch</option>
                <option value="yt_crimson">🔴 YouTube</option>
                <option value="kick_matrix">🟢 Kick</option>
                <option value="oled_black">⬛ OLED</option>
                <option value="sunset_gold">🌅 Sunset</option>
                <option value="titanium_light">⚪ Titanium</option>
            </select>
            <span class="net-status online" id="netBadge">
                <span class="pulse-dot"></span>
                <span id="netText">En vivo</span>
            </span>
            <span class="status-badge" id="badgeStatus">DETENIDO ⚪</span>
        </div>
    </div>

    <!-- TARJETA EN DIRECTO AHORA & AUDIENCIA -->
    <div class="card">
        <div class="card-head">
            <span>🔴 EN EMISIÓN AHORA</span>
            <span id="txtFormatBadge" style="color: var(--primary-glow);">Vertical 9:16</span>
        </div>

        <div class="current-video-box">
            <span style="font-size: 18px;">🎬</span>
            <div class="current-video-title" id="txtVideo">Cargando transmisión...</div>
        </div>

        <div class="telemetry-row">
            <div class="tele-box">
                <div class="tele-label">👁️ En Vivo</div>
                <div class="tele-val" id="txtViewers" style="color: #34d399;">0</div>
            </div>
            <div class="tele-box">
                <div class="tele-label">Salida</div>
                <div class="tele-val" id="txtBitrate">~3,100k</div>
            </div>
            <div class="tele-box">
                <div class="tele-label">FPS</div>
                <div class="tele-val" id="txtFps">30.0</div>
            </div>
            <div class="tele-box">
                <div class="tele-label">Videos</div>
                <div class="tele-val" id="txtQueue">0 vids</div>
            </div>
        </div>
    </div>

    <!-- SECCIÓN MONETIZACIÓN YOUTUBE: CICLO 11:55 Y 4000 MINUTOS -->
    <div class="card mono-card">
        <div class="card-head">
            <span>🎯 MONETIZACIÓN YOUTUBE (CICLO 11:55)</span>
            <button type="button" class="btn-icon-sm" id="btnToggleCycleMobile" onclick="toggleCycleModeMobile()" style="color: #f87171;">
                🔘 Ciclo 11h55m
            </button>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <div>
                <span style="font-size: 10px; font-weight: 700; color: var(--text-muted);">RESTANTE CICLO ACTUAL:</span>
                <div class="mono-timer-display" id="mobileCycleTimer">11:55:00</div>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 10px; font-weight: 700; color: var(--text-muted);">PROGRESO META:</span>
                <div style="font-size: 13px; font-weight: 800; color: #10b981;" id="mobileMonetizationGoal">0 / 4,000 min</div>
            </div>
        </div>

        <div class="progress-track">
            <div class="progress-bar-fill" id="mobileCycleProgressBar"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 10px; color: var(--text-muted);">
            <span id="mobileCycleNumber">Ciclo #1</span>
            <span id="mobileCyclePct">0% ciclo</span>
            <span>Reinicio VOD 11:55</span>
        </div>
    </div>

    <!-- CONTROLES PRINCIPALES -->
    <div class="card">
        <div class="card-head">
            <span>⚡ CONTROLES DE EMISIÓN</span>
        </div>
        <div class="btn-grid">
            <button type="button" class="btn btn-start" id="btnStart" onclick="apiCall('start')">
                ▶️ INICIAR TRANSMISIÓN 24/7
            </button>
            <button type="button" class="btn btn-stop" id="btnStop" onclick="confirmStop()" style="display: none;">
                ⏹️ DETENER TRANSMISIÓN
            </button>
            <button type="button" class="btn btn-action" onclick="apiCall('skip')">
                <span>⏭️</span> Saltar Video
            </button>
            <button type="button" class="btn btn-fmt" onclick="toggleFormat()">
                <span>📱</span> <span id="txtFmt">Vertical 9:16</span>
            </button>
        </div>
    </div>

    <!-- RTMP PROPIO Y MULTI-REDES DESDE EL CELULAR -->
    <div class="card">
        <div class="card-head">
            <span>📡 RTMP PROPIO Y SERVIDOR PERSONAL</span>
            <span style="font-size: 10px; color: var(--primary-glow);">Configuración</span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <input type="text" id="mobileCustomRtmpUrl" class="input-text" placeholder="URL RTMP: rtmp://servidor:1935/live" oninput="saveMobileKeys()">
            <input type="password" id="mobileCustomRtmpKey" class="input-text" placeholder="Clave de Transmisión (Stream Key)" oninput="saveMobileKeys()">
            <div style="display: flex; gap: 6px;">
                <button type="button" class="btn-icon-sm" onclick="testMobileConnection('custom')" style="flex: 1; padding: 8px; color: #38bdf8;">
                    🧪 Probar RTMP Propio
                </button>
                <button type="button" class="btn-icon-sm" onclick="saveMobileKeys()" style="padding: 8px 14px; color: #34d399; font-weight: 800;">
                    💾 Guardar
                </button>
            </div>
        </div>
    </div>

    <!-- STICKERS Y RÓTULOS DESDE EL CELULAR -->
    <div class="card">
        <div class="card-head">
            <span>🎨 STICKERS & RÓTULOS EN VIVO</span>
        </div>
        <div class="stickers-scroll-m">
            <div class="sticker-card-m" onclick="addStickerMobile('/stickers/subscribe.svg', 'Subscribe')">
                <img src="/stickers/subscribe.svg" alt="Sub">
                <span>Sub</span>
            </div>
            <div class="sticker-card-m" onclick="addStickerMobile('/stickers/like.svg', 'Like')">
                <img src="/stickers/like.svg" alt="Like">
                <span>Like</span>
            </div>
            <div class="sticker-card-m" onclick="addStickerMobile('/stickers/live_badge.svg', 'LIVE')">
                <img src="/stickers/live_badge.svg" alt="LIVE">
                <span>LIVE</span>
            </div>
            <div class="sticker-card-m" onclick="addStickerMobile('/stickers/fire.svg', 'Fire')">
                <img src="/stickers/fire.svg" alt="Fire">
                <span>Fuego</span>
            </div>
            <div class="sticker-card-m" onclick="addStickerMobile('/stickers/heart.svg', 'Heart')">
                <img src="/stickers/heart.svg" alt="Heart">
                <span>Love</span>
            </div>
            <div class="sticker-card-m" onclick="addStickerMobile('/stickers/star.svg', 'Star')">
                <img src="/stickers/star.svg" alt="Star">
                <span>Star</span>
            </div>
        </div>
        <div style="display: flex; gap: 6px; margin-top: 8px;">
            <input type="text" id="mobileRotuloInput" class="input-text" placeholder="Nuevo rótulo con emojis..." style="padding: 8px 10px; font-size: 12px;">
            <button type="button" class="btn-icon-sm" onclick="addRotuloMobile()" style="color: #34d399; font-weight: 800; padding: 8px 12px;">
                ➕ Agregar
            </button>
        </div>
    </div>

    <!-- SUBIDA DESDE EL CELULAR -->
    <div class="card">
        <div class="card-head">
            <span>📤 SUBIR VIDEOS DESDE ESTE CELULAR</span>
        </div>

        <div style="display: flex; gap: 8px; margin-bottom: 10px; align-items: center;">
            <span style="font-size: 11px; color: var(--text-muted); font-weight: 700; white-space: nowrap;">Subir a:</span>
            <select id="uploadCategorySelect" class="input-text" style="padding: 7px 10px; font-size: 12px; font-weight: 700;">
                <option value="General">📂 General</option>
            </select>
            <button type="button" class="btn-icon-sm" onclick="createCategoryPrompt()" style="padding: 7px 10px; white-space: nowrap;">
                ➕ Nueva
            </button>
        </div>

        <div class="upload-dropzone" onclick="triggerMobileFileInput()">
            <input type="file" id="mobileFileInput" accept="video/*" multiple style="display: none;" onchange="handleMobileUpload(event)">
            <div class="upload-icon">🎬</div>
            <div class="upload-title">Toca para Subir Videos del Celular</div>
            <div class="upload-sub">Galería, cámara, descargas o archivos</div>
        </div>

        <div class="progress-wrap" id="uploadProgressBox">
            <div class="progress-track">
                <div class="progress-bar-fill" id="progressBarFill"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 11px; margin-top: 6px; font-weight: 700; color: var(--text-muted);">
                <span id="progressFileText">Subiendo video...</span>
                <span id="progressPercentText" style="color: #38bdf8;">0%</span>
            </div>
        </div>
    </div>

    <!-- CHAT EN VIVO DESDE EL CELULAR -->
    <div class="card">
        <div class="card-head">
            <span>💬 CHAT EN DIRECTO (YOUTUBE / FACEBOOK)</span>
            <span id="chatSourceBadge" style="color: #f87171; font-size: 10px;">🔴 En tiempo real</span>
        </div>
        <div class="chat-box-mobile" id="mobileChatBox">
            <div style="font-size: 11px; color: var(--text-muted); text-align: center; margin-top: 30px;">
                Los comentarios de YouTube y Facebook aparecerán aquí en vivo.
            </div>
        </div>
        <div style="display: flex; gap: 6px;">
            <select id="mobileChatPlatform" class="btn-icon-sm" style="background: rgba(15,23,42,0.9);">
                <option value="youtube">🔴 YT</option>
                <option value="facebook">🔵 FB</option>
            </select>
            <input type="text" id="mobileChatInput" class="input-text" placeholder="Responder al chat..." style="padding: 8px 10px; font-size: 12px;" onkeydown="if(event.key==='Enter') sendMobileChatMessage()">
            <button type="button" class="btn-icon-sm" onclick="sendMobileChatMessage()" style="color: #38bdf8; font-weight: 800; padding: 8px 12px;">
                Enviar
            </button>
        </div>
    </div>

    <!-- LISTAS TEMÁTICAS Y VIDEOS (GUARDADAS PERMANENTEMENTE) -->
    <div class="card">
        <div class="card-head">
            <span>📂 LISTAS Y VIDEOS EN SERVIDOR</span>
            <div style="display: flex; gap: 6px; align-items: center;">
                <button type="button" class="btn-icon-sm play" onclick="streamCurrentPlaylistMobile()" style="font-weight: 800; font-size: 10px;">
                    ▶ Transmitir Lista
                </button>
                <span id="txtActiveCatName" style="color: var(--primary-glow); font-weight: 700;">General</span>
            </div>
        </div>
        <div class="cat-scroll" id="catContainer"></div>
        <ul class="playlist" id="playlistContainer"></ul>
    </div>

    <!-- LINK AL PANEL COMPLETO -->
    <div style="text-align: center; margin-top: 4px;">
        <a href="/" class="btn btn-fmt" style="display: inline-flex; padding: 10px 20px; font-size: 12px; border-radius: 999px; text-decoration: none;">
            🖥️ Abrir Panel Completo de Estudio ↗
        </a>
    </div>

    <div class="toast" id="toastBox">Acción enviada</div>

    <script>
        let currentFmt = "vertical";
        let currentCat = "General";
        let allVideos = [];
        let isOnline = true;
        let ws = null;
        let mobileChatList = [];

        function vibrate() {
            if ("vibrate" in navigator) {
                try { navigator.vibrate(25); } catch(e){}
            }
        }

        function notify(msg) {
            vibrate();
            const t = document.getElementById("toastBox");
            t.innerText = msg;
            t.classList.add("show");
            setTimeout(() => t.classList.remove("show"), 2400);
        }

        function changeTheme(themeName) {
            document.documentElement.setAttribute("data-theme", themeName);
            document.getElementById("mobileThemeSelector").value = themeName;
            localStorage.setItem("streamhub_theme", themeName);
            fetch("/api/theme", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ theme: themeName })
            });
        }

        function apiCall(action, extra = {}) {
            vibrate();
            const payload = { action: action, ...extra };

            if (ws && ws.readyState === WebSocket.OPEN) {
                try {
                    ws.send(JSON.stringify(payload));
                    notify("Comando enviado en tiempo real");
                    return;
                } catch(e){}
            }

            fetch("/api/control", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            })
            .then(r => r.json())
            .then(d => notify(d.message || "Comando ejecutado"))
            .catch(() => notify("⚠️ Error al conectar con el servidor"));
        }

        function confirmStop() {
            if (confirm("¿Detener la transmisión 24/7?")) {
                apiCall("stop");
            }
        }

        function toggleFormat() {
            currentFmt = (currentFmt === "vertical") ? "horizontal" : "vertical";
            const label = (currentFmt === "vertical") ? "Vertical 9:16" : "Horizontal 16:9";
            document.getElementById("txtFmt").innerText = label;
            document.getElementById("txtFormatBadge").innerText = label;
            apiCall("switch_format", { format: currentFmt });
        }

        function toggleCycleModeMobile() {
            apiCall("toggle_cycle_mode");
        }

        function streamCurrentPlaylistMobile() {
            apiCall("set_playlist", { category: currentCat });
            notify(`▶ Emitiendo lista: ${currentCat}`);
        }

        function selectCategory(cat) {
            currentCat = cat;
            document.getElementById("uploadCategorySelect").value = cat;
            document.getElementById("txtActiveCatName").innerText = cat;
            renderCategoryTabs();
            renderPlaylist();
            apiCall("set_category", { category: cat });
        }

        function playVideoNow(cat, name) {
            if (confirm(`¿Emitir ahora '${name}'?`)) {
                apiCall("play_now", { category: cat, name: name });
            }
        }

        function previewVideoOnPanel(cat, name) {
            fetch("/api/preview", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ category: cat, name: name })
            }).then(() => notify(`👁️ Vista previa: ${name}`));
        }

        function saveMobileKeys() {
            const url = document.getElementById("mobileCustomRtmpUrl").value.trim();
            const key = document.getElementById("mobileCustomRtmpKey").value.trim();
            apiCall("save_keys", { custom_rtmp_url: url, custom_rtmp_key: key });
            notify("Claves RTMP guardadas");
        }

        function testMobileConnection(plat) {
            const url = document.getElementById("mobileCustomRtmpUrl").value.trim();
            const key = document.getElementById("mobileCustomRtmpKey").value.trim();
            notify("Probando conexión RTMP...");
            fetch("/api/test_connection", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ platform: plat, custom_rtmp_url: url, custom_rtmp_key: key })
            }).then(r => r.json()).then(d => notify(d.message));
        }

        function addStickerMobile(url, name) {
            fetch("/api/overlay/config")
                .then(r => r.json())
                .then(d => {
                    const ovs = d.overlays || [];
                    ovs.push({
                        id: `sticker_${Date.now()}`,
                        type: "sticker",
                        text: name,
                        image_url: url,
                        x: 80,
                        y: 120,
                        width: 80,
                        height: 80,
                        rotation: 0,
                        visible: true
                    });
                    fetch("/api/overlay/config", {
                        method: "POST", headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ overlays: ovs })
                    }).then(() => notify(`Sticker '${name}' agregado`));
                });
        }

        function addRotuloMobile() {
            const inp = document.getElementById("mobileRotuloInput");
            const txt = inp.value.trim();
            if (!txt) return;
            fetch("/api/overlay/config")
                .then(r => r.json())
                .then(d => {
                    const ovs = d.overlays || [];
                    ovs.push({
                        id: `rotulo_${Date.now()}`,
                        type: "rotulo",
                        text: txt,
                        x: 40,
                        y: 200,
                        width: 260,
                        height: 48,
                        rotation: 0,
                        fontSize: 16,
                        color: "#ffffff",
                        bg: "rgba(15, 23, 42, 0.9)",
                        opacity: 0.9,
                        visible: true
                    });
                    inp.value = "";
                    fetch("/api/overlay/config", {
                        method: "POST", headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ overlays: ovs })
                    }).then(() => notify("Rótulo agregado a la transmisión"));
                });
        }

        async function createCategoryPrompt() {
            const name = prompt("Nombre de la nueva lista temática:");
            if (!name || !name.trim()) return;
            try {
                const res = await fetch("/api/category/create", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name: name.trim() })
                });
                const d = await res.json();
                if (d.success) {
                    notify(`Lista '${name.trim()}' creada`);
                    fetch("/api/status").then(r => r.json()).then(updateState);
                }
            } catch (e) {
                notify("Error al crear lista");
            }
        }

        async function deleteVideo(cat, name) {
            if (!confirm(`¿Eliminar '${name}' de '${cat}'?`)) return;
            try {
                const res = await fetch(`/api/delete/${encodeURIComponent(cat)}/${encodeURIComponent(name)}`, { method: "POST" });
                const d = await res.json();
                if (d.success) {
                    notify("Video eliminado");
                    fetch("/api/status").then(r => r.json()).then(updateState);
                }
            } catch (e) {
                notify("Error eliminando video");
            }
        }

        function triggerMobileFileInput() {
            vibrate();
            document.getElementById("mobileFileInput").click();
        }

        function handleMobileUpload(e) {
            const files = e.target.files;
            if (!files || !files.length) return;

            const category = document.getElementById("uploadCategorySelect").value || currentCat;
            const progressBox = document.getElementById("uploadProgressBox");
            const barFill = document.getElementById("progressBarFill");
            const fileTxt = document.getElementById("progressFileText");
            const pctTxt = document.getElementById("progressPercentText");

            progressBox.style.display = "block";
            barFill.style.width = "0%";
            pctTxt.innerText = "0%";
            fileTxt.innerText = `Preparando ${files.length} archivo(s)...`;

            const formData = new FormData();
            formData.append("category", category);
            for (let i = 0; i < files.length; i++) {
                formData.append("video_file", files[i]);
            }

            const xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/upload", true);

            xhr.upload.onprogress = (event) => {
                if (event.lengthComputable) {
                    const percent = Math.round((event.loaded / event.total) * 100);
                    barFill.style.width = percent + "%";
                    pctTxt.innerText = percent + "%";
                    const mbLoaded = (event.loaded / (1024 * 1024)).toFixed(1);
                    const mbTotal = (event.total / (1024 * 1024)).toFixed(1);
                    if (percent >= 100) {
                        fileTxt.innerText = `Procesando en servidor...`;
                    } else {
                        fileTxt.innerText = `Subiendo: ${mbLoaded} / ${mbTotal} MB`;
                    }
                }
            };

            xhr.onload = () => {
                progressBox.style.display = "none";
                e.target.value = "";
                if (xhr.status >= 200 && xhr.status < 300) {
                    notify(`✅ ¡${files.length} video(s) subido(s) a [${category}]!`);
                    currentCat = category;
                    fetch("/api/status").then(r => r.json()).then(updateState);
                } else {
                    notify("❌ Error al subir video desde el celular");
                }
            };

            xhr.onerror = () => {
                progressBox.style.display = "none";
                e.target.value = "";
                notify("❌ Error de red durante la subida");
            };

            xhr.send(formData);
        }

        function sendMobileChatMessage() {
            const inM = document.getElementById("mobileChatInput");
            const text = inM.value.trim();
            if (!text) return;
            const plat = document.getElementById("mobileChatPlatform").value;
            fetch("/api/chat/send", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ platform: plat, message: text })
            }).then(r => r.json()).then(d => {
                inM.value = "";
                if (d.item) {
                    mobileChatList.push(d.item);
                    renderMobileChat();
                }
            });
        }

        function renderMobileChat() {
            const box = document.getElementById("mobileChatBox");
            if (mobileChatList.length === 0) {
                box.innerHTML = `<div style="font-size: 11px; color: var(--text-muted); text-align: center; margin-top: 30px;">Esperando comentarios en vivo...</div>`;
                return;
            }
            box.innerHTML = mobileChatList.map(m => {
                const icon = (m.platform === "youtube") ? "🔴" : "🔵";
                const color = m.is_owner ? "#38bdf8" : ((m.platform === "youtube") ? "#f87171" : "#60a5fa");
                return `
                    <div class="chat-msg-m">
                        <span style="font-size: 11px;">${icon}</span>
                        <strong style="color: ${color};">${m.author}:</strong>
                        <span style="color: #f1f5f9;">${m.message}</span>
                    </div>
                `;
            }).join("");
            box.scrollTop = box.scrollHeight;
        }

        function renderCategoryTabs(cats = null) {
            const container = document.getElementById("catContainer");
            const select = document.getElementById("uploadCategorySelect");
            const catList = cats || window.lastCategories || ["General"];
            window.lastCategories = catList;

            container.innerHTML = catList.map(c => `
                <button type="button" class="btn-cat ${c === currentCat ? 'active' : ''}" onclick="selectCategory('${c}')">
                    📂 ${c}
                </button>
            `).join("");

            select.innerHTML = catList.map(c => `
                <option value="${c}" ${c === currentCat ? 'selected' : ''}>📂 ${c}</option>
            `).join("");
        }

        function renderPlaylist() {
            const vids = allVideos.filter(v => v.category === currentCat);
            const container = document.getElementById("playlistContainer");
            document.getElementById("txtQueue").innerText = `${vids.length} vids`;
            document.getElementById("txtActiveCatName").innerText = currentCat;

            if (vids.length === 0) {
                container.innerHTML = `<li style="font-size: 11px; color: var(--text-muted); text-align: center; padding: 18px 0; background: rgba(3,7,18,0.4); border-radius: 10px;">No hay videos en '${currentCat}'.<br>Sube uno con el botón de arriba.</li>`;
                return;
            }

            container.innerHTML = vids.map(v => {
                const durStr = v.duration ? `${Math.round(v.duration)}s` : "";
                const metaStr = [v.size_formatted, durStr].filter(Boolean).join(" • ");
                return `
                <li class="playlist-item">
                    <div class="video-meta">
                        <span style="font-size: 16px;">🎬</span>
                        <div style="overflow: hidden;">
                            <div class="video-name">${v.name}</div>
                            <div style="font-size: 10px; color: var(--text-muted);">${metaStr}</div>
                        </div>
                    </div>
                    <div style="display: flex; gap: 4px; align-items: center;">
                        <button type="button" class="btn-icon-sm" title="Previa" onclick="previewVideoOnPanel('${v.category}', '${v.name}')">
                            👁️
                        </button>
                        <button type="button" class="btn-icon-sm play" title="Emitir ahora" onclick="playVideoNow('${v.category}', '${v.name}')">
                            ⚡ Emitir
                        </button>
                        <button type="button" class="btn-icon-sm del" title="Eliminar" onclick="deleteVideo('${v.category}', '${v.name}')">
                            🗑️
                        </button>
                    </div>
                </li>
            `}).join("");
        }

        function updateState(data) {
            if (!data) return;
            const isLive = (data.status === "Transmitiendo");
            const badge = document.getElementById("badgeStatus");
            const btnStart = document.getElementById("btnStart");
            const btnStop = document.getElementById("btnStop");

            badge.className = isLive ? "status-badge live" : "status-badge";
            badge.innerText = isLive ? "EN DIRECTO 🔴" : "DETENIDO ⚪";
            btnStart.style.display = isLive ? "none" : "flex";
            btnStop.style.display = isLive ? "flex" : "none";

            document.getElementById("txtVideo").innerText = data.current_video || "Esperando video...";

            currentFmt = data.stream_format || "vertical";
            const fmtLabel = (currentFmt === "vertical") ? "Vertical 9:16" : "Horizontal 16:9";
            document.getElementById("txtFmt").innerText = fmtLabel;
            document.getElementById("txtFormatBadge").innerText = fmtLabel;

            if (data.active_category) currentCat = data.active_category;
            allVideos = data.videos || [];

            renderCategoryTabs(data.categories || ["General"]);
            renderPlaylist();

            if (data.live_viewers !== undefined) {
                document.getElementById("txtViewers").innerText = data.live_viewers;
            }

            if (data.theme) {
                document.documentElement.setAttribute("data-theme", data.theme);
                document.getElementById("mobileThemeSelector").value = data.theme;
            }

            if (data.custom_rtmp_url && !document.getElementById("mobileCustomRtmpUrl").value) {
                document.getElementById("mobileCustomRtmpUrl").value = data.custom_rtmp_url;
            }
            if (data.custom_rtmp_key && !document.getElementById("mobileCustomRtmpKey").value) {
                document.getElementById("mobileCustomRtmpKey").value = data.custom_rtmp_key;
            }

            // Temporizador Ciclo 11:55
            const totalCycleSec = data.cycle_duration_seconds || (11 * 3600 + 55 * 60);
            const elapsedSec = data.cycle_elapsed_seconds || 0;
            const remainingSec = Math.max(0, totalCycleSec - elapsedSec);
            const rHours = Math.floor(remainingSec / 3600);
            const rMins = Math.floor((remainingSec % 3600) / 60);
            const rSecs = remainingSec % 60;
            const pad = (n) => String(n).padStart(2, '0');
            document.getElementById("mobileCycleTimer").innerText = `${pad(rHours)}:${pad(rMins)}:${pad(rSecs)}`;

            const cyclePct = Math.min(100, Math.round((elapsedSec / totalCycleSec) * 100));
            document.getElementById("mobileCycleProgressBar").style.width = cyclePct + "%";
            document.getElementById("mobileCyclePct").innerText = `${cyclePct}%`;
            document.getElementById("mobileCycleNumber").innerText = `Ciclo #${data.cycle_count || 1}`;

            const goal = data.monetization_goal || 4000;
            const unit = data.monetization_unit || "min";
            const prog = data.total_monetization_minutes || 0.0;
            const progDisplay = (unit === "minutos" || unit === "min") ? prog.toFixed(0) : (prog / 60).toFixed(1);
            document.getElementById("mobileMonetizationGoal").innerText = `${progDisplay} / ${goal} ${unit}`;

            const isCycleOn = Boolean(data.youtube_cycle_mode);
            const btnC = document.getElementById("btnToggleCycleMobile");
            btnC.innerText = isCycleOn ? "🔘 Ciclo 11h55m" : "⚪ Modo 24/7";
            btnC.style.color = isCycleOn ? "#f87171" : "#10b981";

            if (data.chat_messages) {
                mobileChatList = data.chat_messages;
                renderMobileChat();
            }

            if (data.logs && data.logs.length > 0) {
                for (let i = data.logs.length - 1; i >= 0; i--) {
                    const l = data.logs[i];
                    if (l.includes("fps=")) {
                        const matchFps = l.match(/fps=\s*([\d.]+)/);
                        if (matchFps) document.getElementById("txtFps").innerText = matchFps[1];
                        const matchBit = l.match(/bitrate=\s*([\d.]+)/);
                        if (matchBit) document.getElementById("txtBitrate").innerText = matchBit[1] + "k";
                        break;
                    }
                }
            }
        }

        /* CONEXION WEBSOCKET */
        function connectWS() {
            const proto = (location.protocol === "https:") ? "wss:" : "ws:";
            ws = new WebSocket(`${proto}//${location.host}/ws/sync`);

            ws.onopen = () => {
                document.getElementById("netBadge").className = "net-status online";
                document.getElementById("netText").innerText = "En tiempo real";
            };

            ws.onmessage = (e) => {
                try {
                    const res = JSON.parse(e.data);
                    if (res.type === "state_update") {
                        updateState(res.state);
                    } else if (res.type === "chat_message") {
                        mobileChatList.push(res.message);
                        renderMobileChat();
                    }
                } catch (err) {}
            };

            ws.onclose = () => {
                document.getElementById("netBadge").className = "net-status offline";
                document.getElementById("netText").innerText = "Reconectando...";
                setTimeout(connectWS, 1500);
            };

            ws.onerror = () => {
                try { ws.close(); } catch(e){}
            };
        }

        connectWS();

        setInterval(() => {
            fetch("/api/status")
                .then(r => r.json())
                .then(d => {
                    updateState(d);
                    if (!ws || ws.readyState !== WebSocket.OPEN) {
                        document.getElementById("netBadge").className = "net-status online";
                        document.getElementById("netText").innerText = "Sincronizado";
                    }
                })
                .catch(() => {
                    document.getElementById("netBadge").className = "net-status offline";
                    document.getElementById("netText").innerText = "Desconectado";
                });
        }, 2500);

        document.addEventListener("visibilitychange", () => {
            if (!document.hidden) {
                fetch("/api/status").then(r => r.json()).then(updateState);
                if (!ws || ws.readyState !== WebSocket.OPEN) connectWS();
            }
        });

        const savedTheme = localStorage.getItem("streamhub_theme") || "cyber_dark";
        changeTheme(savedTheme);
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    html = build_control_html()
    base_panel = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'panel_stream'))
    
    t1 = os.path.join(base_panel, 'templates', 'control.html')
    t2 = os.path.join(base_panel, 'control.html')
    
    os.makedirs(os.path.dirname(t1), exist_ok=True)
    with open(t1, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(t2, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"control.html written to {t1} and {t2} ({len(html)} bytes)")
