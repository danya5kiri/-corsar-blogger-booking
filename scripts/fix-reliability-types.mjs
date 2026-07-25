import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";

const path = "src/creacloud-data.ts";
let content = await readFile(path, "utf8");
const before = `.filter((item): item is ContentItem => Boolean(item?.tourId));`;
const after = `.filter(\n      (item): item is NonNullable<typeof item> => Boolean(item?.tourId),\n    );`;

if (content.includes(after)) {
  console.log("Reliability type correction is already applied.");
  process.exit(0);
}

assert.ok(content.includes(before), "Content filter predicate was not found");
content = content.replace(before, after);
await writeFile(path, content, "utf8");
console.log("Corrected content filter predicate type.");
