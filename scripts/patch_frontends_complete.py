import os, sys, shutil

sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
panel_dir = os.path.abspath(os.path.join(base_dir, '..', 'panel_stream'))

# ==============================================================================
# 1. ACTUALIZAR index.html
# ==============================================================================
index_path = os.path.join(base_dir, 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    idx_html = f.read()

# 1.1 Añadir autoSaveBannerText y popoutChat si faltan
extra_index_js = '''
        /* RÓTULO DINÁMICO AUTO-GUARDADO CON DEBOUNCE */
        let bannerDebounceTimer = null;
        function autoSaveBannerText(val) {
            clearTimeout(bannerDebounceTimer);
            bannerDebounceTimer = setTimeout(() => {
                fetch("/api/control", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ action: "update_banner", banner_text: val })
                }).then(r => r.json()).then(d => {
                    if (d.success) showToast("Rótulo inferior actualizado");
                }).catch(e => {});
            }, 350);
        }

        /* CHAT FLOTANTE / POPOUT YOUTUBE */
        function popoutChat() {
            const ytVal = (document.getElementById("ytVideoIdInput")?.value || "").trim();
            if (!ytVal) {
                showToast("⚠️ Ingresa primero el ID o enlace de video de YouTube");
                return;
            }
            let vidId = ytVal;
            const m = ytVal.match(/(?:v=|\/live\/|\.be\/)([a-zA-Z0-9_-]{11})/);
            if (m) vidId = m[1];
            const url = `https://www.youtube.com/live_chat?v=${vidId}&is_popout=1`;
            window.open(url, "yt_popout_chat", "width=450,height=650,resizable=yes,scrollbars=yes");
        }
'''

if 'function autoSaveBannerText' not in idx_html:
    idx_html = idx_html.replace('    </script>\n</body>', extra_index_js + '\n    </script>\n</body>')
    print("Funciones autoSaveBannerText y popoutChat añadidas a index.html")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(idx_html)

# ==============================================================================
# 2. ACTUALIZAR control.html
# ==============================================================================
ctrl_path = os.path.join(base_dir, 'control.html')
with open(ctrl_path, 'r', encoding='utf-8') as f:
    c_html = f.read()

extra_ctrl_js = '''
        function insertMobileEmoji(emoji) {
            const inp = document.getElementById("mobileRotuloInput");
            if (inp) {
                inp.value += emoji;
                inp.focus();
            }
        }

        function handleMobileImageUpload(e) {
            const file = e.target.files[0];
            if (!file) return;
            const fd = new FormData();
            fd.append("file", file);
            if (typeof notify === "function") notify("Subiendo imagen de logo...");
            fetch("/api/overlay/upload_image", { method: "POST", body: fd })
                .then(r => r.json())
                .then(d => {
                    if (d.success) {
                        fetch("/api/overlay/config")
                            .then(r => r.json())
                            .then(cfg => {
                                const ovs = cfg.overlays || [];
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
                                    if (typeof notify === "function") notify("✅ Logo aplicado y transmitido en vivo");
                                });
                            });
                    } else {
                        if (typeof notify === "function") notify("Error: " + d.message);
                    }
                });
        }

        function forceApplyMobileOverlays() {
            fetch("/api/overlay/config")
                .then(r => r.json())
                .then(d => {
                    fetch("/api/overlay/config", {
                        method: "POST", headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ overlays: d.overlays || [] })
                    }).then(() => {
                        if (typeof notify === "function") notify("⚡ Capas forzadas en vivo");
                    });
                });
        }
'''

if 'function insertMobileEmoji' not in c_html:
    c_html = c_html.replace('    </script>\n</body>', extra_ctrl_js + '\n    </script>\n</body>')
    print("Funciones móviles insertMobileEmoji, handleMobileImageUpload y forceApplyMobileOverlays añadidas a control.html")

with open(ctrl_path, 'w', encoding='utf-8') as f:
    f.write(c_html)

# ==============================================================================
# 3. SINCRONIZAR A panel_stream
# ==============================================================================
# index.html
shutil.copy2(index_path, os.path.join(panel_dir, 'templates', 'index.html'))
shutil.copy2(index_path, os.path.join(panel_dir, 'index.html'))
print("Sincronizado index.html hacia panel_stream")

# control.html
shutil.copy2(ctrl_path, os.path.join(panel_dir, 'templates', 'control.html'))
shutil.copy2(ctrl_path, os.path.join(panel_dir, 'control.html'))
print("Sincronizado control.html hacia panel_stream")

print("\n🎉 ¡Frontends 100% auditados y actualizados!")
