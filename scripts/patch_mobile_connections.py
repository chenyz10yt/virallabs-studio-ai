import os, sys, re, shutil

base_panel = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream"
index_path = os.path.join(base_panel, "index.html")
control_path = os.path.join(base_panel, "control.html")
tpl_index = os.path.join(base_panel, "templates", "index.html")
tpl_control = os.path.join(base_panel, "templates", "control.html")

print("Updating index.html and control.html with unified mobile connectivity...")

# ==============================================================================
# 1. UPDATE index.html
# ==============================================================================
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Update openControlQrModal and add IP detection
old_qr_func = '''function openControlQrModal() {
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
        }'''

new_qr_func = '''let serverLocalIp = "10.243.28.219";
        let allServerIps = ["10.243.28.219"];

        function setQrHost(targetIp) {
            serverLocalIp = targetIp;
            generateQrForHost(targetIp);
        }

        function generateQrForHost(host) {
            const port = window.location.port ? (":" + window.location.port) : ":5000";
            const proto = window.location.protocol + "//";
            const url = proto + host + port + "/control";

            const qrInp = document.getElementById("qrLink");
            if (qrInp) qrInp.value = url;

            const cont = document.getElementById("qrBox");
            if (cont) {
                cont.innerHTML = "";
                try {
                    new QRCode(cont, { text: url, width: 200, height: 200, correctLevel: QRCode.CorrectLevel.M });
                } catch(e) {
                    cont.innerHTML = `<a href="${url}" target="_blank" style="color: #38bdf8; font-size: 14px; text-decoration: underline;">Abrir Control Móvil: ${url}</a>`;
                }
            }

            // Actualizar botones de selector de red
            const selCont = document.getElementById("ipSelectorContainer");
            if (selCont && allServerIps.length > 0) {
                selCont.innerHTML = allServerIps.map(ip => `
                    <button type="button" class="btn-chip ${ip === host ? 'active' : ''}" onclick="setQrHost('${ip}')" style="font-size: 11px; padding: 4px 10px;">
                        ${ip.startsWith('10.') || ip.startsWith('192.168.') ? '📶 Wi-Fi: ' : '🌐 Red: '}${ip}
                    </button>
                `).join("");
            }
        }

        function openControlQrModal() {
            let host = serverLocalIp;
            if (!host || host === "localhost" || host === "127.0.0.1") {
                host = (allServerIps && allServerIps[0]) || "10.243.28.219";
            }
            generateQrForHost(host);
            document.getElementById("controlQrModal").style.display = "flex";
        }

        function copyMobileLink() {
            const inp = document.getElementById("qrLink");
            if (inp) {
                inp.select();
                navigator.clipboard.writeText(inp.value).then(() => {
                    showToast("📋 Enlace copiado. Pégalo en el navegador de tu celular");
                }).catch(() => {
                    document.execCommand('copy');
                    showToast("📋 Enlace copiado al portapapeles");
                });
            }
        }'''

if 'function openControlQrModal()' in html:
    html = re.sub(r'function openControlQrModal\(\)[\s\S]*?document\.getElementById\("controlQrModal"\)\.style\.display = "flex";\s*\}', new_qr_func, html)
    print("Updated openControlQrModal in index.html")

# Update Modal HTML in index.html to include IP selector and copy button
old_modal_inner = '''<div class="modal-box">
            <h3 style="margin-bottom: 8px; font-size: 16px;">📱 Control Remoto Celular</h3>
            <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">
                Escanea este código con la cámara de tu celular para controlar la transmisión en vivo, lanzar videos y moderar el chat:
            </p>
            <div id="qrBox" style="background: #fff; padding: 12px; border-radius: 8px; display: inline-block; margin-bottom: 12px;"></div>
            <div style="display: flex; gap: 6px; margin-bottom: 12px;">
                <input type="text" id="qrLink" readonly style="font-size: 11px; text-align: center; background: rgba(0,0,0,0.3);">
            </div>
            <button type="button" class="btn btn-secondary" onclick="closeControlQrModal()" style="width: 100%;">
                Cerrar
            </button>
        </div>'''

