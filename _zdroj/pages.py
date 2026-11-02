"""Split the one-page design (source.dc.html) into one artboard per page, joined by links.

Writes lumera/project/<Page>.dc.html for every page and lumera/project/canvas.json.
"""
import json, os, re

SP = os.path.dirname(os.path.abspath(__file__))
PROJ = SP + '/lumera/project'

# (artboard file, static file, <title>, nav anchor that marks it active, sections, preview height)
PAGES = [
    ('Main.dc.html', 'index.html', 'LUMERA Real Estate – realitná kancelária Trenčín', None,
     ['HERO', 'TOP PONUKA', 'REFERENCIE', 'VYHĽADÁVANIE', 'SLUŽBY', 'O KANCELARII', 'KDE NAS NAJDETE', 'NEWSLETTER'], 5200),
    ('ONas.dc.html', 'o-nas.html', 'O nás – LUMERA Real Estate', 'o-nas',
     ['O NÁS', 'REFERENCIE', 'KONTAKT'], 2700),
    ('Ponuka.dc.html', 'ponuka.html', 'Ponuka nehnuteľností – LUMERA Real Estate', 'ponuka',
     ['PONUKA VYHLADAVAC', 'KONTAKT'], 3600),
    ('Predat.dc.html', 'chcem-predat.html', 'Chcem predať alebo prenajať nehnuteľnosť – LUMERA Real Estate', 'predat',
     ['PREDAJ HERO', 'PREDAJ SLUZBY', 'REFERENCIE', 'PREDAJ CTA'], 3300),
    ('Nacenenie.dc.html', 'nacenenie.html', 'Nacenenie nehnuteľnosti zadarmo – LUMERA Real Estate', 'nacenenie',
     ['NACENENIE', 'REFERENCIE'], 2000),
    ('Vykup.dc.html', 'vykup.html', 'Výkup nehnuteľností – LUMERA Real Estate', 'vykup',
     ['VÝKUP', 'REFERENCIE', 'KONTAKT'], 2600),
    ('Hypoteky.dc.html', 'hypoteky.html', 'Hypotéky a hypokalkulačka – LUMERA Real Estate', 'hypoteka',
     ['HYPOTÉKA', 'KONTAKT'], 2300),
    ('PravneSluzby.dc.html', 'pravne-sluzby.html', 'Právne služby – LUMERA Real Estate', 'pravne',
     ['PRÁVNE SLUŽBY', 'KONTAKT'], 2100),
    ('Kontakt.dc.html', 'kontakt.html', 'Kontakt – LUMERA Real Estate', 'kontakt',
     ['KONTAKT'], 1500),
    ('Byt28.dc.html', 'byt-28-oktobra.html', '3-izbový byt s 2 balkónmi, Trenčín 28. októbra – LUMERA Real Estate', None,
     ['BYT 28. OKTÓBRA', 'KONTAKT'], 2700),
    ('Zamarovce.dc.html', 'pozemok-zamarovce.html', 'Slnečný pozemok 770 m², Zamarovce – LUMERA Real Estate', None,
     ['POZEMOK ZAMAROVCE', 'KONTAKT'], 2600),
    ('Trebichava.dc.html', 'dom-trebichava.html', 'Vidiecky dom v Trebichave – LUMERA Real Estate', None,
     ['DOM TREBICHAVA', 'KONTAKT'], 2700),
    ('Myjava.dc.html', 'byt-myjava.html', '1-izbový byt, Myjava – LUMERA Real Estate', None,
     ['BYT MYJAVA', 'KONTAKT'], 2700),
    ('Mitice.dc.html', 'dom-trencianske-mitice.html', '5-izbový dom s dvojgarážou, Trenčianske Mitice – LUMERA Real Estate', None,
     ['DOM MITICE', 'KONTAKT'], 2900),
    ('Malacky.dc.html', 'pozemok-malacky.html', 'Priemyselný pozemok 13 000 m², Malacky – LUMERA Real Estate', None,
     ['POZEMOK MALACKY', 'KONTAKT'], 2600),
    ('Svinna.dc.html', 'pozemok-svinna.html', 'Stavebný pozemok 10 833 m², Svinná – LUMERA Real Estate', None,
     ['POZEMOK SVINNA', 'KONTAKT'], 2500),
    ('Odbojarov.dc.html', 'byt-odbojarov-prenajom.html', 'Prenájom 2-izbového bytu, Trenčín Odbojárov – LUMERA Real Estate', None,
     ['BYT ODBOJAROV', 'KONTAKT'], 2700),
    ('Teplice.dc.html', 'byt-trencianske-teplice.html', '3-izbový byt s 2 balkónmi, Trenčianske Teplice – LUMERA Real Estate', None,
     ['BYT TEPLICE', 'KONTAKT'], 2700),
    ('Vlckovce.dc.html', 'byt-vlckovce.html', '3-izbový byt, Vlčkovce – LUMERA Real Estate', None,
     ['BYT VLCKOVCE', 'KONTAKT'], 2800),
    ('Nitra.dc.html', 'pozemok-nitrianske-hrnciarovce.html', 'Priemyselný pozemok 15 843 m², Nitrianske Hrnčiarovce – LUMERA Real Estate', None,
     ['POZEMOK NITRA', 'KONTAKT'], 2700),
    ('Turna.dc.html', 'dom-trencianska-turna.html', 'Moderný rodinný dom s garážou, Trenčianska Turná – LUMERA Real Estate', None,
     ['DOM TURNA', 'KONTAKT'], 2900),
]
TITLES = {'Predat.dc.html': 'Chcem predať', 'Main.dc.html': 'Domov', 'ONas.dc.html': 'O nás', 'Ponuka.dc.html': 'Ponuka nehnuteľností',
          'Nacenenie.dc.html': 'Nacenenie', 'Vykup.dc.html': 'Výkup nehnuteľností', 'Hypoteky.dc.html': 'Hypotéky',
          'PravneSluzby.dc.html': 'Právne služby', 'Kontakt.dc.html': 'Kontakt', 'Byt28.dc.html': 'Byt 28. októbra', 'Zamarovce.dc.html': 'Pozemok Zamarovce', 'Trebichava.dc.html': 'Dom Trebichava', 'Myjava.dc.html': 'Byt Myjava', 'Mitice.dc.html': 'Dom Trenčianske Mitice', 'Malacky.dc.html': 'Pozemok Malacky', 'Svinna.dc.html': 'Pozemok Svinná', 'Odbojarov.dc.html': 'Prenájom Odbojárov', 'Teplice.dc.html': 'Byt Trenčianske Teplice', 'Vlckovce.dc.html': 'Byt Vlčkovce', 'Nitra.dc.html': 'Pozemok Nitrianske Hrnčiarovce', 'Turna.dc.html': 'Dom Trenčianska Turná'}

