export default {
  routes: [
    "/",
    "/projektek",
    "/elerhetoseg",
    "/velemenyek",
    "/szolgaltatasok",
    "/rolam"
  ],
  outDir: "static-pages",
  serveDir: "dist",
  flatOutput: false,
  buildCommand: "npm run build",
  skipPrerenderSelector: '[data-skip-prerender]',
  viewport: { width: 1920, height: 1080 }
};
