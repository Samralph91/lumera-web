# -*- coding: utf-8 -*-
"""Local landing pages (reality-<mesto>.html), the blog, footer links and the homepage teaser.
Runs inside export.py after the core pages are written and before en_build."""
import html, json, os, re, sys

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
import seo
from seo_content import AREAS, POSTS, AUTHOR

SITE = os.path.join(SP, 'site')
BASE = seo.SITE
E = lambda s: html.escape(s, quote=True)
SK_ONLY = [a['file'] for a in AREAS] + [p['file'] for p in POSTS] + ['blog.html']
MONTHS = ['januára', 'februára', 'marca', 'apríla', 'mája', 'júna', 'júla', 'augusta', 'septembra', 'októbra', 'novembra', 'decembra']

NAVY, GOLD, GOLD_D, CREAM, INK, MUTED = '#001939', '#D9AE52', '#8A6A2B', '#F7F5F0', '#1B2533', '#4A5566'
WRAP = 'max-width: 1240px; margin: 0 auto; padding: 0 24px'
EYEBROW = 'margin: 0; font-size: 13px; font-weight: 800; letter-spacing: 0.22em; color: %s' % GOLD
H2 = "margin: 0; font-family: 'Cormorant Garamond', serif; font-weight: 700; color: %s; font-size: clamp(1.9rem, 3.4vw, 2.6rem); line-height: 1.15" % NAVY
BTN_GOLD = 'display: inline-flex; align-items: center; justify-content: center; min-height: 52px; padding: 0 26px; background: %s; color: %s; text-decoration: none; border-radius: 4px; font-weight: 800; font-size: 16px' % (GOLD, NAVY)
BTN_LINE = 'display: inline-flex; align-items: center; justify-content: center; min-height: 52px; padding: 0 26px; border: 1px solid #F7F5F0; color: #F7F5F0; text-decoration: none; border-radius: 4px; font-weight: 700; font-size: 16px'


def human_date(iso):
    y, m, d = iso.split('-')
    return '%d. %s %s' % (int(d), MONTHS[int(m) - 1], y)


def template():
    h = open(os.path.join(SITE, 'kontakt.html')).read()
    head = h[:h.index('</head>')]
    head = re.sub(r'<title>.*?</title>', '<title>%%TITLE%%</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description".*?<meta name="twitter:card"[^>]*>\n', '%%META%%', head, flags=re.S)
    body_start = h.index('</head>')
    header = h[body_start:h.index('</header>') + len('</header>')]
    header = header.replace(' aria-current="page"', '')
    header = header.replace('<a href="kontakt.html" style="color: #D9AE52;', '<a href="kontakt.html" style="color: #F7F5F0;')
    tail = h[h.index('<!-- PÄTA -->'):]
    return head, header, tail


def cards():
    h = open(os.path.join(SITE, 'ponuka.html')).read()
    out = {}
    for a in re.findall(r'<article\b.*?</article>', h, re.S):
        m = re.search(r'<a href="([^"]+\.html)"', a)
        if m:
            out[m.group(1)] = re.sub(r'<article\b[^>]*?(\s*style=)', r'<article\1', a, count=1)
    return out


def meta(page, title, desc, image=BASE + 'trencin.jpg', extra=''):
    url = BASE + page
    return ('<meta name="description" content="%s">\n<link rel="canonical" href="%s">\n'
            '<meta property="og:type" content="website">\n<meta property="og:site_name" content="LUMERA Real Estate">\n'
            '<meta property="og:locale" content="sk_SK">\n<meta property="og:url" content="%s">\n'
            '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n'
            '<meta property="og:image" content="%s">\n<meta name="twitter:card" content="summary_large_image">\n%s') % (
        E(desc), url, url, E(title), E(desc), image, extra)


def ld(obj):
    return '<script type="application/ld+json">%s</script>\n' % json.dumps(obj, ensure_ascii=False)