# where each in-page anchor lives once the site is split into pages
ANCHOR_PAGE = {'domov': 'Main.dc.html', 'sluzby': 'Main.dc.html', 'o-nas': 'ONas.dc.html', 'ponuka': 'Ponuka.dc.html',
               'hladat': 'Ponuka.dc.html', 'nacenenie': 'Nacenenie.dc.html', 'vykup': 'Vykup.dc.html',
               'hypoteka': 'Hypoteky.dc.html', 'pravne': 'PravneSluzby.dc.html', 'kontakt': 'Kontakt.dc.html', 'predat': 'Predat.dc.html', 'vyhladavac': 'Ponuka.dc.html'}
STATIC_NAME = {p[0]: p[1] for p in PAGES}

CHROME_TOP = ['HORNÝ PRUH', 'HLAVIČKA']
CHROME_BOTTOM = ['PÄTA', 'WHATSAPP']


def split_source():
    s = open(SP + '/source.dc.html').read()
    end = s.rindex('</div>\n</x-dc>')
    markers = list(re.finditer(r'<!-- ([^>]+?) -->\n', s[:end]))
    prefix, suffix = s[:markers[0].start()], s[end:]
    sections = {}
    for i, m in enumerate(markers):
        stop = markers[i + 1].start() if i + 1 < len(markers) else end
        sections[m.group(1)] = s[m.start():stop]
    return prefix, sections, suffix


