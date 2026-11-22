// news-image-20261121 v2 entrypoint (Node 22, standard library only).
//
// The entry is a single pre-drawn front page, entry.png, sitting next to
// this file. All this program does is place a copy of it at
// <output>/entry.png, where the grader expects it.
//
// The output directory comes from MAKEFUN_OUTPUT_DIR when set (local runs),
// otherwise /output (the grader's mount). Paths are resolved from this
// script's own location, never from the working directory, because the
// grader may start the program from anywhere. The output directory is
// created if missing; it is never removed.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const entryFile = "entry.png";

// A plain copy: same bytes in, same bytes out, every run.
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, entryFile), join(outDir, entryFile));
