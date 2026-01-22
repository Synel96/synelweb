import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import vike from "vike/plugin";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), vike({ prerender: true })],
  publicDir: 'public',
  resolve: {
    extensions: ['.js', '.jsx', '.json']
  },
  ssr: {
    noExternal: ['@mui/joy', '@mui/material', '@mui/icons-material', '@mui/base', '@emotion/react', '@emotion/styled', '@emotion/cache']
  },
  build: {
    // Optimize chunk size
    chunkSizeWarningLimit: 500,
    // Enable minification
    minify: "terser",
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.logs in production
        drop_debugger: true,
        pure_funcs: ["console.log", "console.info", "console.debug"], // Remove specific console methods
        passes: 2, // Run compression twice for better results
      },
      mangle: {
        safari10: true, // Fix Safari 10 bugs
      },
    },
    // Enable module preload for faster loading
    modulePreload: {
      polyfill: true,
    },
    // Target modern browsers for smaller bundles
    target: "es2015",
    // Enable CSS code splitting
    cssCodeSplit: true,
    // Compress output
    reportCompressedSize: true,
  },
  // Optimize dependencies
  optimizeDeps: {
    include: [
      "react",
      "react-dom",
      "react-router-dom",
      "@mui/joy",
      "@mui/icons-material",
      "@emotion/react",
      "@emotion/styled",
    ],
    exclude: ["@mui/material"], // Exclude if not used
  },
  server: {
    // Warm up frequently used files
    warmup: {
      clientFiles: [
        "./src/pages/ProjectsPage.jsx",
        "./src/components/projects/ProjectsCard.jsx",
        "./src/services/projectsService.js",
      ],
    },
  },
});
