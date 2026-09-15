/**
 * OMNIVIRAL STUDIO AI - MULTISTREAM BROADCAST & LIVE TELEMETRY MODULE
 * Multi-platform RTMP distribution, camera/screen switching, dynamic VU meters & unified chat
 */

import { StorageManager } from './storage.js';

export class MultistreamManager {
  constructor(app) {
    this.app = app;
    this.isLive = false;
    this.currentSource = 'studio'; // 'webcam', 'screen', 'studio'
    this.mediaStream = null;
    this.telemetryInterval = null;
    this.vuInterval = null;
    this.chatInterval = null;

    this.platforms = {
      youtube: true,
      tiktok: true,
      facebook: false,
      twitch: true,
      kick: false,
      twitter: false
    };

    this.mockChatMessages = [
      { id: 1, platform: 'yt', user: 'TechVibe_99', text: '¡Saludos desde México! ¿Qué cámara usas para el multistream?', isQuestion: true, pinned: false },
      { id: 2, platform: 'tt', user: 'sofia.creativity', text: 'Increíble la calidad del stream bro 🔥🔥🔥', isQuestion: false, pinned: false },
      { id: 3, platform: 'tw', user: 'GamerZero_X', text: '¿Cuántos Mbps de bitrate recomiendas para transmitir a TikTok y YouTube a la vez?', isQuestion: true, pinned: false },
      { id: 4, platform: 'fb', user: 'Carlos Mendoza', text: 'Excelente contenido como siempre Alex, compartido en mi grupo!', isQuestion: false, pinned: false },
      { id: 5, platform: 'tt', user: 'daniela_ia', text: 'OMG la voz clonada suena 100% natural, no parece robot 😱', isQuestion: false, pinned: false }
    ];

    this.init();
  }

  init() {
    this.renderPlatformsMatrix();
    this.renderChatMessages();
    this.startAudioVUMeter();
    this.bindEvents();
  }

  renderPlatformsMatrix() {
    const container = document.getElementById('platformsStreamMatrix');
    if (!container) return;

    const meta = {
      youtube: { name: 'YouTube Live', class: 'yt', label: 'YT' },
      tiktok: { name: 'TikTok Live', class: 'tt', label: 'TT' },
      facebook: { name: 'Facebook Live', class: 'fb', label: 'FB' },
      twitch: { name: 'Twitch TV', class: 'tw', label: 'TW' },
      kick: { name: 'Kick Streaming', class: 'kc', label: 'KC' },
      twitter: { name: 'X / Twitter Live', class: 'xx', label: 'X' }
    };

    container.innerHTML = Object.entries(this.platforms).map(([key, isConnected]) => `
      <div class="platform-card-stream ${isConnected ? 'connected' : ''}" data-platform="${key}">
        <div class="platform-info-tag">
          <div class="platform-icon-circle ${meta[key].class}">${meta[key].label}</div>
          <div>
            <div style="font-size:0.84rem; font-weight:700; color:#fff;">${meta[key].name}</div>
            <div style="font-size:0.7rem; color:${isConnected ? '#6ee7b7' : '#94a3b8'};">
              ${isConnected ? '● Enlazado (Listo)' : '○ Desconectado'}
            </div>
          </div>
        </div>
        <label class="toggle-switch">
          <input type="checkbox" class="platform-stream-toggle" data-platform="${key}" ${isConnected ? 'checked' : ''}>
          <span class="toggle-slider"></span>
        </label>
      </div>
    `).join('');
  }

  toggleLiveBroadcast() {
    this.isLive = !this.isLive;
    const liveBtn = document.getElementById('toggleBroadcastBtn');
    const onAirBadge = document.getElementById('broadcastOnAirBadge');

    if (this.isLive) {
      if (liveBtn) {
        liveBtn.innerHTML = '🛑 DETENER MULTITRANSMISIÓN';
        liveBtn.classList.remove('btn-primary');
        liveBtn.classList.add('btn-danger');
      }
      if (onAirBadge) onAirBadge.style.display = 'flex';

      this.startTelemetry();
      this.startSimulatedChat();
      this.app.showToast('🚀 ¡Transmisión en vivo iniciada simultáneamente en plataformas activas!', 'success');
    } else {
      if (liveBtn) {
        liveBtn.innerHTML = '🔴 INICIAR MULTITRANSMISIÓN EN VIVO';
        liveBtn.classList.remove('btn-danger');
        liveBtn.classList.add('btn-primary');
      }
      if (onAirBadge) onAirBadge.style.display = 'none';

      clearInterval(this.telemetryInterval);
      clearInterval(this.chatInterval);
      this.app.showToast('Transmisión finalizada con éxito. Guardando estadísticas.', 'info');
    }
  }

