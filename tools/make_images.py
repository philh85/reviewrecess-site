#!/usr/bin/env python3
"""Makes the game screenshots for the website from the PNG screenshots in /workspace (needs Pillow).
For every shot in game_pages.py:  site/assets/img/games/<key>-640.webp and <key>-1200.webp (16:9, cropped from the top),
and for each game's first shot a 1200 x 630 social-sharing image: site/assets/img/og/<slug>.jpg.
Run only when screenshots change:  python3 tools/make_images.py"""
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from game_pages import GAME_PAGES
SRC = os.environ.get('RR_SHOTS_ROOT', '/workspace')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site', 'assets', 'img')

def crop_to(im, ratio):
    w, h = im.size
    if w / h > ratio:                      # too wide: crop the sides evenly
        nw = round(h * ratio); x = (w - nw) // 2; return im.crop((x, 0, x + nw, h))
    nh = round(w / ratio); return im.crop((0, 0, w, nh))   # too tall: keep the top

def main():
    os.makedirs(os.path.join(OUT, 'games'), exist_ok=True); os.makedirs(os.path.join(OUT, 'og'), exist_ok=True)
    n = 0
    for g in GAME_PAGES:
        for i, (key, src, alt, cap) in enumerate(g['shots']):
            im = Image.open(os.path.join(SRC, src)).convert('RGB')
            base = crop_to(im, 16 / 9)
            for w in (640, 1200):
                h = round(w * 9 / 16)
                base.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, 'games', f'{key}-{w}.webp'), 'WEBP', quality=80, method=6)
                n += 1
            if i == 0:
                crop_to(im, 1200 / 630).resize((1200, 630), Image.LANCZOS).save(os.path.join(OUT, 'og', f"{g['slug']}.jpg"), 'JPEG', quality=82, optimize=True, progressive=True)
    print('wrote', n, 'webp files and', len(GAME_PAGES), 'social images')

if __name__ == '__main__':
    main()
