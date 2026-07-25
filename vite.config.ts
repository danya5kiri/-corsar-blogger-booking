import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig(({ command }) => ({
  // GitHub Pages serves the production build from the repository subpath.
  // Dev servers and embedded chat previews open from the root URL.
  base: command === "build" ? "/-corsar-blogger-booking/" : "/",
  server: {
    host: "0.0.0.0",
    allowedHosts: true,
  },
  preview: {
    host: "0.0.0.0",
    allowedHosts: true,
  },
  plugins: [react()],
  build: {
    outDir: "dist",
    sourcemap: true,
    rollupOptions: {
      input: "vite-entry.html",
    },
  },
}));
