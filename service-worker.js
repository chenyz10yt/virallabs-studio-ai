/**
 * VIRAL LABS - SERVICE WORKER & AUTO-UPDATE ENGINE
 * Version: v3.0.0 AI
 */

const CACHE_NAME = 'virallabs-cache-v3.0.0';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './fanpage.html',
  './manifest.json',
  './css/main.css',
  './css/glassmorphism.css',
  './css/studio.css',
  './css/clipper.css',
  './css/multistream.css',
  './css/planner.css',
  './css/radar.css',
  './css/fanpage.css',
  './css/visualstudio.css',
  './js/bundle.js',
  './js/fanpage.js',
  './assets/logo.jpg',
  './assets/thumbnail_demo.jpg',
  './assets/clip_demo.jpg',
  './assets/fanpage_banner.jpg'
];

// Install Event - Pre-cache Shell
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE).catch((err) => {
        console.warn('Pre-cache note:', err);
      });
    })
  );
});

// Activate Event - Purge ALL Legacy Caches Immediately
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME) {
            console.log('Purging legacy cache:', name);
            return caches.delete(name);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event - NETWORK FIRST (Always get newest changes, fallback to cache if offline)
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        // Fallback to cache if network fails (offline mode)
        return caches.match(event.request).then((cached) => {
          if (cached) return cached;
          if (event.request.headers.get('accept')?.includes('text/html')) {
            return caches.match('./index.html');
          }
        });
      })
  );
});

// Listen for skipWaiting messages
self.addEventListener('message', (event) => {
  if (event.data && event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
});
