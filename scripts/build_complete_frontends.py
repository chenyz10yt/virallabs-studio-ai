import os, sys, shutil

panel_dir = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream"

print("Construyendo frontends completos e integrados...")

# ==============================================================================
# INDEX.HTML
# ==============================================================================
index_html_code = r'''<!DOCTYPE html>
<html lang="es">
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
            --yt-red: #ff0000;
            --fb-blue: #1877f2;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --terminal-bg: #030712;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-base);
            color: var(--text-main);
            min-height: 100vh;
            padding: 16px 14px 60px;
        }

        .container { max-width: 1320px; margin: 0 auto; }

        /* CABECERA CON LOGO NARANJA ORIGINAL Y NOMBRE STREAMHUB */
        .header {
            display: flex; align-items: center; justify-content: space-between;
            flex-wrap: wrap; gap: 14px; margin-bottom: 18px; padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }

        .brand { display: flex; align-items: center; gap: 12px; }
        .brand-icon {
            width: 44px; height: 44px; border-radius: 12px;
            background: linear-gradient(135deg, #ef4444, #f97316);
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; box-shadow: 0 8px 24px rgba(239, 68, 68, 0.4);
            flex-shrink: 0; overflow: hidden;
            border: 1px solid rgba(249, 115, 22, 0.5);
        }
        .brand-icon img {
            width: 32px; height: 32px; object-fit: contain; border-radius: 6px;
        }
        .brand-text h1 { font-size: 20px; font-weight: 800; letter-spacing: -0.3px; color: #fff; }
        .brand-text p { font-size: 12px; color: var(--text-muted); }

        .header-actions { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
        .btn-chip {
            background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border);
            color: var(--text-muted); font-size: 11px; font-weight: 700;
            padding: 7px 12px; border-radius: 8px; cursor: pointer; transition: all 0.2s ease;
            text-decoration: none; display: inline-flex; align-items: center; gap: 6px;
        }
        .btn-chip:hover { background: rgba(255, 255, 255, 0.12); color: #fff; }
        .btn-chip.active { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border-color: rgba(56, 189, 248, 0.4); }

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
            font-size: 14px; font-weight: 800; color: #fff;
            margin-bottom: 14px; border-bottom: 1px solid var(--border); padding-bottom: 10px;
            text-transform: uppercase; letter-spacing: 0.3px;
        }

        /* MONITOR DE VIDEO EN VIVO Y VISTA PREVIA */
        .monitor-frame {
            position: relative; width: 100%; height: 320px; background: #000;
            border-radius: 14px; overflow: hidden; border: 1px solid rgba(56, 189, 248, 0.3);
            margin-bottom: 14px; display: flex; align-items: center; justify-content: center;
            transition: all 0.3s ease;
        }

        .monitor-video {
            width: 100%; height: 100%; object-fit: contain; background: #000;
        }

        .monitor-overlay-badge {
            position: absolute; top: 12px; left: 12px;
            background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(8px);
            padding: 5px 10px; border-radius: 999px; font-size: 11px; font-weight: 800;
            display: flex; align-items: center; gap: 6px; border: 1px solid rgba(255, 255, 255, 0.15);
            z-index: 5;
        }

        .monitor-overlay-banner {
            position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.75); color: #fff; padding: 6px 16px;
            border-radius: 8px; font-size: 12px; font-weight: 700; text-align: center;
            max-width: 90%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
            border: 1px solid rgba(255, 255, 255, 0.2); z-index: 5; display: none;
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
        .metric-value { font-size: 14px; font-weight: 800; color: #38bdf8; font-family: 'JetBrains Mono', monospace; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

        /* SECCIÓN DE MONETIZACIÓN YOUTUBE (CICLO 11:55) */
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
        .platform-btn {
            background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border);
            border-radius: 10px; padding: 10px 4px; color: var(--text-muted);
            font-size: 12px; font-weight: 700; cursor: pointer; text-align: center;
        }
        .platform-btn.active[data-plat="youtube"] { background: rgba(239, 68, 68, 0.18); color: #f87171; border-color: rgba(239, 68, 68, 0.6); }
        .platform-btn.active[data-plat="facebook"] { background: rgba(24, 119, 242, 0.18); color: #60a5fa; border-color: rgba(24, 119, 242, 0.6); }
        .platform-btn.active[data-plat="twitch"] { background: rgba(168, 85, 247, 0.18); color: #c084fc; border-color: rgba(168, 85, 247, 0.6); }
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
            display: flex; flex-direction: column; height: 320px;
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

        /* PLAYLIST & ARCHIVOS */
        .dropzone {
            border: 2px dashed rgba(56, 189, 248, 0.35); border-radius: 12px; padding: 16px;
            text-align: center; cursor: pointer; background: rgba(56, 189, 248, 0.02); margin-bottom: 10px;
        }
        .dropzone:hover { border-color: var(--primary-glow); background: rgba(56, 189, 248, 0.08); }

        .playlist { list-style: none; max-height: 220px; overflow-y: auto; }
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

        /* ESTILOS DE STICKERS EN PANEL */
        .stickers-scroll::-webkit-scrollbar { height: 6px; }
        .stickers-scroll::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        .sticker-card {
            flex-shrink: 0; display: flex; flex-direction: column; align-items: center; gap: 4px;
            padding: 8px; background: rgba(15, 23, 42, 0.8); border: 1px solid var(--border);
            border-radius: 10px; cursor: pointer; transition: all 0.2s ease;
        }
        .sticker-card:hover { transform: scale(1.05); border-color: #38bdf8; background: rgba(30, 41, 59, 0.9); }
        .sticker-card img { width: 38px; height: 38px; object-fit: contain; }

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
        <!-- HEADER CON LOGO NARANJA ORIGINAL Y TÍTULO OFICIAL -->
        <header class="header">
            <div class="brand">
                <div class="brand-icon">
                    <img src="/logo.png" alt="Logo" onerror="this.onerror=null; this.outerHTML='▶';">
                </div>
                <div class="brand-text">
                    <h1>StreamHub 24/7 Studio</h1>
                    <p>Emisión Continua, Ciclos de Monetización & Multi-Chat</p>
                </div>
            </div>

            <div class="header-actions">
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
                <!-- MONITOR EN VIVO Y VISTA PREVIA -->
                <div class="card">
                    <div class="card-title">
                        <span>📺 Monitor en Vivo & Vista Previa</span>
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
                            👁️ Vista Previa
                        </span>
                    </div>

                    <!-- REPRODUCTOR HTML5 REAL -->
                    <div class="monitor-frame" id="monitorFrameContainer">
                        <span class="monitor-overlay-badge" id="monitorOverlayStatus">
                            ⚪ EN ESPERA
                        </span>
                        <video id="liveVideoPlayer" class="monitor-video" playsinline muted loop autoplay></video>
                        <div class="monitor-overlay-banner" id="monitorOverlayBanner"></div>
                    </div>

                    <!-- TELEMETRIA DE EMISION Y AUDIENCIA -->
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

                    <!-- RÓTULO EN PANTALLA -->
                    <div style="margin-top: 10px;">
                        <label for="bannerTextInput" style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 6px;">
                            📝 Rótulo / Texto Inferior en Pantalla:
                        </label>
                        <div style="display: flex; gap: 8px;">
                            <input type="text" id="bannerTextInput" placeholder="Ej: ¡Transmisión en directo continua 24/7!" oninput="previewBannerText(this.value)">
                            <button type="button" class="btn-chip" onclick="updateBannerText()" style="color: #38bdf8;">⚡ Actualizar</button>
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
                                <span style="font-size: 12px; font-weight: 800; color: #fff;">
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
                                💡 <em>YouTube archiva directos de hasta 12h. Al llegar a 11:55, el sistema pausa 15 segundos para consolidar el VOD y reinicia la transmisión automáticamente hasta cumplir la meta.</em>
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
                <!-- CONEXIÓN DE TRANSMISIÓN A REDES -->
                <div class="card">
                    <div class="card-title">
                        <span>🌐 Conexión de Transmisión a Redes</span>
                    </div>

                    <div class="platform-nav">
                        <button type="button" class="platform-btn active" data-plat="youtube" onclick="selectPlatform('youtube')">🔴 YouTube</button>
                        <button type="button" class="platform-btn" data-plat="facebook" onclick="selectPlatform('facebook')">🔵 Facebook</button>
                        <button type="button" class="platform-btn" data-plat="twitch" onclick="selectPlatform('twitch')">🟣 Twitch</button>
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

                    <div id="panelMultistream" class="platform-panel" style="display: none;">
                        <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Emite en varias redes a la vez con un solo clic:</p>
                        <div style="display: flex; gap: 16px; font-size: 13px;">
                            <label><input type="checkbox" id="chkMultiYt" checked onchange="autoSaveKeys()"> 🔴 YouTube</label>
                            <label><input type="checkbox" id="chkMultiFb" onchange="autoSaveKeys()"> 🔵 Facebook</label>
                            <label><input type="checkbox" id="chkMultiTw" onchange="autoSaveKeys()"> 🟣 Twitch</label>
                        </div>
                    </div>

                    <button type="button" class="btn-chip" style="width: 100%; padding: 10px; margin-bottom: 6px; font-weight: bold;" onclick="testConnection()">
                        🧪 Probar Conexión con YouTube / Red Seleccionada
                    </button>
                    <div id="testFeedbackBox" class="test-feedback" style="display: none;"></div>

                    <div class="btn-group">
                        <button type="button" id="btnStart" class="btn btn-start" onclick="startStream()"><span>🔴</span> INICIAR TRANSMISIÓN 24/7</button>
                        <button type="button" id="btnStop" class="btn btn-stop" onclick="stopStream()" disabled><span>⏹</span> Detener</button>
                    </div>
                </div>

                <!-- TARJETA: GRABADOR MAESTRO DE TRANSMISIÓN & DESCARGA EN 1 SOLO VIDEO -->
                <div class="card" style="border-color: rgba(239, 68, 68, 0.4); background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(15, 23, 42, 0.95));">
                    <div class="card-title">
                        <span style="color: #f87171;">🔴 Grabación Maestra (Descarga en 1 Solo Video)</span>
                        <span id="recordingLiveStatusBadge" class="btn-chip" style="color: #34d399; font-size: 10px; border-color: rgba(16, 185, 129, 0.3);">
                            ● Auto-Guardado Activo
                        </span>
                    </div>

                    <p style="font-size: 11px; color: var(--text-muted); margin-bottom: 12px; line-height: 1.4;">
                        Toda tu emisión en vivo se graba continuamente en el servidor con tus logos, rótulos y audio sincronizados. Puedes generar y descargar el video consolidado completo cuando quieras.
                    </p>

                    <div style="display: flex; gap: 8px; margin-bottom: 12px;">
                        <button type="button" class="btn" id="btnCompileNow" onclick="compileAndDownloadMasterRecording()" style="flex: 1; padding: 12px; background: linear-gradient(135deg, #ef4444, #f97316); color: #fff; font-size: 12px; font-weight: 800; border-radius: 10px; box-shadow: 0 4px 15px rgba(239,68,68,0.35);">
                            ⚡ Generar y Descargar Video Hasta Ahora
                        </button>
                        <button type="button" class="btn-chip" onclick="refreshRecordingsList()" title="Refrescar archivos">
                            🔄
                        </button>
                    </div>

                    <span style="font-size: 10px; font-weight: 800; color: var(--text-muted); text-transform: uppercase; display: block; margin-bottom: 6px;">
                        Archivos Listos para Descargar:
                    </span>
                    <ul id="recordingsFileList" style="list-style: none; display: flex; flex-direction: column; gap: 6px; max-height: 180px; overflow-y: auto;">
                        <li style="font-size: 11px; color: var(--text-muted); text-align: center; padding: 12px;">Cargando grabaciones del servidor...</li>
                    </ul>
                </div>

                <!-- TARJETA: STICKERS, LOGOS Y CAPAS EN PANTALLA -->
                <div class="card" style="border-color: rgba(56, 189, 248, 0.35);">
                    <div class="card-title">
                        <span>🎨 Stickers, Logos & Capas en Vivo</span>
                        <button type="button" class="btn-chip" onclick="clearAllOverlays()" style="color: #f87171;">
                            🗑️ Limpiar Capas
                        </button>
                    </div>

                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-size: 11px; font-weight: 700; color: var(--text-muted);">Toca cualquier sticker o logo para colocarlo en la transmisión:</span>
                        <input type="file" id="overlayImageInput" accept="image/*" style="display: none;" onchange="handleOverlayImageUpload(event)">
                        <button type="button" class="btn-chip" onclick="document.getElementById('overlayImageInput').click()" style="color: #38bdf8; font-weight: 700;">
                            🖼️ Subir Logo / PNG
                        </button>
                    </div>

                    <!-- GALERIA DINÁMICA DE STICKERS -->
                    <div class="stickers-scroll" id="stickersGallery" style="display: flex; gap: 8px; overflow-x: auto; padding-bottom: 8px; margin-bottom: 12px;">
                        <span style="font-size: 11px; color: var(--text-muted); padding: 8px;">Cargando stickers del proyecto...</span>
                    </div>

                    <!-- RÓTULO RÁPIDO CON EMOJIS -->
                    <div style="border-top: 1px solid var(--border); padding-top: 10px;">
                        <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 6px;">
                            ✍️ Agregar Rótulo de Texto en Vivo:
                        </label>
                        <div style="display: flex; gap: 6px; margin-bottom: 8px;">
                            <input type="text" id="newRotuloInput" placeholder="Ej: ¡Transmisión en directo continua 24/7! 🔥🚀" style="flex: 1;">
                            <button type="button" class="btn-chip" onclick="addNewRotulo()" style="color: #34d399; font-weight: 800; white-space: nowrap;">
                                ➕ Agregar
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

                    <!-- CAPAS ACTIVAS EN PANTALLA -->
                    <div style="margin-top: 12px; border-top: 1px solid var(--border); padding-top: 10px;">
                        <span style="font-size: 10px; font-weight: 800; color: var(--text-muted); text-transform: uppercase; display: block; margin-bottom: 6px;">
                            Capas Emitiéndose en Vivo:
                        </span>
                        <div id="activeLayersListContainer" style="display: flex; flex-wrap: wrap; gap: 6px;">
                            <span style="font-size: 11px; color: var(--text-muted); padding: 4px;">No hay capas activas.</span>
                        </div>
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
                                Conecta tu transmisión arriba para recibir y responder comentarios en vivo.
                            </div>
                        </div>
                        <div class="chat-input-bar">
                            <select id="chatTargetPlatform" class="btn-chip" style="padding: 7px; background: rgba(15,23,42,0.9);">
                                <option value="youtube">🔴 YouTube</option>
                                <option value="facebook">🔵 Facebook</option>
                            </select>
                            <input type="text" id="chatReplyInput" placeholder="Responder al chat en vivo..." style="padding: 8px 12px; font-size: 12px;" onkeydown="if(event.key==='Enter') sendChatMessage()">
                            <button type="button" class="btn-chip" onclick="sendChatMessage()" style="color: #38bdf8; padding: 8px 14px; font-weight: 800;">
                                Enviar
                            </button>
                        </div>
                    </div>
                </div>

                <!-- LISTAS TEMÁTICAS Y VIDEOS -->
                <div class="card">
                    <div class="card-title">
                        <span>📁 Listas de Videos Temáticas</span>
                        <button type="button" class="btn-chip" onclick="createCategoryPrompt()" style="color: #38bdf8;">+ Nueva Lista</button>
                    </div>

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
        <div style="background: #0d1322; border: 1px solid rgba(56,189,248,0.3); border-radius: 20px; width: 100%; max-width: 420px; padding: 24px; text-align: center;">
            <h3 style="font-size: 18px; margin-bottom: 6px; color: #fff;">📱 Control Remoto Celular</h3>
            <p style="font-size: 12px; color: #94a3b8; margin-bottom: 14px;">Escanea con tu celular para controlar la emisión 24/7:</p>
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
        let activeOverlays = [];

        function showToast(msg) {
            const t = document.getElementById("toast");
            t.innerText = msg;
            t.classList.add("show");
            setTimeout(() => t.classList.remove("show"), 2800);
        }

        /* MONITOR DE VIDEO EN VIVO Y VISTA PREVIA */
        function toggleMuteVideo() {
            const player = document.getElementById("liveVideoPlayer");
            const btn = document.getElementById("btnMute");
            isMuted = !isMuted;
            player.muted = isMuted;
            btn.innerText = isMuted ? "🔇 Silenciado" : "🔊 Audio Activo";
        }

        function previewBannerText(text) {
            const bannerOverlay = document.getElementById("monitorOverlayBanner");
            if (text && text.trim()) {
                bannerOverlay.innerText = text.trim();
                bannerOverlay.style.display = "block";
            } else {
                bannerOverlay.style.display = "none";
            }
        }

        function setVideoPlayerSource(url, isLiveStream = false, videoTitle = "") {
            const player = document.getElementById("liveVideoPlayer");
            const badge = document.getElementById("monitorOverlayStatus");
            const modeText = document.getElementById("monitorModeBadge");

            if (isLiveStream) {
                badge.className = "monitor-overlay-badge";
                badge.innerHTML = `<span style="color: #ef4444; font-size: 14px;">🔴</span> EN DIRECTO AHORA`;
                modeText.innerText = "🔴 En Transmisión";
                modeText.style.color = "#ef4444";
            } else {
                badge.className = "monitor-overlay-badge";
                badge.innerHTML = `👁️ VISTA PREVIA (${videoTitle || "Estudio"})`;
                modeText.innerText = "👁️ Vista Previa";
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
            document.getElementById("panelYoutube").style.display = (plat === "youtube") ? "block" : "none";
            document.getElementById("panelFacebook").style.display = (plat === "facebook") ? "block" : "none";
            document.getElementById("panelTwitch").style.display = (plat === "twitch") ? "block" : "none";
            document.getElementById("panelMultistream").style.display = (plat === "multistream") ? "block" : "none";
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
                mf.style.height = (fmt === "vertical") ? "340px" : "240px";
                mf.style.maxWidth = (fmt === "vertical") ? "240px" : "100%";
                mf.style.margin = (fmt === "vertical") ? "0 auto 14px auto" : "0 0 14px 0";
            }
            fetch("/api/control", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "switch_format", format: fmt })
            });
        }

        function updateBannerText() {
            const txt = document.getElementById("bannerTextInput").value.trim();
            previewBannerText(txt);
            fetch("/api/control", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "update_banner", banner_text: txt })
            }).then(() => showToast("📢 Rótulo actualizado en vivo"));
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

        /* CHAT EN VIVO MULTIPLATAFORMA */
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
            .then(d => {
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
                box.innerHTML = `<div style="font-size: 11px; color: var(--text-muted); text-align: center; margin-top: 40px;">No hay comentarios en esta pestaña aún.</div>`;
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

        /* LÓGICA DE GRABACIÓN MAESTRA Y DESCARGA EN 1 SOLO VIDEO */
        async function refreshRecordingsList() {
            try {
                const res = await fetch("/api/recordings");
                const data = await res.json();
                const cont = document.getElementById("recordingsFileList");
                const badge = document.getElementById("recordingLiveStatusBadge");

                if (data.is_recording) {
                    badge.style.color = "#f87171";
                    badge.innerText = `● Grabando Sesión en Vivo`;
                } else {
                    badge.style.color = "#34d399";
                    badge.innerText = `● Auto-Guardado Activo`;
                }

                if (!data.recordings || !data.recordings.length) {
                    cont.innerHTML = `<li style="font-size: 11px; color: var(--text-muted); text-align: center; padding: 12px;">No hay emisiones grabadas aún. Inicia una transmisión para generar tu primer video.</li>`;
                    return;
                }

                cont.innerHTML = data.recordings.map(r => `
                    <li class="playlist-item" style="border-left: 3px solid #ef4444;">
                        <div style="overflow: hidden; flex: 1;">
                            <p style="font-size: 11px; font-weight: 800; color: #fff; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">🎬 ${r.filename}</p>
                            <span style="font-size: 9px; color: var(--text-muted);">${r.size_formatted} • ${r.date}</span>
                        </div>
                        <div style="display: flex; gap: 4px;">
                            <a href="${r.download_url}" class="btn-chip" style="color: #34d399; font-weight: 800; padding: 4px 10px; text-decoration: none;">
                                ⬇️ Descargar MP4
                            </a>
                            <button type="button" class="btn-chip" onclick="deleteRecordingFile('${r.filename}')" style="color: #f87171; padding: 4px 8px;">
                                🗑️
                            </button>
                        </div>
                    </li>
                `).join("");
            } catch(e) {}
        }

        async function compileAndDownloadMasterRecording() {
            const btn = document.getElementById("btnCompileNow");
            btn.disabled = true;
            btn.innerText = "⏳ Unificando fragmentos en 1 solo MP4...";
            showToast("Consolidando toda la transmisión en un solo archivo de video...");

            try {
                const res = await fetch("/api/recordings/compile", { method: "POST" });
                const data = await res.json();
                if (data.success && data.download_url) {
                    showToast("✅ ¡Video unificado listo! Iniciando descarga...");
                    refreshRecordingsList();
                    const a = document.createElement("a");
                    a.href = data.download_url;
                    a.download = data.filename;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                } else {
                    showToast("⚠️ " + (data.message || "No hay fragmentos suficientes"));
                }
            } catch (e) {
                showToast("❌ Error al consolidar el archivo de video");
            } finally {
                btn.disabled = false;
                btn.innerText = "⚡ Generar y Descargar Video Hasta Ahora";
            }
        }

        async function deleteRecordingFile(filename) {
            if (!confirm(`¿Eliminar la grabación '${filename}' del servidor?`)) return;
            try {
                const res = await fetch(`/api/recordings/delete/${encodeURIComponent(filename)}`, { method: "POST" });
                const data = await res.json();
                if (data.success) {
                    showToast("Grabación eliminada");
                    refreshRecordingsList();
                }
            } catch(e) {}
        }

        /* LÓGICA DE STICKERS, LOGOS Y OVERLAYS */
        async function loadStickersGallery() {
            try {
                const res = await fetch("/api/stickers");
                const data = await res.json();
                const cont = document.getElementById("stickersGallery");
                if (!cont || !data.stickers) return;

                cont.innerHTML = data.stickers.map(stk => {
                    const cleanName = stk.name.replace(/\.[^/.]+$/, "").replace(/^custom_\d+_/, "").replace(/_/g, " ");
                    const isCustom = stk.filename && stk.filename.startsWith("custom_");
                    return `
                        <div class="sticker-card" style="position: relative;" onclick="addStickerOverlay('${stk.url}', '${cleanName}')" title="Toca para agregar a la transmisión">
                            <img src="${stk.url}" alt="${cleanName}">
                            <span style="font-size: 10px; max-width: 65px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${cleanName}</span>
                            ${isCustom ? `
                                <button type="button" onclick="event.stopPropagation(); deleteCustomSticker('${stk.filename}')" 
                                    style="position: absolute; top: -4px; right: -4px; background: #ef4444; color: #fff; border: none; border-radius: 50%; width: 16px; height: 16px; font-size: 9px; cursor: pointer;" title="Eliminar sticker">✕</button>
                            ` : ''}
                        </div>
                    `;
                }).join("");
            } catch(e) {}
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

        function addStickerOverlay(url, name) {
            const newId = `sticker_${Date.now()}`;
            activeOverlays.push({
                id: newId,
                type: "sticker",
                text: name,
                image_url: url,
                x: 60,
                y: 120,
                width: 80,
                height: 80,
                rotation: 0,
                visible: true
            });
            saveAndApplyOverlays();
            renderActiveLayersList();
            showToast(`🎨 Sticker '${name}' aplicado a la emisión`);
        }

        function handleOverlayImageUpload(e) {
            const file = e.target.files[0];
            if (!file) return;
            const fd = new FormData();
            fd.append("image_file", file);
            showToast("Subiendo logo/imagen para transmisión en vivo...");
            fetch("/api/overlay/upload_image", { method: "POST", body: fd })
                .then(r => r.json())
                .then(d => {
                    if (d.success) {
                        const newId = `image_${Date.now()}`;
                        activeOverlays.push({
                            id: newId,
                            type: "image",
                            text: d.filename || "Logo",
                            image_url: d.url,
                            x: 60,
                            y: 80,
                            width: 100,
                            height: 100,
                            rotation: 0,
                            visible: true
                        });
                        saveAndApplyOverlays();
                        renderActiveLayersList();
                        loadStickersGallery();
                        showToast("✅ Logo aplicado y transmitido en vivo");
                    } else {
                        showToast("Error: " + d.message);
                    }
                });
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
                y: 180,
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
            saveAndApplyOverlays();
            renderActiveLayersList();
            showToast("✨ Rótulo aplicado a la transmisión");
        }

        function insertEmoji(em) {
            const inp = document.getElementById("newRotuloInput");
            if (inp) {
                inp.value += em;
                inp.focus();
            }
        }

        function renderActiveLayersList() {
            const cont = document.getElementById("activeLayersListContainer");
            if (!cont) return;
            const visible = activeOverlays.filter(o => o.visible !== false);
            if (!visible.length) {
                cont.innerHTML = '<span style="font-size: 11px; color: var(--text-muted); padding: 4px;">No hay capas activas.</span>';
                return;
            }
            cont.innerHTML = visible.map(o => `
                <div style="display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 20px; font-size: 11px; color: #fff;">
                    <span>${o.type === 'rotulo' ? '✍️' : (o.type === 'badge' ? '🔴' : '🎨')} ${o.text || 'Capa'}</span>
                    <button type="button" onclick="removeOverlayItem('${o.id}')" style="background: none; border: none; color: #f87171; font-weight: bold; cursor: pointer; padding: 0 2px;">✕</button>
                </div>
            `).join("");
        }

        function removeOverlayItem(id) {
            activeOverlays = activeOverlays.filter(o => o.id !== id);
            saveAndApplyOverlays();
            renderActiveLayersList();
            showToast("🗑️ Capa eliminada");
        }

        function clearAllOverlays() {
            if (!confirm("¿Eliminar todas las capas y stickers de la pantalla?")) return;
            activeOverlays = [];
            fetch("/api/overlay/clear", { method: "POST" })
                .then(() => {
                    renderActiveLayersList();
                    showToast("Capas eliminadas");
                });
        }

        function saveAndApplyOverlays() {
            fetch("/api/overlay/config", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    overlays: activeOverlays,
                    preview_width: (currentStreamFormat === "vertical") ? 240 : 420,
                    preview_height: (currentStreamFormat === "vertical") ? 380 : 240
                })
            }).then(() => showToast("⚡ Capas aplicadas al directo"));
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

        /* PRUEBA DE CONEXIÓN */
        async function testConnection() {
            const fbBox = document.getElementById("testFeedbackBox");
            fbBox.className = "test-feedback loading";
            fbBox.innerText = "⏳ Verificando credenciales con YouTube / Servidor...";
            fbBox.style.display = "block";

            try {
                const res = await fetch("/api/test_connection", {
                    method: "POST", headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        platform: currentPlatform,
                        stream_key: document.getElementById("streamKeyInput").value.trim(),
                        facebook_key: document.getElementById("facebookKeyInput").value.trim(),
                        twitch_key: document.getElementById("twitchKeyInput").value.trim(),
                        multistream_targets: {
                            youtube: document.getElementById("chkMultiYt").checked,
                            facebook: document.getElementById("chkMultiFb").checked,
                            twitch: document.getElementById("chkMultiTw").checked
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
                        multistream_targets: {
                            youtube: document.getElementById("chkMultiYt").checked,
                            facebook: document.getElementById("chkMultiFb").checked,
                            twitch: document.getElementById("chkMultiTw").checked
                        }
                    })
                });
            }, 600);
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
                        active_category: currentCategory,
                        format: currentStreamFormat,
                        multistream_targets: {
                            youtube: document.getElementById("chkMultiYt").checked,
                            facebook: document.getElementById("chkMultiFb").checked,
                            twitch: document.getElementById("chkMultiTw").checked
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
            setTimeout(refreshRecordingsList, 2000);
        }

        /* GESTIÓN DE CATEGORIAS Y VIDEOS */
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
            container.innerHTML = allCategories.map(c => `
                <button type="button" class="btn-chip ${c === currentCategory ? 'active' : ''}" onclick="selectCategory('${c}')">
                    📁 ${c}
                </button>
            `).join("");
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

        /* APLICAR ESTADO EN TIEMPO REAL DESDE EL SERVIDOR */
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

            // Sincronizar reproductor de video en vivo
            if (isStreaming && data.current_video_url) {
                setVideoPlayerSource(data.current_video_url, true, data.current_video);
            } else if (!isStreaming && data.preview_video_url) {
                setVideoPlayerSource(data.preview_video_url, false, data.preview_video_name);
            }

            // Sincronizar Formato
            if (data.stream_format) {
                currentStreamFormat = data.stream_format;
                document.getElementById("btnFmt_vertical").classList.toggle("active", currentStreamFormat === "vertical");
                document.getElementById("btnFmt_horizontal").classList.toggle("active", currentStreamFormat === "horizontal");
                const mf = document.querySelector(".monitor-frame");
                if (mf) {
                    mf.style.height = (currentStreamFormat === "vertical") ? "340px" : "240px";
                    mf.style.maxWidth = (currentStreamFormat === "vertical") ? "240px" : "100%";
                    mf.style.margin = (currentStreamFormat === "vertical") ? "0 auto 14px auto" : "0 0 14px 0";
                }
            }

            // Sincronizar Categorías y Videos
            if (data.categories) allCategories = data.categories;
            if (data.videos) allVideos = data.videos;
            if (data.active_category) currentCategory = data.active_category;
            renderCategoryTabs();
            renderPlaylist();

            // Espectadores y Dispositivos
            if (data.live_viewers !== undefined) {
                document.getElementById("liveViewersDisplay").innerText = `${data.live_viewers} en vivo`;
            }
            if (data.panel_connected_devices !== undefined) {
                document.getElementById("connectedDevicesDisplay").innerText = `${data.panel_connected_devices} conectado(s)`;
            }

            // Sincronizar Rótulo
            const inBanner = document.getElementById("bannerTextInput");
            if (inBanner && data.banner_text !== undefined && !inBanner.matches(":focus")) {
                inBanner.value = data.banner_text;
                previewBannerText(data.banner_text);
            }

            // Sincronizar Overlays
            if (data.overlays && (!activeOverlays || activeOverlays.length === 0)) {
                activeOverlays = data.overlays;
                renderActiveLayersList();
            }

            // Sincronizar Modo Ciclo 11:55 y Monetización
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

            // Sincronizar Video ID para Chat
            if (data.youtube_video_id && !document.getElementById("ytVideoIdInput").value) {
                document.getElementById("ytVideoIdInput").value = data.youtube_video_id;
                updatePopoutLinks(data.youtube_video_id);
            }
            if (data.facebook_live_id && !document.getElementById("fbLiveIdInput").value) {
                document.getElementById("fbLiveIdInput").value = data.facebook_live_id;
            }

            // Sincronizar Claves
            if (data.stream_key && !document.getElementById("streamKeyInput").value) {
                document.getElementById("streamKeyInput").value = data.stream_key;
            }
            if (data.facebook_key && !document.getElementById("facebookKeyInput").value) {
                document.getElementById("facebookKeyInput").value = data.facebook_key;
            }
            if (data.twitch_key && !document.getElementById("twitchKeyInput").value) {
                document.getElementById("twitchKeyInput").value = data.twitch_key;
            }

            // Mensajes de Chat
            if (data.chat_messages) {
                allChatMessages = data.chat_messages;
                renderChatMessages();
            }

            // Logs y Telemetría
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

        /* WEBSOCKET DUAL CON RECONEXIÓN */
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
            syncSocket.onclose = () => {
                setTimeout(connectSyncSocket, 2000);
            };
            syncSocket.onerror = () => {
                try { syncSocket.close(); } catch(e){}
            };
        }
        connectSyncSocket();

        // Polling de respaldo cada 2.5s
        setInterval(() => {
            fetch("/api/status").then(r => r.json()).then(applyServerState);
        }, 2500);

        document.addEventListener("DOMContentLoaded", () => {
            setTimeout(refreshRecordingsList, 1500);
            setTimeout(loadStickersGallery, 500);
            fetch("/api/overlay/config").then(r => r.json()).then(d => {
                if (d.overlays) {
                    activeOverlays = d.overlays;
                    renderActiveLayersList();
                }
            });
        });
    </script>
</body>
</html>
'''

