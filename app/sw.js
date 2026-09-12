const CACHE_NAME = 'virallabs-studio-v2.3';
const ASSETS = [
  './index.html',
  './manifest.json',
  './sw.js',
  './version.json',
  './logo.png',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((k) => {
          if (k !== CACHE_NAME) return caches.delete(k);
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);

  // No cachear llamadas a APIs externas de IA ni version.json remoto para que siempre consulte lo mÃ¡s reciente
  if (url.hostname.includes('googleapis.com') || 
      url.hostname.includes('openai.com') || 
      url.hostname.includes('deepseek.com') || 
      url.hostname.includes('pollinations.ai') ||
      url.pathname.endsWith('version.json')) {
    e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
    return;
  }

  // Stale-While-Revalidate para archivos locales (rÃ¡pido + siempre actualizado)
  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {
      const fetchPromise = fetch(e.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200 && e.request.method === 'GET') {
          const resClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, resClone));
        }
        return networkResponse;
      }).catch(() => cachedResponse || caches.match('./index.html'));

      return cachedResponse || fetchPromise;
    })
  );
});
