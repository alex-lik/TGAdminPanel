import react from '@vitejs/plugin-react'; // плагин, поддерживает TSX
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [react()],
});