def crumbs(items):
    parts = []
    for i, (label, href) in enumerate(items):
        if href:
            parts.append('<a href="%s" style="color: %s">%s</a>' % (href, GOLD, E(label)))
        else:
            parts.append('<span aria-current="page">%s</span>' % E(label))
    trail = ' <span aria-hidden="true">›</span> '.join(parts)
    data = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': l, **({'item': BASE + (h if h != 'index.html' else '')} if h else {})}
        for i, (l, h) in enumerate(items)]}
    return ('<nav aria-label="Navigácia" style="font-size: 14px; color: #C7CFDB; display: flex; flex-wrap: wrap; gap: 6px">%s</nav>\n' % trail), data


def hero(eyebrow, h1, lead, crumb_html, sub=''):
    return ('<section style="background: %s; color: %s; padding: 56px 0 72px">\n<div style="%s; display: flex; flex-direction: column; gap: 18px">\n'
            '%s<p style="%s">%s</p>\n<h1 style="margin: 0; font-family: \'Cormorant Garamond\', serif; font-weight: 700; font-size: clamp(2.4rem, 5vw, 3.8rem); line-height: 1.08; max-width: 900px">%s</h1>\n'
            '%s<p style="margin: 0; font-size: 18px; line-height: 1.7; color: #D5DCE6; max-width: 760px">%s</p>\n</div>\n</section>\n') % (
        NAVY, CREAM, WRAP, crumb_html, EYEBROW, E(eyebrow), E(h1), sub, E(lead))


def cta_band(text, primary=('Nacenenie zdarma', 'nacenenie.html')):
    return ('<section style="background: %s; color: %s; padding: 64px 0">\n<div style="%s; display: flex; flex-wrap: wrap; gap: 24px; align-items: center; justify-content: space-between">\n'
            '<p style="margin: 0; font-family: \'Cormorant Garamond\', serif; font-size: clamp(1.6rem, 3vw, 2.2rem); font-weight: 700; line-height: 1.2; max-width: 680px">%s</p>\n'
            '<div class="lm-cta" style="display: flex; flex-wrap: wrap; gap: 12px"><a href="%s" style="%s">%s</a>'
            '<a href="tel:+421949888663" style="%s">Zavolať 0949 888 663</a></div>\n</div>\n</section>\n') % (
        NAVY, CREAM, WRAP, E(text), primary[1], BTN_GOLD, primary[0], BTN_LINE)


SERVICES = [('Chcem predať / prenajať', 'chcem-predat.html'), ('Nacenenie zdarma', 'nacenenie.html'), ('Výkup nehnuteľností', 'vykup.html'),
            ('Hypotéky', 'hypoteky.html'), ('Právne služby', 'pravne-sluzby.html'), ('Ponuka nehnuteľností', 'ponuka.html')]


