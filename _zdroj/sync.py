# -*- coding: utf-8 -*-
"""Keep lumera.sk in step with the agency's listings on nehnutelnosti.sk.

  python3 sync.py map                        # nehnutelnosti id -> listing key / page / current site price
  python3 sync.py set-price <key> <EUR|0>    # 0 = hidden price ("Cena dohodou")
  python3 sync.py sold <key>                 # mark as PREDANÉ (stays as a reference page)
  python3 sync.py unsold <key>
  python3 sync.py build                      # pages.py + export.py -> ./site
  python3 sync.py publish <repo_dir>         # copy ./site into the repo root (never touches _zdroj/ or social/)

<key> is the key in listing.LISTINGS (e.g. turna, byt28, myjava). Fetching nehnutelnosti.sk itself is done by the caller
(this container usually cannot reach it; use the Composio workbench) – compare its prices with `map`.
"""
import json, os, re, shutil, subprocess, sys

sys.dont_write_bytecode = True

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
STATE = os.path.join(SP, 'sync_state.json')


def state():
    return json.load(open(STATE))


def save_state(s):
    json.dump(s, open(STATE, 'w'), ensure_ascii=False, indent=1)


def fmt(n):
    return '{:,}'.format(int(n)).replace(',', ' ') + ' €'


def dc_of(key):
    import pages
    for dc, static, *_ in pages.PAGES:
        if dc[:-8].lower() == key:
            return dc, static
    raise SystemExit('unknown listing key: %s' % key)


def listing_ids():
    import listing
    out = {}
    for key, L in listing.LISTINGS.items():
        m = re.search(r'/detail/([^/]+)/', L['inzerat'])
        out[key] = m.group(1) if m else None
    return out


def cmd_map():
    import listing
    ids = listing_ids()
    for key, L in listing.LISTINGS.items():
        dc, static = dc_of(key)
        print('%-11s %-13s %-42s %-14s %s' % (key, ids[key], static, L['price'], 'SOLD' if listing.is_sold(key) else ''))


def _area(L):
    for k in ('Výmera', 'Výmera bytu', 'Úžitková plocha'):
        for fk, fv in L['facts']:
            if fk == k:
                m = re.match(r'(?:cca\s*)?([\d\s]+(?:,\d+)?)', fv)
                if m:
                    return float(m.group(1).replace(' ', '').replace(',', '.'))
    return None


def cmd_set_price(key, value):
    import listing, vyhladavac
    L = listing.LISTINGS[key]
    dc, static = dc_of(key)
    value = int(float(value))
    old_price = L['price']
    hidden = value == 0
    rent = 'mesiac' in old_price or '/ mes' in old_price
    if hidden:
        new_price = 'Cena dohodou'
        role = L.get('agent', listing.DEFAULT_AGENT)[0]
        new_per = 'Cenu vám rada povie maklérka' if role == 'Maklérka' else 'Cenu vám radi povieme osobne'
    else:
        new_price = fmt(value) + (' / mesiac' if rent else '')
        if ' bez DPH' in old_price:
            new_price = fmt(value) + ' bez DPH'
        new_per = L['per_m2']
        a = _area(L)
        if a and re.match(r'^[\d ]+(,\d+)? € / m²', L['per_m2']) and not rent:
            per = value / a
            txt = ('{:,.2f}'.format(per) if per < 100 else '{:,.0f}'.format(per)).replace(',', ' ').replace('.', ',')
            new_per = re.sub(r'^[\d ]+(,\d+)? € / m²', txt + ' € / m²', L['per_m2'])
        elif L['per_m2'].startswith('Cenu vám'):
            new_per = 'Pomôžeme aj s hypotékou'
    # listing.py
    src = open(os.path.join(SP, 'listing.py')).read()
    block_start = src.index("'%s': {" % key) if "'%s': {" % key in src else src.index('"%s": {' % key)
    block_end = src.index("'photos':", block_start)
    block = src[block_start:block_end]
    block2 = block.replace("'price': %r" % old_price, "'price': %r" % new_price, 1).replace("'per_m2': %r" % L['per_m2'], "'per_m2': %r" % new_per, 1)
    assert block2 != block or old_price == new_price, 'price not found in listing.py'
    open(os.path.join(SP, 'listing.py'), 'w').write(src[:block_start] + block2 + src[block_end:])
    # vyhladavac FACTS
    v = open(os.path.join(SP, 'vyhladavac.py')).read()
    v2 = re.sub(r"('%s':\s*dict\([^)]*?price=)(None|[\d.]+)" % re.escape(dc), lambda m: m.group(1) + ('None' if hidden else str(value)), v, count=1)
    open(os.path.join(SP, 'vyhladavac.py'), 'w').write(v2)
    # source.dc.html: every object that links to this listing
    s = open(os.path.join(SP, 'source.dc.html')).read()

    def card_price(old):
        if hidden:
            return 'Cena dohodou'
        if re.match(r'^[\d ]+ €', old):
            return re.sub(r'^[\d ]+ €', fmt(value), old, count=1)
        return new_price

    def fix(m):
        t = m.group(0)
        t = re.sub(r"(price: ')([^']*)(')", lambda p: p.group(1) + card_price(p.group(2)) + p.group(3), t)
        t = re.sub(r'("price": ")([^"]*)(")', lambda p: p.group(1) + card_price(p.group(2)) + p.group(3), t)
        t = re.sub(r'"fp": (null|[\d.]+)', '"fp": %s' % ('null' if hidden else value), t)
        return t
    s2 = re.sub(r"\{[^{}]*%s[^{}]*\}" % re.escape(dc), fix, s)
    open(os.path.join(SP, 'source.dc.html'), 'w').write(s2)
    print('%s: %s -> %s (%s -> %s)' % (key, old_price, new_price, L['per_m2'], new_per))


def cmd_sold(key, flag=True):
    dc_of(key)
    s = state()
    sold = set(s.get('sold', []))
    (sold.add if flag else sold.discard)(key)
    s['sold'] = sorted(sold)
    save_state(s)
    print('sold:', s['sold'])


def cmd_build():
    shutil.rmtree(os.path.join(SP, '__pycache__'), ignore_errors=True)  # stale bytecode after quick edits
    subprocess.check_call([sys.executable, os.path.join(SP, 'pages.py')], cwd=SP)
    subprocess.check_call([sys.executable, os.path.join(SP, 'export.py')], cwd=SP)


def cmd_publish(repo):
    site = os.path.join(SP, 'site')
    for name in os.listdir(site):
        src, dst = os.path.join(site, name), os.path.join(repo, name)
        if name in ('_zdroj', 'social', '.git'):
            continue
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
    print('copied site ->', repo)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == 'map':
        cmd_map()
    elif a[0] == 'set-price':
        cmd_set_price(a[1], a[2])
    elif a[0] == 'sold':
        cmd_sold(a[1], True)
    elif a[0] == 'unsold':
        cmd_sold(a[1], False)
    elif a[0] == 'build':
        cmd_build()
    elif a[0] == 'publish':
        cmd_publish(a[1])
