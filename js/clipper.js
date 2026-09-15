/**
 * OMNIVIRAL STUDIO AI - AUTO-CLIPPER & REPURPOSER ENGINE
 * Waveform audio analysis, viral hook detector & MrBeast style karaoke subtitles
 */

export class ClipperManager {
  constructor(app) {
    this.app = app;
    this.isPlaying = false;
    this.currentTime = 12.4;
    this.duration = 45.0;
    this.playInterval = null;

    // Subtitle sequence (word-level timestamps for karaoke effect)
    this.subtitles = [
      { start: 0.0, end: 3.2, text: "EL SECRETO QUE", highlight: "NADIE TE DICE", emoji: "🤫" },
      { start: 3.2, end: 7.5, text: "SOBRE EL ALGORITMO", highlight: "DE TIKTOK EN 2026", emoji: "🔥" },
      { start: 7.5, end: 12.0, text: "LAS VISITAS YA NO", highlight: "SON LA MÉTRICA CLAVE", emoji: "❌" },
      { start: 12.0, end: 16.8, text: "LO QUE REALMENTE IMPORTA", highlight: "SON LOS SHARES POR DM", emoji: "🚀" },
      { start: 16.8, end: 22.0, text: "SI CADA PERSONA COMPARTE", highlight: "TU VIDEO A 3 AMIGOS", emoji: "📈" },
      { start: 22.0, end: 28.5, text: "EL ALGORITMO TE IMPULSA", highlight: "A MILLONES DE PERSONAS", emoji: "🤯" }
    ];

    this.candidateClips = [
      {
        id: 'clip-1',
        title: 'El Secreto de los Shares por DM en TikTok',
        hookQuote: '"Las visitas ya no importan, si no logras que lo compartan en privado estás muerto..."',
        startTime: '00:12',
        endTime: '00:48',
        durationSec: 36,
        viralScore: 98,
        retentionPrediction: '88% completion rate',
        tags: ['#TikTokGrowth', '#ViralTips', '#Algoritmo2026']
      },
      {
        id: 'clip-2',
        title: 'Por qué el 95% de los creadores fracasan antes de monetizar',
        hookQuote: '"No es falta de talento, es que publican en las horas equivocadas..."',
        startTime: '01:15',
        endTime: '01:52',
        durationSec: 37,
        viralScore: 94,
        retentionPrediction: '81% completion rate',
        tags: ['#Monetizacion', '#YouTubeShorts', '#Consejos']
      },
      {
        id: 'clip-3',
        title: 'Clonación de Voz: La verdad sobre los derechos de autor',
        hookQuote: '"Si no tienes este certificado, te pueden desmonetizar tu canal entero..."',
        startTime: '03:40',
        endTime: '04:22',
        durationSec: 42,
        viralScore: 91,
        retentionPrediction: '76% completion rate',
        tags: ['#VoiceAI', '#DerechosDeAutor', '#Creadores']
      }
    ];

    this.activeClip = this.candidateClips[0];
    this.init();
  }

  init() {
    this.renderClipsList();
    this.drawWaveform();
    this.bindEvents();
  }

