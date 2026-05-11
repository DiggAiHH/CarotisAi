import path from "path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "fast-deep-equal": path.resolve(
        __dirname,
        "./src/lib/fastDeepEqualShim.ts"
      ),
      globalthis: path.resolve(__dirname, "./src/lib/globalthisShim.ts"),
      seedrandom: path.resolve(__dirname, "./src/lib/seedrandomShim.ts"),
    },
  },
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://backend:8000",
        changeOrigin: true,
        rewrite: (p) => p.replace(/^\/api/, ""),
      },
    },
  },
  worker: {
    format: "es",
  },
  build: {
    outDir: "dist",
    sourcemap: false,
    rollupOptions: {
      external: ["@icr/polyseg-wasm"],
      output: {
        format: "es",
      },
    },
  },
  assetsInclude: ["**/*.wasm"],
  optimizeDeps: {
    exclude: ["@cornerstonejs/core", "@cornerstonejs/dicom-image-loader"],
  },
});