def link_anchors(html, page_body_ids, chrome):
    """In chrome (header/footer) every anchor goes to its page; in content, keep it if the target is on this page."""
    def sub(m):
        a = m.group(1)
        if not chrome and a in page_body_ids:
            return m.group(0)
        target = ANCHOR_PAGE.get(a)
        return 'href="%s"' % target if target else m.group(0)
    return re.sub(r'href="#([a-z-]+)"', sub, html)


def build():
    prefix, sec, suffix = split_source()
    for name in CHROME_TOP + CHROME_BOTTOM:
        assert name in sec, name
    boards, order = {}, []
    for i, (fname, _static, title, active, names, h) in enumerate(PAGES):
        content = ''.join(sec[n] for n in names)
        ids = set(re.findall(r'id="([a-z-]+)"', content))
        top = link_anchors(''.join(sec[n] for n in CHROME_TOP), ids, True)
        bottom = link_anchors(''.join(sec[n] for n in CHROME_BOTTOM), ids, True)
        content = link_anchors(content, ids, False)
        if active:
            target = ANCHOR_PAGE[active]
            old = 'href="%s" style="color: #F7F5F0; text-decoration: none; padding: 10px 0">' % target
            assert top.count(old) == 1, (fname, old)
            top = top.replace(old, 'href="%s" aria-current="page" style="color: {{accent}}; text-decoration: none; padding: 10px 0">' % target)
            mold = 'href="%s" class="lm-mlink"' % target
            assert top.count(mold) == 1, (fname, mold)
            top = top.replace(mold, mold + ' aria-current="page"')
        pre = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, prefix, count=1)
        suf = re.sub(r'"\$preview":\{"width":1440,"height":\d+\}', '"$preview":{"width":1440,"height":%d}' % h, suffix)
        open(os.path.join(PROJ, fname), 'w').write(pre + top + content + bottom + suf)
        col, row = i % 4, i // 4
        boards[fname] = {'x': col * (1440 + 80), 'y': row * (4000 + 300), 'w': 1440, 'h': h,
                         'title': TITLES[fname], 'expand': 'fill', 'is_interactive': True}
        order.append(fname)
    # phone-width previews of two pages (not exported; the live site uses the pages above)
    for j, (src, mname, mh) in enumerate([('Main.dc.html', 'MobilDomov.dc.html', 7200), ('Byt28.dc.html', 'MobilByt28.dc.html', 3600)]):
        t = open(os.path.join(PROJ, src)).read()
        t = re.sub(r'"\$preview":\{"width":1440,"height":\d+\}', '"$preview":{"width":390,"height":%d}' % mh, t)
        open(os.path.join(PROJ, mname), 'w').write(t)
        boards[mname] = {'x': 4 * 1520 + 200 + j * (390 + 80), 'y': 0, 'w': 390, 'h': mh,
                         'title': 'Mobil – ' + TITLES[src], 'is_interactive': True}
        order.append(mname)
    idx_path = os.path.join(PROJ, 'canvas.json')
    idx = json.load(open(idx_path))
    idx['boards'], idx['order'] = boards, order
    idx['notes'] = {
        'row1': {'x': 0, 'y': -300, 'text': 'LUMERA – stránky webu', 'kind': 'title1', 'maxW': 4*1440 + 3*80},
        'mobil': {'x': 4 * 1520 + 200, 'y': -300, 'text': 'Mobil', 'kind': 'title1', 'maxW': 860},
        'detail': {'x': 0, 'y': 2 * 4300 - 300, 'text': 'Detail nehnuteľnosti', 'kind': 'title1', 'maxW': 6000},
    }
    json.dump(idx, open(idx_path, 'w'), ensure_ascii=False, separators=(',', ':'))
    return [p[0] for p in PAGES]


if __name__ == '__main__':
    print(build())
