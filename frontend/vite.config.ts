import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  
  // Root directory configuration - Force Vite to use this directory as root
  root: path.resolve(__dirname, '.'),
  
  // Server configuration for Windows/localhost issues
  server: {
    host: '127.0.0.1',  // Critical for Windows - use 127.0.0.1 instead of 0.0.0.0
    port: 3000,
    open: true,
    // Configure HMR for Windows
    hmr: {
      port: 3001,
    },
    // File system access
    fs: {
      strict: false,
    },
  },
  
  // Preview configuration
  preview: {
    host: '127.0.0.1',
    port: 4173,
  },
  
  // Build configuration
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    // Ensure proper asset handling
    assetsDir: 'assets',
  },
  
  // Base path
  base: '/',
  
  // Resolve configuration
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  
  // Development optimizations
  optimizeDeps: {
    include: ['react', 'react-dom'],
  },
})
