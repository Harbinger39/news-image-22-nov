// Entry program for the 22 November 2026 make.fun news-image entry.
// Copies the pre-rendered front page to the output directory.
// Node 22 stdlib only. No network. Deterministic: copying a fixed file
// always produces byte-identical output.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const src = join(__dirname, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
console.log(`copied ${src} -> ${dest}`);
