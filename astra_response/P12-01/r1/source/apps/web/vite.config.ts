import { fileURLToPath } from 'node:url';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vitest/config';
import { publicShell } from './pwa/build.ts';

export default defineConfig(({ mode }) => {
  const androidOrigin = process.env.VITE_BVA_PRODUCTION_ORIGIN;
  if (mode === 'android-production') {
    if (
      androidOrigin === undefined ||
      !/^https:\/\/(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z](?:[a-z0-9-]*[a-z0-9])?$/.test(
        androidOrigin,
      ) ||
      androidOrigin.endsWith('.localhost')
    )
      throw new Error('Invalid production Android HTTPS origin');
  } else if (androidOrigin !== undefined) {
    throw new Error('Production Android origin requires android-production mode');
  }
  return {
    plugins: [react(), publicShell()],
    // Never load the repository's private dotenv configuration into frontend tooling.
    envDir: false,
    server: {
      host: '127.0.0.1',
      port: 5173,
      strictPort: true,
      cors: false,
      fs: { strict: true, allow: [fileURLToPath(new URL('.', import.meta.url))] },
      proxy: { '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true } },
    },
    build: { sourcemap: false },
    test: {
      environment: 'jsdom',
      environmentOptions: { jsdom: { url: 'http://127.0.0.1:5173/' } },
      setupFiles: ['./src/test/setup.ts'],
      include: ['src/**/*.test.tsx'],
      restoreMocks: true,
    },
  };
});
