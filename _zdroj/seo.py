"""Search engines + social sharing: per-page meta, Open Graph, structured data, sitemap.xml, robots.txt."""
import datetime, html, json, re

SITE = 'https://lumera.sk/'

DESC = {
    'index.html': 'Realitná kancelária LUMERA Real Estate v Trenčíne – predaj, kúpa, prenájom a výkup nehnuteľností, právny servis a hypotekárne poradenstvo pod jednou strechou.',
    'o-nas.html': 'Spoznajte realitnú kanceláriu LUMERA Real Estate a jej zakladateľa Samuela Buchu – individuálny prístup, znalosť trhu v Trenčíne a okolí a férové jednanie.',
    'ponuka.html': 'Aktuálna ponuka bytov, rodinných domov, pozemkov a komerčných nehnuteľností na predaj a prenájom v Trenčíne a okolí. Vyhľadávanie podľa ceny, lokality a výmery.',
    'chcem-predat.html': 'Chcete predať alebo prenajať nehnuteľnosť? Trhová cena, fotky a dron, home staging, obhliadky, zmluvy aj hypotéka pre kupujúceho – kompletný servis LUMERA.',
    'nacenenie.html': 'Zistite, koľko stojí vaša nehnuteľnosť. Bezplatné a nezáväzné nacenenie bytu, domu alebo pozemku v Trenčíne a okolí do 24 hodín.',
    'vykup.html': 'Rýchly výkup nehnuteľností v Trenčíne a okolí – bez čakania na kupca, aj pri exekúcii, dedičstve či ťarche. Záväzná ponuka a právne vybavený prevod.',
    'hypoteky.html': 'Hypokalkulačka a bezplatné hypotekárne poradenstvo – porovnáme ponuky bánk a vybavíme hypotéku od žiadosti až po čerpanie.',
    'pravne-sluzby.html': 'Právne služby pri prevode nehnuteľností – rezervačné a kúpne zmluvy, preverenie listu vlastníctva, návrh na vklad do katastra.',
    'kontakt.html': 'Kontakt na realitnú kanceláriu LUMERA Real Estate – Legionárska 6419, 911 01 Trenčín, tel. 0949 888 663, info@lumera.sk.',
}
PRIORITY = {'index.html': '1.0', 'ponuka.html': '0.9', 'chcem-predat.html': '0.8', 'nacenenie.html': '0.8', 'vykup.html': '0.8'}


def listing_meta(L):
    facts = dict(L['facts'])
    bits = [L['price']]
    for k in ('Výmera', 'Výmera bytu', 'Úžitková plocha'):
        if k in facts:
            bits.append(facts[k].split(' (')[0]); break
    r = facts.get('Počet izieb')
    if r:
        bits.append('1 izba' if r == '1' else r + (' izby' if r in ('2', '3', '4') else ' izieb'))
    desc = '%s – %s. %s. %s' % (L['title'], L['place'], ' · '.join(bits), L['desc'][0])
    if len(desc) > 290:
        desc = desc[:290].rsplit(' ', 1)[0].rstrip(',.;–') + '…'
    return desc, SITE + 'img/%s/%s' % (L['folder'], L['photos'][0][0])


def head_tags(static_name, title, desc, image):
    url = SITE + ('' if static_name == 'index.html' else static_name)
    e = lambda s: html.escape(s, quote=True)
    tags = [
        '<meta name="description" content="%s">' % e(desc),
        '<link rel="canonical" href="%s">' % url,
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="LUMERA Real Estate">',
        '<meta property="og:locale" content="sk_SK">',
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:title" content="%s">' % e(title),
        '<meta property="og:description" content="%s">' % e(desc),
        '<meta property="og:image" content="%s">' % image,
        '<meta name="twitter:card" content="summary_large_image">',
    ]
    if static_name == 'index.html':
        org = {
            '@context': 'https://schema.org', '@type': 'RealEstateAgent', 'name': 'LUMERA Real Estate s.r.o.',
            'url': SITE, 'logo': SITE + 'logo.png', 'image': SITE + 'trencin.jpg',
            'telephone': '+421949888663', 'email': 'info@lumera.sk',
            'address': {'@type': 'PostalAddress', 'streetAddress': 'Legionárska 6419', 'postalCode': '911 01',
                        'addressLocality': 'Trenčín', 'addressCountry': 'SK'},
            'areaServed': [{'@type': 'City', 'name': c} for c in ('Trenčín', 'Trenčianske Teplice', 'Nemšová', 'Dubnica nad Váhom', 'Bánovce nad Bebravou')],
            'founder': {'@type': 'Person', 'name': 'Samuel Bucha', 'jobTitle': 'Managing Director, Real Estate Consultant'},
            'description': 'Realitná kancelária v Trenčíne – predaj, kúpa, prenájom a výkup nehnuteľností, bezplatné nacenenie, právny servis a hypotekárne poradenstvo.',
            'legalName': 'LUMERA Real Estate s.r.o.', 'taxID': '57307440',
            'knowsAbout': ['predaj nehnuteľností', 'nacenenie nehnuteľností', 'výkup nehnuteľností', 'hypotéky', 'home staging'],
            'sameAs': ['https://www.facebook.com/share/1A1Pwqz7iJ/', 'https://www.instagram.com/samuelbucha_realitne_sluzby/',
                       'https://www.nehnutelnosti.sk/realitna-kancelaria/lumera-real-estate-sro/centrala/o-firme/9caeb98b-aa6d-427b-87d2-39b074880e59'],
        }
        tags.append('<script type="application/ld+json">%s</script>' % json.dumps(org, ensure_ascii=False))
    return '\n'.join(tags) + '\n'


def sitemap(files):
    today = datetime.date.today().isoformat()
    rows = ''.join('<url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n'
                   % (SITE + ('' if f == 'index.html' else f), today, PRIORITY.get(f, '0.6' if f not in ('cookies.html', 'ochrana-osobnych-udajov.html') else '0.2'))
                   for f in files)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '</urlset>\n'


ROBOTS = 'User-agent: *\nAllow: /\n\nSitemap: https://lumera.sk/sitemap.xml\n'