  drawWaveform() {
    const canvas = document.getElementById('waveformCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width = canvas.parentElement.clientWidth;
    const h = canvas.height = canvas.parentElement.clientHeight;

    ctx.clearRect(0, 0, w, h);

    const bars = 80;
    const barWidth = w / bars;

    for (let i = 0; i < bars; i++) {
      // Procedural audio amplitude simulation with viral peaks
      const progress = i / bars;
      let amp = Math.sin(i * 0.28) * 0.35 + Math.cos(i * 0.15) * 0.25 + 0.4;
      
      // Add deliberate high energy peaks around viral highlights
      if ((i > 18 && i < 35) || (i > 50 && i < 68)) {
        amp += 0.32;
      }
      amp = Math.min(1.0, Math.max(0.12, amp));

      const barH = amp * (h - 12);
      const x = i * barWidth;
      const y = (h - barH) / 2;

      // Color bars based on energy
      if (amp > 0.7) {
        ctx.fillStyle = '#06b6d4'; // Peak viral
      } else if (amp > 0.45) {
        ctx.fillStyle = '#6366f1';
      } else {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
      }

      ctx.fillRect(x + 1, y, barWidth - 2, barH);
    }
  }

  renderClipsList() {
    const container = document.getElementById('clipsListContainer');
    if (!container) return;

    container.innerHTML = this.candidateClips.map((clip, idx) => `
      <div class="clip-candidate-card ${clip.id === this.activeClip.id ? 'active' : ''}" data-clip-id="${clip.id}">
        <div class="clip-card-header">
          <span class="viral-score-tag high">🔥 ${clip.viralScore}% VIRAL</span>
          <span class="clip-timestamp-badge">⏱️ ${clip.startTime} - ${clip.endTime} (${clip.durationSec}s)</span>
        </div>
        <h4 class="clip-title-preview">${clip.title}</h4>
        <p class="clip-hook-quote">${clip.hookQuote}</p>
        <div class="clip-bottom-actions">
          <button class="btn btn-sm btn-cyber preview-clip-btn" data-clip-id="${clip.id}">
            ▶️ Previsualizar
          </button>
          <button class="btn btn-sm btn-ghost plan-clip-btn" data-clip-id="${clip.id}">
            📅 Programar Post
          </button>
        </div>
      </div>
    `).join('');
  }

  selectClip(clipId) {
    const clip = this.candidateClips.find(c => c.id === clipId);
    if (!clip) return;
    this.activeClip = clip;
    this.renderClipsList();
    this.updateActiveSubtitle();
    this.app.showToast(`Cargando clip: "${clip.title}"`, 'info');
  }

  togglePlayback() {
    this.isPlaying = !this.isPlaying;
    const playBtn = document.getElementById('playPauseClipBtn');

    if (this.isPlaying) {
      if (playBtn) playBtn.innerHTML = '⏸️ Pausar';
      this.playInterval = setInterval(() => {
        this.currentTime += 0.2;
        if (this.currentTime >= this.duration) {
          this.currentTime = 0;
        }
        this.updatePlayerProgress();
      }, 200);
    } else {
      if (playBtn) playBtn.innerHTML = '▶️ Reproducir';
      clearInterval(this.playInterval);
    }
  }

  updatePlayerProgress() {
    const timeDisplay = document.getElementById('clipCurrentTimeDisplay');
    const marker = document.getElementById('waveformMarker');

    if (timeDisplay) {
      const mins = Math.floor(this.currentTime / 60);
      const secs = Math.floor(this.currentTime % 60);
      timeDisplay.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    if (marker) {
      const pct = (this.currentTime / this.duration) * 100;
      marker.style.left = `${pct}%`;
    }

    this.updateActiveSubtitle();
  }

  updateActiveSubtitle() {
    const subContainer = document.getElementById('karaokeSubtitlesBox');
    if (!subContainer) return;

    // Find current active subtitle chunk based on currentTime
    const currentSub = this.subtitles.find(s => this.currentTime >= s.start && this.currentTime < s.end) || this.subtitles[0];

    subContainer.innerHTML = `
      <div class="karaoke-text">
        <span>${currentSub.text}</span>
        <span class="karaoke-highlight">${currentSub.highlight}</span>
        <span class="karaoke-emoji">${currentSub.emoji}</span>
      </div>
    `;
  }

  bindEvents() {
    const playBtn = document.getElementById('playPauseClipBtn');
    if (playBtn) {
      playBtn.addEventListener('click', () => this.togglePlayback());
    }

    // Auto-Analyze Video Stream link / Upload Button
    const analyzeBtn = document.getElementById('startAutoClipBtn');
    if (analyzeBtn) {
      analyzeBtn.addEventListener('click', () => {
        analyzeBtn.innerHTML = '⚡ Analizando Picos de Viralidad...';
        analyzeBtn.disabled = true;

        setTimeout(() => {
          analyzeBtn.innerHTML = '⚡ Detectar Picos y Clips Virales';
          analyzeBtn.disabled = false;
          this.drawWaveform();
          this.app.showToast('¡3 clips de alta retención identificados con subtítulos dinámicos!', 'success');
        }, 1200);
      });
    }

    // Delegate clip list clicks
    const container = document.getElementById('clipsListContainer');
    if (container) {
      container.addEventListener('click', (e) => {
        const previewBtn = e.target.closest('.preview-clip-btn');
        const planBtn = e.target.closest('.plan-clip-btn');
        const card = e.target.closest('.clip-candidate-card');

        if (previewBtn) {
          this.selectClip(previewBtn.dataset.clipId);
          if (!this.isPlaying) this.togglePlayback();
        } else if (planBtn) {
          const clip = this.candidateClips.find(c => c.id === planBtn.dataset.clipId);
          if (clip) {
            this.app.router.switchTab('planner');
            this.app.planner.preparePostFromClip(clip);
          }
        } else if (card) {
          this.selectClip(card.dataset.clipId);
        }
      });
    }

    // Export current clip simulation
    const exportBtn = document.getElementById('exportClipBtn');
    if (exportBtn) {
      exportBtn.addEventListener('click', () => {
        this.app.showToast('Descargando clip vertical 9:16 con subtítulos karaoke incrustados (MP4)', 'success');
      });
    }
  }
}
