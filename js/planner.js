/**
 * OMNIVIRAL STUDIO AI - CONTENT PLANNER & SMART SCHEDULER MODULE
 * Content calendar, algorithm peak posting heatmap, multi-publish queue & phone mockups
 */

import { StorageManager } from './storage.js';

export class PlannerManager {
  constructor(app) {
    this.app = app;
    this.activeMockupPlatform = 'tiktok';
    this.currentMonth = 8; // September (0-indexed)
    this.currentYear = 2026;
    
    this.init();
  }

  init() {
    this.renderCalendar();
    this.renderMockup();
    this.bindEvents();
  }

  renderCalendar() {
    const grid = document.getElementById('calendarGridCells');
    const monthTitle = document.getElementById('calendarMonthTitle');
    if (!grid) return;

    if (monthTitle) {
      monthTitle.textContent = 'Septiembre 2026';
    }

    const data = StorageManager.getData();
    const posts = data.scheduledPosts || [];

    // September 2026 starts on Tuesday (day index 2) and has 30 days
    const firstDayIndex = 2; // 0=Sun, 1=Mon, 2=Tue...
    const totalDays = 30;

    let cellsHtml = '';

    // Empty cells before month start
    for (let i = 0; i < firstDayIndex; i++) {
      cellsHtml += `<div class="calendar-cell" style="opacity:0.25;"><span class="calendar-cell-date">${28 + i}</span></div>`;
    }

    // Days of current month
    for (let day = 1; day <= totalDays; day++) {
      const isToday = day === 14;
      const dayStr = `2026-09-${day.toString().padStart(2, '0')}`;
      const dayPosts = posts.filter(p => p.date === dayStr);

      const postBadges = dayPosts.map(p => {
        const pClass = p.platforms[0] || 'tt';
        return `
          <div class="calendar-post-badge ${pClass}" title="${p.title}">
            <span>${p.platforms.map(plat => plat.substring(0,2).toUpperCase()).join('•')}</span>
            <span>${p.title}</span>
          </div>
        `;
      }).join('');

      cellsHtml += `
        <div class="calendar-cell ${isToday ? 'today' : ''}" data-date="${dayStr}">
          <span class="calendar-cell-date">${day} ${isToday ? '(Hoy)' : ''}</span>
          ${postBadges}
        </div>
      `;
    }

    grid.innerHTML = cellsHtml;
  }

  preparePostFromClip(clip) {
    const titleInput = document.getElementById('newPostTitleInput');
    const captionInput = document.getElementById('newPostCaptionInput');

    if (titleInput) titleInput.value = clip.title;
    if (captionInput) {
      captionInput.value = `${clip.title} 🔥\n\n${clip.hookQuote}\n\n${clip.tags.join(' ')}`;
    }

    this.renderMockup();
    this.app.showToast('Clip importado al compositor de publicaciones.', 'info');
  }

