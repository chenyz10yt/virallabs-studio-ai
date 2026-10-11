import os, sys, re, shutil

base_panel = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream"
index_path = os.path.join(base_panel, "index.html")
control_path = os.path.join(base_panel, "control.html")
tpl_index = os.path.join(base_panel, "templates", "index.html")
tpl_control = os.path.join(base_panel, "templates", "control.html")

print("Updating index.html with instant auto-apply overlays, selected item editor, and high-res pipeline...")

# ==============================================================================
# 1. UPDATE index.html
# ==============================================================================
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace button in card header with prominent Glowing APLICAR EN VIVO YA
old_btn = r'<button type="button" class="btn-chip active" onclick="saveAndApplyOverlays()">' + "\n" + r'                                    💾 Guardar y Aplicar' + "\n" + r'                                </button>'
new_btn = r'<button type="button" id="btnForceApplyOverlays" class="btn-chip active" onclick="saveAndApplyOverlays()" style="background: linear-gradient(135deg, #10b981, #06b6d4); color: #fff; font-weight: 800; border: none; box-shadow: 0 0 14px rgba(16,185,129,0.5);">' + "\n" + r'                                    ⚡ APLICAR EN VIVO YA' + "\n" + r'                                </button>'

if old_btn in html:
    html = html.replace(old_btn, new_btn)
else:
    # Try regex replacement if whitespace differed
    html = re.sub(
        r'<button type="button" class="btn-chip active" onclick="saveAndApplyOverlays\(\)">\s*💾 Guardar y Aplicar\s*</button>',
        r'<button type="button" id="btnForceApplyOverlays" class="btn-chip active" onclick="saveAndApplyOverlays()" style="background: linear-gradient(135deg, #10b981, #06b6d4); color: #fff; font-weight: 800; border: none; box-shadow: 0 0 14px rgba(16,185,129,0.5);">⚡ APLICAR EN VIVO YA</button>',
        html
    )

# Insert the Selected Layer Editor right under </table\s*>\s*</div\s*> for layersTable
editor_html = '''                            </table>
                        </div>

                        <!-- PANEL DE EDICIÓN EN TIEMPO REAL DEL ELEMENTO O RÓTULO SELECCIONADO -->
                        <div id="selectedOverlayEditor" style="margin-top: 12px; padding: 12px; background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 8px; display: none;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <strong id="editorItemTitle" style="font-size: 12px; color: #38bdf8;">⚙️ Editar en Vivo: <span id="editorItemName">Rótulo</span></strong>
                                <button type="button" class="btn-chip" onclick="saveAndApplyOverlays()" style="background: linear-gradient(135deg, #10b981, #06b6d4); color: #fff; font-weight: 800; border: none; padding: 4px 10px;">
                                    ⚡ APLICAR EN VIVO YA
                                </button>
                            </div>
                            <div id="editorTextGroup" style="margin-bottom: 8px;">
                                <label style="font-size: 11px; color: var(--text-muted); display: block; margin-bottom: 4px;">Texto del Rótulo (Aplica en la pantalla de transmisión):</label>
                                <div style="display: flex; gap: 6px;">
                                    <input type="text" id="selectedOverlayTextInput" placeholder="Escribe el texto del rótulo..." oninput="onSelectedOverlayTextChange(this.value)">
                                    <button type="button" class="btn-chip" onclick="saveAndApplyOverlays()" style="color: #34d399; font-weight: 800; white-space: nowrap;">
                                        ⚡ Aplicar
                                    </button>
                                </div>
                            </div>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px; margin-bottom: 8px;">
                                <div>
                                    <label style="font-size: 10px; color: var(--text-muted); display: block;">Color Fondo:</label>
                                    <input type="color" id="selectedOverlayBgInput" value="#0f172a" style="width: 100%; height: 32px; padding: 2px; border-radius: 4px; background: transparent; cursor: pointer;" onchange="onSelectedOverlayBgChange(this.value)">
                                </div>
                                <div>
                                    <label style="font-size: 10px; color: var(--text-muted); display: block;">Color Texto:</label>
                                    <input type="color" id="selectedOverlayColorInput" value="#ffffff" style="width: 100%; height: 32px; padding: 2px; border-radius: 4px; background: transparent; cursor: pointer;" onchange="onSelectedOverlayColorChange(this.value)">
                                </div>
                                <div>
                                    <label style="font-size: 10px; color: var(--text-muted); display: block;">Tamaño Fuente: <span id="editorFontSizeVal">16px</span></label>
                                    <input type="range" id="selectedOverlayFontSizeInput" min="10" max="48" value="16" style="width: 100%;" oninput="onSelectedOverlayFontSizeChange(this.value)">
                                </div>
                                <div>
                                    <label style="font-size: 10px; color: var(--text-muted); display: block;">Giro (360°): <span id="editorRotationVal">0°</span></label>
                                    <input type="range" id="selectedOverlayRotInput" min="0" max="360" value="0" style="width: 100%;" oninput="onSelectedOverlayRotationChange(this.value)">
                                </div>
                            </div>
                            <div style="display: flex; gap: 4px; align-items: center; flex-wrap: wrap;">
                                <span style="font-size: 10px; color: var(--text-muted);">Giro rápido:</span>
                                <button type="button" class="btn-chip" onclick="setOverlayQuickRotation(0)">0°</button>
                                <button type="button" class="btn-chip" onclick="setOverlayQuickRotation(45)">45°</button>
                                <button type="button" class="btn-chip" onclick="setOverlayQuickRotation(90)">90°</button>
                                <button type="button" class="btn-chip" onclick="setOverlayQuickRotation(180)">180°</button>
                                <button type="button" class="btn-chip" onclick="setOverlayQuickRotation(270)">270°</button>
                                <button type="button" class="btn-chip" onclick="saveAndApplyOverlays()" style="margin-left: auto; color: #34d399; font-weight: 700;">
                                    ⚡ Transmitir Capas Ahora
                                </button>
                            </div>
                        </div>'''

