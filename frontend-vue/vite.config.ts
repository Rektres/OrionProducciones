import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  base: process.env.VITE_BASE || '/',
  plugins: [vue()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  server: {
    // VITE_API_URL=/api es una ruta relativa; en dev (puerto 5173) hay que
    // proxyearla al BFF para que /api/imagenes/... y el resto resuelvan igual
    // que en produccion (donde nginx hace este mismo trabajo).
    proxy: {
      '/api': 'http://localhost:3001',
    },
  },
});
