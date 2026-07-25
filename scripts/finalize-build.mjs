import { copyFile, rm } from "node:fs/promises";

await copyFile("dist/vite-entry.html", "dist/index.html");
await rm("dist/vite-entry.html");

console.log("✓ Production entry renamed to dist/index.html");