new_modal_inner = '''<div class="modal-box" style="max-width: 420px; text-align: center;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h3 style="font-size: 16px; margin: 0; color: #38bdf8;">📱 Control Remoto Celular</h3>
                <button type="button" class="btn-chip" onclick="closeControlQrModal()" style="padding: 2px 8px; font-size: 16px;">✕</button>
            </div>
            <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">
                Conecta tu celular a la <strong>misma red Wi-Fi</strong> de esta PC y escanea el código QR o entra a la dirección mostrada abajo:
            </p>
            
            <div id="ipSelectorContainer" style="display: flex; gap: 6px; justify-content: center; margin-bottom: 10px; flex-wrap: wrap;"></div>

            <div id="qrBox" style="background: #fff; padding: 12px; border-radius: 12px; display: inline-block; margin-bottom: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);"></div>

            <div style="display: flex; gap: 6px; margin-bottom: 12px;">
                <input type="text" id="qrLink" readonly style="font-size: 12px; text-align: center; background: rgba(0,0,0,0.4); border: 1px solid rgba(56,189,248,0.4); border-radius: 6px; color: #38bdf8; font-weight: 700; flex: 1;">
                <button type="button" class="btn-chip" onclick="copyMobileLink()" style="background: #38bdf8; color: #0f172a; font-weight: 800; white-space: nowrap; padding: 0 12px;">
                    📋 Copiar
                </button>
            </div>

            <div style="display: flex; gap: 8px;">
                <a id="qrOpenDirectLink" href="/control" target="_blank" class="btn btn-secondary" style="flex: 1; text-decoration: none; padding: 9px; font-size: 12px;">
                    💻 Probar en PC
                </a>
                <button type="button" class="btn btn-primary" onclick="closeControlQrModal()" style="flex: 1; padding: 9px; font-size: 12px;">
                    Listo
                </button>
            </div>
        </div>'''

if 'id="qrBox"' in html and 'id="ipSelectorContainer"' not in html:
    html = re.sub(r'<div class="modal-box">[\s\S]*?id="qrBox"[\s\S]*?Cerrar\s*</button>\s*</div>', new_modal_inner, html)
    print("Updated QR Modal dialog HTML in index.html")

# Update header mobile button to show IP
old_hdr_btn = '<button type="button" class="btn-chip" onclick="openControlQrModal()" style="color: #38bdf8; font-weight: bold;">\n                    📱 Control Celular / QR\n                </button>'
new_hdr_btn = '<button type="button" class="btn-chip" onclick="openControlQrModal()" style="color: #38bdf8; font-weight: bold; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.35); box-shadow: 0 0 10px rgba(56, 189, 248, 0.15);">\n                    📱 Control Celular: <span id="headerMobileIpText" style="color: #fff;">10.243.28.219:5000</span>\n                </button>'

if old_hdr_btn in html:
    html = html.replace(old_hdr_btn, new_hdr_btn)
else:
    html = re.sub(
        r'<button type="button" class="btn-chip" onclick="openControlQrModal\(\)"[^>]*>\s*📱 Control Celular / QR\s*</button>',
        new_hdr_btn,
        html
    )

# Update applyServerState and WebSocket handling to extract IP
old_apply_func = 'function applyServerState(data) {'
new_apply_func = '''function applyServerState(data) {
            if (!data) return;
            if (data.local_ip) {
                serverLocalIp = data.local_ip;
                const txt = document.getElementById("headerMobileIpText");
                if (txt) txt.innerText = `${data.local_ip}:5000`;
            }
            if (data.all_ips && Array.isArray(data.all_ips)) {
                allServerIps = data.all_ips;
            }'''

if old_apply_func in html and 'data.local_ip' not in html:
    html = html.replace(old_apply_func, new_apply_func, 1)
    print("Updated applyServerState with IP extraction in index.html")

# Update syncSocket.onmessage in index.html to handle both state and state_update
old_ws_handle = '''syncSocket.onmessage = (e) => {
                try {
                    const res = JSON.parse(e.data);
                    if (res.type === "state_update") {
                        applyServerState(res.state);
                    } else if (res.type === "chat_message") {
                        allChatMessages.push(res.message);
                        renderChatMessages();
                    }
                } catch(err) {}
            };'''

