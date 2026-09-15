/**
 * VIRAL LABS - VISUAL STUDIO 360° MANIPULATOR & 4K LOSSLESS EXPORTER
 * Free persistent drag-and-drop, 4-corner resizer, 360° rotation knob, mirroring & 4K engine
 */

export class VisualStudio {
  constructor(app) {
    this.app = app;
    this.canvas = null;
    this.ctx = null;
    this.currentAspect = '16:9';
    this.canvasWidth = 1280;
    this.canvasHeight = 720;
    this.bgImage = new Image();
    this.bgLoaded = false;

    // Layer System
    this.layers = [
      {
        id: 'layer-badge',
        type: 'badge',
        text: '🔥 100% VIRAL',
        x: 60,
        y: 60,
        width: 220,
        height: 60,
        rotation: 0,
        scaleX: 1,
        scaleY: 1,
        style: 'pink-badge',
        color: '#ffffff',
        fontSize: 32
      },
      {
        id: 'layer-headline',
        type: 'text',
        text: '¡ESTO CAMBIÓ TODO!',
        x: 60,
        y: 460,
        width: 780,
        height: 110,
        rotation: -2,
        scaleX: 1,
        scaleY: 1,
        style: 'mrbeast',
        color: '#ffe600',
        fontSize: 76
      },
      {
        id: 'layer-subline',
        type: 'text',
        text: 'El nuevo truco de IA revelado para 2026',
        x: 64,
        y: 580,
        width: 650,
        height: 60,
        rotation: 0,
        scaleX: 1,
        scaleY: 1,
        style: 'white-bold',
        color: '#f8fafc',
        fontSize: 38
      }
    ];

    this.selectedLayerId = 'layer-headline';

    // Interactive Drag / Resize / Rotate State
    this.dragAction = null; // 'move', 'resize-tl', 'resize-tr', 'resize-bl', 'resize-br', 'rotate'
    this.dragStartX = 0;
    this.dragStartY = 0;
    this.initialLayerState = null;

    this.init();
  }

  init() {
    this.canvas = document.getElementById('thumbnailCanvas');
    if (this.canvas) {
      this.ctx = this.canvas.getContext('2d');
      this.setupCanvas();
    }
    this.bindEvents();
  }

  setupCanvas() {
    this.setAspectRatio(this.currentAspect);
    this.bgImage.src = 'assets/thumbnail_demo.jpg';
    this.bgImage.onload = () => {
      this.bgLoaded = true;
      this.render();
    };
  }

  setAspectRatio(ratio) {
    this.currentAspect = ratio;
    if (ratio === '16:9') {
      this.canvasWidth = 1280;
      this.canvasHeight = 720;
    } else if (ratio === '9:16') {
      this.canvasWidth = 720;
      this.canvasHeight = 1280;
    } else if (ratio === '1:1') {
      this.canvasWidth = 1080;
      this.canvasHeight = 1080;
    }
    if (this.canvas) {
      this.canvas.width = this.canvasWidth;
      this.canvas.height = this.canvasHeight;
      this.render();
    }
  }

  getSelectedLayer() {
    return this.layers.find(l => l.id === this.selectedLayerId);
  }

  render() {
    if (!this.ctx) return;
    const ctx = this.ctx;
    const w = this.canvasWidth;
    const h = this.canvasHeight;

    ctx.clearRect(0, 0, w, h);

    // 1. Draw Background Image & Dramatic Dark Vignette
    if (this.bgLoaded) {
      const imgRatio = this.bgImage.width / this.bgImage.height;
      const canvasRatio = w / h;
      let renderW, renderH, offsetX, offsetY;

      if (imgRatio > canvasRatio) {
        renderH = h;
        renderW = h * imgRatio;
        offsetX = (w - renderW) / 2;
        offsetY = 0;
      } else {
        renderW = w;
        renderH = w / imgRatio;
        offsetX = 0;
        offsetY = (h - renderH) / 2;
      }
      ctx.drawImage(this.bgImage, offsetX, offsetY, renderW, renderH);

      const grad = ctx.createRadialGradient(w / 2, h / 2, h * 0.35, w / 2, h / 2, Math.max(w, h) * 0.75);
      grad.addColorStop(0, 'rgba(0, 0, 0, 0.1)');
      grad.addColorStop(1, 'rgba(5, 7, 14, 0.88)');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);
    } else {
      ctx.fillStyle = '#0a0d18';
      ctx.fillRect(0, 0, w, h);
    }

    // 2. Render all Layers in order
    this.layers.forEach(layer => {
      this.renderLayer(ctx, layer);
    });

