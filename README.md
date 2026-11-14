# news-image-01 — THE WORLD, 13 November 2026

This is a competition entry: one 1024x1024 image that sums up world news of
Friday 13 November 2026. `news_page.py` draws the page with PIL primitives —
a broadsheet front page with four story panels (US flights grounded in the
Microsoft outage, a tanker striking a New Orleans cruise boat, the US Senate
summoning Nvidia's Huang and Lutnick, and Putin hardening terms as Zelensky
meets US envoys) plus a ticker of three more headlines. It is drawn, not a
photo, so text and icons stay crisp at the gate's size limit. The rendered
file is committed as `entry.png`.

## Run it

```
python3 news_page.py entry.png     # regenerate the page (already committed)
MAKEFUN_OUTPUT_DIR=out node main.ts   # copy entry.png to the output dir
```

`main.ts` is a Node 22 standard-library-only program that copies `entry.png`
to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), byte-for-byte. The
result is a PNG, 1024x1024, about 72 KB — well inside the 1 MiB / 1024x1024
gate.
