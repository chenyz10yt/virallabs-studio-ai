/**
 * OMNIVIRAL STUDIO AI - LOCAL PERSISTENCE & CREATOR STATE STORE
 */

const STORAGE_KEY = 'omniviral_studio_data_v1';

const defaultCreatorState = {
  creator: {
    name: 'Alex Rivera',
    handle: '@alexcreator.ai',
    tier: 'Pro Elite Creator',
    niche: 'Inteligencia Artificial & Tech',
    connectedPlatforms: {
      tiktok: true,
      youtube: true,
      instagram: true,
      facebook: false,
      twitch: true,
      kick: false
    }
  },
  streamSettings: {
    resolution: '1080p60',
    targetBitrate: 6500,
    fps: 60,
    audioBitrate: 160,
    rtmpKeys: {
      youtube: 'yt-live-9823-xxxx-viral',
      tiktok: 'tt-live-4412-xxxx-stream',
      facebook: 'fb-live-1120-xxxx-meta',
      twitch: 'live_8832_tw_xxxx',
      kick: 'sk_us_kick_9021_xxxx'
    }
  },
  scheduledPosts: [
    {
      id: 'post-1',
      title: '5 Herramientas de IA que reemplazan agencias enteras en 2026',
      platforms: ['tiktok', 'instagram', 'youtube'],
      date: '2026-09-14',
      time: '19:00',
      status: 'scheduled',
      caption: '🚀 Si no estás usando estas 5 herramientas de IA en 2026, estás perdiendo el 80% de tu tiempo. La número 4 te volará la cabeza 🤯\n\n#IA #CreadoresDeContenido #Productividad #Tecnologia #Emprendimiento',
      viralScore: 94,
      thumbnail: 'assets/thumbnail_demo.jpg'
    },
    {
      id: 'post-2',
      title: 'Cómo cloné mi voz para narrar videos automáticos legalmente',
      platforms: ['youtube', 'facebook'],
      date: '2026-09-15',
      time: '18:30',
      status: 'scheduled',
      caption: '🎙️ Guía definitiva para clonar tu voz con certificación de derechos de autor y monetizar canales automatizados sin penalizaciones de algoritmo.',
      viralScore: 91,
      thumbnail: 'assets/clip_demo.jpg'
    },
    {
      id: 'post-3',
      title: 'El nuevo cambio de algoritmo en TikTok e Instagram Reels',
      platforms: ['tiktok', 'instagram'],
      date: '2026-09-17',
      time: '20:15',
      status: 'draft',
      caption: '⚠️ ATENCIÓN: El algoritmo cambió este mes. Las visualizaciones ya no importan tanto como esta métrica secreta (los shares por mensaje directo).',
      viralScore: 88,
      thumbnail: 'assets/thumbnail_demo.jpg'
    }
  ],
  savedPrompts: [],
  voiceProfiles: [
    {
      id: 'voice-alex-main',
      name: 'Voz Principal Alex (Clonada)',
      pitch: 1.0,
      cadence: 'Dinámica / Enérgica',
      dateCreated: '2026-09-10',
      licenseId: 'LIC-AUTH-2026-9941-VERIFIED',
      verified: true
    }
  ]
};

export class StorageManager {
  static getData() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        this.saveData(defaultCreatorState);
        return defaultCreatorState;
      }
      return JSON.parse(raw);
    } catch (e) {
      console.warn('Error reading from localStorage, using defaults', e);
      return defaultCreatorState;
    }
  }

  static saveData(data) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      console.error('Error saving to localStorage', e);
    }
  }

  static addPost(post) {
    const data = this.getData();
    data.scheduledPosts.unshift(post);
    this.saveData(data);
    return data.scheduledPosts;
  }

  static deletePost(postId) {
    const data = this.getData();
    data.scheduledPosts = data.scheduledPosts.filter(p => p.id !== postId);
    this.saveData(data);
    return data.scheduledPosts;
  }

  static updatePlatformStatus(platform, isConnected) {
    const data = this.getData();
    data.creator.connectedPlatforms[platform] = isConnected;
    this.saveData(data);
    return data.creator.connectedPlatforms;
  }
}
