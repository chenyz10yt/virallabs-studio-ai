/**
 * OMNIVIRAL STUDIO AI - MAIN APPLICATION CORE & ROUTER
 */

import { StorageManager } from './storage.js';
import { StudioManager } from './studio.js';
import { ClipperManager } from './clipper.js';
import { MultistreamManager } from './multistream.js';
import { VoiceLabManager } from './voicelab.js';
import { PlannerManager } from './planner.js';
import { RadarManager } from './radar.js';

class OmniViralApp {
  constructor() {
    this.activeTab = 'dashboard';
    this.storage = StorageManager;
    this.init();
  }

  init() {
    // Initialize Submodules
    this.studio = new StudioManager(this);
    this.clipper = new ClipperManager(this);
    this.multistream = new MultistreamManager(this);
    this.voicelab = new VoiceLabManager(this);
    this.planner = new PlannerManager(this);
    this.radar = new RadarManager(this);

    this.setupNavigation();
    this.setupHeaderActions();
    this.renderDashboardMetrics();

    // Check URL hash for direct tab linking
    const initialHash = window.location.hash.replace('#', '');
    if (initialHash && document.getElementById(`pane-${initialHash}`)) {
      this.switchTab(initialHash);
    }
  }

  setupNavigation() {
    document.querySelectorAll('.nav-item').forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const tab = item.dataset.tab;
        if (tab) this.switchTab(tab);
      });
    });

    // Quick action cards in dashboard
    document.querySelectorAll('.action-card').forEach(card => {
      card.addEventListener('click', (e) => {
        e.preventDefault();
        const targetTab = card.dataset.tab;
        if (targetTab) this.switchTab(targetTab);
      });
    });
  }

  switchTab(tabName) {
    this.activeTab = tabName;
    window.location.hash = tabName;

    // Update nav active states
    document.querySelectorAll('.nav-item').forEach(item => {
      item.classList.toggle('active', item.dataset.tab === tabName);
    });

    // Update panes
    document.querySelectorAll('.content-pane').forEach(pane => {
      pane.classList.remove('active');
    });

    const targetPane = document.getElementById(`pane-${tabName}`);
    if (targetPane) {
      targetPane.classList.add('active');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Refresh canvas or player if needed
    if (tabName === 'studio' && this.studio) {
      setTimeout(() => this.studio.renderCanvas(), 50);
    } else if (tabName === 'clipper' && this.clipper) {
      setTimeout(() => this.clipper.drawWaveform(), 50);
    } else if (tabName === 'planner' && this.planner) {
      setTimeout(() => this.planner.renderCalendar(), 50);
    }
  }

  renderDashboardMetrics() {
    const data = StorageManager.getData();
    const postsCount = data.scheduledPosts.length;
    const countEl = document.getElementById('dashScheduledCount');
    if (countEl) countEl.textContent = postsCount;
  }

  setupHeaderActions() {
    // Platform quick connection pills in header
    document.querySelectorAll('.platform-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        const platform = pill.dataset.platform;
        const isConnected = pill.classList.toggle('connected');
        StorageManager.updatePlatformStatus(platform, isConnected);
        this.showToast(`${platform.toUpperCase()} ${isConnected ? 'Conectado' : 'Desconectado'}`, 'info');
        if (this.multistream) this.multistream.renderPlatformsMatrix();
      });
    });

    // RTMP Settings Modal
    const settingsBtn = document.getElementById('openSettingsBtn');
    const modal = document.getElementById('rtmpModal');
    const closeBtn = document.getElementById('closeModalBtn');
    const saveRtmpBtn = document.getElementById('saveRtmpSettingsBtn');

    if (settingsBtn && modal) {
      settingsBtn.addEventListener('click', () => modal.classList.add('active'));
    }
    if (closeBtn && modal) {
      closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    }
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('active');
      });
    }
    if (saveRtmpBtn && modal) {
      saveRtmpBtn.addEventListener('click', () => {
        modal.classList.remove('active');
        this.showToast('Configuración RTMP y claves de transmisión guardadas.', 'success');
      });
    }
  }

  showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? '✅' : type === 'warning' ? '⚠️' : 'ℹ️';
    toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.animation = 'toastOut 0.3s forwards';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }
}

// Instantiate on DOM load
document.addEventListener('DOMContentLoaded', () => {
  window.OmniViral = new OmniViralApp();
});
