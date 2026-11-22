// Entry program for the 22 November 2026 make.fun news-image entry.
// Copies the pre-rendered newspaper front page to the output directory.
// Node 22 stdlib only. No network. Deterministic: copying a fixed file
// always produces byte-identical output.
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const src = join(__dirname, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

if (!existsSync(src)) {
  console.error(`entry.png not found next to main.ts: ${src}`);
  process.exit(1);
}

// Guard: refuse to ship anything that is not a 1024x1024 PNG.
const head = readFileSync(src);
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!head.subarray(0, 8).equals(PNG_MAGIC)) {
  console.error("entry.png is not a PNG file");
  process.exit(1);
}
const width = head.readUInt32BE(16);
const height = head.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  console.error(`entry.png is ${width}x${height}, expected 1024x1024`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
const bytes = statSync(dest).size;
console.log(`copied ${src} -> ${dest} (${bytes} bytes)`);
