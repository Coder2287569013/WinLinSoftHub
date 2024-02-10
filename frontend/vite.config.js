import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import fs from 'fs';
import vue from '@vitejs/plugin-vue'

const pathToCert = '../certs/dev.local+4.pem';
const pathToKey = '../certs/dev.local+4-key.pem';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    https: {
      key: fs.readFileSync(pathToKey),
      cert: fs.readFileSync(pathToCert),
    }
  }
});