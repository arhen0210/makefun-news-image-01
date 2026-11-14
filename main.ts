// news-image-01: THE WORLD, Friday 13 November 2026.
// Stories on the page: (1) FAA grounds every US departure in the Microsoft
// outage, (2) tanker hits a New Orleans cruise boat — 32 hurt, all rescued,
// (3) US Senate summons Nvidia's Huang and Lutnick, (4) Putin hardens terms
// as Zelensky meets US envoys and Europe joins the talks.
// Node 22, standard library only.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const src = "entry.png";
const dest = join(process.env.MAKEFUN_OUTPUT_DIR ?? "/output", "entry.png");

mkdirSync(join(dest, ".."), { recursive: true });
// The judge sees exactly these bytes — copy, no re-encode, no resize.
copyFileSync(src, dest);
console.log(`copied ${src} -> ${dest}`);