  startTelemetry() {
    this.telemetryInterval = setInterval(() => {
      // Simulate realistic fluctuation in telemetry
      const baseBitrate = 6200;
      const jitter = Math.floor((Math.random() - 0.5) * 240);
      const bitrate = baseBitrate + jitter;

      const fpsVal = (59.8 + Math.random() * 0.4).toFixed(1);
      const cpuVal = (16 + Math.random() * 5).toFixed(0);

      const bitrateEl = document.getElementById('telemetryBitrate');
      const fpsEl = document.getElementById('telemetryFps');
      const cpuEl = document.getElementById('telemetryCpu');

      if (bitrateEl) bitrateEl.textContent = `${bitrate} kbps`;
      if (fpsEl) fpsEl.textContent = `${fpsVal} FPS`;
      if (cpuEl) cpuEl.textContent = `${cpuVal}%`;
    }, 1000);
  }

  startAudioVUMeter() {
    const leftBar = document.getElementById('vuChannelLeft');
    const rightBar = document.getElementById('vuChannelRight');

    this.vuInterval = setInterval(() => {
      if (this.isLive) {
        const leftVal = 40 + Math.random() * 48;
        const rightVal = 38 + Math.random() * 52;
        if (leftBar) leftBar.style.width = `${leftVal}%`;
        if (rightBar) rightBar.style.width = `${rightVal}%`;
      } else {
        if (leftBar) leftBar.style.width = '12%';
        if (rightBar) rightBar.style.width = '10%';
      }
    }, 120);
  }

  async switchSource(sourceType) {
    this.currentSource = sourceType;
    const videoFeed = document.getElementById('broadcastMainVideo');

    if (sourceType === 'webcam') {
      try {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          this.mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
          if (videoFeed) {
            videoFeed.srcObject = this.mediaStream;
            videoFeed.play();
          }
          this.app.showToast('Fuente cambiada a Cámara Web en vivo', 'success');
          return;
        }
      } catch (err) {
        console.warn('Webcam permission denied or not available, keeping simulated backdrop', err);
        this.app.showToast('Modo cámara en vivo simulado', 'info');
      }
    } else if (sourceType === 'screen') {
      try {
        if (navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia) {
          this.mediaStream = await navigator.mediaDevices.getDisplayMedia({ video: true });
          if (videoFeed) {
            videoFeed.srcObject = this.mediaStream;
            videoFeed.play();
          }
          this.app.showToast('Compartiendo pantalla en vivo', 'success');
          return;
        }
      } catch (err) {
        console.warn('Screen share cancelled, using default scene', err);
      }
    }

