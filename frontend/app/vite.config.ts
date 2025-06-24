import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';    // плагин, поддерживает TSX

export default defineConfig({
  plugins: [react()],
});