  renderMockup() {
    const mockupContainer = document.getElementById('phoneMockupContainer');
    if (!mockupContainer) return;

    const title = document.getElementById('newPostTitleInput')?.value || '5 Herramientas de IA que reemplazan agencias enteras en 2026';
    const caption = document.getElementById('newPostCaptionInput')?.value || '🚀 Si no estás usando estas herramientas en 2026 estás perdiendo horas de trabajo. ¡Mira el video hasta el final!\n\n#IA #Creadores #Tecnologia';

    if (this.activeMockupPlatform === 'tiktok') {
      mockupContainer.innerHTML = `
        <div class="smartphone-device">
          <div class="dynamic-island"></div>
          <div class="phone-screen">
            <img src="assets/clip_demo.jpg" class="phone-media-bg" alt="TikTok Preview">
            <div class="tiktok-overlay-ui">
              <div class="tiktok-top-tabs">
                <span>Siguiendo</span>
                <span class="active">Para ti</span>
              </div>
              <div class="tiktok-bottom-area">
                <div class="tiktok-caption-group">
                  <div class="tiktok-creator-handle">@alexcreator.ai</div>
                  <div class="tiktok-caption-text">${caption}</div>
                  <div style="font-size:0.75rem; color:#fff; margin-top:4px; display:flex; align-items:center; gap:6px;">
                    <span>🎵 Sonido original - Alex Rivera • IA Hacks</span>
                  </div>
                </div>
                <div class="tiktok-right-actions">
                  <div class="tiktok-action-btn">
                    <div class="tiktok-icon-bubble" style="color:#fe0979;">❤️</div>
                    <span>142.5K</span>
                  </div>
                  <div class="tiktok-action-btn">
                    <div class="tiktok-icon-bubble">💬</div>
                    <span>1,890</span>
                  </div>
                  <div class="tiktok-action-btn">
                    <div class="tiktok-icon-bubble" style="color:#ffd000;">⭐</div>
                    <span>45.2K</span>
                  </div>
                  <div class="tiktok-action-btn">
                    <div class="tiktok-icon-bubble">↗️</div>
                    <span>28.4K</span>
                  </div>
                  <div class="tiktok-music-disk">
                    <div style="width:10px; height:10px; border-radius:50%; background:#fff;"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    } else if (this.activeMockupPlatform === 'instagram') {
      mockupContainer.innerHTML = `
        <div class="smartphone-device">
          <div class="dynamic-island"></div>
          <div class="phone-screen">
            <img src="assets/clip_demo.jpg" class="phone-media-bg" alt="Instagram Reel">
            <div class="tiktok-overlay-ui" style="justify-content:flex-end;">
              <div class="tiktok-bottom-area">
                <div class="tiktok-caption-group">
                  <div class="tiktok-creator-handle" style="display:flex; align-items:center; gap:6px;">
                    <span>alexcreator.ai</span>
                    <span style="font-size:0.7rem; border:1px solid #fff; border-radius:4px; padding:1px 4px;">Seguir</span>
                  </div>
                  <div class="tiktok-caption-text">${caption}</div>
                  <div style="font-size:0.75rem; color:#cbd5e1; margin-top:4px;">
                    Audio original • alexcreator.ai
                  </div>
                </div>
                <div class="tiktok-right-actions">
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">🤍</div><span>84.2K</span></div>
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">💬</div><span>720</span></div>
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">✈️</div><span>18.1K</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    } else if (this.activeMockupPlatform === 'youtube') {
      mockupContainer.innerHTML = `
        <div class="smartphone-device">
          <div class="dynamic-island"></div>
          <div class="phone-screen">
            <img src="assets/thumbnail_demo.jpg" class="phone-media-bg" alt="YouTube Shorts">
            <div class="tiktok-overlay-ui" style="justify-content:flex-end;">
              <div class="tiktok-bottom-area">
                <div class="tiktok-caption-group">
                  <div style="font-size:0.86rem; font-weight:800; color:#fff; margin-bottom:4px;">${title}</div>
                  <div class="tiktok-creator-handle" style="display:flex; align-items:center; gap:8px;">
                    <span>Alex Rivera Tech</span>
                    <span style="background:#ff0000; color:#fff; font-size:0.68rem; padding:2px 8px; border-radius:12px; font-weight:700;">SUSCRIBIRSE</span>
                  </div>
                </div>
                <div class="tiktok-right-actions">
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">👍</div><span>96K</span></div>
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">👎</div><span>Dislike</span></div>
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">💬</div><span>1.4K</span></div>
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">↗️</div><span>Compartir</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }
  }

  saveNewPost() {
    const titleInput = document.getElementById('newPostTitleInput');
    const captionInput = document.getElementById('newPostCaptionInput');
    const dateInput = document.getElementById('newPostDateInput');
    const timeInput = document.getElementById('newPostTimeInput');

    const title = titleInput?.value.trim();
    const caption = captionInput?.value.trim();
    const date = dateInput?.value || '2026-09-18';
    const time = timeInput?.value || '19:00';

    if (!title) {
      this.app.showToast('Por favor escribe un título para el contenido.', 'warning');
      return;
    }

    // Platforms checked
    const platforms = [];
    if (document.getElementById('planCheckTT')?.checked) platforms.push('tiktok');
    if (document.getElementById('planCheckIG')?.checked) platforms.push('instagram');
    if (document.getElementById('planCheckYT')?.checked) platforms.push('youtube');
    if (document.getElementById('planCheckFB')?.checked) platforms.push('facebook');

    const newPost = {
      id: 'post-' + Date.now(),
      title: title,
      platforms: platforms.length ? platforms : ['tiktok'],
      date: date,
      time: time,
      status: 'scheduled',
      caption: caption,
      viralScore: Math.floor(88 + Math.random() * 10),
      thumbnail: 'assets/thumbnail_demo.jpg'
    };

    StorageManager.addPost(newPost);
    this.renderCalendar();
    this.app.showToast('¡Contenido programado con éxito para todas las plataformas!', 'success');

    // Reset inputs
    if (titleInput) titleInput.value = '';
    if (captionInput) captionInput.value = '';
    this.renderMockup();
  }

  bindEvents() {
    // Mockup platform switcher
    document.querySelectorAll('.mockup-tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.mockup-tab-btn').forEach(b => b.classList.remove('btn-primary'));
        const target = e.currentTarget;
        target.classList.add('btn-primary');
        this.activeMockupPlatform = target.dataset.platform;
        this.renderMockup();
      });
    });

    // Real-time input synchronization to phone screen
    const titleInput = document.getElementById('newPostTitleInput');
    const captionInput = document.getElementById('newPostCaptionInput');

    if (titleInput) titleInput.addEventListener('input', () => this.renderMockup());
    if (captionInput) captionInput.addEventListener('input', () => this.renderMockup());

    // Schedule post button
    const scheduleBtn = document.getElementById('schedulePostBtn');
    if (scheduleBtn) {
      scheduleBtn.addEventListener('click', () => this.saveNewPost());
    }
  }
}
