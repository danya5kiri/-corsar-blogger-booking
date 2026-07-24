const fs = require("node:fs");
const path = require("node:path");

// Wrapper keeps the precise visual-smoke failure inside the downloadable artifact.
process.on("unhandledRejection", error => {
  const outputDir = path.resolve("artifacts/refinement-smoke");
  fs.mkdirSync(outputDir, { recursive: true });
  const message = error && error.stack ? error.stack : String(error || "Unknown visual smoke error");
  fs.writeFileSync(path.join(outputDir, "visual-smoke-error.txt"), message, "utf8");
  console.error(message);
  process.exitCode = 1;
});

require("./refinement_visual_smoke.cjs");
