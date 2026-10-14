#!/usr/bin/env python3
"""Adds the AdSense script to the <head> of index.html and every file in guides/.
Only inserts one line. Never changes text, images or anything else. Safe to run twice.
Put this file in the repo root (next to index.html) and run:  python add_loader.py"""
import glob
S = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8221947298825158"\n'
     '     crossorigin="anonymous"></script>\n')
for f in ["index.html"] + sorted(glob.glob("guides/*.html")):
    h = open(f, encoding="utf-8").read()
    if "adsbygoogle.js" in h: print("already has it:", f); continue
    if "</head>" not in h: print("no </head>, skipped:", f); continue
    open(f, "w", encoding="utf-8").write(h.replace("</head>", S + "</head>", 1)); print("added:", f)