    // Default or Fallback to Studio Scene Asset
    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach(t => t.stop());
      this.mediaStream = null;
    }
    if (videoFeed) {
      videoFeed.srcObject = null;
      videoFeed.src = 'assets/thumbnail_demo.jpg';
    }
    this.app.showToast('Fuente conmutada a Escena de Estudio Principal', 'info');
  }

  renderChatMessages() {
    const container = document.getElementById('unifiedChatContainer');
    if (!container) return;

    container.innerHTML = this.mockChatMessages.map(msg => `
      <div class="chat-msg-item ${msg.pinned ? 'pinned' : ''}" data-msg-id="${msg.id}">
        <span class="chat-badge ${msg.platform}">${msg.platform}</span>
        <div style="flex:1;">
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <span class="chat-author">${msg.user}</span>
            <button class="btn btn-ghost btn-sm pin-chat-btn" data-msg-id="${msg.id}" style="padding:2px 6px; font-size:0.68rem;">
              ${msg.pinned ? '📌 Fijado' : 'Pin'}
            </button>
          </div>
          <p class="chat-body-text">${msg.text}</p>
        </div>
      </div>
    `).join('');

    // Auto-scroll to bottom
    container.scrollTop = container.scrollHeight;
  }

  startSimulatedChat() {
    const randomComments = [
      { platform: 'yt', user: 'CreatorPro_2026', text: '¡Esa función de auto-clipper está brutal!' },
      { platform: 'tt', user: 'lucas_viral', text: 'Subiendo ahora mismo un video con tu estrategia 🔥' },
      { platform: 'tw', user: 'Elena_Streams', text: '¿Haces streams todos los días a esta hora?' },
      { platform: 'fb', user: 'Manuel Rivera', text: 'Saludos desde España amigo, gran trabajo.' },
      { platform: 'tt', user: 'neon_byte', text: 'La resolución se ve a 60fps súper fluida ⚡' }
    ];

    let idx = 0;
    this.chatInterval = setInterval(() => {
      if (idx < randomComments.length) {
        const comment = randomComments[idx++];
        this.mockChatMessages.push({
          id: Date.now(),
          platform: comment.platform,
          user: comment.user,
          text: comment.text,
          isQuestion: comment.text.includes('?'),
          pinned: false
        });
        this.renderChatMessages();
      }
    }, 4500);
  }

  bindEvents() {
    const liveBtn = document.getElementById('toggleBroadcastBtn');
    if (liveBtn) {
      liveBtn.addEventListener('click', () => this.toggleLiveBroadcast());
    }

    // Source buttons
    document.querySelectorAll('.source-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.source-btn').forEach(b => b.classList.remove('btn-primary'));
        const target = e.currentTarget;
        target.classList.add('btn-primary');
        this.switchSource(target.dataset.source);
      });
    });

    // Platform Stream Key Toggles
    const matrix = document.getElementById('platformsStreamMatrix');
    if (matrix) {
      matrix.addEventListener('change', (e) => {
        if (e.target.classList.contains('platform-stream-toggle')) {
          const platform = e.target.dataset.platform;
          this.platforms[platform] = e.target.checked;
          StorageManager.updatePlatformStatus(platform, e.target.checked);
          this.renderPlatformsMatrix();
          this.app.showToast(`${platform.toUpperCase()} ${e.target.checked ? 'activado' : 'desactivado'} para transmisión`, 'info');
        }
      });
    }

    // Send Chat Message
    const chatInput = document.getElementById('chatUserInput');
    const sendChatBtn = document.getElementById('sendChatMsgBtn');

    const handleSend = () => {
      const text = chatInput?.value?.trim();
      if (text) {
        this.mockChatMessages.push({
          id: Date.now(),
          platform: 'yt',
          user: 'Alex Rivera (Tú)',
          text: text,
          isQuestion: false,
          pinned: false
        });
        chatInput.value = '';
        this.renderChatMessages();
      }
    };

    if (sendChatBtn) sendChatBtn.addEventListener('click', handleSend);
    if (chatInput) {
      chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
      });
    }

    // Delegate Pin Chat Message
    const chatContainer = document.getElementById('unifiedChatContainer');
    if (chatContainer) {
      chatContainer.addEventListener('click', (e) => {
        const pinBtn = e.target.closest('.pin-chat-btn');
        if (pinBtn) {
          const id = parseInt(pinBtn.dataset.msgId);
          const msg = this.mockChatMessages.find(m => m.id === id);
          if (msg) {
            msg.pinned = !msg.pinned;
            this.renderChatMessages();

            // Also show pinned banner on lower third overlay
            const overlayH4 = document.getElementById('lowerThirdH4');
            const overlayP = document.getElementById('lowerThirdP');
            if (msg.pinned && overlayH4 && overlayP) {
              overlayH4.textContent = `💬 Pregunta de ${msg.user} (${msg.platform.toUpperCase()}):`;
              overlayP.textContent = `"${msg.text}"`;
              this.app.showToast('Pregunta fijada en la pantalla de transmisión en vivo', 'success');
            }
          }
        }
      });
    }
  }
}
