import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const isGitHubActions = process.env.GITHUB_ACTIONS === "true";

export default defineConfig({
  // GitHub Pages serves the production build from the repository subpath.
  // Local and embedded chat previews must run from the root URL.
  base: isGitHubActions ? "/-corsar-blogger-booking/" : "/",
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
  },
});