# Replace the table closure with table closure + editor
if 'id="selectedOverlayEditor"' not in html:
    html = re.sub(
        r'</table>\s*</div>\s*(?=\s*</div>\s*</div>\s*<!-- SECCIÓN MONETIZACIÓN)',
        editor_html + '\n                    </div>\n                </div>\n',
        html
    )

# Now replace the overlay javascript functions to enable instant auto-apply and the live editor
old_js_start = html.find('function toggleOverlayVisibility')
old_js_end = html.find('/* CHAT EN VIVO */')

new_js = '''function toggleOverlayVisibility(id) {
            const ov = activeOverlays.find(o => o.id === id);
            if (ov) {
                ov.visible = !ov.visible;
                renderOverlaysCanvas();
                saveAndApplyOverlays(); // AUTO-APLICA DE INMEDIATO EN LA TRANSMISION
            }
        }

        function resetOverlayRotation(id) {
            const ov = activeOverlays.find(o => o.id === id);
            if (ov) {
                ov.rotation = 0;
                renderOverlaysCanvas();
                updateOverlayEditorUI(ov);
                saveAndApplyOverlays(); // AUTO-APLICA DE INMEDIATO EN LA TRANSMISION
            }
        }

        function setOverlayQuickRotation(deg) {
            if (!selectedOverlayId) return;
            const ov = activeOverlays.find(o => o.id === selectedOverlayId);
            if (ov) {
                ov.rotation = deg;
                renderOverlaysCanvas();
                updateOverlayEditorUI(ov);
                saveAndApplyOverlays(); // AUTO-APLICA DE INMEDIATO EN LA TRANSMISION
            }
        }

        function deleteOverlayItem(id) {
            activeOverlays = activeOverlays.filter(o => o.id !== id);
            if (selectedOverlayId === id) {
                selectedOverlayId = null;
                const editor = document.getElementById("selectedOverlayEditor");
                if (editor) editor.style.display = "none";
            }
            renderOverlaysCanvas();
            saveAndApplyOverlays(); // AUTO-APLICA DE INMEDIATO EN LA TRANSMISION
            showToast("🗑️ Elemento eliminado de la transmisión");
        }

        function insertEmoji(em) {
            const inp = document.getElementById("newRotuloInput");
            if (inp) {
                inp.value += em;
                inp.focus();
            }
            if (selectedOverlayId) {
                const edInp = document.getElementById("selectedOverlayTextInput");
                if (edInp) {
                    edInp.value += em;
                    onSelectedOverlayTextChange(edInp.value);
                }
            }
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
            selectOverlay(newId);
            renderOverlaysCanvas();
            saveAndApplyOverlays(); // AUTO-APLICA DE INMEDIATO EN LA TRANSMISION
            showToast("✨ Rótulo aplicado y transmitido en pantalla");
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
            renderOverlaysCanvas();
            saveAndApplyOverlays(); // AUTO-APLICA DE INMEDIATO EN LA TRANSMISION
            showToast(`🎨 Sticker '${name}' aplicado y transmitido en pantalla`);
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
                        selectOverlay(newId);
                        renderOverlaysCanvas();
                        saveAndApplyOverlays(); // AUTO-APLICA DE INMEDIATO EN LA TRANSMISION
                        showToast("✅ Logo aplicado y transmitido en vivo");
                    } else {
                        showToast("Error: " + d.message);
                    }
                });
        }

        let overlayDebounceTimer = null;
        function saveAndApplyOverlays(silent = false) {
            const layer = document.getElementById("overlayCanvasLayer");
            const pw = layer ? layer.clientWidth : 240;
            const ph = layer ? layer.clientHeight : 380;
            fetch("/api/overlay/config", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    overlays: activeOverlays,
                    preview_width: pw,
                    preview_height: ph
                })
            }).then(r => r.json()).then(d => {
                if (d.success && !silent) {
                    showToast("⚡ Capas y stickers aplicados a la transmisión");
                }
            }).catch(err => console.error(err));
        }

        /* EDITOR EN VIVO DE CAPA SELECCIONADA */
        function updateOverlayEditorUI(ov) {
            const editor = document.getElementById("selectedOverlayEditor");
            if (!editor) return;
            if (!ov) {
                editor.style.display = "none";
                return;
            }
            editor.style.display = "block";
            const isText = (ov.type === "rotulo" || ov.type === "badge" || !ov.image_url);
            const textGroup = document.getElementById("editorTextGroup");
            if (textGroup) textGroup.style.display = isText ? "block" : "none";

            const textInp = document.getElementById("selectedOverlayTextInput");
            if (textInp && isText) textInp.value = ov.text || "";

            const titleSpan = document.getElementById("editorItemName");
            if (titleSpan) titleSpan.innerText = ov.text || (ov.type === "sticker" ? "Sticker" : "Logo");

            const rotInp = document.getElementById("selectedOverlayRotInput");
            if (rotInp) rotInp.value = ov.rotation || 0;
            const rotVal = document.getElementById("editorRotationVal");
            if (rotVal) rotVal.innerText = `${Math.round(ov.rotation || 0)}°`;

            const fontInp = document.getElementById("selectedOverlayFontSizeInput");
            if (fontInp) fontInp.value = ov.fontSize || 16;
            const fontVal = document.getElementById("editorFontSizeVal");
            if (fontVal) fontVal.innerText = `${ov.fontSize || 16}px`;
        }

        function onSelectedOverlayTextChange(val) {
            if (!selectedOverlayId) return;
            const ov = activeOverlays.find(o => o.id === selectedOverlayId);
            if (ov) {
                ov.text = val;
                renderOverlaysCanvas();
                clearTimeout(overlayDebounceTimer);
                overlayDebounceTimer = setTimeout(() => {
                    saveAndApplyOverlays(true);
                }, 350);
            }
        }

        function onSelectedOverlayBgChange(val) {
            if (!selectedOverlayId) return;
            const ov = activeOverlays.find(o => o.id === selectedOverlayId);
            if (ov) {
                ov.bg = val;
                renderOverlaysCanvas();
                saveAndApplyOverlays();
            }
        }

        function onSelectedOverlayColorChange(val) {
            if (!selectedOverlayId) return;
            const ov = activeOverlays.find(o => o.id === selectedOverlayId);
            if (ov) {
                ov.color = val;
                renderOverlaysCanvas();
                saveAndApplyOverlays();
            }
        }

        function onSelectedOverlayFontSizeChange(val) {
            if (!selectedOverlayId) return;
            const ov = activeOverlays.find(o => o.id === selectedOverlayId);
            if (ov) {
                ov.fontSize = parseInt(val) || 16;
                const fontVal = document.getElementById("editorFontSizeVal");
                if (fontVal) fontVal.innerText = `${val}px`;
                renderOverlaysCanvas();
                clearTimeout(overlayDebounceTimer);
                overlayDebounceTimer = setTimeout(() => {
                    saveAndApplyOverlays(true);
                }, 350);
            }
        }

        function onSelectedOverlayRotationChange(val) {
            if (!selectedOverlayId) return;
            const ov = activeOverlays.find(o => o.id === selectedOverlayId);
            if (ov) {
                ov.rotation = parseFloat(val) || 0;
                const rotVal = document.getElementById("editorRotationVal");
                if (rotVal) rotVal.innerText = `${Math.round(val)}°`;
                renderOverlaysCanvas();
                clearTimeout(overlayDebounceTimer);
                overlayDebounceTimer = setTimeout(() => {
                    saveAndApplyOverlays(true);
                }, 250);
            }
        }

        /* INTERACCIÓN DRAG, RESIZE 8-HANDLES & ROTATE 360° */
        let currentDragState = null;

        function startOverlayInteraction(e, id) {
            e.stopPropagation();
            selectOverlay(id);
            const ov = activeOverlays.find(o => o.id === id);
            if (!ov) return;
            updateOverlayEditorUI(ov);

            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            const target = e.target;

            if (target.classList.contains("rot-handle")) {
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

                const snapAngles = [0, 45, 90, 135, 180, 225, 270, 315, 360];
                snapAngles.forEach(snap => {
                    if (Math.abs(angle - snap) < 4) angle = snap % 360;
                });
                ov.rotation = Math.round(angle);
                const rotVal = document.getElementById("editorRotationVal");
                if (rotVal) rotVal.innerText = `${ov.rotation}°`;
                const rotInp = document.getElementById("selectedOverlayRotInput");
                if (rotInp) rotInp.value = ov.rotation;
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
            if (currentDragState) {
                currentDragState = null;
                renderOverlaysCanvas();
                saveAndApplyOverlays(true); // AUTO-APLICA DE INMEDIATO EN VIVO AL SOLTAR!
            }
            window.removeEventListener("mousemove", onOverlayInteractionMove);
            window.removeEventListener("mouseup", endOverlayInteraction);
            window.removeEventListener("touchmove", onOverlayInteractionMove);
            window.removeEventListener("touchend", endOverlayInteraction);
        }

        '''

