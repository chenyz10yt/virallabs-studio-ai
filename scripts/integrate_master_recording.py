import os, sys, re, shutil

sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
panel_dir = os.path.abspath(os.path.join(base_dir, '..', 'panel_stream'))

print("Directorio Web y App:", base_dir)
print("Directorio Panel Stream:", panel_dir)

# ==============================================================================
# 1. ACTUALIZAR index.html
# ==============================================================================
web_index = os.path.join(base_dir, 'index.html')
with open(web_index, 'r', encoding='utf-8') as f:
    html = f.read()

# 1.1 Insertar CSS .playlist-item si no existe
if '.playlist-item' not in html:
    css_insert = '''        .playlist-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 12px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            gap: 8px;
            transition: all 0.2s ease;
        }
        .playlist-item:hover {
            background: rgba(30, 41, 59, 0.8);
            border-color: rgba(239, 68, 68, 0.4);
        }
    </style>'''
    html = html.replace('    </style>', css_insert, 1)
    print("CSS .playlist-item insertado en index.html")

# 1.2 Insertar TARJETA DE GRABACION MAESTRA debajo de TARJETA 5
card_marker = '''                    <!-- LISTA DE VIDEOS (CON AMBOS IDs) -->
                    <div id="playlistContainer" style="max-height: 240px; overflow-y: auto;"></div>
                    <div id="categoryVideosList" style="display: none;"></div>
                </div>'''

new_card_html = '''                    <!-- LISTA DE VIDEOS (CON AMBOS IDs) -->
                    <div id="playlistContainer" style="max-height: 240px; overflow-y: auto;"></div>
                    <div id="categoryVideosList" style="display: none;"></div>
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
                        Toda tu emisión en vivo (sin importar si dura 1 hora, 2 horas o más) se guarda continuamente en el servidor con tus logos, rótulos y audio sincronizados. Puedes generar y descargar el video consolidado completo cuando quieras.
                    </p>

                    <!-- BOTÓN PARA CONSOLIDAR Y DESCARGAR HASTA EL MINUTO ACTUAL -->
                    <div style="display: flex; gap: 8px; margin-bottom: 12px;">
                        <button type="button" class="btn" id="btnCompileNow" onclick="compileAndDownloadMasterRecording()" style="flex: 1; padding: 12px; background: linear-gradient(135deg, #ef4444, #f97316); color: #fff; font-size: 12px; font-weight: 800; border-radius: 10px; box-shadow: 0 4px 15px rgba(239,68,68,0.35);">
                            ⚡ Generar y Descargar Video Hasta Ahora
                        </button>
                        <button type="button" class="btn-chip" onclick="refreshRecordingsList()" title="Refrescar archivos">
                            🔄
                        </button>
                    </div>

                    <!-- LISTA DE VIDEOS MAESTROS GUARDADOS -->
                    <span style="font-size: 10px; font-weight: 800; color: var(--text-muted); text-transform: uppercase; display: block; margin-bottom: 6px;">
                        Archivos Listos para Descargar:
                    </span>
                    <ul id="recordingsFileList" style="list-style: none; display: flex; flex-direction: column; gap: 6px; max-height: 180px; overflow-y: auto;">
                        <li style="font-size: 11px; color: var(--text-muted); text-align: center; padding: 12px;">Cargando grabaciones del servidor...</li>
                    </ul>
                </div>'''

if 'id="btnCompileNow"' not in html:
    if card_marker in html:
        html = html.replace(card_marker, new_card_html, 1)
        print("Tarjeta de Grabación Maestra insertada en index.html")
    else:
        print("⚠️ No se encontró card_marker exacto en index.html")

# 1.3 Actualizar badge en applyServerState si no está
if 'recordingLiveStatusBadge' not in html[html.find('function applyServerState'):html.find('/* WEBSOCKET */')]:
    apply_state_marker = 'btnStop.disabled = !isStreaming;'
    apply_state_insert = '''btnStop.disabled = !isStreaming;

            const recBadge = document.getElementById("recordingLiveStatusBadge");
            if (recBadge) {
                if (isStreaming) {
                    recBadge.style.color = "#f87171";
                    recBadge.innerText = "● Grabando Sesión en Vivo";
                } else {
                    recBadge.style.color = "#94a3b8";
                    recBadge.innerText = "⚪ En Espera";
                }
            }'''
    html = html.replace(apply_state_marker, apply_state_insert, 1)
    print("Actualización de recordingLiveStatusBadge añadida a applyServerState en index.html")