def area_page(a, C, others):
    crumb_html, crumb_ld = crumbs([('Domov', 'index.html'), (a['h1'], None)])
    s = hero('REALITNÁ KANCELÁRIA · ' + a['short'].upper(), a['h1'], a['lead'], crumb_html)
    # text + services
    s += '<section style="padding: 80px 0">\n<div style="%s; display: flex; flex-wrap: wrap; gap: 48px">\n<div style="flex: 1 1 560px; min-width: 0; display: flex; flex-direction: column; gap: 32px">\n' % WRAP
    for h2, ps in a['body']:
        s += '<div style="display: flex; flex-direction: column; gap: 12px">\n<h2 style="%s">%s</h2>\n' % (H2, E(h2))
        s += ''.join('<p style="margin: 0; font-size: 17px; line-height: 1.75; color: %s">%s</p>\n' % (INK, E(p)) for p in ps)
        s += '</div>\n'
    s += '</div>\n<aside style="flex: 1 1 300px; min-width: 0; align-self: flex-start; background: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 28px; display: flex; flex-direction: column; gap: 6px">\n'
    s += '<p style="margin: 0 0 8px; font-size: 13px; font-weight: 800; letter-spacing: 0.16em; color: %s">NAŠE SLUŽBY</p>\n' % GOLD_D
    s += ''.join('<a href="%s" style="display: flex; justify-content: space-between; align-items: center; min-height: 46px; border-bottom: 1px solid #EFEBE1; color: %s; text-decoration: none; font-weight: 700">%s<span aria-hidden="true" style="color: %s">→</span></a>\n' % (h, NAVY, l, GOLD_D) for l, h in SERVICES)
    s += '<p style="margin: 14px 0 0; font-size: 15px; color: %s">Kancelária: Legionárska 6419, Trenčín<br><a href="tel:+421949888663" style="color: %s; font-weight: 800">0949 888 663</a> · <a href="mailto:info@lumera.sk" style="color: %s">info@lumera.sk</a></p>\n' % (MUTED, NAVY, NAVY)
    s += '</aside>\n</div>\n</section>\n'
    # listings
    items = [C[f] for f in a['listings'] if f in C]
    if items:
        s += '<section style="background: #EFEBE1; padding: 80px 0">\n<div style="%s; display: flex; flex-direction: column; gap: 28px">\n' % WRAP
        s += '<div style="display: flex; flex-wrap: wrap; gap: 12px 24px; align-items: end; justify-content: space-between"><h2 style="%s">%s</h2><a href="ponuka.html" style="color: %s; font-weight: 800">Celá ponuka →</a></div>\n' % (H2, E(a['listings_title']), GOLD_D)
        s += '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%%, 280px), 1fr)); gap: 24px">\n%s</div>\n</div>\n</section>\n' % ''.join(items)
    # FAQ
    s += '<section style="padding: 80px 0">\n<div style="max-width: 860px; margin: 0 auto; padding: 0 24px; display: flex; flex-direction: column; gap: 16px">\n<p style="%s; color: %s">ČASTÉ OTÁZKY</p>\n<h2 style="%s">%s – otázky a odpovede</h2>\n' % (EYEBROW, GOLD_D, H2, E(a['h1']))
    for q, ans in a['faq']:
        s += ('<details style="background: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 0 22px">\n'
              '<summary style="cursor: pointer; padding: 18px 0; font-weight: 800; font-size: 17px; color: %s">%s</summary>\n'
              '<p style="margin: 0 0 18px; font-size: 16px; line-height: 1.7; color: %s">%s</p>\n</details>\n') % (NAVY, E(q), INK, E(ans))
    s += '<p style="margin: 16px 0 0; font-size: 15px; color: %s">Pôsobíme aj v ďalších lokalitách: %s.</p>\n' % (
        MUTED, ', '.join('<a href="%s" style="color: %s">%s</a>' % (o['file'], GOLD_D, o['town']) for o in others))
    s += '</div>\n</section>\n'
    s += cta_band('Zistite, koľko stojí vaša nehnuteľnosť v lokalite %s – zadarmo a nezáväzne.' % a['town'])
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ans}} for q, ans in a['faq']]}
    biz = {'@context': 'https://schema.org', '@type': 'RealEstateAgent', 'name': 'LUMERA Real Estate s.r.o.', 'url': BASE,
           'telephone': '+421949888663', 'email': 'info@lumera.sk', 'image': BASE + 'trencin.jpg',
           'address': {'@type': 'PostalAddress', 'streetAddress': 'Legionárska 6419', 'postalCode': '911 01', 'addressLocality': 'Trenčín', 'addressCountry': 'SK'},
           'areaServed': {'@type': 'City', 'name': a['town']}}
    return s, ld(faq_ld) + ld(crumb_ld) + ld(biz)


def render_body(blocks):
    out = []
    for kind, val in blocks:
        if kind == 'h2':
            out.append('<h2 style="margin: 28px 0 0; font-size: 24px; font-weight: 800; color: %s; line-height: 1.3">%s</h2>' % (NAVY, E(val)))
        elif kind == 'p':
            out.append('<p style="margin: 0; font-size: 18px; line-height: 1.8; color: %s">%s</p>' % (INK, val if '<a ' in val else E(val)))
        elif kind == 'ul':
            out.append('<ul style="margin: 0; padding-left: 22px; font-size: 18px; line-height: 1.8; color: %s; display: flex; flex-direction: column; gap: 6px">%s</ul>' % (
                INK, ''.join('<li>%s</li>' % (x if '<strong>' in x else E(x)) for x in val)))
        elif kind == 'note':
            out.append('<p style="margin: 12px 0 0; font-size: 15px; line-height: 1.7; color: %s; background: #EFEBE1; border-left: 3px solid %s; padding: 14px 18px; border-radius: 0 4px 4px 0">%s</p>' % (MUTED, GOLD, E(val)))
    return '\n'.join(out) + '\n'


