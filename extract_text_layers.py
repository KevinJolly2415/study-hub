import os
import sys
import json
import time
from pathlib import Path
import pypdfium2 as pdfium

PROJECT_ROOT = Path(r"C:\Users\kevin\.gemini\antigravity\scratch\study-slides-hub")
PUBLIC_DIR = PROJECT_ROOT / "public"
DOCS_DIR = PUBLIC_DIR / "docs"
SLIDES_DIR = PUBLIC_DIR / "slides"
MANIFEST_PATH = PUBLIC_DIR / "data" / "manifest.json"
SRC_MANIFEST_PATH = PROJECT_ROOT / "src" / "data" / "manifest.json"

with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

print("=== Extracting Selectable Text Layers for All Slides ===", flush=True)
t0 = time.time()
updated_decks = 0
total_rects_saved = 0

for subject in manifest["subjects"]:
    for deck in subject["decks"]:
        deck_id = deck["id"]
        pdf_file = DOCS_DIR / f"{deck_id}.pdf"
        meta_file = SLIDES_DIR / deck_id / "meta.json"

        if not pdf_file.exists():
            continue

        try:
            doc = pdfium.PdfDocument(str(pdf_file))
        except Exception as e:
            print(f"Error opening {pdf_file.name}: {e}", flush=True)
            continue

        num_pages = len(doc)
        deck_slides = deck.get("slides", [])

        for i in range(min(num_pages, len(deck_slides))):
            page = doc[i]
            pw, ph = page.get_width(), page.get_height()
            tp = page.get_textpage()
            n_rects = tp.count_rects()

            rects = []
            for r_idx in range(n_rects):
                l, b, r, t = tp.get_rect(r_idx)
                txt = tp.get_text_bounded(l, b, r, t)
                if not txt:
                    continue

                l_pct = round((l / pw) * 100, 2)
                t_pct = round(((ph - t) / ph) * 100, 2)
                w_pct = round(((r - l) / pw) * 100, 2)
                h_pct = round(((t - b) / ph) * 100, 2)

                if w_pct <= 0 or h_pct <= 0:
                    continue

                rects.append({
                    "l": l_pct,
                    "t": t_pct,
                    "w": w_pct,
                    "h": h_pct,
                    "text": txt
                })

            total_rects_saved += len(rects)
            deck_slides[i]["rects"] = rects

        # Also write to local deck meta.json
        if meta_file.exists():
            try:
                with open(meta_file, "r", encoding="utf-8") as mf:
                    cached_meta = json.load(mf)
                cached_meta["slides"] = deck_slides
                with open(meta_file, "w", encoding="utf-8") as mf:
                    json.dump(cached_meta, mf, indent=2)
            except Exception:
                pass

        updated_decks += 1

# Save updated manifests
with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

with open(SRC_MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

dt = time.time() - t0
print(f"SUCCESS: Attached selectable text layers to {updated_decks} decks ({total_rects_saved} text blocks) in {dt:.2f}s!", flush=True)

