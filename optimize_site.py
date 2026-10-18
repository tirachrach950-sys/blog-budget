#!/usr/bin/env python3
"""
optimize_site.py - performance pass for the Plainfolio static site.

Run from the folder that contains index.html (safe to run again and again):
    pip install Pillow
    python optimize_site.py

Run it after every edit / after python build.py.

ADD A NEW PHOTO: drop any jpg/png/webp (any size) into /originals and run this script.
It creates   sm/NAME.webp (760x507 cards)  xs/NAME.webp (480x320 phones)
             images/NAME.jpg (1200px share image for og:image / Pinterest)

What it does to the pages
  - card images: srcset (480w phone / 760w), lazy, async decode
  - home hero: preload so the biggest image starts downloading immediately
  - Google Fonts: no longer blocks first paint (display=swap everywhere)
  - /assets/style.css and /assets/site.js get ?v=hash so they can be cached for a year
  - hero float animation runs 3 times then rests (was endless); gray placeholder behind images
  - folder-style pages (about/index.html ...) so links work on ANY host with no rewrite rules
"""
import hashlib, re, shutil, sys
from pathlib import Path
try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is missing. Run:  pip install Pillow")

ROOT = Path(__file__).resolve().parent
Q = 78

def crop_resize(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * r)), max(h, round(im.height * r))), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))

# ---------------------------------------------------------- 0. new photos
made = 0
orig = ROOT / "originals"
for f in sorted(orig.iterdir()) if orig.is_dir() else []:
    if f.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
        continue
    name = re.sub(r"[^a-z0-9]+", "-", f.stem.lower()).strip("-")
    share = ROOT / "images" / f"{name}.jpg"
    if share.exists() and share.stat().st_mtime >= f.stat().st_mtime:
        continue
    im = Image.open(f).convert("RGB")
    for d in ("images", "sm", "xs"):
        (ROOT / d).mkdir(exist_ok=True)
    (im if im.width <= 1200 else im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
     ).save(share, "JPEG", quality=80, optimize=True, progressive=True)
    crop_resize(im, 760, 507).save(ROOT / "sm" / f"{name}.webp", "WEBP", quality=Q, method=6)
    crop_resize(im, 480, 320).save(ROOT / "xs" / f"{name}.webp", "WEBP", quality=Q, method=6)
    made += 1
print(f"originals: {made} new photo(s) processed")

# ------------------------------- 1. xs thumbnails from existing sm images
(ROOT / "xs").mkdir(exist_ok=True)
for sm in sorted((ROOT / "sm").glob("*.webp")):
    xs = ROOT / "xs" / sm.name
    if sm.name.startswith("laptop-budget") or (xs.exists() and xs.stat().st_mtime >= sm.stat().st_mtime):
        continue
    im = Image.open(sm).convert("RGB")
    im.resize((480, round(im.height * 480 / im.width)), Image.LANCZOS).save(xs, "WEBP", quality=Q, method=6)
    made += 1
print(f"thumbnails: {made} file(s) written")

# ------------------------------------------------------------ 2. the pages
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
FONT = re.compile(r'<link href="(https://fonts\.googleapis\.com/css2\?[^"]+?)display=(?:swap|optional)" rel="stylesheet">')
HERO = '<link rel="preload" as="image" href="/sm/laptop-budget.webp" fetchpriority="high">\n'
EXTRA_CSS = ".card img,.heroimg img{background:#dde6e0}"

def card_img(m):
    tag = m.group(0)
    src = re.search(r'\bsrc="/sm/([^"/]+)\.webp"', tag)
    if not src or "srcset" in tag or 'fetchpriority="high"' in tag or src.group(1).startswith("laptop-budget"):
        return tag
    n = src.group(1)
    return tag.replace(f'src="/sm/{n}.webp"',
        f'src="/sm/{n}.webp" srcset="/xs/{n}.webp 480w, /sm/{n}.webp 760w" sizes="(max-width:640px) 92vw, 380px"', 1)

def h(path):
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]

def tweak_css(css):
    css = css.replace("animation:float 7s ease-in-out infinite", "animation:float 7s ease-in-out 3")
    return css

# assets/style.css first (so its hash is final)
sheet = ROOT / "assets" / "style.css"
if sheet.exists():
    css = tweak_css(sheet.read_text(encoding="utf-8"))
    css = re.sub(r"/\*.*?\*/\n?", "", css, flags=re.S)
    if EXTRA_CSS not in css:
        css = css.rstrip() + "\n" + EXTRA_CSS + "\n"
    sheet.write_text(css, encoding="utf-8")

pages = [ROOT / "index.html"] + sorted(ROOT.glob("*.html")) + sorted((ROOT / "guides").glob("*.html"))
done, changed = set(), 0
for p in pages:
    if p in done or not p.exists():
        continue
    done.add(p)
    t = old = p.read_text(encoding="utf-8")
    t = IMG_TAG.sub(card_img, t)
    t = FONT.sub(lambda m: (f'<link rel="preload" as="style" href="{m.group(1)}display=swap" '
                            f'onload="this.onload=null;this.rel=\'stylesheet\'">'
                            f'<noscript><link rel="stylesheet" href="{m.group(1)}display=swap"></noscript>'), t)
    t = tweak_css(t)
    if "<style>" in t and EXTRA_CSS not in t:                      # inline CSS pages
        t = t.replace("</style>", EXTRA_CSS + "</style>", 1)
    if p.name == "index.html" and 'rel="preload" as="image"' not in t:
        t = t.replace("<style>", HERO + "<style>", 1)
    for a in ("assets/style.css", "assets/site.js"):
        if (ROOT / a).exists():
            t = re.sub(rf'/{re.escape(a)}(\?v=[0-9a-f]+)?"', f'/{a}?v={h(a)}"', t)
    if t != old:
        p.write_text(t, encoding="utf-8")
        changed += 1
print(f"html: {changed} file(s) updated")

# --------------------------------------- 3. folder-style pages (any host)
for p in pages:
    if p.name == "index.html" or p.name.startswith("google") or not p.exists():
        continue
    d = p.with_suffix("")
    d.mkdir(exist_ok=True)
    shutil.copyfile(p, d / "index.html")
print("folder pages: refreshed")
print("Done.")