with open(os.path.join(panel_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html_code)

templates_index = os.path.join(panel_dir, "templates", "index.html")
os.makedirs(os.path.dirname(templates_index), exist_ok=True)
shutil.copy2(os.path.join(panel_dir, "index.html"), templates_index)
print("index.html y templates/index.html completados.")

# ==============================================================================
# CONTROL.HTML
# ==============================================================================
control_html_code = r'''<!DOCTYPE html>
<html lang="es">
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
            max-width: 520px;
            margin: 0 auto;
        }

        /* CABECERA CON LOGO NARANJA ORIGINAL Y NOMBRE STREAMHUB */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
            gap: 8px;
        }

        .header-brand {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .brand-icon {
            width: 34px;
            height: 34px;
            border-radius: 10px;
            background: linear-gradient(135deg, #ef4444, #f97316);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4);
            border: 1px solid rgba(249, 115, 22, 0.6);
            overflow: hidden;
            flex-shrink: 0;
        }
        .brand-icon img {
            width: 24px;
            height: 24px;
            object-fit: contain;
            border-radius: 4px;
        }

        .header-brand h1 {
            font-size: 16px;
            font-weight: 800;
            color: #fff;
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

        /* VIDEO ACTUAL MARQUEE */
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
            color: #38bdf8;
            margin-top: 2px;
        }

        /* MONETIZACION Y CICLO 11:55 EN CELULAR */
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
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.35);
        }

        /* STICKERS EN EL CELULAR */
        .stickers-scroll-m {
            display: flex; gap: 8px; overflow-x: auto; padding-bottom: 6px;
            scrollbar-width: none; -webkit-overflow-scrolling: touch;
        }
        .stickers-scroll-m::-webkit-scrollbar { display: none; }
        .sticker-card-m {
            flex-shrink: 0; background: rgba(3, 7, 18, 0.7); border: 1px solid var(--border);
            border-radius: 10px; padding: 6px 8px; display: flex; flex-direction: column;
            align-items: center; gap: 4px; cursor: pointer; text-align: center;
        }
        .sticker-card-m:active { transform: scale(0.94); border-color: #38bdf8; }
        .sticker-card-m img { width: 34px; height: 34px; object-fit: contain; }

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
            background: rgba(2, 132, 199, 0.25); border-color: #38bdf8;
            color: #38bdf8;
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
            <span class="brand-icon">
                <img src="/logo.png" alt="Logo" onerror="this.onerror=null; this.outerHTML='▶';">
            </span>
            <h1>StreamHub Mando</h1>
        </div>
        <div class="status-pill-group">
            <span class="net-status online" id="netBadge">
                <span class="pulse-dot"></span>
                <span id="netText">En tiempo real</span>
            </span>
            <span class="status-badge" id="badgeStatus">DETENIDO ⚪</span>
        </div>
    </div>

    <!-- TARJETA EN DIRECTO AHORA & AUDIENCIA -->
    <div class="card">
        <div class="card-head">
            <span>🔴 EN EMISIÓN AHORA (YOUTUBE)</span>
            <span id="txtFormatBadge" style="color: #38bdf8;">Vertical 9:16</span>
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

    <!-- GRABADOR MAESTRO DE TRANSMISIÓN & DESCARGA EN 1 SOLO VIDEO (MÓVIL) -->
    <div class="card" style="border-color: rgba(239, 68, 68, 0.4); background: linear-gradient(135deg, rgba(239, 68, 68, 0.12), rgba(15, 23, 42, 0.95));">
        <div class="card-head">
            <span style="color: #f87171; font-weight: 800;">🔴 GRABACIÓN MAESTRA (1 SOLO MP4)</span>
            <span id="recordingLiveStatusBadge" style="color: #34d399; font-size: 10px; border: 1px solid rgba(16, 185, 129, 0.3); padding: 2px 6px; border-radius: 6px;">
                ● Auto-Guardado
            </span>
        </div>
        <p style="font-size: 11px; color: var(--text-muted); margin-bottom: 10px; line-height: 1.4;">
            Toda la transmisión se graba en tiempo real en el servidor. Puedes compilar y descargar el video consolidado completo directamente a tu celular.
        </p>
        <div style="display: flex; gap: 8px; margin-bottom: 10px;">
            <button type="button" class="btn" id="btnCompileNow" onclick="compileAndDownloadMasterRecording()" style="flex: 1; padding: 12px; background: linear-gradient(135deg, #ef4444, #f97316); color: #fff; font-size: 12px; font-weight: 800; border-radius: 10px; box-shadow: 0 4px 15px rgba(239,68,68,0.35);">
                ⚡ Generar y Descargar Hasta Ahora
            </button>
            <button type="button" class="btn-icon-sm" onclick="refreshRecordingsList()" title="Refrescar" style="padding: 0 12px;">
                🔄
            </button>
        </div>
        <span style="font-size: 10px; font-weight: 800; color: var(--text-muted); text-transform: uppercase; display: block; margin-bottom: 6px;">
            Archivos Listos para Descargar:
        </span>
        <ul id="recordingsFileList" style="list-style: none; display: flex; flex-direction: column; gap: 6px; max-height: 180px; overflow-y: auto; padding: 0; margin: 0;">
            <li style="font-size: 11px; color: var(--text-muted); text-align: center; padding: 12px;">Cargando grabaciones...</li>
        </ul>
    </div>

    <!-- STICKERS Y RÓTULOS DESDE EL CELULAR -->
    <div class="card">
        <div class="card-head">
            <span>🎨 STICKERS & RÓTULOS EN VIVO</span>
            <button type="button" class="btn-icon-sm" onclick="clearOverlaysMobile()" style="color: #f87171;">
                Limpiar
            </button>
        </div>

        <div class="stickers-scroll-m" id="mobileStickersScroll">
            <span style="font-size: 11px; color: var(--text-muted); padding: 4px;">Cargando stickers...</span>
        </div>

        <input type="file" id="mobileLogoInput" accept="image/*" style="display: none;" onchange="handleMobileLogoUpload(event)">
        <button type="button" class="btn-icon-sm" onclick="document.getElementById('mobileLogoInput').click()" style="color: #38bdf8; font-weight: 700; width: 100%; margin: 8px 0; padding: 8px;">
            📷 Subir Logo / Imagen desde el Celular
        </button>

        <!-- RÓTULO DE TEXTO CON EMOJIS EN CELULAR -->
        <div style="display: flex; gap: 6px; margin-top: 6px;">
            <input type="text" id="mobileRotuloInput" class="input-text" placeholder="Rótulo con emojis..." style="padding: 8px 10px; font-size: 12px;">
            <button type="button" class="btn-icon-sm" onclick="addRotuloMobile()" style="color: #34d399; font-weight: 800; padding: 8px 12px; white-space: nowrap;">
                ➕ Agregar
            </button>
        </div>
        <div style="display: flex; gap: 4px; overflow-x: auto; padding: 6px 0;">
            <button type="button" class="btn-icon-sm" onclick="insertEmojiMobile('🔴')">🔴</button>
            <button type="button" class="btn-icon-sm" onclick="insertEmojiMobile('🔥')">🔥</button>
            <button type="button" class="btn-icon-sm" onclick="insertEmojiMobile('⭐')">⭐</button>
            <button type="button" class="btn-icon-sm" onclick="insertEmojiMobile('💬')">💬</button>
            <button type="button" class="btn-icon-sm" onclick="insertEmojiMobile('⚡')">⚡</button>
            <button type="button" class="btn-icon-sm" onclick="insertEmojiMobile('❤️')">❤️</button>
            <button type="button" class="btn-icon-sm" onclick="insertEmojiMobile('👍')">👍</button>
            <button type="button" class="btn-icon-sm" onclick="insertEmojiMobile('🔔')">🔔</button>
            <button type="button" class="btn-icon-sm" onclick="insertEmojiMobile('🎉')">🎉</button>
        </div>

        <!-- CAPAS ACTIVAS EN PANTALLA -->
        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid var(--border);">
            <span style="font-size: 10px; font-weight: 800; color: var(--text-muted); text-transform: uppercase; display: block; margin-bottom: 6px;">
                Capas Activas en Vivo:
            </span>
            <div id="mobileActiveLayersList" style="display: flex; flex-wrap: wrap; gap: 6px;">
                <span style="font-size: 11px; color: var(--text-muted); padding: 4px;">Cargando capas...</span>
            </div>
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

    <!-- RÓTULO EN PANTALLA -->
    <div class="card">
        <div class="card-head">
            <span>✍️ RÓTULO INFERIOR EN PANTALLA</span>
        </div>
        <div style="display: flex; gap: 8px;">
            <input type="text" id="bannerTextInput" class="input-text" placeholder="Ej: ¡Transmisión en directo continua 24/7!">
            <button type="button" class="btn btn-action" onclick="updateBannerText()" style="padding: 10px 14px; white-space: nowrap;">
                🚀 Enviar
            </button>
        </div>
    </div>

    <!-- LISTAS TEMÁTICAS Y VIDEOS -->
    <div class="card">
        <div class="card-head">
            <span>📂 LISTAS Y VIDEOS EN SERVIDOR</span>
            <span id="txtActiveCatName" style="color: #38bdf8; font-weight: 700;">General</span>
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
            if (confirm("¿Detener la transmisión 24/7 en YouTube?")) {
                apiCall("stop");
                setTimeout(refreshRecordingsList, 2000);
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

        function selectCategory(cat) {
            currentCat = cat;
            document.getElementById("uploadCategorySelect").value = cat;
            document.getElementById("txtActiveCatName").innerText = cat;
            renderCategoryTabs();
            renderPlaylist();
            apiCall("set_category", { category: cat });
        }

        function playVideoNow(cat, name) {
            if (confirm(`¿Emitir ahora '${name}' en YouTube?`)) {
                apiCall("play_now", { category: cat, name: name });
            }
        }

        function previewVideoOnPanel(cat, name) {
            fetch("/api/preview", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ category: cat, name: name })
            }).then(() => notify(`👁️ Vista previa cargada en panel: ${name}`));
        }

        function updateBannerText() {
            const txt = document.getElementById("bannerTextInput").value.trim();
            apiCall("update_banner", { banner_text: txt });
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
                        <button type="button" class="btn-icon-sm" title="Previa en panel" onclick="previewVideoOnPanel('${v.category}', '${v.name}')">
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

        /* LÓGICA DE GRABACIÓN MAESTRA EN EL MÓVIL */
        async function refreshRecordingsList() {
            try {
                const res = await fetch("/api/recordings");
                const data = await res.json();
                const cont = document.getElementById("recordingsFileList");
                const badge = document.getElementById("recordingLiveStatusBadge");

                if (data.is_recording) {
                    badge.style.color = "#f87171";
                    badge.innerText = `● Grabando Sesión en Vivo`;
                } else {
                    badge.style.color = "#34d399";
                    badge.innerText = `● Auto-Guardado`;
                }

                if (!data.recordings || !data.recordings.length) {
                    cont.innerHTML = `<li style="font-size: 11px; color: var(--text-muted); text-align: center; padding: 12px;">No hay emisiones grabadas aún.</li>`;
                    return;
                }

                cont.innerHTML = data.recordings.map(r => `
                    <li class="playlist-item" style="border-left: 3px solid #ef4444;">
                        <div style="overflow: hidden; flex: 1;">
                            <p style="font-size: 11px; font-weight: 800; color: #fff; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">🎬 ${r.filename}</p>
                            <span style="font-size: 9px; color: var(--text-muted);">${r.size_formatted} • ${r.date}</span>
                        </div>
                        <div style="display: flex; gap: 4px;">
                            <a href="${r.download_url}" class="btn-icon-sm" style="color: #34d399; font-weight: 800; text-decoration: none;">
                                ⬇️ Descargar
                            </a>
                            <button type="button" class="btn-icon-sm del" onclick="deleteRecordingFile('${r.filename}')">
                                🗑️
                            </button>
                        </div>
                    </li>
                `).join("");
            } catch(e) {}
        }

        async function compileAndDownloadMasterRecording() {
            const btn = document.getElementById("btnCompileNow");
            btn.disabled = true;
            btn.innerText = "⏳ Generando MP4...";
            notify("Consolidando transmisión en 1 solo archivo...");

            try {
                const res = await fetch("/api/recordings/compile", { method: "POST" });
                const data = await res.json();
                if (data.success && data.download_url) {
                    notify("✅ ¡Video unificado listo!");
                    refreshRecordingsList();
                    const a = document.createElement("a");
                    a.href = data.download_url;
                    a.download = data.filename;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                } else {
                    notify("⚠️ " + (data.message || "Error al compilar"));
                }
            } catch (e) {
                notify("❌ Error al consolidar video");
            } finally {
                btn.disabled = false;
                btn.innerText = "⚡ Generar y Descargar Hasta Ahora";
            }
        }

        async function deleteRecordingFile(filename) {
            if (!confirm(`¿Eliminar la grabación '${filename}'?`)) return;
            try {
                const res = await fetch(`/api/recordings/delete/${encodeURIComponent(filename)}`, { method: "POST" });
                const data = await res.json();
                if (data.success) {
                    notify("Grabación eliminada");
                    refreshRecordingsList();
                }
            } catch(e) {}
        }

        /* LÓGICA DE STICKERS Y LOGOS EN EL MÓVIL */
        async function loadMobileStickers() {
            try {
                const res = await fetch("/api/stickers");
                const data = await res.json();
                const cont = document.getElementById("mobileStickersScroll");
                if (!cont || !data.stickers) return;

                cont.innerHTML = data.stickers.map(stk => {
                    const cleanName = stk.name.replace(/\.[^/.]+$/, "").replace(/^custom_\d+_/, "").replace(/_/g, " ");
                    return `
                        <div class="sticker-card-m" onclick="addStickerMobile('${stk.url}', '${cleanName}')" title="Toca para emitir en directo">
                            <img src="${stk.url}" alt="${cleanName}">
                            <span style="font-size: 10px; color: var(--text-muted); display: block; max-width: 65px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${cleanName}</span>
                        </div>
                    `;
                }).join("");
            } catch(e) {}
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
                    }).then(() => {
                        notify(`Sticker '${name}' agregado`);
                        refreshMobileActiveOverlays();
                    });
                });
        }

        function handleMobileLogoUpload(e) {
            const file = e.target.files[0];
            if (!file) return;
            const fd = new FormData();
            fd.append("image_file", file);
            notify("Subiendo logo...");
            fetch("/api/overlay/upload_image", { method: "POST", body: fd })
                .then(r => r.json())
                .then(d => {
                    if (d.success) {
                        fetch("/api/overlay/config")
                            .then(r => r.json())
                            .then(c => {
                                const ovs = c.overlays || [];
                                ovs.push({
                                    id: `image_${Date.now()}`,
                                    type: "image",
                                    text: d.filename || "Logo Móvil",
                                    image_url: d.url,
                                    x: 60,
                                    y: 80,
                                    width: 100,
                                    height: 100,
                                    rotation: 0,
                                    visible: true
                                });
                                fetch("/api/overlay/config", {
                                    method: "POST", headers: { "Content-Type": "application/json" },
                                    body: JSON.stringify({ overlays: ovs })
                                }).then(() => {
                                    notify("✅ Logo aplicado y transmitido en vivo");
                                    loadMobileStickers();
                                    refreshMobileActiveOverlays();
                                });
                            });
                    }
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
                    }).then(() => {
                        notify("Rótulo agregado a la transmisión");
                        refreshMobileActiveOverlays();
                    });
                });
        }

        function insertEmojiMobile(em) {
            const inp = document.getElementById("mobileRotuloInput");
            if (inp) {
                inp.value += em;
                inp.focus();
            }
        }

        async function refreshMobileActiveOverlays() {
            try {
                const res = await fetch("/api/overlay/config");
                const data = await res.json();
                const cont = document.getElementById("mobileActiveLayersList");
                if (!cont) return;

                const ovs = (data.overlays || []).filter(o => o.visible !== false);
                if (!ovs.length) {
                    cont.innerHTML = '<span style="font-size: 11px; color: var(--text-muted); padding: 4px;">No hay capas activas.</span>';
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
                notify("Capa eliminada");
                refreshMobileActiveOverlays();
            } catch(e) {}
        }

        function clearOverlaysMobile() {
            if (!confirm("¿Eliminar todas las capas activas?")) return;
            fetch("/api/overlay/clear", { method: "POST" })
                .then(() => {
                    notify("Capas eliminadas");
                    refreshMobileActiveOverlays();
                });
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

            // Espectadores en vivo
            if (data.live_viewers !== undefined) {
                document.getElementById("txtViewers").innerText = data.live_viewers;
            }

            // Temporizador Ciclo 11:55 en el celular
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

            // Meta Monetización
            const goal = data.monetization_goal || 4000;
            const unit = data.monetization_unit || "min";
            const prog = data.total_monetization_minutes || 0.0;
            const progDisplay = (unit === "minutos" || unit === "min") ? prog.toFixed(0) : (prog / 60).toFixed(1);
            document.getElementById("mobileMonetizationGoal").innerText = `${progDisplay} / ${goal} ${unit}`;

            const isCycleOn = Boolean(data.youtube_cycle_mode);
            const btnC = document.getElementById("btnToggleCycleMobile");
            btnC.innerText = isCycleOn ? "🔘 Ciclo 11h55m" : "⚪ Modo 24/7";
            btnC.style.color = isCycleOn ? "#f87171" : "#10b981";

            const inBanner = document.getElementById("bannerTextInput");
            if (inBanner && data.banner_text !== undefined && !inBanner.matches(":focus")) {
                inBanner.value = data.banner_text;
            }

            // Chat
            if (data.chat_messages) {
                mobileChatList = data.chat_messages;
                renderMobileChat();
            }

            // Telemetría FPS y Bitrate
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

        /* CONEXION DUAL WEBSOCKET + AUTO-POLLING */
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

        document.addEventListener("DOMContentLoaded", () => {
            setTimeout(refreshRecordingsList, 1500);
            setTimeout(loadMobileStickers, 500);
            setTimeout(refreshMobileActiveOverlays, 800);
        });
    </script>
</body>
</html>
'''

with open(os.path.join(panel_dir, "control.html"), "w", encoding="utf-8") as f:
    f.write(control_html_code)

templates_control = os.path.join(panel_dir, "templates", "control.html")
os.makedirs(os.path.dirname(templates_control), exist_ok=True)
shutil.copy2(os.path.join(panel_dir, "control.html"), templates_control)
print("control.html y templates/control.html completados.")

print("Frontends listos!")
