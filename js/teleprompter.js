/**
 * VIRAL LABS - TELEPROMPTER PRO MODULE
 * Floating prompter with auto-scroll, physical beam-splitter mirror mode,
 * WPM speed control, font scaler and direct AI script importer.
 */

export class TeleprompterPro {
  constructor(app) {
    this.app = app;
    this.container = null;
    this.scrollArea = null;
    this.contentEl = null;
    this.isPlaying = false;
    this.speedWpm = 140; // Default words per minute
    this.fontSize = 28; // Default font size in px
    this.isMirrored = false;
    this.isExpanded = false;
    this.scrollPos = 0;
    this.animationFrameId = null;
    this.lastTimestamp = null;

    this.defaultScript = `¡Bienvenidos a Viral Labs! 🚀\n\nEn este video te revelo el secreto que los creadores de más de 1 millón de suscriptores usan para dominar el algoritmo en 2026.\n\nEl 95% de los creadores cometen el error de enfocarse únicamente en las vistas. Pero la verdadera métrica clave es la tasa de retención en los primeros 3 segundos y el ratio de compartidos por mensaje directo.\n\nQuédate hasta el final porque te mostraré paso a paso cómo estructurar tu gancho viral para multiplicar tu alcance por 10x.\n\n¡Dale like, suscríbete y activa la campana para no perderte las próximas estrategias!`;

    this.init();
  }

  init() {
    this.container = document.getElementById('teleprompterDock');
    if (!this.container) return;

    this.scrollArea = document.getElementById('prompterScrollArea');
    this.contentEl = document.getElementById('prompterTextContent');

    if (this.contentEl && !this.contentEl.value) {
      this.contentEl.value = this.defaultScript;
    }

    this.bindEvents();
    this.updateStyle();
  }

  bindEvents() {
    // Controls
    const playBtn = document.getElementById('prompterPlayBtn');
    const resetBtn = document.getElementById('prompterResetBtn');
    const mirrorBtn = document.getElementById('prompterMirrorBtn');
    const expandBtn = document.getElementById('prompterExpandBtn');
    const closeBtn = document.getElementById('prompterCloseBtn');
    const speedSlider = document.getElementById('prompterSpeedSlider');
    const fontSlider = document.getElementById('prompterFontSlider');
    const importScriptBtn = document.getElementById('prompterImportScriptBtn');
    const openPrompterNavBtn = document.getElementById('openPrompterBtn');

    if (playBtn) {
      playBtn.addEventListener('click', () => this.togglePlay());
    }
    if (resetBtn) {
      resetBtn.addEventListener('click', () => this.resetScroll());
    }
    if (mirrorBtn) {
      mirrorBtn.addEventListener('click', () => this.toggleMirror());
    }
    if (expandBtn) {
      expandBtn.addEventListener('click', () => this.toggleExpand());
    }
    if (closeBtn) {
      closeBtn.addEventListener('click', () => this.hide());
    }
    if (openPrompterNavBtn) {
      openPrompterNavBtn.addEventListener('click', (e) => {
        e.preventDefault();
        this.show();
      });
    }

    if (speedSlider) {
      speedSlider.addEventListener('input', (e) => {
        this.speedWpm = parseInt(e.target.value, 10);
        const label = document.getElementById('prompterSpeedVal');
        if (label) label.textContent = `${this.speedWpm} WPM`;
      });
    }

    if (fontSlider) {
      fontSlider.addEventListener('input', (e) => {
        this.fontSize = parseInt(e.target.value, 10);
        this.updateStyle();
        const label = document.getElementById('prompterFontVal');
        if (label) label.textContent = `${this.fontSize}px`;
      });
    }

    if (importScriptBtn) {
      importScriptBtn.addEventListener('click', () => this.importScriptFromStudio());
    }

    // Keyboard Hotkeys when Teleprompter is visible
    window.addEventListener('keydown', (e) => {
      if (!this.container || !this.container.classList.contains('active')) return;
      // Don't trigger if user is actively typing in the textarea
      if (document.activeElement === this.contentEl) return;

      if (e.code === 'Space') {
        e.preventDefault();
        this.togglePlay();
      } else if (e.code === 'ArrowUp') {
        e.preventDefault();
        this.adjustSpeed(10);
      } else if (e.code === 'ArrowDown') {
        e.preventDefault();
        this.adjustSpeed(-10);
      } else if (e.key === 'r' || e.key === 'R') {
        this.resetScroll();
      } else if (e.key === 'm' || e.key === 'M') {
        this.toggleMirror();
      }
    });

    // Make floating header draggable
    const header = document.getElementById('prompterHeader');
    if (header) {
      let isDragging = false;
      let startX, startY, initialLeft, initialTop;

      header.addEventListener('mousedown', (e) => {
        if (e.target.tagName === 'BUTTON' || e.target.closest('button')) return;
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        const rect = this.container.getBoundingClientRect();
        initialLeft = rect.left;
        initialTop = rect.top;
        this.container.style.bottom = 'auto';
        this.container.style.right = 'auto';
        this.container.style.left = `${initialLeft}px`;
        this.container.style.top = `${initialTop}px`;
      });

      window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        this.container.style.left = `${Math.max(10, Math.min(window.innerWidth - 300, initialLeft + dx))}px`;
        this.container.style.top = `${Math.max(10, Math.min(window.innerHeight - 200, initialTop + dy))}px`;
      });

