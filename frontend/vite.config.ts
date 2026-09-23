import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

const backendUrl = process.env.BACKEND_URL || "http://localhost:8003";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: true,
    port: 5176,
    strictPort: true,
    proxy: {
      "/api": {
        target: backendUrl,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