# 1.4 Insertar funciones JavaScript de Grabación Maestra
js_code_block = '''
        /* LÓGICA DE GRABACIÓN MAESTRA Y DESCARGA EN 1 SOLO VIDEO */
        async function refreshRecordingsList() {
            try {
                const res = await fetch("/api/recordings");
                const data = await res.json();
                const cont = document.getElementById("recordingsFileList");
                const badge = document.getElementById("recordingLiveStatusBadge");

                if (badge) {
                    if (data.is_recording) {
                        badge.style.color = "#f87171";
                        badge.innerText = `● Grabando Sesión en Vivo`;
                    } else {
                        badge.style.color = "#94a3b8";
                        badge.innerText = `⚪ En Espera`;
                    }
                }

                if (!cont) return;

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
            if (btn) {
                btn.disabled = true;
                btn.innerText = "⏳ Unificando fragmentos en 1 solo MP4...";
            }
            if (typeof showToast === "function") {
                showToast("Consolidando toda la transmisión en un solo archivo de video...");
            }

            try {
                const res = await fetch("/api/recordings/compile", { method: "POST" });
                const data = await res.json();
                if (data.success && data.download_url) {
                    if (typeof showToast === "function") {
                        showToast("✅ ¡Video unificado listo! Iniciando descarga...");
                    }
                    refreshRecordingsList();
                    // Disparar la descarga automática
                    const a = document.createElement("a");
                    a.href = data.download_url;
                    a.download = data.filename;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                } else {
                    if (typeof showToast === "function") {
                        showToast("⚠️ " + (data.message || "No hay fragmentos suficientes"));
                    }
                }
            } catch (e) {
                if (typeof showToast === "function") {
                    showToast("❌ Error al consolidar el archivo de video");
                }
            } finally {
                if (btn) {
                    btn.disabled = false;
                    btn.innerText = "⚡ Generar y Descargar Video Hasta Ahora";
                }
            }
        }

        async function deleteRecordingFile(filename) {
            if (!confirm(`¿Eliminar la grabación '${filename}' del servidor?`)) return;
            try {
                const res = await fetch(`/api/recordings/delete/${encodeURIComponent(filename)}`, { method: "POST" });
                const data = await res.json();
                if (data.success) {
                    if (typeof showToast === "function") {
                        showToast("Grabación eliminada");
                    }
                    refreshRecordingsList();
                }
            } catch(e) {}
        }

        // Cargar lista de grabaciones al iniciar
        document.addEventListener("DOMContentLoaded", () => {
            setTimeout(refreshRecordingsList, 1500);
        });
'''

if 'function refreshRecordingsList' not in html:
    html = html.replace('    </script>\n</body>', js_code_block + '\n    </script>\n</body>')
    print("Lógica JavaScript de Grabación Maestra añadida a index.html")

# Guardar web y app/index.html
with open(web_index, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Guardado {web_index} ({len(html)} bytes)")

# Sincronizar a panel_stream/templates/index.html y panel_stream/index.html
tpl_index = os.path.join(panel_dir, 'templates', 'index.html')
root_index = os.path.join(panel_dir, 'index.html')
os.makedirs(os.path.dirname(tpl_index), exist_ok=True)

with open(tpl_index, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Sincronizado {tpl_index} ({len(html)} bytes)")

with open(root_index, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Sincronizado {root_index} ({len(html)} bytes)")

# ==============================================================================
# 2. ACTUALIZAR control.html (Mando Móvil)
# ==============================================================================
web_ctrl = os.path.join(base_dir, 'control.html')
with open(web_ctrl, 'r', encoding='utf-8') as f:
    c_html = f.read()

# 2.1 Insertar tarjeta en control.html debajo de CONTROLES PRINCIPALES
ctrl_marker = '''            <button type="button" class="btn btn-fmt" onclick="toggleFormat()">
                <span>📱</span> <span id="txtFmt">Vertical 9:16</span>
            </button>
        </div>
    </div>'''

ctrl_card_html = '''            <button type="button" class="btn btn-fmt" onclick="toggleFormat()">
                <span>📱</span> <span id="txtFmt">Vertical 9:16</span>
            </button>
        </div>
    </div>

    <!-- GRABADOR MAESTRO DE TRANSMISIÓN & DESCARGA EN 1 SOLO VIDEO (MÓVIL) -->
    <div class="card" style="border-color: rgba(239, 68, 68, 0.4); background: linear-gradient(135deg, rgba(239, 68, 68, 0.12), rgba(15, 23, 42, 0.95));">
        <div class="card-head">
            <span style="color: #f87171; font-weight: 800;">🔴 GRABACIÓN MAESTRA (1 SOLO MP4)</span>
            <span id="recordingLiveStatusBadge" class="live-pill" style="color: #34d399; font-size: 10px; border: 1px solid rgba(16, 185, 129, 0.3); padding: 2px 6px; border-radius: 6px;">
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
    </div>'''

if 'id="btnCompileNow"' not in c_html:
    if ctrl_marker in c_html:
        c_html = c_html.replace(ctrl_marker, ctrl_card_html, 1)
        print("Tarjeta de Grabación Maestra insertada en control.html")
    else:
        print("⚠️ No se encontró ctrl_marker en control.html")

if 'function refreshRecordingsList' not in c_html:
    c_html = c_html.replace('    </script>\n</body>', js_code_block + '\n    </script>\n</body>')
    print("Lógica JavaScript de Grabación Maestra añadida a control.html")

# Guardar web y app/control.html
with open(web_ctrl, 'w', encoding='utf-8') as f:
    f.write(c_html)
print(f"Guardado {web_ctrl} ({len(c_html)} bytes)")

# Sincronizar a panel_stream/templates/control.html y panel_stream/control.html
tpl_ctrl = os.path.join(panel_dir, 'templates', 'control.html')
root_ctrl = os.path.join(panel_dir, 'control.html')

with open(tpl_ctrl, 'w', encoding='utf-8') as f:
    f.write(c_html)
print(f"Sincronizado {tpl_ctrl} ({len(c_html)} bytes)")

with open(root_ctrl, 'w', encoding='utf-8') as f:
    f.write(c_html)
print(f"Sincronizado {root_ctrl} ({len(c_html)} bytes)")

print("\n🎉 ¡Sincronización de Grabación Maestra completada al 100%!")
