import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // Enable code splitting
    rollupOptions: {
      output: {
        manualChunks(id) {
          // Split node_modules into separate chunks
          if (id.includes('node_modules')) {
            // React ecosystem
            if (id.includes('react') || id.includes('react-dom') || id.includes('react-router')) {
              return 'react-vendor';
            }
            // MUI Joy and core components
            if (id.includes('@mui/joy')) {
              return 'mui-joy';
            }
            // MUI Material (if used)
            if (id.includes('@mui/material')) {
              return 'mui-material';
            }
            // MUI icons
            if (id.includes('@mui/icons-material')) {
              return 'mui-icons';
            }
            // Emotion (styling)
            if (id.includes('@emotion')) {
              return 'emotion';
            }
            // Other vendors
            return 'vendor';
          }
        },
        // Optimize asset loading
        assetFileNames: 'assets/[name]-[hash][extname]',
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
      },
    },
    // Optimize chunk size
    chunkSizeWarningLimit: 500,
    // Enable minification
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.logs in production
        drop_debugger: true,
        pure_funcs: ['console.log', 'console.info', 'console.debug'], // Remove specific console methods
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
    target: 'es2015',
    // Enable CSS code splitting
    cssCodeSplit: true,
    // Compress output
    reportCompressedSize: true,
  },
  // Optimize dependencies
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom', '@mui/joy'],
    exclude: ['@mui/material'], // Exclude if not used
  },
});
