// news-image-20261121 — "21 November 2026 — One Day in One Image"
//
// The entry is one pre-drawn image (entry.png) summing up Saturday
// 21 November 2026's world news. This program copies that image into
// the grader's output directory, byte for byte, on every run.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const source = join(here, "entry.png");
const target = join(outDir, "entry.png");

// Fail loudly if the image is missing instead of writing nothing.
if (!existsSync(source)) {
  throw new Error(`entry image not found: ${source}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// A plain copy is deterministic by construction: the same input bytes
// land in the output on every run, so two runs are byte-identical.
if (statSync(source).size !== statSync(target).size) {
  throw new Error("copied entry image has an unexpected size");
}