def post_page(p, posts):
    crumb_html, crumb_ld = crumbs([('Domov', 'index.html'), ('Blog', 'blog.html'), (p['title'], None)])
    sub = '<p style="margin: 0; font-size: 15px; color: #C7CFDB">%s · %s</p>\n' % (AUTHOR, human_date(p['date']))
    s = hero('BLOG · RADY K NEHNUTEĽNOSTIAM', p['title'], p['lead'], crumb_html, sub)
    s += '<section style="padding: 64px 0 80px">\n<article style="max-width: 760px; margin: 0 auto; padding: 0 24px; display: flex; flex-direction: column; gap: 16px">\n'
    cta = next((v for k, v in p['body'] if k == 'cta'), None)
    s += render_body([b for b in p['body'] if b[0] != 'cta'])
    s += ('<div style="margin-top: 28px; display: flex; gap: 18px; align-items: center; border-top: 1px solid #E4DFD3; padding-top: 24px">'
          '<img src="samuel.jpg" alt="" width="64" height="64" loading="lazy" style="width: 64px; height: 64px; border-radius: 50%%; object-fit: cover">'
          '<p style="margin: 0; font-size: 15px; line-height: 1.6; color: %s"><strong style="color: %s">%s</strong><br>Managing Director · Real Estate Consultant, LUMERA Real Estate</p></div>\n') % (MUTED, NAVY, AUTHOR)
    s += '</article>\n</section>\n'
    more = [q for q in posts if q is not p][:3]
    s += '<section style="background: #EFEBE1; padding: 64px 0">\n<div style="%s; display: flex; flex-direction: column; gap: 24px">\n<h2 style="%s">Ďalšie články</h2>\n' % (WRAP, H2)
    s += '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%%, 300px), 1fr)); gap: 20px">%s</div>\n</div>\n</section>\n' % ''.join(post_card(q) for q in more)
    s += cta_band(cta or 'Chcete poradiť s predajom alebo kúpou?', ('Chcem predať / prenajať', 'chcem-predat.html'))
    art = {'@context': 'https://schema.org', '@type': 'Article', 'headline': p['title'], 'description': p['desc'],
           'datePublished': p['date'], 'dateModified': p['date'], 'inLanguage': 'sk',
           'author': {'@type': 'Person', 'name': AUTHOR}, 'image': BASE + 'trencin.jpg',
           'publisher': {'@type': 'Organization', 'name': 'LUMERA Real Estate s.r.o.', 'logo': {'@type': 'ImageObject', 'url': BASE + 'logo.png'}},
           'mainEntityOfPage': BASE + p['file']}
    return s, ld(art) + ld(crumb_ld)


def post_card(p):
    return ('<a href="%s" style="display: flex; flex-direction: column; gap: 10px; background: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 24px; text-decoration: none">'
            '<span style="font-size: 13px; color: %s; font-weight: 700">%s</span>'
            '<span style="font-size: 19px; font-weight: 800; color: %s; line-height: 1.35">%s</span>'
            '<span style="font-size: 15px; line-height: 1.6; color: %s">%s</span>'
            '<span style="margin-top: auto; color: %s; font-weight: 800">Čítať článok →</span></a>') % (
        p['file'], GOLD_D, human_date(p['date']), NAVY, E(p['title']), MUTED, E(p['desc']), GOLD_D)


def blog_index(posts):
    crumb_html, crumb_ld = crumbs([('Domov', 'index.html'), ('Blog', None)])
    s = hero('BLOG', 'Rady a tipy k nehnuteľnostiam',
             'Praktické články o predaji, kúpe a financovaní nehnuteľností – zrozumiteľne a z praxe realitnej kancelárie v Trenčíne.', crumb_html)
    s += '<section style="padding: 72px 0 88px">\n<div style="%s">\n<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%%, 340px), 1fr)); gap: 24px">%s</div>\n</div>\n</section>\n' % (
        WRAP, ''.join(post_card(p) for p in posts))
    s += cta_band('Máte otázku, na ktorú tu nenájdete odpoveď? Zavolajte nám.')
    return s, ld(crumb_ld)


FOOT_MARK = '<span style="border-top: 1px solid #12305A; padding-top: 20px">'


