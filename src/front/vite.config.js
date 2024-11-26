import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Esto permite que Vite escuche en 0.0.0.0
    port: 5173, // Asegúrate de que coincida con el puerto configurado en Docker
  },
})