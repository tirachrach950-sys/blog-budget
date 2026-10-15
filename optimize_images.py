#!/usr/bin/env python3
"""
optimize_images.py  -  make the Plainfolio site lighter.

What it does
  1. Converts every JPG/PNG inside the /images folder (and /images/sm) to WebP.
     The original files are kept (they are still used for og:image / social sharing).
  2. Rewrites the <img> tags in ALL .html files so visitors load the .webp version.
     Only <img> tags are touched, so og:image and other meta tags stay as .jpg.

How to use (from the folder that contains index.html):
  pip install Pillow
  python optimize_images.py

Safe to run again and again: it skips images that are already converted
and only rewrites a path when the matching .webp file really exists.
"""
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is missing. Run:  pip install Pillow")

ROOT = Path(__file__).resolve().parent
IMG_DIR = ROOT / "images"
QUALITY = 78      # 75-82 is the sweet spot for photos
MAX_WIDTH = 1400  # nothing on the site is displayed wider than this

if not IMG_DIR.is_dir():
    sys.exit(f"Folder not found: {IMG_DIR}  (run this script from your site's root folder)")

# ---- 1. Convert images ------------------------------------------------------
before = after = converted = 0
for src in sorted(IMG_DIR.rglob("*")):
    if src.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        continue
    dst = src.with_suffix(".webp")
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        continue
    im = ImageOps.exif_transpose(Image.open(src))
    if im.width > MAX_WIDTH:
        im = im.resize((MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)), Image.LANCZOS)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    im.save(dst, "WEBP", quality=QUALITY, method=6)
    before += src.stat().st_size
    after += dst.stat().st_size
    converted += 1
    print(f"  {src.relative_to(ROOT)}: {src.stat().st_size // 1024} KB -> {dst.stat().st_size // 1024} KB")

if converted:
    print(f"\nConverted {converted} images: {before // 1024} KB -> {after // 1024} KB "
          f"({100 - after * 100 // max(before, 1)}% lighter)\n")
else:
    print("No new images to convert.\n")

# ---- 2. Point <img> tags to the .webp files ---------------------------------
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
IMG_PATH = re.compile(r"(/images/[^\s\"',]+)\.(?:jpe?g|png)", re.I)

def to_webp(m):
    webp = ROOT / (m.group(1).lstrip("/") + ".webp")
    return m.group(1) + ".webp" if webp.exists() else m.group(0)

changed_files = []
for html in ROOT.rglob("*.html"):
    if any(part in {"node_modules", ".git"} for part in html.parts):
        continue
    text = html.read_text(encoding="utf-8")
    new = IMG_TAG.sub(lambda t: IMG_PATH.sub(to_webp, t.group(0)), text)
    if new != text:
        html.write_text(new, encoding="utf-8")
        changed_files.append(html.relative_to(ROOT))

print(f"Updated {len(changed_files)} HTML file(s):")
for f in changed_files:
    print("  ", f)
print("\nDone. Upload the new .webp files in /images plus the updated .html files.")
