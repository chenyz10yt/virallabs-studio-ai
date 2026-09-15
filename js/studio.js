/**
 * OMNIVIRAL STUDIO AI - STUDIO & CANVAS DESIGNER MODULE
 * Scriptwriting, Prompt Engineering & Interactive Canvas Designer
 */

export class StudioManager {
  constructor(app) {
    this.app = app;
    this.canvas = null;
    this.ctx = null;
    this.currentAspect = '16:9';
    this.activeStyle = 'mrbeast';
    this.canvasWidth = 1280;
    this.canvasHeight = 720;
    this.bgImage = new Image();
    this.bgImageLoaded = false;
    
    // Canvas Text State
    this.textLayers = {
      headline: '¡ESTO CAMBIÓ TODO!',
      subline: 'El nuevo truco de IA revelado',
      badgeText: '🔥 100% VIRAL'
    };

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
      this.bgImageLoaded = true;
      this.renderCanvas();
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
    this.canvas.width = this.canvasWidth;
    this.canvas.height = this.canvasHeight;
    this.renderCanvas();
  }

  renderCanvas() {
    if (!this.ctx) return;
    const ctx = this.ctx;
    const w = this.canvasWidth;
    const h = this.canvasHeight;

    // Draw Background
    if (this.bgImageLoaded) {
      // Cover fit image
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

      // Add dramatic dark vignette / gradient
      const gradient = ctx.createRadialGradient(w / 2, h / 2, h * 0.3, w / 2, h / 2, Math.max(w, h) * 0.75);
      gradient.addColorStop(0, 'rgba(0, 0, 0, 0.1)');
      gradient.addColorStop(1, 'rgba(3, 7, 18, 0.85)');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, w, h);
    } else {
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, w, h);
    }

    // Apply Style Settings for Text
    const isVertical = this.currentAspect === '9:16';
    const scale = w / 1280;

    // 1. Draw Badge Tag
    if (this.textLayers.badgeText) {
      ctx.save();
      const badgeFontSize = Math.round(36 * scale);
      ctx.font = `900 ${badgeFontSize}px 'Outfit', sans-serif`;
      const textMetrics = ctx.measureText(this.textLayers.badgeText);
      const paddingX = 26 * scale;
      const paddingY = 14 * scale;
      const badgeW = textMetrics.width + paddingX * 2;
      const badgeH = badgeFontSize + paddingY * 2;
      const badgeX = isVertical ? (w - badgeW) / 2 : 60 * scale;
      const badgeY = isVertical ? 120 * scale : 60 * scale;

      // Badge Background glow & pill
      ctx.shadowColor = 'rgba(236, 72, 153, 0.6)';
      ctx.shadowBlur = 20 * scale;
      ctx.fillStyle = '#ec4899';
      ctx.beginPath();
      ctx.roundRect(badgeX, badgeY, badgeW, badgeH, 12 * scale);
      ctx.fill();

      // Badge Text
      ctx.shadowBlur = 0;
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'top';
      ctx.fillText(this.textLayers.badgeText, badgeX + paddingX, badgeY + paddingY);
      ctx.restore();
    }

    // 2. Draw Headline with thick outline
    if (this.textLayers.headline) {
      ctx.save();
      const headFontSize = Math.round((isVertical ? 64 : 76) * scale);
      ctx.font = `900 ${headFontSize}px 'Outfit', sans-serif`;
      ctx.textAlign = isVertical ? 'center' : 'left';
      ctx.textBaseline = 'middle';

      const posX = isVertical ? w / 2 : 60 * scale;
      const posY = isVertical ? h * 0.65 : h * 0.68;

      this.drawStrokedText(
        ctx,
        this.textLayers.headline,
        posX,
        posY,
        this.activeStyle,
        headFontSize,
        scale
      );
      ctx.restore();
    }

    // 3. Draw Subline
    if (this.textLayers.subline) {
      ctx.save();
      const subFontSize = Math.round((isVertical ? 38 : 42) * scale);
      ctx.font = `800 ${subFontSize}px 'Inter', sans-serif`;
      ctx.textAlign = isVertical ? 'center' : 'left';
      ctx.textBaseline = 'middle';

      const posX = isVertical ? w / 2 : 60 * scale;
      const posY = isVertical ? h * 0.77 : h * 0.82;

      ctx.shadowColor = 'rgba(0, 0, 0, 0.9)';
      ctx.shadowBlur = 12 * scale;
      ctx.fillStyle = '#f8fafc';
      ctx.fillText(this.textLayers.subline, posX, posY);
      ctx.restore();
    }
  }

  drawStrokedText(ctx, text, x, y, style, fontSize, scale) {
    const strokeWidth = 14 * scale;
    ctx.lineJoin = 'miter';
    ctx.miterLimit = 2;

    // Outer thick black stroke for high readability
    ctx.lineWidth = strokeWidth;
    ctx.strokeStyle = '#000000';
    ctx.strokeText(text, x, y);

    // Deep drop shadow
    ctx.shadowColor = 'rgba(0, 0, 0, 0.9)';
    ctx.shadowBlur = 24 * scale;
    ctx.shadowOffsetX = 6 * scale;
    ctx.shadowOffsetY = 8 * scale;

    if (style === 'mrbeast') {
      ctx.fillStyle = '#ffe600'; // MrBeast Yellow
    } else if (style === 'neon-cyan') {
      ctx.fillStyle = '#00f2fe';
    } else if (style === 'fire-rose') {
      ctx.fillStyle = '#ff4b4b';
    } else {
      ctx.fillStyle = '#ffffff';
    }

    ctx.fillText(text, x, y);
  }

  exportThumbnail() {
    if (!this.canvas) return;
    const link = document.createElement('a');
    link.download = `omniviral_thumbnail_${this.currentAspect.replace(':', '_')}.png`;
    link.href = this.canvas.toDataURL('image/png', 1.0);
    link.click();
    this.app.showToast('Portada descargada en alta resolución (PNG)', 'success');
  }

  generateViralScript(topic, niche, format) {
    const scripts = {
      'short': `⚡ GUION VIRAL PARA TIKTOK / REELS / SHORTS (60s)
🎯 TEMA: "${topic || 'Inteligencia Artificial para Automatizar Contenido'}"
🏷️ NICHO: ${niche.toUpperCase()}

[0:00 - 0:03] 🔥 HOOK PSICOLÓGICO (Brecha de Curiosidad):
"Si creas contenido y tardas más de 30 minutos por video, estás tirando tu tiempo a la basura... te muestro el truco que usan las agencias millonarias."
(Acción: Mirada fija a cámara con acercamiento rápido de zoom)

[0:03 - 0:18] 📈 RETENCIÓN & PROBLEMA:
"El 95% de los creadores se rinden porque se queman editando subtítulos, buscando ideas y diseñando portadas. Pero mira esto..."
(B-roll: Captura de pantalla mostrando la plataforma en acción)

[0:18 - 0:42] 💡 LA SOLUCIÓN REVELADA (Valor Máximo):
"Paso 1: Entras a OmniViral y pegas tu stream o tema central.
Paso 2: La IA detecta los mejores momentos y te corta 5 clips verticales automáticos con subtítulos estilo MrBeast.
Paso 3: Clonamos tu voz para narrar historias sin que tengas que grabar 20 tomas."

[0:42 - 0:55] 🚀 RESULTADO & PRUEBA SOCIAL:
"En solo 5 minutos tienes una semana entera de contenido programado para TikTok, Instagram y YouTube Shorts al mismo tiempo."

[0:55 - 1:00] 🎯 CALL TO ACTION (Llamada a la Acción de Alto Engagement):
"Guarda este video antes de que lo borren y comenta 'VIRAL' para enviarte la guía de algoritmos gratis."`,

      'midjourney': `🎨 PROMPT HIPER-CINEMÁTICO PARA MIDJOURNEY / FLUX / SDXL:
Topic: "${topic || 'Futuristic creator workspace with holographic analytics'}"

Prompt:
"A charismatic content creator in a cutting-edge neon cyberpunk broadcast studio, speaking passionately into a broadcast microphone, dynamic multi-monitor displays showing glowing holographic viral analytics graphs, volumetric neon turquoise and magenta rim lighting, cinematic 85mm portrait lens, f/1.4 shallow depth of field, ultra-detailed textures, photorealistic 8k, hyper-vibrant color grading --ar 16:9 --style raw --v 6.1"

💡 Parámetros de Cámara Recomendados:
• Iluminación: Volumetric Soft Neons + Key Light frontal a 45°
• Lente: 85mm prime para desenfoque de fondo cinematográfico
• Relación de aspecto: --ar 16:9 (YouTube) o --ar 9:16 (TikTok/Reels)`,

      'video_ai': `🎬 PROMPT & STORYBOARD PARA RUNWAY GEN-3 / KLING / SORA:
Topic: "${topic || 'Streamer celebrating viral milestone'}"

Scene Prompt:
"Cinematic first-person camera slow push-in towards an expressive young creator reacting with immense genuine excitement looking at high-tech holographic subscriber count crossing 1,000,000, futuristic dark room illuminated by pulsating cyan LED ambient lights, camera floating with smooth gimbal motion, hyperrealistic facial micro-expressions, 4k cinematic broadcast, 60fps."

🎬 Movimiento de Cámara: Slow Zoom-In + Subtle Orbit (Pan +0.5)
⏱️ Duración: 5.0 segundos en bucle perfecto.`
    };

    return scripts[format] || scripts['short'];
  }

  bindEvents() {
    // Aspect Ratio buttons
    document.querySelectorAll('.aspect-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.aspect-btn').forEach(b => b.classList.remove('active'));
        const target = e.currentTarget;
        target.classList.add('active');
        this.setAspectRatio(target.dataset.aspect);
      });
    });

    // Style presets
    document.querySelectorAll('.preset-chip').forEach(chip => {
      chip.addEventListener('click', (e) => {
        this.activeStyle = e.currentTarget.dataset.style;
        this.renderCanvas();
      });
    });

    // Headline inputs
    const headlineInput = document.getElementById('canvasHeadlineInput');
    const sublineInput = document.getElementById('canvasSublineInput');
    const badgeInput = document.getElementById('canvasBadgeInput');

    if (headlineInput) {
      headlineInput.addEventListener('input', (e) => {
        this.textLayers.headline = e.target.value;
        this.renderCanvas();
      });
    }
    if (sublineInput) {
      sublineInput.addEventListener('input', (e) => {
        this.textLayers.subline = e.target.value;
        this.renderCanvas();
      });
    }
    if (badgeInput) {
      badgeInput.addEventListener('input', (e) => {
        this.textLayers.badgeText = e.target.value;
        this.renderCanvas();
      });
    }

    // Image Upload for Canvas
    const imgUploadInput = document.getElementById('canvasBgUpload');
    if (imgUploadInput) {
      imgUploadInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (event) => {
            this.bgImage.src = event.target.result;
            this.bgImage.onload = () => {
              this.bgImageLoaded = true;
              this.renderCanvas();
              this.app.showToast('Imagen de fondo cargada en el lienzo', 'success');
            };
          };
          reader.readAsDataURL(file);
        }
      });
    }

    // Export Button
    const exportBtn = document.getElementById('exportThumbnailBtn');
    if (exportBtn) {
      exportBtn.addEventListener('click', () => this.exportThumbnail());
    }

    // Script Generator Button
    const genScriptBtn = document.getElementById('generateScriptBtn');
    if (genScriptBtn) {
      genScriptBtn.addEventListener('click', () => {
        const topic = document.getElementById('scriptTopicInput')?.value || '';
        const niche = document.getElementById('scriptNicheSelect')?.value || 'ia';
        const format = document.querySelector('.subtab-btn.active')?.dataset.format || 'short';
        
        genScriptBtn.innerHTML = '✨ Generando con IA...';
        genScriptBtn.disabled = true;

        setTimeout(() => {
          const result = this.generateViralScript(topic, niche, format);
          const resultEl = document.getElementById('generatedScriptOutput');
          if (resultEl) {
            resultEl.textContent = result;
          }
          genScriptBtn.innerHTML = '✨ Generar Guion Viral';
          genScriptBtn.disabled = false;
          this.app.showToast('¡Guion y prompts de alta retención generados!', 'success');
        }, 600);
      });
    }

    // Copy Prompt Button
    const copyBtn = document.getElementById('copyScriptOutputBtn');
    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        const text = document.getElementById('generatedScriptOutput')?.textContent;
        if (text) {
          navigator.clipboard.writeText(text);
          this.app.showToast('Copiado al portapapeles', 'info');
        }
      });
    }
  }
}
