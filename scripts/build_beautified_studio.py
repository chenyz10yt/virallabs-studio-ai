import os, sys, re, shutil

base_panel = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream"
index_path = os.path.join(base_panel, "index.html")
tpl_index = os.path.join(base_panel, "templates", "index.html")

print("Generating unified, highly aesthetic and beautifully organized index.html...")

with open(index_path, 'r', encoding='utf-8') as f:
    current_content = f.read()

script_start = current_content.find('<script>')
script_end = current_content.rfind('</script>')
if script_start != -1 and script_end != -1:
    extracted_script = current_content[script_start + len('<script>'):script_end]
else:
    print("ERROR: could not locate script tag!")
    sys.exit(1)

# Ensure subtab switchers and DOM compatibility helpers exist in script
compat_js = '''
        /* NAVEGACION UNIFICADA DE SUB-PESTANAS */
        function switchOverlaySubTab(tabId) {
            document.querySelectorAll(".overlay-subtab-btn").forEach(btn => {
                btn.classList.toggle("active", btn.dataset.tab === tabId);
            });
            document.querySelectorAll(".overlay-tab-pane").forEach(pane => {
                pane.style.display = (pane.id === `overlay_pane_${tabId}`) ? "block" : "none";
            });
        }

        function switchCommunitySubTab(tabId) {
            document.querySelectorAll(".community-subtab-btn").forEach(btn => {
                btn.classList.toggle("active", btn.dataset.tab === tabId);
            });
            document.querySelectorAll(".community-tab-pane").forEach(pane => {
                pane.style.display = (pane.id === `community_pane_${tabId}`) ? "block" : "none";
            });
        }

        // Sincronizacion de alias para elementos clave
        function syncElementAliases() {
            const pairs = [
                ['categoryTabs', 'categoryTabsContainer'],
                ['playlistContainer', 'categoryVideosList'],
                ['chatMessagesBox', 'chatMessagesContainer'],
                ['chatReplyInput', 'chatInputText'],
                ['terminalLogs', 'ffmpegLogsBox'],
                ['toast', 'toastNotice'],
                ['cycleCountBadge', 'cycleCounterText'],
                ['monetizationTotalBar', 'cycleProgressBar'],
                ['cycleElapsedPercent', 'cycleProgressText']
            ];
        }
'''

if 'function switchOverlaySubTab' not in extracted_script:
    extracted_script = compat_js + "\n" + extracted_script

