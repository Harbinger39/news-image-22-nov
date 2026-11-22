// Entry point for the make.fun "Sum up 22 November's world news in one
// image" competition (news-image-20261122).
//
// The finished image is a file in this repository: entry.png (1024x1024,
// deterministic, drawn in code by compose22.py). This script copies it to
// the output directory the harness expects, with no network access and no
// other side effects.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
