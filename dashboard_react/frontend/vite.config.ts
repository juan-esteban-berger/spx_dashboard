import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// API URL from environment variable
const API_URL = process.env.VITE_API_URL || 'http://localhost:30009'

export default defineConfig({
  plugins: [react()],
  base: '/spx-react/',
  server: {
    port: 8081,
    host: true,
    proxy: {
      '/api': {
        target: API_URL,
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  }
})
