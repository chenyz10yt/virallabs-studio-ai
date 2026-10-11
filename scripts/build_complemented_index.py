import os

def build_index_html():
    return r'''<!DOCTYPE html>
<html lang="es" data-theme="cyber_dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>StreamHub 24/7 Studio - Panel de Control & Monetización</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <style>
        :root {
            --bg-base: #060911;
            --bg-surface: #0d1322;
            --bg-card: rgba(15, 23, 42, 0.85);
            --border: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(56, 189, 248, 0.35);
            --primary: #0284c7;
            --primary-glow: #38bdf8;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --terminal-bg: #030712;
            --accent-gradient: linear-gradient(135deg, #ef4444, #f97316);
        }

        /* 7 TEMAS PERSONALIZABLES */
        [data-theme="twitch_purple"] {
            --bg-base: #0b0416;
            --bg-surface: #17092c;
            --bg-card: rgba(26, 14, 46, 0.88);
            --border: rgba(192, 132, 252, 0.15);
            --border-glow: rgba(192, 132, 252, 0.45);
            --primary: #9333ea;
            --primary-glow: #c084fc;
            --accent-gradient: linear-gradient(135deg, #a855f7, #6366f1);
        }

        [data-theme="yt_crimson"] {
            --bg-base: #0e0507;
            --bg-surface: #1f0a0e;
            --bg-card: rgba(36, 14, 19, 0.88);
            --border: rgba(239, 68, 68, 0.15);
            --border-glow: rgba(239, 68, 68, 0.45);
            --primary: #dc2626;
            --primary-glow: #f87171;
            --accent-gradient: linear-gradient(135deg, #ef4444, #b91c1c);
        }

        [data-theme="kick_matrix"] {
            --bg-base: #040d07;
            --bg-surface: #0a1f11;
            --bg-card: rgba(12, 33, 19, 0.88);
            --border: rgba(16, 185, 129, 0.18);
            --border-glow: rgba(16, 185, 129, 0.5);
            --primary: #059669;
            --primary-glow: #34d399;
            --accent-gradient: linear-gradient(135deg, #10b981, #00e701);
        }

        [data-theme="oled_black"] {
            --bg-base: #000000;
            --bg-surface: #0a0a0a;
            --bg-card: rgba(18, 18, 18, 0.94);
            --border: rgba(255, 255, 255, 0.12);
            --border-glow: rgba(255, 255, 255, 0.35);
            --primary: #2563eb;
            --primary-glow: #60a5fa;
            --accent-gradient: linear-gradient(135deg, #3b82f6, #1d4ed8);
        }

        [data-theme="sunset_gold"] {
            --bg-base: #0f0a05;
            --bg-surface: #1c1308;
            --bg-card: rgba(33, 22, 12, 0.88);
            --border: rgba(245, 158, 11, 0.18);
            --border-glow: rgba(245, 158, 11, 0.5);
            --primary: #d97706;
            --primary-glow: #fbbf24;
            --accent-gradient: linear-gradient(135deg, #f59e0b, #ea580c);
        }

        [data-theme="titanium_light"] {
            --bg-base: #f1f5f9;
            --bg-surface: #e2e8f0;
            --bg-card: rgba(255, 255, 255, 0.92);
            --border: rgba(0, 0, 0, 0.1);
            --border-glow: rgba(2, 132, 199, 0.35);
            --primary: #0284c7;
            --primary-glow: #0284c7;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --terminal-bg: #0f172a;
            --accent-gradient: linear-gradient(135deg, #0284c7, #2563eb);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-base);
            color: var(--text-main);
            min-height: 100vh;
            padding: 16px 14px 60px;
            transition: background 0.3s ease, color 0.3s ease;
        }

        .container { max-width: 1360px; margin: 0 auto; }

        /* CABECERA */
        .header {
            display: flex; align-items: center; justify-content: space-between;
            flex-wrap: wrap; gap: 14px; margin-bottom: 18px; padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }

        .brand { display: flex; align-items: center; gap: 12px; }
        .brand-icon {
            width: 44px; height: 44px; border-radius: 12px;
            background: var(--accent-gradient);
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; box-shadow: 0 8px 24px rgba(239, 68, 68, 0.4);
            flex-shrink: 0;
        }
        .brand-text h1 { font-size: 20px; font-weight: 800; letter-spacing: -0.3px; color: var(--text-main); }
        .brand-text p { font-size: 12px; color: var(--text-muted); }

        .header-actions { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
        .btn-chip {
            background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border);
            color: var(--text-muted); font-size: 11px; font-weight: 700;
            padding: 7px 12px; border-radius: 8px; cursor: pointer; transition: all 0.2s ease;
            text-decoration: none; display: inline-flex; align-items: center; gap: 6px;
        }
        .btn-chip:hover { background: rgba(255, 255, 255, 0.12); color: var(--text-main); }
        .btn-chip.active { background: rgba(56, 189, 248, 0.2); color: var(--primary-glow); border-color: var(--primary-glow); }

        .theme-select {
            background: var(--bg-surface); color: var(--text-main); border: 1px solid var(--border);
            border-radius: 8px; padding: 6px 10px; font-size: 11px; font-weight: 700; outline: none;
            cursor: pointer;
        }

        .badge-live {
            display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px;
            border-radius: 999px; font-size: 12px; font-weight: 800;
            background: rgba(148, 163, 184, 0.12); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.25);
        }
        .badge-live.active {
            background: rgba(239, 68, 68, 0.2); color: #f87171;
            border-color: rgba(239, 68, 68, 0.5); box-shadow: 0 0 16px rgba(239, 68, 68, 0.35);
        }

        /* GRID PRINCIPAL */
        .grid { display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 18px; }
        @media (max-width: 1080px) { .grid { grid-template-columns: 1fr; } }

        .card {
            background: var(--bg-card); backdrop-filter: blur(16px);
            border: 1px solid var(--border); border-radius: 16px; padding: 18px; margin-bottom: 18px;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4);
        }
        .card-title {
            display: flex; align-items: center; justify-content: space-between;
            font-size: 14px; font-weight: 800; color: var(--text-main);
            margin-bottom: 14px; border-bottom: 1px solid var(--border); padding-bottom: 10px;
            text-transform: uppercase; letter-spacing: 0.3px;
        }

        /* MONITOR DE VIDEO Y CAPA CANVAS CON 8 TIRADORES */
        .monitor-frame {
            position: relative; width: 100%; height: 380px; background: #000;
            border-radius: 14px; overflow: hidden; border: 1px solid var(--border-glow);
            margin-bottom: 14px; display: flex; align-items: center; justify-content: center;
            user-select: none;
        }

        .monitor-video {
            width: 100%; height: 100%; object-fit: contain; background: #000; pointer-events: none;
        }

        .overlay-canvas-layer {
            position: absolute; inset: 0; width: 100%; height: 100%;
            pointer-events: auto; z-index: 10; overflow: hidden;
        }

        /* ELEMENTOS SOBRE EL CANVAS */
        .canvas-overlay-item {
            position: absolute; cursor: move; touch-action: none;
            display: flex; align-items: center; justify-content: center;
            padding: 6px 12px; border-radius: 8px; font-weight: 800;
            border: 1px dashed rgba(255, 255, 255, 0.3);
            transform-origin: center center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            transition: box-shadow 0.15s ease;
            box-sizing: border-box;
        }

        .canvas-overlay-item:hover {
            border-color: var(--primary-glow);
        }

        .canvas-overlay-item.selected {
            border: 2px solid var(--primary-glow) !important;
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.5) !important;
        }

        /* 8 TIRADORES DE TAMAÑO */
        .canvas-overlay-item .handle {
            display: none; position: absolute; width: 10px; height: 10px;
            background: #fff; border: 2px solid var(--primary); border-radius: 2px;
            z-index: 20;
        }

        .canvas-overlay-item.selected .handle { display: block; }

        .handle.nw { top: -6px; left: -6px; cursor: nwse-resize; }
        .handle.n  { top: -6px; left: 50%; transform: translateX(-50%); cursor: ns-resize; }
        .handle.ne { top: -6px; right: -6px; cursor: nesw-resize; }
        .handle.e  { top: 50%; right: -6px; transform: translateY(-50%); cursor: ew-resize; }
        .handle.se { bottom: -6px; right: -6px; cursor: nwse-resize; }
        .handle.s  { bottom: -6px; left: 50%; transform: translateX(-50%); cursor: ns-resize; }
        .handle.sw { bottom: -6px; left: -6px; cursor: nesw-resize; }
        .handle.w  { top: 50%; left: -6px; transform: translateY(-50%); cursor: ew-resize; }

        /* TIRADOR DE ROTACIÓN 360° CON MÁSTIL */
        .canvas-overlay-item .rot-stem {
            display: none; position: absolute; top: -24px; left: 50%; width: 2px; height: 24px;
            background: var(--primary-glow); transform: translateX(-50%); z-index: 18;
        }
        .canvas-overlay-item .rot-handle {
            display: none; position: absolute; top: -34px; left: 50%; width: 16px; height: 16px;
            background: #fff; border: 2px solid var(--primary); border-radius: 50%;
            transform: translateX(-50%); cursor: grab; z-index: 22; box-shadow: 0 2px 8px rgba(0,0,0,0.4);
        }
        .canvas-overlay-item .rot-deg-badge {
            display: none; position: absolute; top: -56px; left: 50%; transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.85); color: #38bdf8; font-size: 10px; font-weight: 800;
            padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(56, 189, 248, 0.4);
            white-space: nowrap; z-index: 25; font-family: 'JetBrains Mono', monospace;
        }

        .canvas-overlay-item.selected .rot-stem,
        .canvas-overlay-item.selected .rot-handle,
        .canvas-overlay-item.selected .rot-deg-badge {
            display: block;
        }

        .monitor-controls-bar {
            display: flex; align-items: center; justify-content: space-between;
            gap: 8px; margin-bottom: 14px; flex-wrap: wrap;
        }

        /* METRICAS Y AUDIENCIA */
        .metrics-bar { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 14px; }
        @media (max-width: 768px) { .metrics-bar { grid-template-columns: repeat(2, 1fr); } }
        .metric-box {
            background: rgba(3, 7, 18, 0.6); border: 1px solid var(--border);
            border-radius: 10px; padding: 10px; text-align: center;
        }
        .metric-label { font-size: 10px; color: var(--text-muted); font-weight: 700; text-transform: uppercase; margin-bottom: 2px; }
        .metric-value { font-size: 14px; font-weight: 800; color: var(--primary-glow); font-family: 'JetBrains Mono', monospace; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

        /* ESTUDIO DE OVERLAYS & STICKERS */
        .overlay-studio {
            background: rgba(15, 23, 42, 0.65); border: 1px solid var(--border);
            border-radius: 12px; padding: 14px; margin-top: 10px;
        }

        .stickers-scroll {
            display: flex; gap: 8px; overflow-x: auto; padding: 8px 4px; margin-bottom: 10px;
            scrollbar-width: thin;
        }
        .sticker-card {
            background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border);
            border-radius: 10px; padding: 8px; cursor: pointer; text-align: center;
            min-width: 64px; flex-shrink: 0; transition: all 0.2s ease;
        }
        .sticker-card:hover { transform: translateY(-2px); border-color: var(--primary-glow); background: rgba(56, 189, 248, 0.12); }
        .sticker-card img { width: 36px; height: 36px; object-fit: contain; display: block; margin: 0 auto 4px; }
        .sticker-card span { font-size: 10px; font-weight: 700; color: var(--text-muted); display: block; }

        .layers-table {
            width: 100%; border-collapse: collapse; font-size: 11px; margin-top: 10px;
        }
        .layers-table th, .layers-table td {
            padding: 6px 8px; border-bottom: 1px solid var(--border); text-align: left;
        }
        .layers-table th { color: var(--text-muted); font-weight: 800; text-transform: uppercase; }

        /* SECCIÓN DE MONETIZACIÓN YOUTUBE */
        .monetization-box {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(2, 132, 199, 0.08));
            border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 14px; padding: 14px;
            margin-bottom: 16px;
        }
        .mono-header {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 10px; flex-wrap: wrap; gap: 8px;
        }
        .mono-timer {
            font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 800;
            color: #f87171; letter-spacing: 1px; text-shadow: 0 0 12px rgba(239, 68, 68, 0.4);
        }
        .progress-track {
            height: 10px; background: rgba(255, 255, 255, 0.08); border-radius: 999px;
            overflow: hidden; margin: 8px 0; position: relative;
        }
        .progress-bar-fill {
            height: 100%; width: 0%;
            background: linear-gradient(90deg, #ef4444, #f97316, #10b981);
            border-radius: 999px; transition: width 0.3s ease;
        }
        .mono-info-row {
            display: flex; justify-content: space-between; font-size: 11px;
            font-weight: 700; color: var(--text-muted);
        }

        /* PLATAFORMAS & CLAVES */
        .platform-nav { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 14px; }
        @media (max-width: 600px) { .platform-nav { grid-template-columns: repeat(2, 1fr); } }
        .platform-btn {
            background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border);
            border-radius: 10px; padding: 10px 4px; color: var(--text-muted);
            font-size: 11px; font-weight: 700; cursor: pointer; text-align: center;
        }
        .platform-btn.active[data-plat="youtube"] { background: rgba(239, 68, 68, 0.18); color: #f87171; border-color: rgba(239, 68, 68, 0.6); }
        .platform-btn.active[data-plat="facebook"] { background: rgba(24, 119, 242, 0.18); color: #60a5fa; border-color: rgba(24, 119, 242, 0.6); }
        .platform-btn.active[data-plat="twitch"] { background: rgba(168, 85, 247, 0.18); color: #c084fc; border-color: rgba(168, 85, 247, 0.6); }
        .platform-btn.active[data-plat="custom"] { background: rgba(56, 189, 248, 0.18); color: #38bdf8; border-color: rgba(56, 189, 248, 0.6); }
        .platform-btn.active[data-plat="tiktok"] { background: rgba(255, 0, 80, 0.18); color: #ff0050; border-color: rgba(255, 0, 80, 0.6); }
        .platform-btn.active[data-plat="kick"] { background: rgba(0, 231, 1, 0.18); color: #00e701; border-color: rgba(0, 231, 1, 0.6); }
        .platform-btn.active[data-plat="multistream"] { background: rgba(16, 185, 129, 0.18); color: #34d399; border-color: rgba(16, 185, 129, 0.6); }

        .platform-panel { background: rgba(15, 23, 42, 0.65); border: 1px solid var(--border); border-radius: 12px; padding: 14px; margin-bottom: 12px; }

        .input-group { margin-bottom: 12px; }
        .input-group label { display: flex; align-items: center; justify-content: space-between; font-size: 12px; font-weight: 700; color: var(--text-main); margin-bottom: 6px; }
        .input-group label a { color: var(--primary-glow); text-decoration: none; font-size: 11px; }
        .input-wrapper { position: relative; display: flex; align-items: center; }

        input[type="text"], input[type="password"] {
            width: 100%; background: rgba(15, 23, 42, 0.9); border: 1px solid var(--border);
            border-radius: 10px; padding: 10px 14px; color: #fff; font-size: 13px; outline: none;
        }
        input:focus { border-color: var(--primary-glow); box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15); }
        .toggle-key { position: absolute; right: 10px; background: none; border: none; color: var(--text-muted); cursor: pointer; font-size: 15px; }

        .btn-group { display: grid; grid-template-columns: 2fr 1fr; gap: 10px; margin-top: 14px; }
        .btn { padding: 14px 16px; border-radius: 12px; border: none; font-size: 13px; font-weight: 800; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 8px; }
        .btn-start { background: linear-gradient(135deg, #10b981, #059669); color: #fff; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.35); }
        .btn-stop { background: linear-gradient(135deg, #ef4444, #dc2626); color: #fff; }
        .btn:disabled { opacity: 0.45; cursor: not-allowed; }

        /* CENTRO DE CHAT EN VIVO */
        .chat-container {
            display: flex; flex-direction: column; height: 340px;
            background: rgba(3, 7, 18, 0.7); border: 1px solid var(--border);
            border-radius: 14px; overflow: hidden;
        }
        .chat-tabs {
            display: flex; border-bottom: 1px solid var(--border); background: rgba(15, 23, 42, 0.9);
        }
        .chat-tab {
            flex: 1; padding: 9px; font-size: 11px; font-weight: 800; text-align: center;
            cursor: pointer; color: var(--text-muted); background: none; border: none;
            transition: all 0.2s ease;
        }
        .chat-tab.active {
            color: #fff; background: rgba(255, 255, 255, 0.05); border-bottom: 2px solid var(--primary-glow);
        }
        .chat-messages-box {
            flex: 1; overflow-y: auto; padding: 12px; display: flex; flex-direction: column; gap: 8px;
        }
        .chat-msg {
            display: flex; gap: 8px; font-size: 12px; line-height: 1.4;
            background: rgba(255, 255, 255, 0.02); padding: 6px 10px; border-radius: 8px;
        }
        .chat-msg.owner {
            background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.3);
        }
        .chat-author { font-weight: 800; white-space: nowrap; }
        .chat-author.yt { color: #f87171; }
        .chat-author.fb { color: #60a5fa; }
        .chat-author.me { color: #38bdf8; }
        .chat-input-bar {
            padding: 8px 10px; border-top: 1px solid var(--border); background: rgba(15, 23, 42, 0.9);
            display: flex; gap: 8px; align-items: center;
        }

        /* PLAYLIST */
        .dropzone {
            border: 2px dashed rgba(56, 189, 248, 0.35); border-radius: 12px; padding: 16px;
            text-align: center; cursor: pointer; background: rgba(56, 189, 248, 0.02); margin-bottom: 10px;
        }
        .dropzone:hover { border-color: var(--primary-glow); background: rgba(56, 189, 248, 0.08); }

        .playlist { list-style: none; max-height: 240px; overflow-y: auto; }
        .playlist-item {
            background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border);
            border-radius: 10px; padding: 8px 10px; margin-bottom: 6px;
            display: flex; align-items: center; justify-content: space-between; gap: 10px;
        }
        .video-meta { display: flex; align-items: center; gap: 8px; min-width: 0; flex: 1; }
        .video-name { font-size: 12px; font-weight: 700; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

        .terminal {
            background: var(--terminal-bg); border: 1px solid var(--border); border-radius: 12px;
            padding: 12px; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #38bdf8;
            height: 140px; overflow-y: auto; white-space: pre-wrap; line-height: 1.4;
        }

        .test-feedback {
            font-size: 12px; font-weight: 600; padding: 8px 14px; border-radius: 8px; margin-top: 8px;
        }
        .test-feedback.success { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); }
        .test-feedback.error { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.35); }
        .test-feedback.loading { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.35); }

        .toast {
            position: fixed; bottom: 24px; right: 24px; padding: 12px 20px; border-radius: 10px;
            background: var(--bg-card); color: #fff; border: 1px solid #38bdf8;
            box-shadow: 0 10px 30px rgba(0,0,0,0.7); font-size: 13px; font-weight: 700;
            transform: translateY(80px); opacity: 0; transition: all 0.25s ease; z-index: 1000;
        }
        .toast.show { transform: translateY(0); opacity: 1; }
    </style>
</head>
<body>
    <div class="container">
        <!-- CABECERA -->
        <header class="header">
            <div class="brand">
                <div class="brand-icon">▶</div>
                <div class="brand-text">
                    <h1>StreamHub 24/7 Studio</h1>
                    <p>Emisión Continua, Ciclos de Monetización & Multi-Chat</p>
                </div>
            </div>

            <div class="header-actions">
                <select id="themeSelector" class="theme-select" onchange="changeTheme(this.value)">
                    <option value="cyber_dark">🌌 Tema: Cyber Dark</option>
                    <option value="twitch_purple">🟣 Tema: Twitch Violet</option>
                    <option value="yt_crimson">🔴 Tema: YouTube Crimson</option>
                    <option value="kick_matrix">🟢 Tema: Kick Matrix</option>
                    <option value="oled_black">⬛ Tema: OLED Black</option>
                    <option value="sunset_gold">🌅 Tema: Sunset Gold</option>
                    <option value="titanium_light">⚪ Tema: Titanium Light</option>
                </select>

                <a href="https://studio.youtube.com/channel/UC/livestreaming" target="_blank" rel="noopener" class="btn-chip" style="color: #f87171;">
                    🔴 YouTube Studio ↗
                </a>
                <a href="https://www.facebook.com/live/producer" target="_blank" rel="noopener" class="btn-chip" style="color: #60a5fa;">
                    🔵 Facebook Producer ↗
                </a>
                <button type="button" class="btn-chip" onclick="openControlQrModal()" style="color: #38bdf8; font-weight: bold;">
                    📱 Control Celular / QR
                </button>
                <span id="liveBadge" class="badge-live">
                    <span id="statusText">DETENIDO ⏹</span>
                </span>
            </div>
        </header>

        <div class="grid">
            <!-- COLUMNA IZQUIERDA -->
            <div>
                <!-- MONITOR EN VIVO Y VISTA PREVIA CON CANVAS INTERACTIVO -->
                <div class="card">
                    <div class="card-title">
                        <span>📺 Monitor en Vivo & Capas Interactivas</span>
                        <div style="display: flex; gap: 6px;">
                            <button type="button" class="btn-chip" onclick="toggleMuteVideo()" id="btnMute">
                                🔇 Silenciado
                            </button>
                            <button type="button" class="btn-chip" onclick="skipCurrentVideo()" style="color: #38bdf8;">
                                ⏭ Saltar Video
                            </button>
                        </div>
                    </div>

                    <!-- SELECTOR DE FORMATO -->
                    <div class="monitor-controls-bar">
                        <div style="display: flex; gap: 6px;">
                            <button type="button" class="btn-chip active" id="btnFmt_vertical" onclick="changeFormat('vertical')">
                                📱 Vertical 9:16 (Shorts/Reels)
                            </button>
                            <button type="button" class="btn-chip" id="btnFmt_horizontal" onclick="changeFormat('horizontal')">
                                🖥️ Panorámico 16:9
                            </button>
                        </div>
                        <span id="monitorModeBadge" style="font-size: 11px; font-weight: 700; color: #38bdf8;">
                            👁️ Mueve o gira elementos en el video
                        </span>
                    </div>

                    <!-- REPRODUCTOR CON LIENZO DE TIRADORES (8 HANDLES + ROTACIÓN 360°) -->
                    <div class="monitor-frame" id="monitorFrameContainer">
                        <video id="liveVideoPlayer" class="monitor-video" playsinline muted loop autoplay></video>
                        <div id="overlayCanvasLayer" class="overlay-canvas-layer"></div>
                    </div>

                    <!-- METRICAS DE EMISION -->
                    <div class="metrics-bar">
                        <div class="metric-box">
                            <div class="metric-label">Video Actual</div>
                            <div class="metric-value" id="currentVideoDisplay">Ninguno</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-label">👁️ Espectadores</div>
                            <div class="metric-value" id="liveViewersDisplay" style="color: #34d399;">0 en vivo</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-label">Bitrate / FPS</div>
                            <div class="metric-value" id="telemetryBitrate">~3,100k / 30fps</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-label">📱 Dispositivos</div>
                            <div class="metric-value" id="connectedDevicesDisplay">1 conectado</div>
                        </div>
                    </div>

                    <!-- ESTUDIO UNIVERSAL DE OVERLAYS, STICKERS Y LOGOS -->
                    <div class="overlay-studio">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 12px; font-weight: 800; color: #fff;">
                                🎨 STICKERS OFICIALES & LOGOS (Toca para agregar al video)
                            </span>
                            <div style="display: flex; gap: 6px;">
                                <input type="file" id="overlayImageInput" accept="image/*" style="display: none;" onchange="handleOverlayImageUpload(event)">
                                <button type="button" class="btn-chip" onclick="document.getElementById('overlayImageInput').click()" style="color: #38bdf8;">
                                    🖼️ Subir Logo / Imagen PNG
                                </button>
                                <button type="button" class="btn-chip active" onclick="saveAndApplyOverlays()">
                                    💾 Guardar y Aplicar
                                </button>
                            </div>
                        </div>

                        <!-- GALERIA DE 8 STICKERS -->
                        <div class="stickers-scroll" id="stickersGallery">
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/subscribe.svg', 'Subscribe')">
                                <img src="/stickers/subscribe.svg" alt="Subscribe" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'%23ef4444\'><path d=\'M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z\'/></svg>'">
                                <span>Subscribe</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/like.svg', 'Like')">
                                <img src="/stickers/like.svg" alt="Like">
                                <span>Like</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/live_badge.svg', 'LIVE')">
                                <img src="/stickers/live_badge.svg" alt="LIVE">
                                <span>En Directo</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/fire.svg', 'Fire')">
                                <img src="/stickers/fire.svg" alt="Fire">
                                <span>Fuego</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/heart.svg', 'Heart')">
                                <img src="/stickers/heart.svg" alt="Heart">
                                <span>Corazón</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/star.svg', 'Star')">
                                <img src="/stickers/star.svg" alt="Star">
                                <span>Estrella</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/verified.svg', 'Verified')">
                                <img src="/stickers/verified.svg" alt="Verified">
                                <span>Verificado</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/cross.svg', 'Cross')">
                                <img src="/stickers/cross.svg" alt="Cross">
                                <span>Cruz</span>
                            </div>
                        </div>

                        <!-- CREAR RÓTULO CON EMOJIS -->
                        <div style="margin-top: 10px;">
                            <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 6px;">
                                ✍️ Crear Rótulo de Texto con Emojis:
                            </label>
                            <div style="display: flex; gap: 6px; margin-bottom: 6px;">
                                <input type="text" id="newRotuloInput" placeholder="Ej: ¡Transmisión en directo continua 24/7! 🚀">
                                <button type="button" class="btn-chip" onclick="addNewRotulo()" style="color: #34d399; font-weight: 800; white-space: nowrap;">
                                    ➕ Agregar Rótulo
                                </button>
                            </div>
                            <div style="display: flex; gap: 4px; overflow-x: auto; padding-bottom: 4px;">
                                <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertEmoji('🔴')">🔴</button>
                                <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertEmoji('🔥')">🔥</button>
                                <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertEmoji('⭐')">⭐</button>
                                <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertEmoji('💬')">💬</button>
                                <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertEmoji('⚡')">⚡</button>
                                <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertEmoji('❤️')">❤️</button>
                                <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertEmoji('👍')">👍</button>
                                <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertEmoji('🔔')">🔔</button>
                                <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertEmoji('🎉')">🎉</button>
                            </div>
                        </div>

                        <!-- TABLA DE CAPAS ACTIVAS -->
                        <div style="margin-top: 10px; max-height: 160px; overflow-y: auto;">
                            <table class="layers-table" id="layersTable">
                                <thead>
                                    <tr>
                                        <th>Capa / Elemento</th>
                                        <th>Rotación</th>
                                        <th>Tamaño</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody id="layersTableBody"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- SECCIÓN MONETIZACIÓN YOUTUBE: CICLO 11:55 Y 4000 MINUTOS -->
                <div class="card">
                    <div class="card-title">
                        <span>🎯 Monetización YouTube (Ciclo 11h 55m & Meta 4,000)</span>
                        <button type="button" class="btn-chip" id="btnToggleCycleMode" onclick="toggleCycleMode()" style="color: #f87171;">
                            🔘 Modo Ciclo 11:55: ACTIVO
                        </button>
                    </div>

                    <div class="monetization-box">
                        <div class="mono-header">
                            <div>
                                <span style="font-size: 11px; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">
                                    ⏳ TIEMPO RESTANTE CICLO ACTUAL:
                                </span>
                                <div class="mono-timer" id="cycleCountdownText">11:55:00</div>
                            </div>
                            <div style="text-align: right;">
                                <span style="font-size: 11px; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">
                                    CICLO NÚMERO:
                                </span>
                                <div style="font-size: 18px; font-weight: 800; color: #38bdf8;" id="cycleCountBadge">#1</div>
                            </div>
                        </div>

                        <!-- Barra de ciclo 11:55 -->
                        <div class="progress-track">
                            <div class="progress-bar-fill" id="cycleProgressBar"></div>
                        </div>
                        <div class="mono-info-row">
                            <span>0h 00m</span>
                            <span id="cycleElapsedPercent">0% del ciclo</span>
                            <span>11h 55m (Reinicio VOD)</span>
                        </div>

                        <!-- Meta total hacia los 4000 minutos -->
                        <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.08);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <span style="font-size: 12px; font-weight: 800; color: var(--text-main);">
                                    🚀 PROGRESO HACIA MONETIZACIÓN:
                                </span>
                                <span style="font-size: 13px; font-weight: 800; color: #10b981;" id="monetizationGoalText">
                                    0.0 / 4,000 min (0%)
                                </span>
                            </div>
                            <div class="progress-track" style="height: 12px;">
                                <div class="progress-bar-fill" id="monetizationTotalBar" style="background: linear-gradient(90deg, #0284c7, #10b981);"></div>
                            </div>
                            <p style="font-size: 11px; color: var(--text-muted); margin-top: 6px; line-height: 1.4;">
                                💡 <em>YouTube archiva videos de hasta 12h. Al llegar a 11:55, el sistema pausa 15 segundos para guardar el VOD y reinicia la transmisión automáticamente hasta cumplir la meta de monetización.</em>
                            </p>
                        </div>
                    </div>
                </div>

                <!-- TERMINAL FFmpeg -->
                <div class="card">
                    <div class="card-title">
                        <span>📟 Monitor de FFmpeg (Logs de Emisión)</span>
                    </div>
                    <div class="terminal" id="terminalLogs">Esperando actividad de streaming...</div>
                </div>
            </div>

            <!-- COLUMNA DERECHA -->
            <div>
                <!-- CONEXIÓN DE TRANSMISIÓN A REDES Y RTMP PROPIO -->
                <div class="card">
                    <div class="card-title">
                        <span>🌐 Conexión de Transmisión a Redes</span>
                    </div>

                    <div class="platform-nav">
                        <button type="button" class="platform-btn active" data-plat="youtube" onclick="selectPlatform('youtube')">🔴 YouTube</button>
                        <button type="button" class="platform-btn" data-plat="facebook" onclick="selectPlatform('facebook')">🔵 Facebook</button>
                        <button type="button" class="platform-btn" data-plat="twitch" onclick="selectPlatform('twitch')">🟣 Twitch</button>
                        <button type="button" class="platform-btn" data-plat="custom" onclick="selectPlatform('custom')">📡 RTMP Propio</button>
                        <button type="button" class="platform-btn" data-plat="tiktok" onclick="selectPlatform('tiktok')">🎵 TikTok</button>
                        <button type="button" class="platform-btn" data-plat="kick" onclick="selectPlatform('kick')">🟢 Kick</button>
                        <button type="button" class="platform-btn" data-plat="multistream" onclick="selectPlatform('multistream')">🔀 Multi-Stream</button>
                    </div>

                    <div id="panelYoutube" class="platform-panel">
                        <div class="input-group">
                            <label for="streamKeyInput">
                                <span>Clave de Transmisión de YouTube:</span>
                                <a href="https://studio.youtube.com/channel/UC/livestreaming" target="_blank" rel="noopener">👉 Abrir YouTube Studio ↗</a>
                            </label>
                            <div class="input-wrapper">
                                <input type="password" id="streamKeyInput" placeholder="Pega tu clave (abcd-1234-wxyz-5678)" oninput="autoSaveKeys()">
                                <button type="button" class="toggle-key" onclick="toggleKeyVisibility('streamKeyInput')">👁️</button>
                            </div>
                        </div>
                    </div>

                    <div id="panelFacebook" class="platform-panel" style="display: none;">
                        <div class="input-group">
                            <label for="facebookKeyInput">
                                <span>Clave de Stream de Facebook (Página o Perfil):</span>
                                <a href="https://www.facebook.com/live/producer" target="_blank" rel="noopener">👉 Abrir Facebook Live Producer ↗</a>
                            </label>
                            <div class="input-wrapper">
                                <input type="password" id="facebookKeyInput" placeholder="Pega tu clave (FB-xxxxxxxxxxxx)" oninput="autoSaveKeys()">
                                <button type="button" class="toggle-key" onclick="toggleKeyVisibility('facebookKeyInput')">👁️</button>
                            </div>
                        </div>
                    </div>

                    <div id="panelTwitch" class="platform-panel" style="display: none;">
                        <div class="input-group">
                            <label for="twitchKeyInput">
                                <span>Clave de Stream de Twitch:</span>
                                <a href="https://dashboard.twitch.tv/settings/stream" target="_blank" rel="noopener">👉 Abrir Twitch Dashboard ↗</a>
                            </label>
                            <div class="input-wrapper">
                                <input type="password" id="twitchKeyInput" placeholder="Pega tu clave (live_xxxxxxxx)" oninput="autoSaveKeys()">
                                <button type="button" class="toggle-key" onclick="toggleKeyVisibility('twitchKeyInput')">👁️</button>
                            </div>
                        </div>
                    </div>

                    <!-- RTMP PROPIO (DESTACADO Y CLARO) -->
                    <div id="panelCustom" class="platform-panel" style="display: none;">
                        <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 8px; padding: 10px; margin-bottom: 12px; font-size: 11px; color: #38bdf8;">
                            ℹ️ <strong>RTMP PROPIO:</strong> Conecta tu VPS personal, servidor NGINX-RTMP, Restream, o servidor privado de retransmisión.
                        </div>
                        <div class="input-group">
                            <label for="customRtmpUrlInput">URL del Servidor RTMP (Ej: rtmp://tu-servidor:1935/live):</label>
                            <input type="text" id="customRtmpUrlInput" placeholder="rtmp://tu-servidor.com:1935/live" oninput="autoSaveKeys()">
                        </div>
                        <div class="input-group">
                            <label for="customRtmpKeyInput">Clave de Transmisión (Stream Key):</label>
                            <div class="input-wrapper">
                                <input type="password" id="customRtmpKeyInput" placeholder="Clave secreta del servidor RTMP" oninput="autoSaveKeys()">
                                <button type="button" class="toggle-key" onclick="toggleKeyVisibility('customRtmpKeyInput')">👁️</button>
                            </div>
                        </div>
                    </div>

                    <!-- TIKTOK -->
                    <div id="panelTiktok" class="platform-panel" style="display: none;">
                        <div class="input-group">
                            <label for="tiktokServerInput">Servidor RTMP de TikTok:</label>
                            <input type="text" id="tiktokServerInput" placeholder="rtmp://live-push.tiktok.com/live" oninput="autoSaveKeys()">
                        </div>
                        <div class="input-group">
                            <label for="tiktokKeyInput">Clave de Stream de TikTok Live:</label>
                            <div class="input-wrapper">
                                <input type="password" id="tiktokKeyInput" placeholder="Pega tu clave de TikTok Live" oninput="autoSaveKeys()">
                                <button type="button" class="toggle-key" onclick="toggleKeyVisibility('tiktokKeyInput')">👁️</button>
                            </div>
                        </div>
                    </div>

                    <!-- KICK -->
                    <div id="panelKick" class="platform-panel" style="display: none;">
                        <div class="input-group">
                            <label for="kickServerInput">Servidor RTMP de Kick:</label>
                            <input type="text" id="kickServerInput" placeholder="rtmps://fa723fc1b171.global-contribute.live-video.net:443/app" oninput="autoSaveKeys()">
                        </div>
                        <div class="input-group">
                            <label for="kickKeyInput">Clave de Stream de Kick:</label>
                            <div class="input-wrapper">
                                <input type="password" id="kickKeyInput" placeholder="sk_us-west_..." oninput="autoSaveKeys()">
                                <button type="button" class="toggle-key" onclick="toggleKeyVisibility('kickKeyInput')">👁️</button>
                            </div>
                        </div>
                    </div>

                    <!-- MULTISTREAM -->
                    <div id="panelMultistream" class="platform-panel" style="display: none;">
                        <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Emite en varias plataformas a la vez con un solo clic:</p>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; font-size: 12px; font-weight: 700;">
                            <label><input type="checkbox" id="chkMultiYt" checked onchange="autoSaveKeys()"> 🔴 YouTube</label>
                            <label><input type="checkbox" id="chkMultiFb" onchange="autoSaveKeys()"> 🔵 Facebook</label>
                            <label><input type="checkbox" id="chkMultiTw" onchange="autoSaveKeys()"> 🟣 Twitch</label>
                            <label><input type="checkbox" id="chkMultiCustom" onchange="autoSaveKeys()"> 📡 RTMP Propio</label>
                            <label><input type="checkbox" id="chkMultiTiktok" onchange="autoSaveKeys()"> 🎵 TikTok</label>
                            <label><input type="checkbox" id="chkMultiKick" onchange="autoSaveKeys()"> 🟢 Kick</label>
                        </div>
                    </div>

                    <button type="button" class="btn-chip" style="width: 100%; padding: 10px; margin-bottom: 6px; font-weight: bold;" onclick="testConnection()">
                        🧪 Probar Conexión con la Plataforma Seleccionada
                    </button>
                    <div id="testFeedbackBox" class="test-feedback" style="display: none;"></div>

                    <div class="btn-group">
                        <button type="button" id="btnStart" class="btn btn-start" onclick="startStream()"><span>🔴</span> INICIAR TRANSMISIÓN 24/7</button>
                        <button type="button" id="btnStop" class="btn btn-stop" onclick="stopStream()" disabled><span>⏹</span> Detener</button>
                    </div>
                </div>

                <!-- CHAT EN VIVO MULTI-PLATAFORMA (YOUTUBE & FACEBOOK) -->
                <div class="card">
                    <div class="card-title">
                        <span>💬 Chat en Vivo (YouTube & Facebook)</span>
                        <div style="display: flex; gap: 6px;">
                            <a id="btnPopoutYtChat" href="#" target="_blank" rel="noopener" class="btn-chip" style="display: none; color: #f87171;">
                                ↗ Popout YT
                            </a>
                            <a href="https://www.facebook.com/live/producer" target="_blank" rel="noopener" class="btn-chip" style="color: #60a5fa;">
                                ↗ FB Producer
                            </a>
                        </div>
                    </div>

                    <!-- Vincular stream ID para chat -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr auto; gap: 6px; margin-bottom: 10px;">
                        <input type="text" id="ytVideoIdInput" placeholder="ID o Link YouTube Live" style="padding: 8px 10px; font-size: 11px;">
                        <input type="text" id="fbLiveIdInput" placeholder="ID Facebook Live" style="padding: 8px 10px; font-size: 11px;">
                        <button type="button" class="btn-chip" onclick="connectLiveChats()" style="color: #38bdf8; font-weight: 700;">
                            🔗 Conectar
                        </button>
                    </div>

                    <div class="chat-container">
                        <div class="chat-tabs">
                            <button type="button" class="chat-tab active" data-tab="all" onclick="selectChatTab('all')">💬 Todos</button>
                            <button type="button" class="chat-tab" data-tab="youtube" onclick="selectChatTab('youtube')">🔴 YouTube</button>
                            <button type="button" class="chat-tab" data-tab="facebook" onclick="selectChatTab('facebook')">🔵 Facebook</button>
                        </div>
                        <div class="chat-messages-box" id="chatMessagesBox">
                            <div style="font-size: 11px; color: var(--text-muted); text-align: center; margin-top: 40px;">
                                Conecta el ID de tu transmisión arriba para ver y responder mensajes en tiempo real.
                            </div>
                        </div>
                        <div class="chat-input-bar">
                            <select id="chatTargetPlatform" class="btn-chip" style="padding: 7px; background: rgba(15,23,42,0.9);">
                                <option value="youtube">🔴 YouTube</option>
                                <option value="facebook">🔵 Facebook</option>
                            </select>
                            <input type="text" id="chatReplyInput" placeholder="Escribe una respuesta al chat..." style="padding: 8px 12px; font-size: 12px;" onkeydown="if(event.key==='Enter') sendChatMessage()">
                            <button type="button" class="btn-chip" onclick="sendChatMessage()" style="color: #38bdf8; padding: 8px 14px; font-weight: 800;">
                                Enviar
                            </button>
                        </div>
                    </div>
                </div>

                <!-- LISTAS TEMÁTICAS Y VIDEOS (GUARDADAS PERMANENTEMENTE) -->
                <div class="card">
                    <div class="card-title">
                        <span>📁 Listas de Videos (Guardadas)</span>
                        <div style="display: flex; gap: 6px;">
                            <button type="button" class="btn-chip active" onclick="streamCurrentPlaylist()" style="color: #34d399; font-weight: 800;">
                                ▶ Transmitir Esta Lista
                            </button>
                            <button type="button" class="btn-chip" onclick="createCategoryPrompt()" style="color: #38bdf8;">
                                + Nueva Lista
                            </button>
                        </div>
                    </div>

                    <!-- TABS DE LISTAS DE REPRODUCCION -->
                    <div id="categoryTabs" style="display: flex; gap: 6px; overflow-x: auto; margin-bottom: 12px;"></div>

                    <div class="dropzone" onclick="document.getElementById('videoFileInput').click()">
                        <input type="file" id="videoFileInput" style="display: none;" accept="video/*" multiple onchange="handleFileSelect(event)">
                        <div style="font-size: 26px; margin-bottom: 4px;">☁️</div>
                        <div style="font-size: 13px; font-weight: 700;">Haz clic o arrastra videos aquí</div>
                    </div>

                    <ul class="playlist" id="playlistContainer"></ul>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL QR PARA CONTROL REMOTO -->
    <div id="controlQrModal" style="position: fixed; inset: 0; background: rgba(3,7,18,0.85); backdrop-filter: blur(8px); z-index: 999; display: none; align-items: center; justify-content: center; padding: 20px;" onclick="if(event.target===this) closeControlQrModal()">
        <div style="background: var(--bg-surface); border: 1px solid var(--border-glow); border-radius: 20px; width: 100%; max-width: 420px; padding: 24px; text-align: center;">
            <h3 style="font-size: 18px; margin-bottom: 6px; color: #fff;">📱 Control Remoto Celular</h3>
            <p style="font-size: 12px; color: #94a3b8; margin-bottom: 14px;">Escanea con tu celular para controlar la emisión 24/7 y subir videos:</p>
            <div id="qrBox" style="display: inline-block; background: #fff; padding: 12px; border-radius: 12px; margin-bottom: 14px;"></div>
            <div>
                <input type="text" id="qrLink" readonly style="font-size: 11px; text-align: center; width: 100%; padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.3); color: #38bdf8;">
            </div>
            <button type="button" class="btn-chip" onclick="closeControlQrModal()" style="margin-top: 14px; padding: 8px 24px;">Cerrar</button>
        </div>
    </div>

    <div class="toast" id="toast">Notificación</div>

    <script>
        let isStreaming = false;
        let allVideos = [];
        let allCategories = ["General"];
        let currentCategory = "General";
        let currentPlatform = "youtube";
        let currentStreamFormat = "vertical";
        let serverLocalIp = window.location.hostname;
        let activeChatTab = "all";
        let allChatMessages = [];
        let isMuted = true;
        let lastPlayedUrl = "";

        /* OVERLAYS SYSTEM (8 HANDLES + ROTACIÓN 360°) */
        let activeOverlays = [];
        let selectedOverlayId = null;

        function showToast(msg) {
            const t = document.getElementById("toast");
            t.innerText = msg;
            t.classList.add("show");
            setTimeout(() => t.classList.remove("show"), 2800);
        }

        /* TEMAS */
        function changeTheme(themeName) {
            document.documentElement.setAttribute("data-theme", themeName);
            document.getElementById("themeSelector").value = themeName;
            localStorage.setItem("streamhub_theme", themeName);
            fetch("/api/theme", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ theme: themeName })
            });
        }

        /* MONITOR VIDEO */
        function toggleMuteVideo() {
            const player = document.getElementById("liveVideoPlayer");
            const btn = document.getElementById("btnMute");
            isMuted = !isMuted;
            player.muted = isMuted;
            btn.innerText = isMuted ? "🔇 Silenciado" : "🔊 Audio Activo";
        }

        function setVideoPlayerSource(url, isLiveStream = false, videoTitle = "") {
            const player = document.getElementById("liveVideoPlayer");
            const modeText = document.getElementById("monitorModeBadge");
            if (isLiveStream) {
                modeText.innerText = "🔴 En Transmisión";
                modeText.style.color = "#ef4444";
            } else {
                modeText.innerText = `👁️ Vista Previa (${videoTitle || "Estudio"})`;
                modeText.style.color = "#38bdf8";
            }
            if (url && url !== lastPlayedUrl) {
                lastPlayedUrl = url;
                player.src = url;
                player.play().catch(() => {});
            }
        }

        function previewVideoFile(cat, name) {
            const url = `/videos/${encodeURIComponent(cat)}/${encodeURIComponent(name)}`;
            setVideoPlayerSource(url, false, name);
            showToast(`👁️ Vista previa: ${name}`);
            fetch("/api/preview", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ category: cat, name: name })
            });
        }

        /* PLATAFORMAS & CLAVES */
        function selectPlatform(plat) {
            currentPlatform = plat;
            document.querySelectorAll(".platform-btn").forEach(b => {
                b.classList.toggle("active", b.dataset.plat === plat);
            });
            const panels = ["panelYoutube", "panelFacebook", "panelTwitch", "panelCustom", "panelTiktok", "panelKick", "panelMultistream"];
            panels.forEach(p => {
                const el = document.getElementById(p);
                if (el) el.style.display = "none";
            });
            if (plat === "youtube") document.getElementById("panelYoutube").style.display = "block";
            else if (plat === "facebook") document.getElementById("panelFacebook").style.display = "block";
            else if (plat === "twitch") document.getElementById("panelTwitch").style.display = "block";
            else if (plat === "custom") document.getElementById("panelCustom").style.display = "block";
            else if (plat === "tiktok") document.getElementById("panelTiktok").style.display = "block";
            else if (plat === "kick") document.getElementById("panelKick").style.display = "block";
            else if (plat === "multistream") document.getElementById("panelMultistream").style.display = "block";
            autoSaveKeys();
        }

        function toggleKeyVisibility(id) {
            const el = document.getElementById(id);
            el.type = (el.type === "password") ? "text" : "password";
        }

        function changeFormat(fmt) {
            currentStreamFormat = fmt;
            document.getElementById("btnFmt_vertical").classList.toggle("active", fmt === "vertical");
            document.getElementById("btnFmt_horizontal").classList.toggle("active", fmt === "horizontal");

            const mf = document.querySelector(".monitor-frame");
            if (mf) {
                mf.style.height = (fmt === "vertical") ? "380px" : "260px";
                mf.style.maxWidth = (fmt === "vertical") ? "240px" : "100%";
                mf.style.margin = (fmt === "vertical") ? "0 auto 14px auto" : "0 0 14px 0";
            }
            fetch("/api/control", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "switch_format", format: fmt })
            });
        }

        async function skipCurrentVideo() {
            await fetch("/api/control", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "skip" })
            });
            showToast("⏭ Saltando al siguiente video...");
        }

        function toggleCycleMode() {
            fetch("/api/control", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "toggle_cycle_mode" })
            })
            .then(r => r.json())
            .then(d => showToast(d.message || "Modo actualizado"));
        }

        /* AUTO SAVE KEYS */
        let autoSaveTimer = null;
        function autoSaveKeys() {
            clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(() => {
                fetch("/api/control", {
                    method: "POST", headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        action: "save_keys",
                        platform: currentPlatform,
                        stream_key: document.getElementById("streamKeyInput").value.trim(),
                        facebook_key: document.getElementById("facebookKeyInput").value.trim(),
                        twitch_key: document.getElementById("twitchKeyInput").value.trim(),
                        custom_rtmp_url: document.getElementById("customRtmpUrlInput").value.trim(),
                        custom_rtmp_key: document.getElementById("customRtmpKeyInput").value.trim(),
                        tiktok_server: document.getElementById("tiktokServerInput").value.trim(),
                        tiktok_key: document.getElementById("tiktokKeyInput").value.trim(),
                        kick_server: document.getElementById("kickServerInput").value.trim(),
                        kick_key: document.getElementById("kickKeyInput").value.trim(),
                        multistream_targets: {
                            youtube: document.getElementById("chkMultiYt").checked,
                            facebook: document.getElementById("chkMultiFb").checked,
                            twitch: document.getElementById("chkMultiTw").checked,
                            custom: document.getElementById("chkMultiCustom").checked,
                            tiktok: document.getElementById("chkMultiTiktok").checked,
                            kick: document.getElementById("chkMultiKick").checked
                        }
                    })
                });
            }, 500);
        }

        async function testConnection() {
            const fbBox = document.getElementById("testFeedbackBox");
            fbBox.className = "test-feedback loading";
            fbBox.innerText = `⏳ Verificando conexión con ${currentPlatform.toUpperCase()}...`;
            fbBox.style.display = "block";

            try {
                const res = await fetch("/api/test_connection", {
                    method: "POST", headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        platform: currentPlatform,
                        stream_key: document.getElementById("streamKeyInput").value.trim(),
                        facebook_key: document.getElementById("facebookKeyInput").value.trim(),
                        twitch_key: document.getElementById("twitchKeyInput").value.trim(),
                        custom_rtmp_url: document.getElementById("customRtmpUrlInput").value.trim(),
                        custom_rtmp_key: document.getElementById("customRtmpKeyInput").value.trim(),
                        tiktok_key: document.getElementById("tiktokKeyInput").value.trim(),
                        tiktok_server: document.getElementById("tiktokServerInput").value.trim(),
                        kick_key: document.getElementById("kickKeyInput").value.trim(),
                        kick_server: document.getElementById("kickServerInput").value.trim(),
                        multistream_targets: {
                            youtube: document.getElementById("chkMultiYt").checked,
                            facebook: document.getElementById("chkMultiFb").checked,
                            twitch: document.getElementById("chkMultiTw").checked,
                            custom: document.getElementById("chkMultiCustom").checked,
                            tiktok: document.getElementById("chkMultiTiktok").checked,
                            kick: document.getElementById("chkMultiKick").checked
                        }
                    })
                });
                const d = await res.json();
                fbBox.className = d.success ? "test-feedback success" : "test-feedback error";
                fbBox.innerText = d.message;
            } catch (err) {
                fbBox.className = "test-feedback error";
                fbBox.innerText = "❌ Error contactando al servidor: " + err.message;
            }
        }

        async function startStream() {
            try {
                const res = await fetch("/api/control", {
                    method: "POST", headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        action: "start",
                        platform: currentPlatform,
                        stream_key: document.getElementById("streamKeyInput").value.trim(),
                        facebook_key: document.getElementById("facebookKeyInput").value.trim(),
                        twitch_key: document.getElementById("twitchKeyInput").value.trim(),
                        custom_rtmp_url: document.getElementById("customRtmpUrlInput").value.trim(),
                        custom_rtmp_key: document.getElementById("customRtmpKeyInput").value.trim(),
                        tiktok_key: document.getElementById("tiktokKeyInput").value.trim(),
                        kick_key: document.getElementById("kickKeyInput").value.trim(),
                        active_category: currentCategory,
                        format: currentStreamFormat,
                        multistream_targets: {
                            youtube: document.getElementById("chkMultiYt").checked,
                            facebook: document.getElementById("chkMultiFb").checked,
                            twitch: document.getElementById("chkMultiTw").checked,
                            custom: document.getElementById("chkMultiCustom").checked,
                            tiktok: document.getElementById("chkMultiTiktok").checked,
                            kick: document.getElementById("chkMultiKick").checked
                        }
                    })
                });
                const d = await res.json();
                showToast(d.message || "Emisión iniciada");
            } catch (err) {
                showToast("Error al iniciar emisión");
            }
        }

        async function stopStream() {
            const res = await fetch("/api/control", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "stop" })
            });
            const d = await res.json();
            showToast(d.message || "Emisión detenida");
        }

        /* PLAYLISTS & VIDEOS */
        function streamCurrentPlaylist() {
            fetch("/api/control", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "set_playlist", category: currentCategory })
            }).then(() => showToast(`▶ Transmitiendo lista: ${currentCategory}`));
        }

        async function createCategoryPrompt() {
            const name = prompt("Nombre de la nueva lista temática (ej. Prédicas, Shorts, Alabanzas):");
            if (!name || !name.trim()) return;
            const res = await fetch("/api/category/create", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: name.trim() })
            });
            const d = await res.json();
            if (d.success) {
                showToast(`Lista '${name.trim()}' creada`);
                fetch("/api/status").then(r => r.json()).then(applyServerState);
            }
        }

        function selectCategory(cat) {
            currentCategory = cat;
            renderCategoryTabs();
            renderPlaylist();
            fetch("/api/control", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "set_category", category: cat })
            });
        }

        function renderCategoryTabs() {
            const container = document.getElementById("categoryTabs");
            container.innerHTML = allCategories.map(c => {
                const count = allVideos.filter(v => v.category === c).length;
                return `
                <button type="button" class="btn-chip ${c === currentCategory ? 'active' : ''}" onclick="selectCategory('${c}')">
                    📁 ${c} <span style="opacity: 0.7; font-size: 10px;">(${count})</span>
                </button>
            `}).join("");
        }

        function renderPlaylist() {
            const vids = allVideos.filter(v => v.category === currentCategory);
            const container = document.getElementById("playlistContainer");

            if (vids.length === 0) {
                container.innerHTML = `<li style="font-size: 12px; color: var(--text-muted); text-align: center; padding: 20px;">No hay videos en '${currentCategory}'. Sube archivos arriba.</li>`;
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
                    <div style="display: flex; gap: 4px;">
                        <button type="button" class="btn-chip" onclick="previewVideoFile('${v.category}', '${v.name}')" title="Ver previa en monitor">
                            👁️ Previa
                        </button>
                        <button type="button" class="btn-chip" onclick="playVideoImmediately('${v.category}', '${v.name}')" style="color: #34d399;" title="Emitir ahora">
                            ⚡ Emitir
                        </button>
                        <button type="button" class="btn-chip" onclick="deleteVideo('${v.category}', '${v.name}')" style="color: #f87171;" title="Eliminar">
                            🗑️
                        </button>
                    </div>
                </li>
            `}).join("");
        }

        function playVideoImmediately(cat, name) {
            if (confirm(`¿Transmitir '${name}' inmediatamente en vivo?`)) {
                fetch("/api/control", {
                    method: "POST", headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ action: "play_now", category: cat, name: name })
                }).then(() => showToast(`⚡ Emitiendo: ${name}`));
            }
        }

        async function deleteVideo(cat, filename) {
            if (!confirm(`¿Eliminar '${filename}' de la lista '${cat}'?`)) return;
            const res = await fetch(`/api/delete/${encodeURIComponent(cat)}/${encodeURIComponent(filename)}`, { method: "POST" });
            const d = await res.json();
            if (d.success) {
                showToast("Video eliminado");
                fetch("/api/status").then(r => r.json()).then(applyServerState);
            }
        }

        async function handleFileSelect(event) {
            const files = event.target.files;
            if (!files.length) return;
            const formData = new FormData();
            formData.append("category", currentCategory);
            for (let i = 0; i < files.length; i++) {
                formData.append("video_file", files[i]);
            }
            showToast(`Subiendo ${files.length} video(s)...`);
            try {
                const res = await fetch("/api/upload", { method: "POST", body: formData });
                const d = await res.json();
                if (d.success) {
                    showToast(d.message);
                    fetch("/api/status").then(r => r.json()).then(applyServerState);
                } else {
                    showToast("Error en subida: " + (d.message || ""));
                }
            } catch (err) {
                showToast("Error de red durante la subida");
            }
        }

        /* OVERLAYS ENGINE CON 8 TIRADORES Y ROTACIÓN 360° */
        function renderOverlaysCanvas() {
            const container = document.getElementById("overlayCanvasLayer");
            if (!container) return;
            container.innerHTML = "";

            activeOverlays.forEach(ov => {
                if (!ov.visible) return;
                const el = document.createElement("div");
                el.className = `canvas-overlay-item ${ov.id === selectedOverlayId ? 'selected' : ''}`;
                el.id = `canvas_ov_${ov.id}`;
                el.style.left = `${ov.x}px`;
                el.style.top = `${ov.y}px`;
                if (ov.width) el.style.width = `${ov.width}px`;
                if (ov.height) el.style.height = `${ov.height}px`;
                el.style.transform = `rotate(${ov.rotation || 0}deg)`;
                el.style.fontSize = `${ov.fontSize || 14}px`;
                el.style.color = ov.color || "#fff";
                el.style.backgroundColor = ov.bg || "rgba(15, 23, 42, 0.85)";
                el.style.opacity = ov.opacity || 1;

                if (ov.type === "image" || ov.type === "sticker") {
                    el.innerHTML = `<img src="${ov.image_url}" alt="Overlay" style="width: 100%; height: 100%; object-fit: contain; pointer-events: none;">`;
                } else {
                    el.innerText = ov.text || "";
                }

                // Tiradores
                const handles = ["nw", "n", "ne", "e", "se", "s", "sw", "w"];
                handles.forEach(h => {
                    const hd = document.createElement("div");
                    hd.className = `handle ${h}`;
                    hd.dataset.handle = h;
                    el.appendChild(hd);
                });

                // Mástil y Tirador de rotación
                const stem = document.createElement("div");
                stem.className = "rot-stem";
                el.appendChild(stem);

                const rotHandle = document.createElement("div");
                rotHandle.className = "rot-handle";
                rotHandle.title = "Arrastra para rotar 360°";
                el.appendChild(rotHandle);

                const degBadge = document.createElement("div");
                degBadge.className = "rot-deg-badge";
                degBadge.innerText = `${Math.round(ov.rotation || 0)}°`;
                el.appendChild(degBadge);

                el.addEventListener("mousedown", (e) => startOverlayInteraction(e, ov.id));
                el.addEventListener("touchstart", (e) => startOverlayInteraction(e, ov.id), { passive: false });

                container.appendChild(el);
            });

            renderLayersTable();
        }

        function renderLayersTable() {
            const tbody = document.getElementById("layersTableBody");
            if (!tbody) return;
            if (activeOverlays.length === 0) {
                tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">No hay capas en pantalla</td></tr>`;
                return;
            }

            tbody.innerHTML = activeOverlays.map(ov => `
                <tr style="${ov.id === selectedOverlayId ? 'background: rgba(56, 189, 248, 0.1);' : ''}">
                    <td>
                        <strong style="color: ${ov.id === selectedOverlayId ? '#38bdf8' : '#fff'};">${ov.text || ov.id}</strong>
                    </td>
                    <td>${Math.round(ov.rotation || 0)}°</td>
                    <td>${Math.round(ov.width || 120)}x${Math.round(ov.height || 40)}</td>
                    <td>
                        <button type="button" class="btn-chip" onclick="toggleOverlayVisibility('${ov.id}')" title="Mostrar/Ocultar">
                            ${ov.visible ? '👁️' : '🙈'}
                        </button>
                        <button type="button" class="btn-chip" onclick="resetOverlayRotation('${ov.id}')" title="Resetear giro a 0°">
                            🔄 0°
                        </button>
                        <button type="button" class="btn-chip" onclick="deleteOverlayItem('${ov.id}')" style="color: #f87171;" title="Eliminar">
                            🗑️
                        </button>
                    </td>
                </tr>
            `).join("");
        }

        function selectOverlay(id) {
            selectedOverlayId = id;
            renderOverlaysCanvas();
        }

        function toggleOverlayVisibility(id) {
            const ov = activeOverlays.find(o => o.id === id);
            if (ov) {
                ov.visible = !ov.visible;
                renderOverlaysCanvas();
            }
        }

        function resetOverlayRotation(id) {
            const ov = activeOverlays.find(o => o.id === id);
            if (ov) {
                ov.rotation = 0;
                renderOverlaysCanvas();
            }
        }

        function deleteOverlayItem(id) {
            activeOverlays = activeOverlays.filter(o => o.id !== id);
            if (selectedOverlayId === id) selectedOverlayId = null;
            renderOverlaysCanvas();
        }

        function insertEmoji(em) {
            const inp = document.getElementById("newRotuloInput");
            inp.value += em;
            inp.focus();
        }

        function addNewRotulo() {
            const inp = document.getElementById("newRotuloInput");
            const text = inp.value.trim();
            if (!text) return;
            const newId = `rotulo_${Date.now()}`;
            activeOverlays.push({
                id: newId,
                type: "rotulo",
                text: text,
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
            selectOverlay(newId);
            showToast("➕ Rótulo agregado al lienzo");
        }

        function addStickerOverlay(url, name) {
            const newId = `sticker_${Date.now()}`;
            activeOverlays.push({
                id: newId,
                type: "sticker",
                text: name,
                image_url: url,
                x: 80,
                y: 120,
                width: 80,
                height: 80,
                rotation: 0,
                fontSize: 12,
                color: "#ffffff",
                bg: "transparent",
                opacity: 1,
                visible: true
            });
            selectOverlay(newId);
            showToast(`🎨 Sticker '${name}' colocado`);
        }

        function handleOverlayImageUpload(e) {
            const file = e.target.files[0];
            if (!file) return;
            const fd = new FormData();
            fd.append("image_file", file);
            showToast("Subiendo imagen para el lienzo...");
            fetch("/api/overlay/upload_image", { method: "POST", body: fd })
                .then(r => r.json())
                .then(d => {
                    if (d.success) {
                        addStickerOverlay(d.url, "Logo Personalizado");
                        showToast("✅ Logo subido y colocado en el lienzo");
                    } else {
                        showToast("Error: " + d.message);
                    }
                });
        }

        function saveAndApplyOverlays() {
            fetch("/api/overlay/config", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ overlays: activeOverlays })
            }).then(() => showToast("💾 Rótulos y capas guardados en emisión"));
        }

        /* INTERACCIÓN DRAG, RESIZE 8-HANDLES & ROTATE 360° */
        let currentDragState = null;

        function startOverlayInteraction(e, id) {
            e.stopPropagation();
            selectOverlay(id);
            const ov = activeOverlays.find(o => o.id === id);
            if (!ov) return;

            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            const target = e.target;

            if (target.classList.contains("rot-handle")) {
                // Modo rotación 360°
                const el = document.getElementById(`canvas_ov_${id}`);
                const rect = el.getBoundingClientRect();
                const centerX = rect.left + rect.width / 2;
                const centerY = rect.top + rect.height / 2;
                currentDragState = {
                    mode: "rotate",
                    id: id,
                    centerX: centerX,
                    centerY: centerY,
                    startRotation: ov.rotation || 0
                };
            } else if (target.classList.contains("handle")) {
                // Modo resize (8 handles)
                currentDragState = {
                    mode: "resize",
                    id: id,
                    handle: target.dataset.handle,
                    startX: clientX,
                    startY: clientY,
                    origX: ov.x,
                    origY: ov.y,
                    origW: ov.width || 120,
                    origH: ov.height || 40
                };
            } else {
                // Modo mover / drag
                currentDragState = {
                    mode: "drag",
                    id: id,
                    startX: clientX,
                    startY: clientY,
                    origX: ov.x,
                    origY: ov.y
                };
            }

            window.addEventListener("mousemove", onOverlayInteractionMove);
            window.addEventListener("mouseup", endOverlayInteraction);
            window.addEventListener("touchmove", onOverlayInteractionMove, { passive: false });
            window.addEventListener("touchend", endOverlayInteraction);
        }

        function onOverlayInteractionMove(e) {
            if (!currentDragState) return;
            e.preventDefault();
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            const ov = activeOverlays.find(o => o.id === currentDragState.id);
            if (!ov) return;

            if (currentDragState.mode === "drag") {
                const dx = clientX - currentDragState.startX;
                const dy = clientY - currentDragState.startY;
                ov.x = Math.max(0, currentDragState.origX + dx);
                ov.y = Math.max(0, currentDragState.origY + dy);
            } else if (currentDragState.mode === "rotate") {
                const dx = clientX - currentDragState.centerX;
                const dy = clientY - currentDragState.centerY;
                let angle = Math.atan2(dy, dx) * (180 / Math.PI) + 90;
                if (angle < 0) angle += 360;

                // Snap magnético a 0, 45, 90, 135, 180, 225, 270, 315, 360
                const snapAngles = [0, 45, 90, 135, 180, 225, 270, 315, 360];
                snapAngles.forEach(snap => {
                    if (Math.abs(angle - snap) < 4) angle = snap % 360;
                });
                ov.rotation = Math.round(angle);
            } else if (currentDragState.mode === "resize") {
                const dx = clientX - currentDragState.startX;
                const dy = clientY - currentDragState.startY;
                const h = currentDragState.handle;

                if (h.includes("e")) ov.width = Math.max(30, currentDragState.origW + dx);
                if (h.includes("s")) ov.height = Math.max(20, currentDragState.origH + dy);
                if (h.includes("w")) {
                    const newW = Math.max(30, currentDragState.origW - dx);
                    ov.x = currentDragState.origX + (currentDragState.origW - newW);
                    ov.width = newW;
                }
                if (h.includes("n")) {
                    const newH = Math.max(20, currentDragState.origH - dy);
                    ov.y = currentDragState.origY + (currentDragState.origH - newH);
                    ov.height = newH;
                }
            }

            renderOverlaysCanvas();
        }

        function endOverlayInteraction() {
            currentDragState = null;
            window.removeEventListener("mousemove", onOverlayInteractionMove);
            window.removeEventListener("mouseup", endOverlayInteraction);
            window.removeEventListener("touchmove", onOverlayInteractionMove);
            window.removeEventListener("touchend", endOverlayInteraction);
        }

        /* CHAT EN VIVO */
        function selectChatTab(tab) {
            activeChatTab = tab;
            document.querySelectorAll(".chat-tab").forEach(t => {
                t.classList.toggle("active", t.dataset.tab === tab);
            });
            renderChatMessages();
        }

        function connectLiveChats() {
            const yt = document.getElementById("ytVideoIdInput").value.trim();
            const fb = document.getElementById("fbLiveIdInput").value.trim();
            fetch("/api/chat/connect", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ youtube_video_id: yt, facebook_live_id: fb })
            })
            .then(r => r.json())
            .then(() => {
                showToast("🔗 Conectando chats en vivo...");
                updatePopoutLinks(yt);
            });
        }

        function updatePopoutLinks(ytVid) {
            const btnPop = document.getElementById("btnPopoutYtChat");
            if (ytVid) {
                let vidId = ytVid;
                const m = ytVid.match(/(?:v=|\/live\/|\.be\/)([a-zA-Z0-9_-]{11})/);
                if (m) vidId = m[1];
                btnPop.href = `https://www.youtube.com/live_chat?v=${vidId}&is_popout=1`;
                btnPop.style.display = "inline-flex";
            }
        }

        function sendChatMessage() {
            const inMsg = document.getElementById("chatReplyInput");
            const text = inMsg.value.trim();
            if (!text) return;
            const plat = document.getElementById("chatTargetPlatform").value;

            fetch("/api/chat/send", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ platform: plat, message: text })
            })
            .then(r => r.json())
            .then(d => {
                inMsg.value = "";
                if (d.item) {
                    allChatMessages.push(d.item);
                    renderChatMessages();
                }
            });
        }

        function renderChatMessages() {
            const box = document.getElementById("chatMessagesBox");
            const filtered = allChatMessages.filter(m => {
                if (activeChatTab === "all") return true;
                return m.platform === activeChatTab;
            });

            if (filtered.length === 0) {
                box.innerHTML = `<div style="font-size: 11px; color: var(--text-muted); text-align: center; margin-top: 40px;">No hay mensajes en esta pestaña aún.</div>`;
                return;
            }

            box.innerHTML = filtered.map(m => {
                const platIcon = (m.platform === "youtube") ? "🔴" : "🔵";
                const authorClass = m.is_owner ? "me" : ((m.platform === "youtube") ? "yt" : "fb");
                return `
                    <div class="chat-msg ${m.is_owner ? 'owner' : ''}">
                        <span style="font-size: 12px;">${platIcon}</span>
                        <div style="flex: 1; overflow: hidden;">
                            <span class="chat-author ${authorClass}">${m.author}:</span>
                            <span style="color: #f1f5f9;">${m.message}</span>
                            ${m.amount ? `<span style="background: #eab308; color: #000; font-size: 10px; font-weight: 800; padding: 2px 6px; border-radius: 4px; margin-left: 6px;">${m.amount}</span>` : ''}
                        </div>
                        <span style="font-size: 10px; color: var(--text-muted);">${m.datetime || ''}</span>
                    </div>
                `;
            }).join("");

            box.scrollTop = box.scrollHeight;
        }

        /* MODAL QR */
        function openControlQrModal() {
            const host = (serverLocalIp && serverLocalIp !== "localhost" && serverLocalIp !== "127.0.0.1") 
                         ? serverLocalIp : window.location.hostname;
            const port = window.location.port ? (":" + window.location.port) : ":5000";
            const proto = window.location.protocol + "//";
            const url = proto + host + port + "/control";

            document.getElementById("qrLink").value = url;
            const cont = document.getElementById("qrBox");
            cont.innerHTML = "";
            new QRCode(cont, { text: url, width: 180, height: 180 });
            document.getElementById("controlQrModal").style.display = "flex";
        }

        function closeControlQrModal() {
            document.getElementById("controlQrModal").style.display = "none";
        }

        /* SINCRONIZACION Y ESTADO DEL SERVIDOR */
        function applyServerState(data) {
            if (!data) return;
            isStreaming = (data.status === "Transmitiendo");

            const badge = document.getElementById("liveBadge");
            const btnStart = document.getElementById("btnStart");
            const btnStop = document.getElementById("btnStop");
            const curVid = document.getElementById("currentVideoDisplay");

            badge.className = isStreaming ? "badge-live active" : "badge-live";
            document.getElementById("statusText").innerText = isStreaming ? "EN DIRECTO 24/7 🔴" : "DETENIDO ⏹";
            btnStart.disabled = isStreaming;
            btnStop.disabled = !isStreaming;

            curVid.innerText = data.current_video || "Ninguno";

            if (isStreaming && data.current_video_url) {
                setVideoPlayerSource(data.current_video_url, true, data.current_video);
            } else if (!isStreaming && data.preview_video_url) {
                setVideoPlayerSource(data.preview_video_url, false, data.preview_video_name);
            }

            if (data.stream_format) {
                currentStreamFormat = data.stream_format;
                document.getElementById("btnFmt_vertical").classList.toggle("active", currentStreamFormat === "vertical");
                document.getElementById("btnFmt_horizontal").classList.toggle("active", currentStreamFormat === "horizontal");
                const mf = document.querySelector(".monitor-frame");
                if (mf) {
                    mf.style.height = (currentStreamFormat === "vertical") ? "380px" : "260px";
                    mf.style.maxWidth = (currentStreamFormat === "vertical") ? "240px" : "100%";
                    mf.style.margin = (currentStreamFormat === "vertical") ? "0 auto 14px auto" : "0 0 14px 0";
                }
            }

            if (data.categories) allCategories = data.categories;
            if (data.videos) allVideos = data.videos;
            if (data.active_category) currentCategory = data.active_category;
            renderCategoryTabs();
            renderPlaylist();

            if (data.live_viewers !== undefined) {
                document.getElementById("liveViewersDisplay").innerText = `${data.live_viewers} en vivo`;
            }
            if (data.panel_connected_devices !== undefined) {
                document.getElementById("connectedDevicesDisplay").innerText = `${data.panel_connected_devices} conectado(s)`;
            }

            if (data.theme) {
                document.documentElement.setAttribute("data-theme", data.theme);
                document.getElementById("themeSelector").value = data.theme;
            }

            if (data.overlays && (!activeOverlays || activeOverlays.length === 0)) {
                activeOverlays = data.overlays;
                renderOverlaysCanvas();
            }

            // Monetización
            const btnCycle = document.getElementById("btnToggleCycleMode");
            const isCycleOn = Boolean(data.youtube_cycle_mode);
            btnCycle.innerText = isCycleOn ? "🔘 Modo Ciclo 11:55: ACTIVO" : "⚪ Modo 24/7 Continuo";
            btnCycle.style.color = isCycleOn ? "#f87171" : "#10b981";

            const totalCycleSec = data.cycle_duration_seconds || (11 * 3600 + 55 * 60);
            const elapsedSec = data.cycle_elapsed_seconds || 0;
            const remainingSec = Math.max(0, totalCycleSec - elapsedSec);
            const rHours = Math.floor(remainingSec / 3600);
            const rMins = Math.floor((remainingSec % 3600) / 60);
            const rSecs = remainingSec % 60;
            const pad = (n) => String(n).padStart(2, '0');
            document.getElementById("cycleCountdownText").innerText = `${pad(rHours)}:${pad(rMins)}:${pad(rSecs)}`;
            document.getElementById("cycleCountBadge").innerText = `#${data.cycle_count || 1}`;

            const cyclePct = Math.min(100, Math.round((elapsedSec / totalCycleSec) * 100));
            document.getElementById("cycleProgressBar").style.width = cyclePct + "%";
            document.getElementById("cycleElapsedPercent").innerText = `${cyclePct}% del ciclo`;

            const goal = data.monetization_goal || 4000;
            const unit = data.monetization_unit || "minutos";
            const prog = data.total_monetization_minutes || 0.0;
            const progDisplay = (unit === "minutos") ? prog.toFixed(1) : (prog / 60).toFixed(1);
            const progPct = Math.min(100, ((prog / goal) * 100)).toFixed(1);
            document.getElementById("monetizationGoalText").innerText = `${progDisplay} / ${goal} ${unit} (${progPct}%)`;
            document.getElementById("monetizationTotalBar").style.width = Math.min(100, progPct) + "%";

            // IDs y Claves
            if (data.youtube_video_id && !document.getElementById("ytVideoIdInput").value) {
                document.getElementById("ytVideoIdInput").value = data.youtube_video_id;
                updatePopoutLinks(data.youtube_video_id);
            }
            if (data.facebook_live_id && !document.getElementById("fbLiveIdInput").value) {
                document.getElementById("fbLiveIdInput").value = data.facebook_live_id;
            }
            if (data.stream_key && !document.getElementById("streamKeyInput").value) {
                document.getElementById("streamKeyInput").value = data.stream_key;
            }
            if (data.facebook_key && !document.getElementById("facebookKeyInput").value) {
                document.getElementById("facebookKeyInput").value = data.facebook_key;
            }
            if (data.twitch_key && !document.getElementById("twitchKeyInput").value) {
                document.getElementById("twitchKeyInput").value = data.twitch_key;
            }
            if (data.custom_rtmp_url && !document.getElementById("customRtmpUrlInput").value) {
                document.getElementById("customRtmpUrlInput").value = data.custom_rtmp_url;
            }
            if (data.custom_rtmp_key && !document.getElementById("customRtmpKeyInput").value) {
                document.getElementById("customRtmpKeyInput").value = data.custom_rtmp_key;
            }
            if (data.tiktok_key && !document.getElementById("tiktokKeyInput").value) {
                document.getElementById("tiktokKeyInput").value = data.tiktok_key;
            }
            if (data.kick_key && !document.getElementById("kickKeyInput").value) {
                document.getElementById("kickKeyInput").value = data.kick_key;
            }

            if (data.chat_messages) {
                allChatMessages = data.chat_messages;
                renderChatMessages();
            }

            if (data.logs && data.logs.length > 0) {
                const term = document.getElementById("terminalLogs");
                term.innerHTML = data.logs.map(l => `<div>${l}</div>`).join("");
                term.scrollTop = term.scrollHeight;

                for (let i = data.logs.length - 1; i >= 0; i--) {
                    const l = data.logs[i];
                    if (l.includes("fps=")) {
                        const mFps = l.match(/fps=\s*([\d.]+)/);
                        const mBit = l.match(/bitrate=\s*([\d.]+)/);
                        if (mFps && mBit) {
                            document.getElementById("telemetryBitrate").innerText = `~${mBit[1]}k / ${mFps[1]}fps`;
                            break;
                        }
                    }
                }
            }
        }

        /* WEBSOCKET */
        let syncSocket = null;
        function connectSyncSocket() {
            const wsProto = (location.protocol === "https:") ? "wss:" : "ws:";
            syncSocket = new WebSocket(`${wsProto}//${location.host}/ws/sync`);
            syncSocket.onmessage = (e) => {
                try {
                    const res = JSON.parse(e.data);
                    if (res.type === "state_update") {
                        applyServerState(res.state);
                    } else if (res.type === "chat_message") {
                        allChatMessages.push(res.message);
                        renderChatMessages();
                    }
                } catch(err) {}
            };
            syncSocket.onclose = () => setTimeout(connectSyncSocket, 2000);
            syncSocket.onerror = () => { try { syncSocket.close(); } catch(e){} };
        }
        connectSyncSocket();

        setInterval(() => {
            fetch("/api/status").then(r => r.json()).then(applyServerState);
        }, 2500);

        // Inicializar tema guardado
        const savedTheme = localStorage.getItem("streamhub_theme") || "cyber_dark";
        changeTheme(savedTheme);
        renderOverlaysCanvas();
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    html = build_index_html()
    base_panel = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'panel_stream'))
    
    t1 = os.path.join(base_panel, 'templates', 'index.html')
    t2 = os.path.join(base_panel, 'index.html')
    
    os.makedirs(os.path.dirname(t1), exist_ok=True)
    with open(t1, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(t2, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"index.html written to {t1} and {t2} ({len(html)} bytes)")