new_ws_handle = '''syncSocket.onmessage = (e) => {
                try {
                    const res = JSON.parse(e.data);
                    if (res.type === "state_update" || res.type === "state") {
                        applyServerState(res.state || res);
                    } else if (res.type === "chat_message" || res.type === "chat") {
                        allChatMessages.push(res.message);
                        renderChatMessages();
                    }
                    if (res.local_ip) {
                        serverLocalIp = res.local_ip;
                        const txt = document.getElementById("headerMobileIpText");
                        if (txt) txt.innerText = `${res.local_ip}:5000`;
                    }
                    if (res.all_ips) {
                        allServerIps = res.all_ips;
                    }
                } catch(err) {}
            };'''

if old_ws_handle in html:
    html = html.replace(old_ws_handle, new_ws_handle)
    print("Updated WebSocket message handler in index.html")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)
with open(tpl_index, 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved index.html and templates/index.html")

# ==============================================================================
# 2. UPDATE control.html
# ==============================================================================
with open(control_path, 'r', encoding='utf-8') as f:
    c_html = f.read()

# Enhance apiCall in control.html to ensure 100% reliable action delivery
old_api_call = '''function apiCall(action, extra = {}) {
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
        }'''

new_api_call = '''function apiCall(action, extra = {}) {
            vibrate();
            const payload = { action: action, ...extra };

            // Enviar siempre por HTTP para garantizar ejecución inmediata e indestructible
            fetch("/api/control", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            })
            .then(r => r.json())
            .then(d => {
                notify(d.message || "Comando ejecutado");
                // También enviar por WebSocket para refrescar a otros clientes si está conectado
                if (ws && ws.readyState === WebSocket.OPEN) {
                    try { ws.send(JSON.stringify(payload)); } catch(e){}
                }
            })
            .catch(() => {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    try {
                        ws.send(JSON.stringify(payload));
                        notify("Comando enviado por WebSocket");
                        return;
                    } catch(e){}
                }
                notify("⚠️ Error al conectar con el servidor");
            });
        }'''

if 'function apiCall(action, extra = {})' in c_html:
    c_html = re.sub(r'function apiCall\(action, extra = \{\}\)[\s\S]*?notify\("⚠️ Error al conectar con el servidor"\)\);\s*\}', new_api_call, c_html)
    print("Updated apiCall in control.html for guaranteed delivery")

# Enhance previewVideoOnPanel in control.html
old_preview_call = '''function previewVideoOnPanel(cat, name) {
            fetch("/api/preview", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ category: cat, name: name })
            }).then(() => notify(`👁️ Vista previa: ${name}`));
        }'''

new_preview_call = '''function previewVideoOnPanel(cat, name) {
            fetch("/api/preview", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ category: cat, name: name })
            }).then(r => r.json()).then(d => {
                notify(d.message || `👁️ Vista previa: ${name}`);
            }).catch(() => notify(`👁️ Vista previa activada: ${name}`));
        }'''

if old_preview_call in c_html:
    c_html = c_html.replace(old_preview_call, new_preview_call)
    print("Updated previewVideoOnPanel in control.html")

# Update WebSocket handler in control.html to accept state and state_update
old_ctl_ws = '''ws.onmessage = (e) => {
                try {
                    const res = JSON.parse(e.data);
                    if (res.type === "state_update") {
                        updateState(res.state);
                    } else if (res.type === "chat_message") {
                        mobileChatList.push(res.message);
                        renderMobileChat();
                    }
                } catch (err) {}
            };'''

new_ctl_ws = '''ws.onmessage = (e) => {
                try {
                    const res = JSON.parse(e.data);
                    if (res.type === "state_update" || res.type === "state") {
                        updateState(res.state || res);
                    } else if (res.type === "chat_message" || res.type === "chat") {
                        mobileChatList.push(res.message);
                        renderMobileChat();
                    }
                } catch (err) {}
            };'''

if old_ctl_ws in c_html:
    c_html = c_html.replace(old_ctl_ws, new_ctl_ws)
    print("Updated WebSocket onmessage in control.html")

# Ensure netBadge indicates connected host
c_html = c_html.replace(
    'document.getElementById("netText").innerText = "En tiempo real";',
    'document.getElementById("netText").innerText = "En tiempo real (" + location.hostname + ")";'
)

with open(control_path, 'w', encoding='utf-8') as f:
    f.write(c_html)
with open(tpl_control, 'w', encoding='utf-8') as f:
    f.write(c_html)
print("Saved control.html and templates/control.html")