def footer_links():
    areas = ' · '.join('<a href="%s" style="color: #C7CFDB">%s</a>' % (a['file'], a['town']) for a in AREAS)
    return ('<div class="lm-areas" style="display: flex; flex-wrap: wrap; gap: 6px 14px; line-height: 2">'
            '<span style="color: %s; font-weight: 800">Reality v okolí:</span> %s · <a href="blog.html" style="color: #C7CFDB">Blog</a></div>\n') % (GOLD, areas)


def home_teaser():
    links = ''.join('<a href="%s" style="display: inline-flex; align-items: center; min-height: 44px; padding: 0 16px; border: 1px solid #CFC8B8; border-radius: 4px; background: #FFFFFF; color: %s; text-decoration: none; font-weight: 700">%s</a>' % (
        a['file'], NAVY, a['town']) for a in AREAS)
    return ('<!-- BLOG TEASER -->\n<section style="padding: 88px 0; background: #EFEBE1">\n<div style="%s; display: flex; flex-direction: column; gap: 28px">\n'
            '<div style="display: flex; flex-direction: column; gap: 12px"><p style="%s; color: %s">RADY A TIPY</p><h2 style="%s">Užitočné články pre predávajúcich aj kupujúcich</h2></div>\n'
            '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%%, 280px), 1fr)); gap: 20px">%s</div>\n'
            '<div style="display: flex; flex-direction: column; gap: 12px; margin-top: 12px"><h3 style="margin: 0; font-size: 18px; font-weight: 800; color: %s">Realitná kancelária pre Trenčín a okolie</h3>'
            '<div style="display: flex; flex-wrap: wrap; gap: 10px">%s</div></div>\n</div>\n</section>\n%s<!-- /BLOG TEASER -->\n\n') % (
        WRAP, EYEBROW, GOLD_D, H2, ''.join(post_card(p) for p in POSTS[:4]), NAVY, links, __import__('ai').faq_block())


def build():
    head, header, tail = template()
    C = cards()
    pages = []
    for a in AREAS:
        body, extra = area_page(a, C, [o for o in AREAS if o is not a])
        pages.append((a['file'], a['title'], meta(a['file'], a['title'], a['desc'], extra=extra), body))
    for p in POSTS:
        body, extra = post_page(p, POSTS)
        t = p['title'] + ' | LUMERA Real Estate'
        pages.append((p['file'], t, meta(p['file'], t, p['desc'], extra=extra), body))
    body, extra = blog_index(POSTS)
    t = 'Blog – rady k predaju, kúpe a hypotékam | LUMERA Real Estate'
    pages.append(('blog.html', t, meta('blog.html', t, 'Praktické rady k predaju a kúpe nehnuteľností, daniam a hypotékam od realitnej kancelárie LUMERA Real Estate z Trenčína.', extra=extra), body))
    for f, title, m, body in pages:
        open(os.path.join(SITE, f), 'w').write(head.replace('%%TITLE%%', E(title)).replace('%%META%%', m) + header + '\n\n' + body + '\n' + tail)
    # footer links on every page + homepage teaser
    for f in os.listdir(SITE):
        if not f.endswith('.html'):
            continue
        path = os.path.join(SITE, f)
        h = open(path).read()
        if FOOT_MARK in h and 'class="lm-areas"' not in h:
            h = h.replace(FOOT_MARK, footer_links() + FOOT_MARK, 1)
        if f == 'index.html' and '<!-- BLOG TEASER -->' not in h:
            h = h.replace('<!-- PÄTA -->', home_teaser() + '<!-- PÄTA -->', 1)
        open(path, 'w').write(h)
    # sitemap
    sm_path = os.path.join(SITE, 'sitemap.xml')
    sm = open(sm_path).read()
    lastmod = re.search(r'<lastmod>([^<]+)</lastmod>', sm).group(1)
    rows = ''.join('<url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n' % (
        BASE + f, lastmod, '0.8' if f.startswith('reality-') else '0.6') for f, *_ in pages)
    open(sm_path, 'w').write(sm.replace('</urlset>', rows + '</urlset>'))
    print('seo pages', len(pages))


if __name__ == '__main__':
    build()
