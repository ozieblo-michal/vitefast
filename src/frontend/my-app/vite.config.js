// import { defineConfig, loadEnv } from 'vite';
// import react from '@vitejs/plugin-react';

// export default defineConfig(({ mode }) => {
//   const env = loadEnv(mode, import.meta.env.VITE_MODE || '');

//   return {
//     plugins: [react()],
//     build: {
//       outDir: 'dist',
//     },
//     base: "/vitefast/",
//     server: {
//       proxy: {
//         '/dummy': env.VITE_BACKEND_URL || 'http://localhost:80',
//       },
//     },
//   };
// });



import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  // Załaduj zmienne środowiskowe na podstawie trybu
  const env = loadEnv(mode, process.cwd());

  return {
    plugins: [react()],
    build: {
      outDir: 'dist',
    },
    base: "/vitefast/",
    server: {
      proxy: {
        '/dummy': env.VITE_BACKEND_URL || 'http://localhost:80',
      },
    },
  };
});
