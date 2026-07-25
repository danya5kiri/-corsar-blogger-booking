import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  base: "/-corsar-blogger-booking/",
  server: {
    host: "0.0.0.0",
    allowedHosts: ["terminal.local"],
  },
  plugins: [react()],
  build: {
    outDir: "dist",
    sourcemap: true,
  },
});
