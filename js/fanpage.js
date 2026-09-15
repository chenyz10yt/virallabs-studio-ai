/**
 * VIRAL LABS - FANPAGE PUBLIC PORTAL & SYNCHRONIZER
 * Synchronizes in real time with Viral Labs Studio via Storage & BroadcastChannel
 */

class FanpageManager {
  constructor() {
    this.broadcastChannel = null;
    this.posts = [];
    this.isLive = false;
    this.comments = [
      { id: 1, author: 'Valeria Gómez', text: '¡Esperando con ansias el próximo tutorial de IA! Eres el mejor Alex 👏', time: 'Hace 10 min' },
      { id: 2, author: 'David Tech', text: 'Los clips que subes a TikTok me ayudaron a conseguir mis primeros 10k seguidores 🔥', time: 'Hace 35 min' },
      { id: 3, author: 'Camila Ríos', text: '¿A qué hora empieza el stream de hoy? Ya estoy lista en el chat 🎮', time: 'Hace 1 hora' }
    ];

    this.init();
  }

  init() {
    this.setupBroadcastSync();
    this.loadInitialData();
    this.renderPostsFeed();
    this.renderFanComments();
    this.bindEvents();
  }

  setupBroadcastSync() {
    // 1. BroadcastChannel API for multi-tab zero-delay sync
    if ('BroadcastChannel' in window) {
      this.broadcastChannel = new BroadcastChannel('virallabs_channel');
      this.broadcastChannel.onmessage = (event) => {
        if (event.data.type === 'STREAM_TOGGLE') {
          this.setLiveState(event.data.isLive);
        } else if (event.data.type === 'NEW_POST') {
          this.loadInitialData();
          this.renderPostsFeed();
        }
      };
    }

    // 2. Fallback to localStorage 'storage' event across tabs
    window.addEventListener('storage', (e) => {
      if (e.key === 'omniviral_studio_data_v1') {
        this.loadInitialData();
        this.renderPostsFeed();
      } else if (e.key === 'virallabs_stream_live') {
        this.setLiveState(e.newValue === 'true');
      }
    });

    // Check if live state was already set
    const savedLive = localStorage.getItem('virallabs_stream_live') === 'true';
    this.setLiveState(savedLive);
  }

  loadInitialData() {
    try {
      const raw = localStorage.getItem('omniviral_studio_data_v1');
      if (raw) {
        const data = JSON.parse(raw);
        this.posts = data.scheduledPosts || [];
      }
    } catch (e) {
      console.warn('Error loading fanpage data', e);
    }
  }

  setLiveState(isLive) {
    this.isLive = isLive;
    const liveCard = document.getElementById('fanpageLiveCard');
    const navLiveBadge = document.getElementById('fanpageNavLiveBadge');

    if (liveCard) {
      liveCard.classList.toggle('active-live', isLive);
    }
    if (navLiveBadge) {
      navLiveBadge.style.display = isLive ? 'inline-flex' : 'none';
    }
  }

  renderPostsFeed() {
    const feed = document.getElementById('communityPostsFeed');
    if (!feed) return;

    if (this.posts.length === 0) {
      feed.innerHTML = '<div style="padding:24px; text-align:center; color:var(--text-muted);">No hay publicaciones activas por el momento.</div>';
      return;
    }

    feed.innerHTML = this.posts.map(post => `
      <article class="post-card-fan">
        <div class="post-card-head">
          <div class="post-card-author">
            <div class="post-avatar-mini">AR</div>
            <div>
              <div style="font-weight:700; font-size:0.95rem; color:#fff;">Alex Rivera <span style="color:#06b6d4;">✓</span></div>
              <div style="font-size:0.75rem; color:var(--text-muted);">${post.date} • Publicado vía Viral Labs</div>
            </div>
          </div>
          <div style="display:flex; gap:6px;">
            ${post.platforms.map(plat => `<span class="badge badge-purple">${plat.toUpperCase()}</span>`).join('')}
          </div>
        </div>

        <p class="post-body-text">${post.caption || post.title}</p>

        <div class="post-media-wrap">
          <img src="${post.thumbnail || 'assets/thumbnail_demo.jpg'}" alt="${post.title}">
        </div>

        <div class="post-actions-bar">
          <button class="post-like-btn" onclick="this.classList.toggle('liked')">
            <span>❤️</span> <span>Me gusta</span>
          </button>
          <button class="post-like-btn">
            <span>💬</span> <span>Comentarios</span>
          </button>
          <button class="post-like-btn" onclick="navigator.clipboard.writeText(window.location.href); alert('Enlace copiado al portapapeles');">
            <span>↗️</span> <span>Compartir</span>
          </button>
        </div>
      </article>
    `).join('');
  }

  renderFanComments() {
    const list = document.getElementById('fanCommentsList');
    if (!list) return;

    list.innerHTML = this.comments.map(c => `
      <div style="padding:10px 14px; background:rgba(255,255,255,0.03); border-radius:var(--radius-xs); border:1px solid rgba(255,255,255,0.05); margin-bottom:8px;">
        <div style="display:flex; justify-content:space-between; font-size:0.76rem; margin-bottom:4px;">
          <strong style="color:#67e8f9;">${c.author}</strong>
          <span style="color:var(--text-muted);">${c.time}</span>
        </div>
        <div style="font-size:0.82rem; color:#cbd5e1;">${c.text}</div>
      </div>
    `).join('');
  }

  addComment(author, text) {
    if (!text || text.trim() === '') return;
    this.comments.unshift({
      id: Date.now(),
      author: author || 'Fan Seguidor',
      text: text.trim(),
      time: 'Justo ahora'
    });
    this.renderFanComments();
  }

  bindEvents() {
    const commentInput = document.getElementById('fanCommentInput');
    const sendBtn = document.getElementById('sendFanCommentBtn');

    if (sendBtn && commentInput) {
      sendBtn.addEventListener('click', () => {
        this.addComment('Tú (Comunidad)', commentInput.value);
        commentInput.value = '';
      });
      commentInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.addComment('Tú (Comunidad)', commentInput.value);
          commentInput.value = '';
        }
      });
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.ViralLabsFanpage = new FanpageManager();
});