new_html = r'''<!DOCTYPE html>
<html lang="es" data-theme="cyber_dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StreamHub 24/7 Studio - Panel de Emisión Profesional</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <style>
        :root {
            --bg-base: #060911;
            --bg-surface: #0c1222;
            --bg-card: rgba(15, 23, 42, 0.78);
            --bg-card-hover: rgba(22, 33, 58, 0.88);
            --border: rgba(255, 255, 255, 0.08);
            --border-hover: rgba(56, 189, 248, 0.28);
            --border-glow: rgba(56, 189, 248, 0.45);
            --primary: #0284c7;
            --primary-glow: #38bdf8;
            --success: #10b981;
            --success-glow: #34d399;
            --danger: #ef4444;
            --danger-glow: #f87171;
            --warning: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --terminal-bg: #030712;
            --accent-gradient: linear-gradient(135deg, #0284c7, #38bdf8);
            --accent-glow: 0 0 20px rgba(56, 189, 248, 0.35);
        }

        /* 7 TEMAS PERSONALIZADOS COMPLETAMENTE ARMONIZADOS */
        [data-theme="twitch_purple"] {
            --bg-base: #090414;
            --bg-surface: #14092b;
            --bg-card: rgba(24, 13, 48, 0.82);
            --border: rgba(192, 132, 252, 0.14);
            --border-hover: rgba(192, 132, 252, 0.35);
            --border-glow: rgba(192, 132, 252, 0.5);
            --primary: #9333ea;
            --primary-glow: #c084fc;
            --accent-gradient: linear-gradient(135deg, #9333ea, #c084fc);
            --accent-glow: 0 0 20px rgba(192, 132, 252, 0.35);
        }

        [data-theme="yt_crimson"] {
            --bg-base: #0d0406;
            --bg-surface: #1c090d;
            --bg-card: rgba(36, 13, 19, 0.82);
            --border: rgba(239, 68, 68, 0.14);
            --border-hover: rgba(239, 68, 68, 0.35);
            --border-glow: rgba(239, 68, 68, 0.5);
            --primary: #dc2626;
            --primary-glow: #f87171;
            --accent-gradient: linear-gradient(135deg, #dc2626, #f87171);
            --accent-glow: 0 0 20px rgba(239, 68, 68, 0.35);
        }

        [data-theme="kick_matrix"] {
            --bg-base: #030d06;
            --bg-surface: #071c0d;
            --bg-card: rgba(10, 34, 17, 0.82);
            --border: rgba(16, 185, 129, 0.16);
            --border-hover: rgba(16, 185, 129, 0.38);
            --border-glow: rgba(16, 185, 129, 0.55);
            --primary: #059669;
            --primary-glow: #34d399;
            --accent-gradient: linear-gradient(135deg, #059669, #34d399);
            --accent-glow: 0 0 20px rgba(16, 185, 129, 0.35);
        }

        [data-theme="oled_black"] {
            --bg-base: #000000;
            --bg-surface: #0a0a0a;
            --bg-card: rgba(15, 15, 15, 0.92);
            --border: rgba(255, 255, 255, 0.10);
            --border-hover: rgba(255, 255, 255, 0.28);
            --border-glow: rgba(255, 255, 255, 0.45);
            --primary: #2563eb;
            --primary-glow: #60a5fa;
            --accent-gradient: linear-gradient(135deg, #2563eb, #60a5fa);
            --accent-glow: 0 0 20px rgba(96, 165, 250, 0.35);
        }

        [data-theme="sunset_gold"] {
            --bg-base: #0d0803;
            --bg-surface: #1c1106;
            --bg-card: rgba(33, 20, 10, 0.82);
            --border: rgba(245, 158, 11, 0.16);
            --border-hover: rgba(245, 158, 11, 0.38);
            --border-glow: rgba(245, 158, 11, 0.55);
            --primary: #d97706;
            --primary-glow: #fbbf24;
            --accent-gradient: linear-gradient(135deg, #d97706, #fbbf24);
            --accent-glow: 0 0 20px rgba(245, 158, 11, 0.35);
        }

        [data-theme="titanium_light"] {
            --bg-base: #f1f5f9;
            --bg-surface: #e2e8f0;
            --bg-card: rgba(255, 255, 255, 0.88);
            --bg-card-hover: rgba(248, 250, 252, 0.98);
            --border: rgba(0, 0, 0, 0.08);
            --border-hover: rgba(2, 132, 199, 0.3);
            --border-glow: rgba(2, 132, 199, 0.45);
            --primary: #0284c7;
            --primary-glow: #0284c7;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --text-dim: #94a3b8;
            --terminal-bg: #0f172a;
            --accent-gradient: linear-gradient(135deg, #0284c7, #38bdf8);
            --accent-glow: 0 0 20px rgba(2, 132, 199, 0.25);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            min-height: 100vh;
            line-height: 1.5;
            overflow-x: hidden;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        .container {
            max-width: 1540px;
            margin: 0 auto;
            padding: 16px 22px 36px;
        }

        /* HEADER BAR */
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 20px;
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border);
            border-radius: 18px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            gap: 12px;
            flex-wrap: wrap;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-icon {
            font-size: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid var(--border-glow);
            border-radius: 12px;
            box-shadow: var(--accent-glow);
        }

        .brand-text h1 {
            font-size: 18px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        [data-theme="titanium_light"] .brand-text h1 {
            background: linear-gradient(135deg, #0f172a 30%, #334155 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand-text p {
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 500;
        }

        .header-center {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .badge-live {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.5px;
            background: rgba(239, 68, 68, 0.12);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.35);
            transition: all 0.3s ease;
        }

        .badge-live.active {
            background: rgba(239, 68, 68, 0.25);
            color: #ef4444;
            border-color: #ef4444;
            box-shadow: 0 0 16px rgba(239, 68, 68, 0.5);
        }

        .live-pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: currentColor;
            box-shadow: 0 0 10px currentColor;
            animation: pulseDot 1.8s infinite;
        }

        @keyframes pulseDot {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.3); opacity: 0.5; }
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .theme-select {
            background: var(--bg-surface);
            color: var(--text-main);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 7px 12px;
            font-size: 11px;
            font-weight: 700;
            outline: none;
            cursor: pointer;
            transition: border 0.2s;
        }
        .theme-select:hover { border-color: var(--border-hover); }

        /* UNIFIED 2-COLUMN BALANCED GRID */
        .grid {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 20px;
            align-items: start;
        }

        @media (max-width: 1080px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }

        /* CARD GLASSMORPHISM DESIGN */
        .card {
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 18px 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.35);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .card:hover {
            border-color: var(--border-hover);
        }

        .card-title {
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 0.2px;
            margin-bottom: 14px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
            color: var(--text-main);
        }

        /* SUB-PESTANAS (TABS INTERNAS) */
        .subtab-bar {
            display: flex;
            gap: 6px;
            background: rgba(0, 0, 0, 0.3);
            padding: 4px;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 14px;
        }

        .subtab-btn {
            flex: 1;
            padding: 7px 12px;
            font-size: 11px;
            font-weight: 700;
            border-radius: 8px;
            border: none;
            background: transparent;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
            white-space: nowrap;
        }

        .subtab-btn:hover {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.04);
        }

        .subtab-btn.active {
            background: var(--accent-gradient);
            color: #ffffff;
            font-weight: 800;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.35);
        }

        /* BOTONES GLOBALES */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 9px 16px;
            font-size: 12px;
            font-weight: 700;
            border-radius: 10px;
            border: 1px solid transparent;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
        }

        .btn-primary {
            background: var(--accent-gradient);
            color: #ffffff;
            box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
        }
        .btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(2, 132, 199, 0.45);
        }

        .btn-success {
            background: linear-gradient(135deg, #059669, #10b981);
            color: #ffffff;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
        }
        .btn-success:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45);
        }

        .btn-danger {
            background: linear-gradient(135deg, #dc2626, #ef4444);
            color: #ffffff;
            box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35);
        }
        .btn-danger:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(239, 68, 68, 0.45);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.06);
            color: var(--text-main);
            border-color: var(--border);
        }
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.12);
            border-color: var(--border-hover);
        }

        .btn-chip {
            padding: 5px 10px;
            font-size: 11px;
            font-weight: 700;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border);
            color: var(--text-main);
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .btn-chip:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: var(--border-hover);
        }
        .btn-chip.active {
            background: var(--accent-gradient);
            color: #ffffff;
            border-color: transparent;
        }

        /* INPUTS & FORMS */
        input[type="text"], input[type="password"], select {
            width: 100%;
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 9px 12px;
            color: var(--text-main);
            font-size: 12px;
            outline: none;
            transition: border 0.2s, box-shadow 0.2s;
            font-family: inherit;
        }
        input:focus, select:focus {
            border-color: var(--primary-glow);
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.25);
        }

        /* MONITOR EN VIVO & LIENZO */
        .monitor-controls-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
            flex-wrap: wrap;
            gap: 8px;
        }

        .monitor-frame {
            position: relative;
            width: 100%;
            background: #000;
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid var(--border);
            aspect-ratio: 16 / 9;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: aspect-ratio 0.3s ease;
            box-shadow: inset 0 0 40px rgba(0, 0, 0, 0.8);
        }

        .monitor-frame.vertical {
            aspect-ratio: 9 / 16;
            max-height: 520px;
            margin: 0 auto;
        }

        .monitor-video {
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
        }

        .overlay-canvas-layer {
            position: absolute;
            inset: 0;
            pointer-events: none;
            overflow: hidden;
        }

        .canvas-overlay-item {
            position: absolute;
            pointer-events: auto;
            cursor: grab;
            user-select: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            transform-origin: center center;
            transition: box-shadow 0.15s ease;
        }
        .canvas-overlay-item:active { cursor: grabbing; }
        .canvas-overlay-item.selected {
            outline: 2px dashed #38bdf8;
            outline-offset: 4px;
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.6);
        }

        /* METRICAS DE EMISION */
        .metrics-bar {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-top: 12px;
            margin-bottom: 12px;
        }

        .metric-box {
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 8px 10px;
            text-align: center;
        }

        .metric-label {
            font-size: 10px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            margin-bottom: 2px;
        }

        .metric-value {
            font-size: 12px;
            font-weight: 800;
            color: var(--text-main);
            font-family: 'JetBrains Mono', monospace;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* STICKERS GALLERY */
        .stickers-scroll {
            display: flex;
            gap: 10px;
            overflow-x: auto;
            padding: 6px 2px 10px;
        }

        .sticker-card {
            flex: 0 0 80px;
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 8px 6px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .sticker-card:hover {
            transform: translateY(-2px);
            border-color: var(--primary-glow);
            box-shadow: 0 4px 14px rgba(56, 189, 248, 0.25);
        }
        .sticker-card img {
            width: 44px;
            height: 44px;
            object-fit: contain;
            display: block;
            margin: 0 auto 4px;
            filter: drop-shadow(0 2px 6px rgba(0,0,0,0.4));
        }
        .sticker-card span {
            font-size: 10px;
            font-weight: 700;
            color: var(--text-muted);
            display: block;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        /* TABLA DE CAPAS */
        .layers-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 11px;
        }
        .layers-table th {
            text-align: left;
            padding: 8px 10px;
            color: var(--text-muted);
            font-weight: 800;
            border-bottom: 1px solid var(--border);
            text-transform: uppercase;
            font-size: 10px;
        }
        .layers-table td {
            padding: 8px 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            vertical-align: middle;
        }

        /* MONETIZACION CAJA */
        .monetization-box {
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 14px;
        }

        .mono-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .mono-timer {
            font-family: 'JetBrains Mono', monospace;
            font-size: 28px;
            font-weight: 800;
            color: #38bdf8;
            letter-spacing: -0.5px;
            line-height: 1;
        }

        .progress-bar-bg {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 8px;
        }

        .progress-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #38bdf8, #10b981);
            width: 0%;
            transition: width 0.4s ease;
        }

        /* CONSOLA DE LOGS */
        .terminal-box {
            background: var(--terminal-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            height: 160px;
            overflow-y: auto;
            color: #a5f3fc;
            line-height: 1.5;
        }

        /* PLATAFORMAS TABS */
        .plat-tabs {
            display: flex;
            gap: 6px;
            overflow-x: auto;
            margin-bottom: 14px;
            padding-bottom: 4px;
        }
        .plat-tab {
            padding: 7px 12px;
            font-size: 11px;
            font-weight: 800;
            border-radius: 10px;
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid var(--border);
            color: var(--text-muted);
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }
        .plat-tab:hover {
            color: var(--text-main);
            border-color: var(--border-hover);
        }
        .plat-tab.active {
            background: var(--accent-gradient);
            color: #fff;
            border-color: transparent;
            box-shadow: 0 4px 14px rgba(0,0,0,0.3);
        }

        /* LISTAS & VIDEOS */
        .cat-tabs {
            display: flex;
            gap: 6px;
            overflow-x: auto;
            margin-bottom: 12px;
            padding-bottom: 4px;
        }
        .cat-tab {
            padding: 6px 12px;
            font-size: 11px;
            font-weight: 700;
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid var(--border);
            color: var(--text-muted);
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }
        .cat-tab.active {
            background: rgba(56, 189, 248, 0.2);
            color: #38bdf8;
            border-color: #38bdf8;
        }

        .video-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 9px 12px;
            border-radius: 10px;
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid var(--border);
            margin-bottom: 6px;
            transition: all 0.15s;
        }
        .video-item:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: var(--border-hover);
        }

        .upload-dropzone {
            border: 1.5px dashed var(--border);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            background: rgba(0, 0, 0, 0.2);
            margin-bottom: 12px;
        }
        .upload-dropzone:hover {
            border-color: var(--primary-glow);
            background: rgba(56, 189, 248, 0.05);
        }

        /* CHAT */
        .chat-container {
            height: 220px;
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 10px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .chat-msg {
            display: flex;
            gap: 8px;
            font-size: 11px;
            line-height: 1.4;
            padding: 6px 8px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.02);
        }
        .chat-badge {
            font-size: 9px;
            font-weight: 800;
            padding: 2px 5px;
            border-radius: 4px;
            height: fit-content;
            text-transform: uppercase;
        }
        .chat-badge.yt { background: #dc2626; color: #fff; }
        .chat-badge.fb { background: #1877f2; color: #fff; }
        .chat-badge.mod { background: #10b981; color: #fff; }

        /* MODAL */
        .modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.82);
            backdrop-filter: blur(8px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 100;
            padding: 14px;
        }
        .modal-box {
            background: var(--bg-surface);
            border: 1px solid var(--border-glow);
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 16px 48px rgba(0, 0, 0, 0.8);
        }

        /* TOAST */
        #toastNotice, #toast {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 200;
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid var(--primary-glow);
            color: #fff;
            padding: 12px 20px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 700;
            box-shadow: 0 8px 30px rgba(0,0,0,0.6);
            display: none;
            backdrop-filter: blur(12px);
            animation: fadeIn 0.25s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body data-theme="cyber_dark">
    <div class="container">
        <!-- CABECERA PROFESIONAL DE EMISION -->
        <header class="header">
            <div class="brand">
                <div class="brand-icon">📡</div>
                <div class="brand-text">
                    <h1>STREAMHUB 24/7 STUDIO</h1>
                    <p>Producción & Transmisión Multiplataforma en Vivo</p>
                </div>
            </div>

            <!-- CONTROLES CENTRALES DE ESTADO -->
            <div class="header-center">
                <span id="liveBadge" class="badge-live">
                    <span class="live-pulse-dot"></span>
                    <span id="statusText">DETENIDO ⏹</span>
                </span>
                <span id="monitorModeBadge" style="display: none; font-size: 11px; padding: 4px 8px; border-radius: 6px; background: rgba(56,189,248,0.15); color: #38bdf8;">PRODUCCION</span>
                <span id="connectedDevicesDisplay" style="display: none;">0</span>
                <button type="button" class="btn btn-success" id="btnStart" onclick="startStream()" style="padding: 8px 16px;">
                    🚀 Iniciar Emisión
                </button>
                <button type="button" class="btn btn-danger" id="btnStop" onclick="stopStream()" style="padding: 8px 16px; display: none;">
                    ⏹ Detener
                </button>
            </div>

            <!-- ACCIONES SUPERIORES -->
            <div class="header-actions">
                <button type="button" class="btn-chip" onclick="openControlQrModal()" style="color: #38bdf8; font-weight: bold; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.35); box-shadow: 0 0 10px rgba(56, 189, 248, 0.15);">
                    📱 Control Celular: <span id="headerMobileIpText" style="color: #fff;">10.243.28.219:5000</span>
                </button>
                <select id="themeSelector" class="theme-select" onchange="changeTheme(this.value)" title="Tema Visual">
                    <option value="cyber_dark">🌌 Cyber Dark</option>
                    <option value="twitch_purple">💜 Twitch Purple</option>
                    <option value="yt_crimson">🔴 YouTube Red</option>
                    <option value="kick_matrix">🟩 Kick Matrix</option>
                    <option value="oled_black">🖤 OLED Black</option>
                    <option value="sunset_gold">🌅 Sunset Gold</option>
                    <option value="titanium_light">💡 Titanium Light</option>
                </select>
            </div>
        </header>

        <!-- GRID PRINCIPAL UNIFICADO -->
        <div class="grid">
            <!-- ============================================================================== -->
            <!-- COLUMNA IZQUIERDA: MONITOR EN VIVO & ESTUDIO DE CAPAS / OVERLAYS               -->
            <!-- ============================================================================== -->
            <div>
                <!-- TARJETA 1: MONITOR DE EMISION EN VIVO -->
                <div class="card">
                    <div class="card-title">
                        <span>📺 Monitor en Vivo & Lienzo de Emisión</span>
                        <div style="display: flex; gap: 6px;">
                            <button type="button" class="btn-chip" onclick="toggleMuteVideo()" id="btnMute">
                                🔇 Silenciado
                            </button>
                            <button type="button" class="btn-chip" onclick="skipCurrentVideo()" style="color: #38bdf8;">
                                ⏭️ Saltar Video
                            </button>
                        </div>
                    </div>

                    <!-- SELECTOR DE FORMATO -->
                    <div class="monitor-controls-bar">
                        <div style="display: flex; gap: 6px;">
                            <button type="button" class="btn-chip active" id="btnFmt_vertical" onclick="changeFormat('vertical')">
                                📱 Vertical 9:16 (Shorts/TikTok)
                            </button>
                            <button type="button" class="btn-chip" id="btnFmt_horizontal" onclick="changeFormat('horizontal')">
                                💻 Horizontal 16:9 (YouTube/Twitch)
                            </button>
                        </div>
                        <span style="font-size: 11px; color: var(--text-muted);">
                            Lienzo: <strong id="lblCanvasRes" style="color: #38bdf8;">1080x1920</strong>
                        </span>
                    </div>

                    <!-- REPRODUCTOR CON LIENZO INTERACTIVO -->
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
                            <div class="metric-label">⏱️ Tiempo / FPS / Bitrate</div>
                            <div class="metric-value">
                                <span id="accumulatedTimeDisplay">0.0 m</span> | <span id="telemetryBitrate" style="color: #38bdf8;">~4500k / 30fps</span>
                            </div>
                        </div>
                    </div>

                    <!-- ROTULO INFERIOR DE TRANSMISION -->
                    <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border); border-radius: 12px; padding: 10px;">
                        <label style="font-size: 10px; font-weight: 800; color: var(--text-muted); display: block; margin-bottom: 6px; text-transform: uppercase;">
                            🔴 Rótulo Inferior de Emisión:
                        </label>
                        <div style="display: flex; gap: 6px;">
                            <input type="text" id="bannerTextInput" placeholder="Ej: 🔴 Transmisión En Vivo 24/7 | Suscríbete y comparte..." oninput="autoSaveBannerText(this.value)">
                            <button type="button" class="btn-chip" onclick="saveAndApplyOverlays()" style="color: #34d399; font-weight: 800; white-space: nowrap;">
                                ⚡ Aplicar Rótulo
                            </button>
                        </div>
                    </div>
                </div>

                <!-- TARJETA 2: ESTUDIO DE CAPAS, ROTULOS Y STICKERS -->
                <div class="card">
                    <div class="card-title">
                        <span>🎨 Estudio de Capas, Rótulos y Stickers</span>
                        <button type="button" id="btnForceApplyOverlays" class="btn-chip active" onclick="saveAndApplyOverlays()" style="background: linear-gradient(135deg, #10b981, #06b6d4); color: #fff; font-weight: 800; border: none; box-shadow: 0 0 14px rgba(16,185,129,0.5);">
                            ⚡ APLICAR EN VIVO YA
                        </button>
                    </div>

                    <!-- SUB-PESTANAS ORGANIZADAS -->
                    <div class="subtab-bar">
                        <button type="button" class="subtab-btn overlay-subtab-btn active" data-tab="stickers" onclick="switchOverlaySubTab('stickers')">
                            🎭 Stickers & Logos
                        </button>
                        <button type="button" class="subtab-btn overlay-subtab-btn" data-tab="rotulos" onclick="switchOverlaySubTab('rotulos')">
                            ✍️ Rótulos & Textos
                        </button>
                        <button type="button" class="subtab-btn overlay-subtab-btn" data-tab="layers" onclick="switchOverlaySubTab('layers')">
                            📑 Capas en Pantalla
                        </button>
                    </div>

                    <!-- PANEL 1: STICKERS & LOGOS -->
                    <div id="overlay_pane_stickers" class="overlay-tab-pane" style="display: block;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <span style="font-size: 11px; font-weight: 700; color: var(--text-muted);">Toca cualquier sticker para colocarlo en la transmisión:</span>
                            <input type="file" id="overlayImageInput" accept="image/*" style="display: none;" onchange="handleOverlayImageUpload(event)">
                            <button type="button" class="btn-chip" onclick="document.getElementById('overlayImageInput').click()" style="color: #38bdf8; font-weight: 700;">
                                🖼️ Subir Logo / Imagen PNG
                            </button>
                        </div>
                        <div class="stickers-scroll" id="stickersGallery">
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/subscribe.png', 'Subscribe')">
                                <img src="/stickers/subscribe.png" alt="Subscribe"><span>Subscribe</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/like.png', 'Like')">
                                <img src="/stickers/like.png" alt="Like"><span>Like</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/live_badge.png', 'LIVE')">
                                <img src="/stickers/live_badge.png" alt="LIVE"><span>LIVE</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/fire.png', 'Fuego')">
                                <img src="/stickers/fire.png" alt="Fire"><span>Fuego</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/heart.png', 'Corazón')">
                                <img src="/stickers/heart.png" alt="Heart"><span>Corazón</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/star.png', 'Estrella')">
                                <img src="/stickers/star.png" alt="Star"><span>Estrella</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/verified.png', 'Verificado')">
                                <img src="/stickers/verified.png" alt="Verified"><span>Verificado</span>
                            </div>
                            <div class="sticker-card" onclick="addStickerOverlay('/stickers/cross.png', 'Cruz')">
                                <img src="/stickers/cross.png" alt="Cross"><span>Cruz</span>
                            </div>
                        </div>
                    </div>

                    <!-- PANEL 2: ROTULOS Y TEXTOS CON EMOJIS -->
                    <div id="overlay_pane_rotulos" class="overlay-tab-pane" style="display: none;">
                        <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 6px;">
                            ✍️ Escribe el rótulo de texto que saldrá en la transmisión:
                        </label>
                        <div style="display: flex; gap: 6px; margin-bottom: 8px;">
                            <input type="text" id="newRotuloInput" placeholder="Ej: ¡Transmisión en directo continua 24/7! 🚀🔥">
                            <button type="button" class="btn-chip" onclick="addNewRotulo()" style="color: #34d399; font-weight: 800; white-space: nowrap;">
                                ➕ Agregar Rótulo
                            </button>
                        </div>
                        <div style="display: flex; gap: 4px; overflow-x: auto; padding-bottom: 4px; margin-bottom: 10px;">
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

                    <!-- PANEL 3: TABLA DE CAPAS ACTIVAS -->
                    <div id="overlay_pane_layers" class="overlay-tab-pane" style="display: none;">
                        <div style="max-height: 180px; overflow-y: auto; background: rgba(0,0,0,0.25); border-radius: 12px; border: 1px solid var(--border);">
                            <table class="layers-table" id="layersTable">
                                <thead>
                                    <tr>
                                        <th>Capa / Elemento</th>
                                        <th>Giro</th>
                                        <th>Tamaño</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody id="layersTableBody"></tbody>
                            </table>
                        </div>
                    </div>

                    <!-- PANEL DE EDICION EN TIEMPO REAL DEL ELEMENTO O ROTULO SELECCIONADO -->
                    <div id="selectedOverlayEditor" style="margin-top: 14px; padding: 14px; background: rgba(15, 23, 42, 0.85); border: 1.5px solid rgba(56, 189, 248, 0.35); border-radius: 14px; display: none; box-shadow: 0 6px 20px rgba(0,0,0,0.5);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <strong id="editorItemTitle" style="font-size: 12px; color: #38bdf8;">⚙️ Editar en Vivo: <span id="editorItemName">Rótulo</span></strong>
                            <button type="button" class="btn-chip" onclick="saveAndApplyOverlays()" style="background: linear-gradient(135deg, #10b981, #06b6d4); color: #fff; font-weight: 800; border: none; padding: 5px 12px;">
                                ⚡ APLICAR EN VIVO YA
                            </button>
                        </div>
                        <div id="editorTextGroup" style="margin-bottom: 10px;">
                            <label style="font-size: 11px; color: var(--text-muted); display: block; margin-bottom: 4px;">Texto del Rótulo (Se aplica directamente al video):</label>
                            <div style="display: flex; gap: 6px;">
                                <input type="text" id="selectedOverlayTextInput" placeholder="Escribe el texto del rótulo..." oninput="onSelectedOverlayTextChange(this.value)">
                                <button type="button" class="btn-chip" onclick="saveAndApplyOverlays()" style="color: #34d399; font-weight: 800; white-space: nowrap;">
                                    ⚡ Aplicar
                                </button>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 10px;">
                            <div>
                                <label style="font-size: 10px; color: var(--text-muted); display: block; margin-bottom: 4px;">Color Fondo:</label>
                                <input type="color" id="selectedOverlayBgInput" value="#0f172a" style="width: 100%; height: 32px; padding: 2px; border-radius: 8px; background: transparent; cursor: pointer;" onchange="onSelectedOverlayBgChange(this.value)">
                            </div>
                            <div>
                                <label style="font-size: 10px; color: var(--text-muted); display: block; margin-bottom: 4px;">Color Texto:</label>
                                <input type="color" id="selectedOverlayColorInput" value="#ffffff" style="width: 100%; height: 32px; padding: 2px; border-radius: 8px; background: transparent; cursor: pointer;" onchange="onSelectedOverlayColorChange(this.value)">
                            </div>
                            <div>
                                <label style="font-size: 10px; color: var(--text-muted); display: block; margin-bottom: 4px;">Tamaño Fuente: <span id="editorFontSizeVal">16px</span></label>
                                <input type="range" id="selectedOverlayFontSizeInput" min="10" max="48" value="16" style="width: 100%;" oninput="onSelectedOverlayFontSizeChange(this.value)">
                            </div>
                            <div>
                                <label style="font-size: 10px; color: var(--text-muted); display: block; margin-bottom: 4px;">Giro (360°): <span id="editorRotationVal">0°</span></label>
                                <input type="range" id="selectedOverlayRotInput" min="0" max="360" value="0" style="width: 100%;" oninput="onSelectedOverlayRotationChange(this.value)">
                            </div>
                        </div>
                        <div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;">
                            <span style="font-size: 10px; color: var(--text-muted);">Giro rápido:</span>
                            <button type="button" class="btn-chip" onclick="setOverlayQuickRotation(0)">0°</button>
                            <button type="button" class="btn-chip" onclick="setOverlayQuickRotation(45)">45°</button>
                            <button type="button" class="btn-chip" onclick="setOverlayQuickRotation(90)">90°</button>
                            <button type="button" class="btn-chip" onclick="setOverlayQuickRotation(180)">180°</button>
                            <button type="button" class="btn-chip" onclick="setOverlayQuickRotation(270)">270°</button>
                            <button type="button" class="btn-chip" onclick="saveAndApplyOverlays()" style="margin-left: auto; color: #34d399; font-weight: 800;">
                                ⚡ Transmitir Capas Ahora
                            </button>
                        </div>
                    </div>
                </div>

                <!-- TARJETA 3: CONSOLA DE LOGS FFMPEG -->
                <div class="card">
                    <div class="card-title">
                        <span>📟 Monitor de FFmpeg (Logs de Emisión)</span>
                        <button type="button" class="btn-chip" onclick="document.getElementById('ffmpegLogsBox').innerText = ''; if(document.getElementById('terminalLogs')) document.getElementById('terminalLogs').innerText = ''; showToast('Logs limpiados');">
                            🗑️ Limpiar
                        </button>
                    </div>
                    <div class="terminal-box" id="ffmpegLogsBox">
                        <div id="terminalLogs">[SISTEMA] Motor 24/7 listo. Conectando salidas de transmisión...</div>
                    </div>
                </div>
            </div>

            <!-- ============================================================================== -->
            <!-- COLUMNA DERECHA: REDES, PLAYLISTS, MONETIZACION & CHAT EN VIVO                 -->
            <!-- ============================================================================== -->
            <div>
                <!-- TARJETA 4: CONEXION DE TRANSMISION A REDES -->
                <div class="card">
                    <div class="card-title">
                        <span>🌐 Conexión de Transmisión a Redes</span>
                        <div style="display: flex; gap: 6px;">
                            <button type="button" class="btn-chip" onclick="testConnection()" style="color: #34d399; font-weight: 700;">
                                🔌 Probar Conexión
                            </button>
                        </div>
                    </div>

                    <!-- FEEDBACK TEST CONEXION -->
                    <div id="testFeedbackBox" style="display: none; padding: 8px 12px; border-radius: 8px; margin-bottom: 10px; font-size: 11px;"></div>

                    <!-- SELECTOR DE PLATAFORMAS -->
                    <div class="plat-tabs" id="platformTabs">
                        <div class="plat-tab active" data-platform="youtube" onclick="selectPlatform('youtube')">YouTube</div>
                        <div class="plat-tab" data-platform="facebook" onclick="selectPlatform('facebook')">Facebook Live</div>
                        <div class="plat-tab" data-platform="twitch" onclick="selectPlatform('twitch')">Twitch</div>
                        <div class="plat-tab" data-platform="tiktok" onclick="selectPlatform('tiktok')">TikTok</div>
                        <div class="plat-tab" data-platform="kick" onclick="selectPlatform('kick')">Kick</div>
                        <div class="plat-tab" data-platform="custom" onclick="selectPlatform('custom')">RTMP Propio</div>
                        <div class="plat-tab" data-platform="multistream" onclick="selectPlatform('multistream')">🔥 Multistream</div>
                    </div>

                    <!-- FORMULARIO DE CLAVES DINAMICO (CON AMBOS IDs PARA COMPATIBILIDAD JS) -->
                    <div id="platformFields">
                        <div id="panelYoutube" class="plat-field" style="display: block;">
                            <div id="field_youtube">
                                <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 4px;">
                                    Clave de Transmisión YouTube:
                                </label>
                                <div style="display: flex; gap: 6px;">
                                    <input type="password" id="streamKeyInput" placeholder="xxxx-xxxx-xxxx-xxxx" oninput="autoSaveKeys()">
                                    <button type="button" class="btn-chip" onclick="toggleKeyVisibility('streamKeyInput')" title="Ver/Ocultar">👁️</button>
                                </div>
                            </div>
                        </div>

                        <div id="panelFacebook" class="plat-field" style="display: none;">
                            <div id="field_facebook">
                                <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 4px;">
                                    Clave de Transmisión Facebook Live:
                                </label>
                                <div style="display: flex; gap: 6px;">
                                    <input type="password" id="facebookKeyInput" placeholder="FB-xxxxxxxxx" oninput="autoSaveKeys()">
                                    <button type="button" class="btn-chip" onclick="toggleKeyVisibility('facebookKeyInput')" title="Ver/Ocultar">👁️</button>
                                </div>
                            </div>
                        </div>

                        <div id="panelTwitch" class="plat-field" style="display: none;">
                            <div id="field_twitch">
                                <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 4px;">
                                    Clave de Transmisión Twitch:
                                </label>
                                <div style="display: flex; gap: 6px;">
                                    <input type="password" id="twitchKeyInput" placeholder="live_xxxxxxxxx" oninput="autoSaveKeys()">
                                    <button type="button" class="btn-chip" onclick="toggleKeyVisibility('twitchKeyInput')" title="Ver/Ocultar">👁️</button>
                                </div>
                            </div>
                        </div>

                        <div id="panelTiktok" class="plat-field" style="display: none;">
                            <div id="field_tiktok">
                                <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 4px;">
                                    Servidor RTMP TikTok (De tu Live Center):
                                </label>
                                <input type="text" id="tiktokServerInput" value="rtmp://live-push.tiktok.com/live" style="margin-bottom: 6px;" oninput="autoSaveKeys()">
                                <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 4px;">
                                    Clave de Transmisión TikTok:
                                </label>
                                <div style="display: flex; gap: 6px;">
                                    <input type="password" id="tiktokKeyInput" placeholder="Clave generada en TikTok Live Studio" oninput="autoSaveKeys()">
                                    <button type="button" class="btn-chip" onclick="toggleKeyVisibility('tiktokKeyInput')" title="Ver/Ocultar">👁️</button>
                                </div>
                            </div>
                        </div>

                        <div id="panelKick" class="plat-field" style="display: none;">
                            <div id="field_kick">
                                <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 4px;">
                                    Servidor RTMP Kick:
                                </label>
                                <input type="text" id="kickServerInput" value="rtmp://fa7237973e51.global-contribute.live-video.net/app" style="margin-bottom: 6px;" oninput="autoSaveKeys()">
                                <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 4px;">
                                    Clave de Transmisión Kick:
                                </label>
                                <div style="display: flex; gap: 6px;">
                                    <input type="password" id="kickKeyInput" placeholder="sk_us-west-2_xxxxxxxxx" oninput="autoSaveKeys()">
                                    <button type="button" class="btn-chip" onclick="toggleKeyVisibility('kickKeyInput')" title="Ver/Ocultar">👁️</button>
                                </div>
                            </div>
                        </div>

                        <div id="panelCustom" class="plat-field" style="display: none;">
                            <div id="field_custom">
                                <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 4px;">
                                    URL del Servidor RTMP Propio (Nginx / VPS / OBS):
                                </label>
                                <input type="text" id="customRtmpUrlInput" placeholder="rtmp://mi-servidor.com/live o rtmp://127.0.0.1:1935/live" style="margin-bottom: 6px;" oninput="autoSaveKeys()">
                                <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 4px;">
                                    Clave / Clave Stream:
                                </label>
                                <div style="display: flex; gap: 6px;">
                                    <input type="password" id="customRtmpKeyInput" placeholder="mi_canal_privado" oninput="autoSaveKeys()">
                                    <button type="button" class="btn-chip" onclick="toggleKeyVisibility('customRtmpKeyInput')" title="Ver/Ocultar">👁️</button>
                                </div>
                            </div>
                        </div>

                        <div id="panelMultistream" class="plat-field" style="display: none;">
                            <div id="field_multistream">
                                <p style="font-size: 11px; color: var(--text-muted); margin-bottom: 8px;">
                                    Activa las plataformas simultáneas a emitir en paralelo:
                                </p>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                                    <label style="display: flex; align-items: center; gap: 8px; font-size: 11px; cursor: pointer;">
                                        <input type="checkbox" id="chkMultiYt" checked onchange="autoSaveKeys()">
                                        <input type="checkbox" id="ms_target_youtube" checked style="display:none;"> YouTube Live
                                    </label>
                                    <label style="display: flex; align-items: center; gap: 8px; font-size: 11px; cursor: pointer;">
                                        <input type="checkbox" id="chkMultiFb" onchange="autoSaveKeys()">
                                        <input type="checkbox" id="ms_target_facebook" style="display:none;"> Facebook Live
                                    </label>
                                    <label style="display: flex; align-items: center; gap: 8px; font-size: 11px; cursor: pointer;">
                                        <input type="checkbox" id="chkMultiTw" onchange="autoSaveKeys()">
                                        <input type="checkbox" id="ms_target_twitch" style="display:none;"> Twitch
                                    </label>
                                    <label style="display: flex; align-items: center; gap: 8px; font-size: 11px; cursor: pointer;">
                                        <input type="checkbox" id="chkMultiTiktok" onchange="autoSaveKeys()">
                                        <input type="checkbox" id="ms_target_tiktok" style="display:none;"> TikTok
                                    </label>
                                    <label style="display: flex; align-items: center; gap: 8px; font-size: 11px; cursor: pointer;">
                                        <input type="checkbox" id="chkMultiKick" onchange="autoSaveKeys()">
                                        <input type="checkbox" id="ms_target_kick" style="display:none;"> Kick
                                    </label>
                                    <label style="display: flex; align-items: center; gap: 8px; font-size: 11px; cursor: pointer;">
                                        <input type="checkbox" id="chkMultiCustom" onchange="autoSaveKeys()">
                                        <input type="checkbox" id="ms_target_custom" style="display:none;"> RTMP Propio
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- TARJETA 5: LISTAS DE VIDEOS & BIBLIOTECA 24/7 -->
                <div class="card">
                    <div class="card-title">
                        <span>📁 Listas de Reproducción & Videos 24/7</span>
                        <div style="display: flex; gap: 6px;">
                            <button type="button" class="btn-chip" onclick="createCategoryPrompt()" style="color: #38bdf8; font-weight: 700;">
                                ➕ Nueva Lista
                            </button>
                            <button type="button" class="btn-chip" onclick="streamCurrentPlaylist()" style="color: #34d399; font-weight: 700;">
                                🚀 Emitir Lista
                            </button>
                        </div>
                    </div>

                    <!-- PESTANAS DE LISTAS (CON AMBOS IDs) -->
                    <div class="cat-tabs" id="categoryTabs"></div>
                    <div id="categoryTabsContainer" style="display: none;"></div>

                    <!-- DROPZONE PARA SUBIR VIDEOS -->
                    <div class="upload-dropzone" onclick="document.getElementById('videoUploadInput').click()">
                        <input type="file" id="videoUploadInput" multiple accept="video/*" style="display: none;" onchange="handleFileSelect(event)">
                        <div style="font-size: 20px; margin-bottom: 4px;">📤</div>
                        <div style="font-size: 12px; font-weight: 700; color: var(--text-main);">Toca para subir videos a esta lista</div>
                        <div style="font-size: 10px; color: var(--text-muted);">(MP4, MKV, MOV, TS compatibles)</div>
                    </div>

                    <!-- LISTA DE VIDEOS (CON AMBOS IDs) -->
                    <div id="playlistContainer" style="max-height: 240px; overflow-y: auto;"></div>
                    <div id="categoryVideosList" style="display: none;"></div>
                </div>

                <!-- TARJETA 6: CHAT EN VIVO & MONETIZACION YOUTUBE -->
                <div class="card">
                    <div class="card-title">
                        <span>💬 Chat en Vivo & Monetización YouTube</span>
                        <span id="chatStatusBadge" style="font-size: 11px; color: #34d399; font-weight: 700;">● Conectado</span>
                    </div>

                    <!-- SUB-PESTANAS DE COMUNIDAD -->
                    <div class="subtab-bar">
                        <button type="button" class="subtab-btn community-subtab-btn active" data-tab="chat" onclick="switchCommunitySubTab('chat')">
                            💬 Chat Multicámara
                        </button>
                        <button type="button" class="subtab-btn community-subtab-btn" data-tab="monetization" onclick="switchCommunitySubTab('monetization')">
                            🎯 Monetización 11:55
                        </button>
                    </div>

                    <!-- SUB-PANEL 1: CHAT MULTICAMARA -->
                    <div id="community_pane_chat" class="community-tab-pane" style="display: block;">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 8px;">
                            <input type="text" id="ytVideoIdInput" placeholder="YouTube Video ID / URL" style="font-size: 11px;" onchange="connectLiveChats()">
                            <input type="text" id="fbLiveIdInput" placeholder="Facebook Live Video ID" style="font-size: 11px;" onchange="connectLiveChats()">
                        </div>
                        <div style="display: flex; gap: 6px; margin-bottom: 8px;">
                            <input type="password" id="fbAccessTokenInput" placeholder="Token de Acceso FB (Opcional)" style="font-size: 11px; flex: 1;" onchange="connectLiveChats()">
                            <select id="chatTargetPlatform" style="width: auto; font-size: 11px; font-weight: 700;">
                                <option value="all">Todas</option>
                                <option value="youtube">YouTube</option>
                                <option value="facebook">Facebook</option>
                            </select>
                            <button type="button" id="btnPopoutYtChat" class="btn-chip" onclick="popoutChat()" title="Ventana Emergente">🗗</button>
                        </div>

                        <div class="chat-container" id="chatMessagesBox">
                            <div class="chat-msg">
                                <span class="chat-badge mod">SISTEMA</span>
                                <div>
                                    <strong style="color: #38bdf8;">Moderador AI:</strong>
                                    <span style="color: var(--text-muted);">Chat multicámara listo. Los comentarios aparecerán aquí en vivo.</span>
                                </div>
                            </div>
                        </div>
                        <div id="chatMessagesContainer" style="display: none;"></div>

                        <div style="display: flex; gap: 6px;">
                            <input type="text" id="chatReplyInput" placeholder="Escribe una respuesta como Moderador..." onkeydown="if(event.key==='Enter') sendChatMessage()">
                            <input type="hidden" id="chatInputText">
                            <button type="button" class="btn-chip" onclick="sendChatMessage()" style="color: #38bdf8; font-weight: 800; white-space: nowrap;">
                                📨 Enviar
                            </button>
                        </div>
                    </div>

                    <!-- SUB-PANEL 2: MONETIZACION 11:55 -->
                    <div id="community_pane_monetization" class="community-tab-pane" style="display: none;">
                        <div class="monetization-box">
                            <div class="mono-header">
                                <div>
                                    <span style="font-size: 10px; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">
                                        ⏳ TIEMPO RESTANTE CICLO ACTUAL:
                                    </span>
                                    <div class="mono-timer" id="cycleCountdownText">11:55:00</div>
                                </div>
                                <div style="text-align: right;">
                                    <span style="font-size: 10px; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">
                                        CICLOS:
                                    </span>
                                    <div style="font-size: 20px; font-weight: 800; color: #f87171;" id="cycleCountBadge">#0</div>
                                    <span id="cycleCounterText" style="display:none;">#0</span>
                                </div>
                            </div>

                            <div class="progress-bar-bg">
                                <div class="progress-bar-fill" id="monetizationTotalBar"></div>
                                <div class="progress-bar-fill" id="cycleProgressBar" style="display: none;"></div>
                            </div>
                            <div style="display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted); margin-bottom: 12px;">
                                <span>Progreso monetización:</span>
                                <strong id="monetizationGoalText" style="color: #38bdf8;">0.0 / 4,000 minutos (0%)</strong>
                                <span id="cycleElapsedPercent" style="display:none;">0%</span>
                                <span id="cycleProgressText" style="display:none;">0%</span>
                            </div>

                            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border); padding-top: 10px;">
                                <span style="font-size: 11px; color: var(--text-muted);">Transición 24/7 automática:</span>
                                <button type="button" class="btn-chip" id="btnToggleCycleMode" onclick="toggleCycleMode()" style="color: #f87171; font-weight: 800;">
                                    🔘 Modo Ciclo 11:55: ACTIVO
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL DE CONTROL CELULAR / CODIGO QR -->
    <div class="modal-overlay" id="controlQrModal">
        <div class="modal-box" style="max-width: 440px; text-align: center;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h3 style="font-size: 16px; margin: 0; color: #38bdf8; font-weight: 800;">📱 Control Remoto Celular</h3>
                <button type="button" class="btn-chip" onclick="closeControlQrModal()" style="padding: 2px 8px; font-size: 16px;">✕</button>
            </div>
            <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px; line-height: 1.4;">
                Conecta tu celular a la <strong>misma red Wi-Fi</strong> de esta PC y escanea el código QR para controlar la transmisión en tu mano:
            </p>
            
            <div id="ipSelectorContainer" style="display: flex; gap: 6px; justify-content: center; margin-bottom: 12px; flex-wrap: wrap;"></div>

            <div id="qrBox" style="background: #fff; padding: 14px; border-radius: 16px; display: inline-block; margin-bottom: 14px; box-shadow: 0 8px 24px rgba(0,0,0,0.6);"></div>

            <div style="display: flex; gap: 6px; margin-bottom: 14px;">
                <input type="text" id="qrLink" readonly style="font-size: 12px; text-align: center; background: rgba(0,0,0,0.4); border: 1px solid rgba(56,189,248,0.4); border-radius: 8px; color: #38bdf8; font-weight: 700; flex: 1;">
                <button type="button" class="btn-chip" onclick="copyMobileLink()" style="background: #38bdf8; color: #0f172a; font-weight: 800; white-space: nowrap; padding: 0 14px;">
                    📋 Copiar
                </button>
            </div>

            <div style="display: flex; gap: 8px;">
                <a id="qrOpenDirectLink" href="/control" target="_blank" class="btn btn-secondary" style="flex: 1; text-decoration: none; padding: 10px; font-size: 12px;">
                    💻 Probar en PC
                </a>
                <button type="button" class="btn btn-primary" onclick="closeControlQrModal()" style="flex: 1; padding: 10px; font-size: 12px;">
                    Listo
                </button>
            </div>
        </div>
    </div>

    <!-- NOTIFICACION TOAST FLOTANTE -->
    <div id="toastNotice"><div id="toast"></div></div>

    <!-- JAVASCRIPT DEL ESTUDIO -->
    <script>
''' + extracted_script + '''
    </script>
</body>
</html>
'''

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_html)
with open(tpl_index, 'w', encoding='utf-8') as f:
    f.write(new_html)

shutil.copyfile(index_path, r"c:\Users\Admin\Desktop\chenyz.app\web y app\index.html")

print("SUCCESS: index.html regenerated, synced to panel_stream, templates, and web y app!")