if old_js_start != -1 and old_js_end != -1:
    html = html[:old_js_start] + new_js + html[old_js_end:]
    print("Replaced overlay JS functions in index.html successfully.")

# Also in selectOverlay, call updateOverlayEditorUI
html = html.replace(
    '''function selectOverlay(id) {
            selectedOverlayId = id;
            renderOverlaysCanvas();
        }''',
    '''function selectOverlay(id) {
            selectedOverlayId = id;
            renderOverlaysCanvas();
            const ov = activeOverlays.find(o => o.id === id);
            if (ov) updateOverlayEditorUI(ov);
        }'''
)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)
with open(tpl_index, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html and templates/index.html successfully!")

# ==============================================================================
# 2. UPDATE control.html
# ==============================================================================
with open(control_path, 'r', encoding='utf-8') as f:
    c_html = f.read()

# Add mobile image upload & live apply button in control.html
mobile_extras_html = '''        <div style="display: flex; gap: 4px; margin-top: 8px; overflow-x: auto; padding-bottom: 2px;">
            <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertMobileEmoji('🔴')">🔴</button>
            <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertMobileEmoji('🔥')">🔥</button>
            <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertMobileEmoji('⭐')">⭐</button>
            <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertMobileEmoji('🚀')">🚀</button>
            <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertMobileEmoji('❤️')">❤️</button>
            <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertMobileEmoji('👍')">👍</button>
            <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertMobileEmoji('🔔')">🔔</button>
            <button type="button" class="btn-chip" style="padding: 4px 8px;" onclick="insertMobileEmoji('🎉')">🎉</button>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px;">
            <input type="file" id="mobileOverlayImageInput" accept="image/*" style="display: none;" onchange="handleMobileImageUpload(event)">
            <button type="button" class="btn btn-secondary" onclick="document.getElementById('mobileOverlayImageInput').click()" style="padding: 9px 6px; font-size: 11px; background: rgba(56, 189, 248, 0.15); color: #38bdf8; font-weight: 700; border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 6px;">
                📷 Subir Logo Móvil
            </button>
            <button type="button" class="btn btn-primary" onclick="forceApplyMobileOverlays()" style="padding: 9px 6px; font-size: 11px; background: linear-gradient(135deg, #10b981, #06b6d4); font-weight: 800; border: none; border-radius: 6px;">
                ⚡ APLICAR EN VIVO
            </button>
        </div>'''

if 'mobileOverlayImageInput' not in c_html:
    target_pos = c_html.find('id="mobileRotuloInput"')
    if target_pos != -1:
        # find closure of the div containing mobileRotuloInput
        div_end = c_html.find('</div>', target_pos) + len('</div>')
        c_html = c_html[:div_end] + "\n" + mobile_extras_html + c_html[div_end:]
        print("Added mobile image upload and live apply buttons to control.html!")

# Update mobile functions
mobile_js = '''        function insertMobileEmoji(em) {
            const inp = document.getElementById("mobileRotuloInput");
            if (inp) {
                inp.value += em;
                inp.focus();
            }
        }

        function handleMobileImageUpload(e) {
            const file = e.target.files[0];
            if (!file) return;
            const fd = new FormData();
            fd.append("image_file", file);
            notify("Subiendo logo desde el móvil...");
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
                                }).then(() => notify("✅ Logo aplicado y transmitido en vivo"));
                            });
                    } else {
                        notify("Error: " + d.message);
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
                    }).then(() => notify("⚡ Capas forzadas en vivo"));
                });
        }
'''

if 'handleMobileImageUpload' not in c_html:
    c_html = c_html.replace('function addRotuloMobile() {', mobile_js + '\n        function addRotuloMobile() {')
    print("Added mobile JS functions to control.html!")

with open(control_path, 'w', encoding='utf-8') as f:
    f.write(c_html)
with open(tpl_control, 'w', encoding='utf-8') as f:
    f.write(c_html)

print("Updated control.html and templates/control.html successfully!")