    // 3. Render 360° Manipulator Bounding Box for Selected Layer
    const selected = this.getSelectedLayer();
    if (selected) {
      this.renderManipulatorGizmo(ctx, selected);
    }
  }

  renderLayer(ctx, layer) {
    ctx.save();

    // Center of layer
    const cx = layer.x + layer.width / 2;
    const cy = layer.y + layer.height / 2;

    ctx.translate(cx, cy);
    ctx.rotate((layer.rotation * Math.PI) / 180);
    ctx.scale(layer.scaleX, layer.scaleY);
    ctx.translate(-cx, -cy);

    if (layer.type === 'badge') {
      // Badge Graphic
      ctx.shadowColor = 'rgba(236, 72, 153, 0.6)';
      ctx.shadowBlur = 18;
      ctx.fillStyle = '#ec4899';
      ctx.beginPath();
      ctx.roundRect(layer.x, layer.y, layer.width, layer.height, 14);
      ctx.fill();

      // Text inside badge
      ctx.shadowBlur = 0;
      ctx.fillStyle = '#ffffff';
      ctx.font = `900 ${layer.fontSize}px 'Outfit', sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(layer.text, cx, cy);
    } else {
      // Stroked Headline / Subline Text
      const scale = this.canvasWidth / 1280;
      ctx.font = `900 ${layer.fontSize * scale}px 'Outfit', sans-serif`;
      ctx.textAlign = 'left';
      ctx.textBaseline = 'top';

      // Thick black outline for viral pop
      ctx.lineWidth = 14 * scale;
      ctx.lineJoin = 'miter';
      ctx.miterLimit = 2;
      ctx.strokeStyle = '#000000';
      ctx.strokeText(layer.text, layer.x, layer.y);

      // Shadow & Color fill
      ctx.shadowColor = 'rgba(0, 0, 0, 0.9)';
      ctx.shadowBlur = 20 * scale;
      ctx.shadowOffsetX = 4 * scale;
      ctx.shadowOffsetY = 6 * scale;

      ctx.fillStyle = layer.color;
      ctx.fillText(layer.text, layer.x, layer.y);
    }

    ctx.restore();
  }

  renderManipulatorGizmo(ctx, layer) {
    ctx.save();
    const cx = layer.x + layer.width / 2;
    const cy = layer.y + layer.height / 2;

    ctx.translate(cx, cy);
    ctx.rotate((layer.rotation * Math.PI) / 180);
    ctx.translate(-cx, -cy);

    // Glowing cyan dashed bounding box
    ctx.strokeStyle = '#06b6d4';
    ctx.lineWidth = 2;
    ctx.setLineDash([6, 4]);
    ctx.strokeRect(layer.x - 4, layer.y - 4, layer.width + 8, layer.height + 8);

    // Solid Handles (Corner Resizers)
    ctx.setLineDash([]);
    ctx.fillStyle = '#06b6d4';
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;

    const handleSize = 12;
    const corners = [
      { x: layer.x - 4, y: layer.y - 4 }, // TL
      { x: layer.x + layer.width + 4, y: layer.y - 4 }, // TR
      { x: layer.x - 4, y: layer.y + layer.height + 4 }, // BL
      { x: layer.x + layer.width + 4, y: layer.y + layer.height + 4 } // BR
    ];

    corners.forEach(corner => {
      ctx.beginPath();
      ctx.roundRect(corner.x - handleSize / 2, corner.y - handleSize / 2, handleSize, handleSize, 3);
      ctx.fill();
      ctx.stroke();
    });

    // Rotation Knob Handle at the top center
    const rotX = cx;
    const rotY = layer.y - 32;

    // Stem line
    ctx.beginPath();
    ctx.moveTo(rotX, layer.y - 4);
    ctx.lineTo(rotX, rotY);
    ctx.strokeStyle = '#06b6d4';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Knob circle
    ctx.beginPath();
    ctx.arc(rotX, rotY, 10, 0, Math.PI * 2);
    ctx.fillStyle = '#8b5cf6';
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.stroke();

    ctx.restore();
  }

  // Transformations
  mirrorHorizontal() {
    const layer = this.getSelectedLayer();
    if (!layer) return;
    layer.scaleX = layer.scaleX * -1;
    this.render();
    this.app.showToast('Capa volteada horizontalmente (Espejo)', 'info');
  }

  mirrorVertical() {
    const layer = this.getSelectedLayer();
    if (!layer) return;
    layer.scaleY = layer.scaleY * -1;
    this.render();
    this.app.showToast('Capa volteada verticalmente (Espejo)', 'info');
  }

  duplicateLayer() {
    const layer = this.getSelectedLayer();
    if (!layer) return;
    const clone = JSON.parse(JSON.stringify(layer));
    clone.id = 'layer-' + Date.now();
    clone.x += 30;
    clone.y += 30;
    this.layers.push(clone);
    this.selectedLayerId = clone.id;
    this.render();
    this.app.showToast('Capa duplicada.', 'success');
  }

  deleteLayer() {
    if (this.layers.length <= 1) {
      this.app.showToast('Debes mantener al menos una capa.', 'warning');
      return;
    }
    this.layers = this.layers.filter(l => l.id !== this.selectedLayerId);
    this.selectedLayerId = this.layers[0].id;
    this.render();
    this.app.showToast('Capa eliminada.', 'info');
  }

  bringForward() {
    const idx = this.layers.findIndex(l => l.id === this.selectedLayerId);
    if (idx < this.layers.length - 1) {
      const temp = this.layers[idx];
      this.layers[idx] = this.layers[idx + 1];
      this.layers[idx + 1] = temp;
      this.render();
    }
  }

  sendBackward() {
    const idx = this.layers.findIndex(l => l.id === this.selectedLayerId);
    if (idx > 0) {
      const temp = this.layers[idx];
      this.layers[idx] = this.layers[idx - 1];
      this.layers[idx - 1] = temp;
      this.render();
    }
  }

  // Motor de Exportación Ultra HD 4K Lossless
  exportUltraHD4K(format = 'png') {
    if (!this.canvas) return;

    this.app.showToast('🚀 Procesando renderizado Ultra HD 4K Lossless...', 'info');

    setTimeout(() => {
      const exportCanvas = document.createElement('canvas');
      let targetW = 3840;
      let targetH = 2160;

      if (this.currentAspect === '9:16') {
        targetW = 2160;
        targetH = 3840;
      } else if (this.currentAspect === '1:1') {
        targetW = 2160;
        targetH = 2160;
      }

      exportCanvas.width = targetW;
      exportCanvas.height = targetH;
      const expCtx = exportCanvas.getContext('2d');

      // High-resolution image smoothing
      expCtx.imageSmoothingEnabled = true;
      expCtx.imageSmoothingQuality = 'high';

      // Scale factor from working canvas to 4K
      const scale = targetW / this.canvasWidth;
      expCtx.scale(scale, scale);

      // 1. Draw Background
      if (this.bgLoaded) {
        const imgRatio = this.bgImage.width / this.bgImage.height;
        const canvasRatio = this.canvasWidth / this.canvasHeight;
        let rW, rH, oX, oY;

        if (imgRatio > canvasRatio) {
          rH = this.canvasHeight;
          rW = this.canvasHeight * imgRatio;
          oX = (this.canvasWidth - rW) / 2;
          oY = 0;
        } else {
          rW = this.canvasWidth;
          rH = this.canvasWidth / imgRatio;
          oX = 0;
          oY = (this.canvasHeight - rH) / 2;
        }
        expCtx.drawImage(this.bgImage, oX, oY, rW, rH);

        const grad = expCtx.createRadialGradient(
          this.canvasWidth / 2, this.canvasHeight / 2, this.canvasHeight * 0.35,
          this.canvasWidth / 2, this.canvasHeight / 2, Math.max(this.canvasWidth, this.canvasHeight) * 0.75
        );
        grad.addColorStop(0, 'rgba(0, 0, 0, 0.1)');
        grad.addColorStop(1, 'rgba(5, 7, 14, 0.88)');
        expCtx.fillStyle = grad;
        expCtx.fillRect(0, 0, this.canvasWidth, this.canvasHeight);
      }

      // 2. Render all layers without gizmos
      this.layers.forEach(layer => {
        this.renderLayer(expCtx, layer);
      });

      // 3. Download Lossless 4K PNG
      const link = document.createElement('a');
      link.download = `virallabs_4k_lossless_${this.currentAspect.replace(':', '_')}.png`;
      link.href = exportCanvas.toDataURL('image/png', 1.0);
      link.click();

      this.app.showToast(`✨ Exportación Ultra HD 4K (${targetW}x${targetH}px) completada con éxito.`, 'success');
    }, 400);
  }

  // Pointer / Mouse events on Canvas for Drag, Resize and 360 Rotation
  getCanvasPoint(e) {
    const rect = this.canvas.getBoundingClientRect();
    const scaleX = this.canvasWidth / rect.width;
    const scaleY = this.canvasHeight / rect.height;
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY
    };
  }

  bindEvents() {
    if (!this.canvas) return;

    this.canvas.addEventListener('mousedown', (e) => {
      const pt = this.getCanvasPoint(e);
      const selected = this.getSelectedLayer();

      // Check Rotation knob hit
      if (selected) {
        const cx = selected.x + selected.width / 2;
        const rotY = selected.y - 32;
        const distToRot = Math.hypot(pt.x - cx, pt.y - rotY);

        if (distToRot <= 16) {
          this.dragAction = 'rotate';
          this.initialLayerState = { ...selected };
          return;
        }

        // Check corner resizers hit
        const handleHitRadius = 14;
        const corners = {
          'resize-tl': { x: selected.x - 4, y: selected.y - 4 },
          'resize-tr': { x: selected.x + selected.width + 4, y: selected.y - 4 },
          'resize-bl': { x: selected.x - 4, y: selected.y + selected.height + 4 },
          'resize-br': { x: selected.x + selected.width + 4, y: selected.y + selected.height + 4 }
        };

        for (const [action, pos] of Object.entries(corners)) {
          if (Math.hypot(pt.x - pos.x, pt.y - pos.y) <= handleHitRadius) {
            this.dragAction = action;
            this.dragStartX = pt.x;
            this.dragStartY = pt.y;
            this.initialLayerState = { ...selected };
            return;
          }
        }
      }

      // Check hit on any layer to select & drag
      let hitLayer = null;
      for (let i = this.layers.length - 1; i >= 0; i--) {
        const l = this.layers[i];
        if (pt.x >= l.x && pt.x <= l.x + l.width && pt.y >= l.y && pt.y <= l.y + l.height) {
          hitLayer = l;
          break;
        }
      }

      if (hitLayer) {
        this.selectedLayerId = hitLayer.id;
        this.dragAction = 'move';
        this.dragStartX = pt.x - hitLayer.x;
        this.dragStartY = pt.y - hitLayer.y;
        this.render();
      }
    });

    window.addEventListener('mousemove', (e) => {
      if (!this.dragAction) return;
      const pt = this.getCanvasPoint(e);
      const layer = this.getSelectedLayer();
      if (!layer) return;

      if (this.dragAction === 'move') {
        layer.x = pt.x - this.dragStartX;
        layer.y = pt.y - this.dragStartY;
        this.render();
      } else if (this.dragAction === 'rotate') {
        const cx = layer.x + layer.width / 2;
        const cy = layer.y + layer.height / 2;
        const angleRad = Math.atan2(pt.y - cy, pt.x - cx);
        let deg = Math.round((angleRad * 180) / Math.PI + 90);
        if (deg < 0) deg += 360;

        // Snap near cardinal angles
        if (Math.abs(deg - 0) < 5 || Math.abs(deg - 360) < 5) deg = 0;
        if (Math.abs(deg - 90) < 5) deg = 90;
        if (Math.abs(deg - 180) < 5) deg = 180;
        if (Math.abs(deg - 270) < 5) deg = 270;

        layer.rotation = deg;
        this.render();
      } else if (this.dragAction.startsWith('resize-')) {
        const init = this.initialLayerState;
        const dx = pt.x - this.dragStartX;
        const dy = pt.y - this.dragStartY;

        if (this.dragAction === 'resize-br') {
          layer.width = Math.max(60, init.width + dx);
          layer.height = Math.max(30, init.height + dy);
        } else if (this.dragAction === 'resize-bl') {
          layer.width = Math.max(60, init.width - dx);
          layer.x = init.x + dx;
          layer.height = Math.max(30, init.height + dy);
        } else if (this.dragAction === 'resize-tr') {
          layer.width = Math.max(60, init.width + dx);
          layer.height = Math.max(30, init.height - dy);
          layer.y = init.y + dy;
        } else if (this.dragAction === 'resize-tl') {
          layer.width = Math.max(60, init.width - dx);
          layer.x = init.x + dx;
          layer.height = Math.max(30, init.height - dy);
          layer.y = init.y + dy;
        }
        this.render();
      }
    });

    window.addEventListener('mouseup', () => {
      this.dragAction = null;
    });

    // Toolbar Buttons
    const mirrorHBtn = document.getElementById('toolMirrorHBtn');
    const mirrorVBtn = document.getElementById('toolMirrorVBtn');
    const duplicateBtn = document.getElementById('toolDuplicateBtn');
    const deleteBtn = document.getElementById('toolDeleteBtn');
    const layerUpBtn = document.getElementById('toolLayerUpBtn');
    const layerDownBtn = document.getElementById('toolLayerDownBtn');
    const export4KBtn = document.getElementById('export4KBtn');

    if (mirrorHBtn) mirrorHBtn.addEventListener('click', () => this.mirrorHorizontal());
    if (mirrorVBtn) mirrorVBtn.addEventListener('click', () => this.mirrorVertical());
    if (duplicateBtn) duplicateBtn.addEventListener('click', () => this.duplicateLayer());
    if (deleteBtn) deleteBtn.addEventListener('click', () => this.deleteLayer());
    if (layerUpBtn) layerUpBtn.addEventListener('click', () => this.bringForward());
    if (layerDownBtn) layerDownBtn.addEventListener('click', () => this.sendBackward());
    if (export4KBtn) export4KBtn.addEventListener('click', () => this.exportUltraHD4K());
  }
}