      window.addEventListener('mouseup', () => {
        isDragging = false;
      });
    }
  }

  show() {
    if (!this.container) return;
    this.container.classList.add('active');
    this.app.showToast('Teleprompter Pro activado. Usa [Espacio] para pausar/reanudar.', 'info');
  }

  hide() {
    if (!this.container) return;
    this.pause();
    this.container.classList.remove('active');
  }

  togglePlay() {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.play();
    }
  }

  play() {
    this.isPlaying = true;
    const playBtn = document.getElementById('prompterPlayBtn');
    if (playBtn) playBtn.innerHTML = '⏸️ Pausar';
    this.lastTimestamp = performance.now();
    this.scrollLoop();
  }

  pause() {
    this.isPlaying = false;
    const playBtn = document.getElementById('prompterPlayBtn');
    if (playBtn) playBtn.innerHTML = '▶️ Iniciar';
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }

  resetScroll() {
    this.pause();
    this.scrollPos = 0;
    if (this.scrollArea) {
      this.scrollArea.scrollTop = 0;
    }
    this.app.showToast('Teleprompter reiniciado al inicio.', 'info');
  }

  toggleMirror() {
    this.isMirrored = !this.isMirrored;
    const mirrorBtn = document.getElementById('prompterMirrorBtn');
    if (mirrorBtn) {
      mirrorBtn.classList.toggle('active', this.isMirrored);
    }
    this.updateStyle();
    this.app.showToast(this.isMirrored ? 'Modo Espejo Reflejado Activado (Para Cristal Físico)' : 'Modo Espejo Desactivado', 'info');
  }

  toggleExpand() {
    this.isExpanded = !this.isExpanded;
    this.container.classList.toggle('expanded', this.isExpanded);
    const expandBtn = document.getElementById('prompterExpandBtn');
    if (expandBtn) {
      expandBtn.innerHTML = this.isExpanded ? '🗗 Reducir' : '🗖 Expandir';
    }
  }

  adjustSpeed(delta) {
    this.speedWpm = Math.max(60, Math.min(320, this.speedWpm + delta));
    const slider = document.getElementById('prompterSpeedSlider');
    const label = document.getElementById('prompterSpeedVal');
    if (slider) slider.value = this.speedWpm;
    if (label) label.textContent = `${this.speedWpm} WPM`;
  }

  updateStyle() {
    if (this.scrollArea) {
      this.scrollArea.style.transform = this.isMirrored ? 'scaleX(-1)' : 'none';
    }
    if (this.contentEl) {
      this.contentEl.style.fontSize = `${this.fontSize}px`;
      this.contentEl.style.lineHeight = '1.7';
    }
  }

  scrollLoop() {
    if (!this.isPlaying) return;

    const now = performance.now();
    const dt = (now - this.lastTimestamp) / 1000;
    this.lastTimestamp = now;

    // Convert WPM to approximate vertical pixels per second
    // ~140 WPM is approx 45px/sec at 28px font size
    const pxPerSec = (this.speedWpm / 140) * 48 * (this.fontSize / 28);
    this.scrollPos += pxPerSec * dt;

    if (this.scrollArea) {
      this.scrollArea.scrollTop = this.scrollPos;

      // Check if reached bottom
      if (this.scrollArea.scrollTop + this.scrollArea.clientHeight >= this.scrollArea.scrollHeight - 10) {
        this.pause();
        this.app.showToast('Fin de la lectura del Teleprompter completado.', 'success');
        return;
      }
    }

    this.animationFrameId = requestAnimationFrame(() => this.scrollLoop());
  }

  importScriptFromStudio() {
    const scriptBox = document.getElementById('scriptOutput');
    if (scriptBox && scriptBox.textContent.trim()) {
      const text = scriptBox.textContent.trim();
      if (this.contentEl) {
        this.contentEl.value = text;
        this.resetScroll();
        this.show();
        this.app.showToast('Guión importado exitosamente al Teleprompter Pro.', 'success');
      }
    } else {
      this.app.showToast('Primero genera un guión en el AI Studio para importarlo.', 'warning');
    }
  }
}
