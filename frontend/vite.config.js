import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      'api': path.resolve(__dirname, 'src/api'),
      'store': path.resolve(__dirname, 'src/store'),
      'menu-items': path.resolve(__dirname, 'src/menu-items'),
      'config': path.resolve(__dirname, 'src/config'),
      'ui-component': path.resolve(__dirname, 'src/ui-component'),
      'hooks': path.resolve(__dirname, 'src/hooks'),
      'assets': path.resolve(__dirname, 'src/assets'),
      'utils': path.resolve(__dirname, 'src/utils'),
      'contexts': path.resolve(__dirname, 'src/contexts'),
    },
  },
});
