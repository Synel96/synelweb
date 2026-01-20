const CACHE_NAME = "synelweb-cache-v1";
const CORE_ASSETS = [
  "/",
  "/index.html",
  "/assets/index-B_YyKZb9.js",
  "/assets/index-fhGOmIYN.css",
  // Ide vehetsz fel további fontos asseteket, pl. képeket, logókat
];

// Telepítéskor cache-eljük az alap fájlokat
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS))
  );
  self.skipWaiting();
});

// Aktiváláskor azonnal átveszi az irányítást
self.addEventListener("activate", (event) => {
  self.clients.claim();
});

// Fetch: először cache-ből, ha nincs, akkor hálózatról
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  event.respondWith(
    caches.match(event.request).then((response) => {
      return (
        response ||
        fetch(event.request).then((networkResponse) => {
          // Csak sikeres válaszokat cache-elünk
          if (
            networkResponse &&
            networkResponse.status === 200 &&
            networkResponse.type === "basic"
          ) {
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, networkResponse.clone());
            });
          }
          return networkResponse;
        })
      );
    })
  );
});
