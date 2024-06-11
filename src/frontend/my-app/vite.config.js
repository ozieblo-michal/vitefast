import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());

  return {
    plugins: [react()],
    build: {
      outDir: 'dist',
    },
    base: "/vitefast/",
    server: {
      proxy: {
        '/': {
          target: env.VITE_BACKEND_URL,
          changeOrigin: true,
          secure: true,
        },
      },
    },
  };
});
