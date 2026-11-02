# -*- coding: utf-8 -*-
"""Visibility for AI assistants and Bing: llms.txt, robots.txt, IndexNow key, homepage FAQ (+FAQPage data)."""
import html, json, os

SITE = 'https://lumera.sk/'
INDEXNOW_KEY = '7f3c9a2e5b8d4f16a0c2e9b7d4a1f358'

FAQ = [
    ('Kde sídli realitná kancelária LUMERA Real Estate?',
     'Kancelária LUMERA Real Estate je v Trenčíne na adrese Legionárska 6419, 911 01 Trenčín. Stretnutie si môžete dohodnúť na telefóne 0949 888 663 alebo e-mailom na info@lumera.sk.'),
    ('Aké služby ponúka LUMERA Real Estate?',
     'Predaj, kúpu, prenájom a výkup bytov, rodinných domov, pozemkov a komerčných nehnuteľností. K tomu bezplatné nacenenie, profesionálne fotky a zábery z dronu, home staging, právny servis pri prevode (zmluvy, kataster) a hypotekárne poradenstvo – všetko na jednom mieste.'),
    ('V akých lokalitách pôsobíte?',
     'Hlavne v Trenčíne a okolí – v Trenčianskych Tepliciach, Nemšovej, Dubnici nad Váhom, Bánovciach nad Bebravou a v okolitých obciach. Predávame aj nehnuteľnosti v iných regiónoch Slovenska, napríklad v Myjave, Malackách, pri Trnave a pri Nitre.'),
    ('Koľko stojí nacenenie nehnuteľnosti?',
     'Nacenenie je zadarmo a nezáväzné. Stačí vyplniť krátky formulár na lumera.sk/nacenenie.html a odhad trhovej ceny pošleme do 24 hodín.'),
    ('Vykupujete nehnuteľnosti?',
     'Áno. Ak potrebujete predať rýchlo – aj pri dedičstve, spoluvlastníctve, exekúcii alebo ťarche – pripravíme záväznú ponuku na výkup a prevod právne vybavíme.'),
    ('Kto stojí za realitnou kanceláriou LUMERA?',
     'Kanceláriu vedie jej majiteľ a konateľ Samuel Bucha, ktorý je zároveň realitným maklérom. S klientmi pracuje aj maklérka Katarína Ribovičová.'),
]


def faq_block():
    items = ''.join(
        '<details style="background: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 0 22px">'
        '<summary style="cursor: pointer; padding: 18px 0; font-weight: 800; font-size: 17px; color: #001939">%s</summary>'
        '<p style="margin: 0 0 18px; font-size: 16px; line-height: 1.7; color: #1B2533">%s</p></details>\n' % (html.escape(q), html.escape(a))
        for q, a in FAQ)
    data = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    return ('<section style="padding: 88px 0">\n<div style="max-width: 860px; margin: 0 auto; padding: 0 24px; display: flex; flex-direction: column; gap: 14px">\n'
            '<p style="margin: 0; font-size: 13px; font-weight: 800; letter-spacing: 0.22em; color: #8A6A2B">ČASTÉ OTÁZKY</p>\n'
            '<h2 style="margin: 0 0 8px; font-family: \'Cormorant Garamond\', serif; font-weight: 700; color: #001939; font-size: clamp(1.9rem, 3.4vw, 2.6rem); line-height: 1.15">'
            'Realitná kancelária LUMERA v Trenčíne – otázky a odpovede</h2>\n%s</div>\n'
            '<script type="application/ld+json">%s</script>\n</section>\n') % (items, json.dumps(data, ensure_ascii=False))


ROBOTS = '''User-agent: *
Allow: /

# AI assistants and search engines are welcome
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: GPTBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Bingbot
Allow: /

Sitemap: https://lumera.sk/sitemap.xml
'''


def llms_txt():
    import listing
    from seo_content import AREAS, POSTS
    lines = [
        '# LUMERA Real Estate – realitná kancelária Trenčín', '',
        '> LUMERA Real Estate s.r.o. je realitná kancelária v Trenčíne (Slovensko). Predaj, kúpa, prenájom a výkup nehnuteľností, '
        'bezplatné nacenenie, home staging, právny servis pri prevode a hypotekárne poradenstvo pod jednou strechou. '
        'Pôsobí v Trenčíne a okolí (Trenčianske Teplice, Nemšová, Dubnica nad Váhom, Bánovce nad Bebravou) aj v ďalších regiónoch Slovenska.', '',
        '- Kancelária: Legionárska 6419, 911 01 Trenčín',
        '- Telefón: +421 949 888 663 (Samuel Bucha, majiteľ, konateľ a maklér)',
        '- E-mail: info@lumera.sk',
        '- Firma: LUMERA Real Estate s.r.o., IČO 57307440, sídlo Sedličná 91, 913 11 Trenčianske Stankovce',
        '- Web: https://lumera.sk/ (anglicky: https://lumera.sk/en/)',
        '- Facebook: https://www.facebook.com/share/1A1Pwqz7iJ/',
        '- Instagram: https://www.instagram.com/samuelbucha_realitne_sluzby/',
        '- Recenzie klientov z Google sú na úvodnej stránke webu', '',
        '## Služby',
        '- [Ponuka nehnuteľností s vyhľadávaním](%sponuka.html)' % SITE,
        '- [Chcem predať alebo prenajať](%schcem-predat.html): trhová cena, fotky a dron, home staging, obhliadky, zmluvy, hypotéka pre kupujúceho' % SITE,
        '- [Nacenenie nehnuteľnosti zdarma do 24 hodín](%snacenenie.html)' % SITE,
        '- [Výkup nehnuteľností](%svykup.html)' % SITE,
        '- [Hypotéky a hypokalkulačka](%shypoteky.html)' % SITE,
        '- [Právne služby](%spravne-sluzby.html)' % SITE,
        '- [O nás – Samuel Bucha](%so-nas.html)' % SITE,
        '- [Kontakt](%skontakt.html)' % SITE, '',
        '## Lokality', ] + ['- [%s](%s%s)' % (a['h1'], SITE, a['file']) for a in AREAS] + ['', '## Aktuálna ponuka']
    for key, L in listing.LISTINGS.items():
        if listing.is_sold(key):
            continue
        import pages
        static = next(s for d, s, *_ in pages.PAGES if d[:-8].lower() == key)
        lines.append('- [%s – %s](%s%s): %s' % (L['title'], L['place'], SITE, static, L['price']))
    lines += ['', '## Časté otázky'] + ['- **%s** %s' % (q, a) for q, a in FAQ]
    lines += ['', '## Články'] + ['- [%s](%s%s)' % (p['title'], SITE, p['file']) for p in POSTS]
    return '\n'.join(lines) + '\n'


def write(out_dir):
    open(os.path.join(out_dir, 'robots.txt'), 'w').write(ROBOTS)
    open(os.path.join(out_dir, 'llms.txt'), 'w').write(llms_txt())
    open(os.path.join(out_dir, INDEXNOW_KEY + '.txt'), 'w').write(INDEXNOW_KEY)
