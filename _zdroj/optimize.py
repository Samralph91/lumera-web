# -*- coding: utf-8 -*-
"""Make the published site lighter: recompress photos, small thumbnails for property cards, smaller logo."""
import glob, os, re
from PIL import Image

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
MAX_SIDE, Q, THUMB_W = 1600, 80, 720


def jpeg(src, dst, max_side, q):
    im = Image.open(src)
    im = im.convert('RGB')
    if max(im.size) > max_side:
        im.thumbnail((max_side, max_side), Image.LANCZOS)
    im.save(dst, 'JPEG', quality=q, optimize=True, progressive=True)


def main():
    before = sum(os.path.getsize(f) for f in glob.glob(SITE + '/img/**/*.jpg', recursive=True))
    for f in glob.glob(SITE + '/img/**/*.jpg', recursive=True) + [SITE + '/trencin.jpg']:
        if f.endswith('-t.jpg'):
            continue
        jpeg(f, f, MAX_SIDE if 'trencin' not in f else 2000, Q)
    jpeg(SITE + '/samuel.jpg', SITE + '/samuel.jpg', 640, 82)
    # card thumbnails
    used = set()
    for page in glob.glob(SITE + '/*.html'):
        h = open(page).read()
        def sub(m):
            src = m.group(1)
            thumb = src[:-4] + '-t.jpg'
            if src not in used:
                im = Image.open(os.path.join(SITE, src)).convert('RGB')
                im.thumbnail((THUMB_W, THUMB_W * 2), Image.LANCZOS)
                im.save(os.path.join(SITE, thumb), 'JPEG', quality=78, optimize=True, progressive=True)
                used.add(src)
            return "url('%s')" % thumb
        h2 = re.sub(r"url\('(img/[^']+?)(?<!-t)\.jpg'\)", lambda m: sub(type('M', (), {'group': lambda self, i: m.group(1) + '.jpg'})()), h)
        if h2 != h:
            open(page, 'w').write(h2)
    # logo is shown ~56 px high: 3x for sharp screens is plenty
    logo = Image.open(SITE + '/logo.png')
    logo.thumbnail((420, 240), Image.LANCZOS)
    logo.save(SITE + '/logo.png', optimize=True)
    after = sum(os.path.getsize(f) for f in glob.glob(SITE + '/img/**/*.jpg', recursive=True) if not f.endswith('-t.jpg'))
    print('images %d kB -> %d kB, %d thumbnails, logo %d kB' % (before // 1024, after // 1024, len(used), os.path.getsize(SITE + '/logo.png') // 1024))


if __name__ == '__main__':
    main()
