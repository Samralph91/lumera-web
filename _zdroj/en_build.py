# -*- coding: utf-8 -*-
"""Build lumera.sk/en/ from the built Slovak site and add a working SK/EN switch to both versions.
Run after export.py:  python3 en_build.py"""
import html, json, os, re, sys
from html.parser import HTMLParser

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
from tr_en import T as T1
from tr_en2 import T as T2
from tr_en3 import T as T3
import listing, seo
from seo_pages import SK_ONLY

SITE = os.path.join(SP, 'site')
EN = os.path.join(SITE, 'en')
T = {**T1, **T2, **T3}
T.update({
    'Ďakujeme, správu sme dostali.': 'Thank you, we have received your message.',
    'Ozveme sa vám čo najskôr, zvyčajne ešte v ten istý pracovný deň.': "We'll get back to you as soon as possible, usually the same working day.",
    'Zavrieť': 'Close',
    'PREDANÉ': 'SOLD', 'Predané': 'Sold', 'Podobnú nehnuteľnosť vám radi nájdeme.': "We'd be happy to find you a similar property.",
    'Chcem podobnú nehnuteľnosť': 'I want a similar property',
    'Reality v okolí:': 'Areas we cover (Slovak):', 'Blog': 'Blog (Slovak)',
    'LOKALITA': 'LOCATION', 'Zadajte obec alebo mesto.': 'Enter a town or village.', 'Odosielam…': 'Sending…',
    '3. z 6': '3rd of 6', '2 596 € / m²': '€2,596 / m²', '70,77 € / m²': '€70.77 / m²', '186 € / m²': '€186 / m²',
    '77,64 m²': '77.64 m²', '27,86 m²': '27.86 m²', '105,50 m²': '105.50 m²', '2,5 m²': '2.5 m²',
    '13\xa0000 m²': '13,000 m²', '10\xa0833 m²': '10,833 m²', '15\xa0843 m²': '15,843 m²',
    '13 000 m²': '13,000 m²', '15 843 m²': '15,843 m²', 'cca 110 m²': 'approx. 110 m²',
})
TEXT_ATTRS = ('alt', 'aria-label', 'placeholder', 'title', 'data-v')
ASSET_RX = re.compile(r'((?:src|href|content)=")(?!https?:|mailto:|tel:|#|\.\./|data:)((?:img/|logo\.png|trencin\.jpg|samuel\.jpg)[^"]*)"')
RX_FOTKA = re.compile(r'^Fotka (\d+)$')
RX_HYPO = re.compile(r'^Hypotéka od ([\d\xa0 ]+) € / mes\.\*$')
missing = set()


def tr(s):
    """Translate one stripped string; returns None when unknown."""
    if s in T:
        return T[s]
    m = RX_FOTKA.match(s)
    if m:
        return 'Photo ' + m.group(1)
    n = s.replace('\xa0', ' ')
    if n != s and n in T:
        return T[n]
    m = re.match(r'^(\d{1,3}(?: \d{3})*)(,\d+)? €( / m²| / mesiac| bez DPH)?$', n)
    if m:
        tail = {None: '', ' / m²': ' / m²', ' / mesiac': ' / month', ' bez DPH': ' excl. VAT'}[m.group(3)]
        return '€' + m.group(1).replace(' ', ',') + (m.group(2) or '').replace(',', '.') + tail
    m = RX_HYPO.match(s)
    if m:
        return 'Mortgage from €%s / month*' % m.group(1).replace('\xa0', ',').replace(' ', ',')
    return None


def tr_keep_ws(d):
    t = d.strip()
    if not t or not re.search(r'[A-Za-zÀ-ž€]', t):
        return d
    e = tr(html.unescape(t)) if '&' in t else tr(t)
    if e is None:
        missing.add(t)
        return d
    lead = d[:len(d) - len(d.lstrip())]
    trail = d[len(d.rstrip()):]
    return lead + (html.escape(e, quote=False) if '&' in t or '<' in e else e) + trail


class Rewriter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out, self.raw = [], None

    def _attrs(self, tag, attrs):
        a = dict(attrs)
        res = []
        for k, v in attrs:  # HTMLParser hands over unescaped values
            if v is None:
                res.append(' ' + k); continue
            if k in TEXT_ATTRS and re.search(r'[A-Za-zÀ-ž]', v):
                e = tr(v)
                if e is None and k != 'data-v':
                    missing.add(v)
                v = e if e is not None else v
            elif k == 'value' and tag == 'input' and a.get('name') == '_subject':
                v = T.get(v, v)
            elif k == 'content' and tag == 'meta' and a.get('property') == 'og:title':
                v = T.get(v, v)
            res.append(' %s="%s"' % (k, v.replace('&', '&amp;').replace('"', '&quot;')))
        return ''.join(res)

    def handle_starttag(self, tag, attrs):
        self.out.append('<%s%s>' % (tag, self._attrs(tag, attrs)))
        if tag in ('script', 'style'):
            self.raw = tag

    def handle_startendtag(self, tag, attrs):
        self.out.append('<%s%s/>' % (tag, self._attrs(tag, attrs)))

    def handle_endtag(self, tag):
        self.raw = None
        self.out.append('</%s>' % tag)

    def handle_data(self, d):
        if self.raw == 'script':
            self.out.append(tr_js(d))
        elif self.raw:
            self.out.append(d)
        else:
            self.out.append(tr_keep_ws(d))

    def handle_entityref(self, n): self.out.append('&%s;' % n)
    def handle_charref(self, n): self.out.append('&#%s;' % n)
    def handle_comment(self, d): self.out.append('<!--%s-->' % d)
    def handle_decl(self, d): self.out.append('<!%s>' % d)


JS_LIT = re.compile(r"""(===\s*)?(['"])((?:(?!\2)[^\\\n]|\\.)*)\2""")


def tr_js(code):
    if 'ld+json' in code[:0]:
        return code
    code = code.replace("' Z 3 · '", "' OF 3 · '").replace("toLocaleString('sk-SK'", "toLocaleString('en-GB'")
    code = code.replace("return v.toLocaleString('en-GB',{minimumFractionDigits:d,maximumFractionDigits:d})+' €'", "return '€'+v.toLocaleString('en-GB',{minimumFractionDigits:d,maximumFractionDigits:d})")
    code = code.replace("'ponuka.html?'", "'ponuka.html?'")

    def sub(m):
        if m.group(1):  # comparisons against data values stay Slovak
            return m.group(0)
        s = m.group(3)
        if not re.search(r'[A-Za-zÀ-ž]', s):
            return m.group(0)
        e = tr(s)
        if e is None:
            return m.group(0)
        return m.group(2) + e.replace('\\', '\\\\').replace(m.group(2), '\\' + m.group(2)) + m.group(2)
    return JS_LIT.sub(sub, code)


SWITCH_TOP = '<span style="display: flex; gap: 10px; font-weight: 700"><span style="color: #D9AE52">SK</span><span>EN</span></span>'


def switch_top(lang, sk_href, en_href):
    on, off = 'color: #D9AE52; text-decoration: none', 'color: #C7CFDB; text-decoration: none'
    return ('<span style="display: flex; gap: 10px; font-weight: 700">'
            '<a href="%s" hreflang="sk" lang="sk" %sstyle="%s">SK</a>'
            '<a href="%s" hreflang="en" lang="en" %sstyle="%s">EN</a></span>') % (
        sk_href, 'aria-current="true" ' if lang == 'sk' else '', on if lang == 'sk' else off,
        en_href, 'aria-current="true" ' if lang == 'en' else '', on if lang == 'en' else off)


def switch_mobile(lang, sk_href, en_href):
    b = 'flex: 1; display: flex; align-items: center; justify-content: center; min-height: 44px; border-radius: 4px; text-decoration: none; font-weight: 800; font-size: 14px; letter-spacing: 0.08em; '
    on, off = b + 'background: #F7F5F0; color: #001939', b + 'border: 1px solid #2A4C7E; color: #F7F5F0'
    return ('<div style="display: flex; gap: 10px; margin-top: 18px" aria-label="%s">'
            '<a href="%s" hreflang="sk" lang="sk" style="%s">SLOVENSKY</a>'
            '<a href="%s" hreflang="en" lang="en" style="%s">ENGLISH</a></div>\n') % (
        'Jazyk' if lang == 'sk' else 'Language', sk_href, on if lang == 'sk' else off, en_href, on if lang == 'en' else off)


def add_switch(h, lang, page):
    sk_href = ('../' if lang == 'en' else '') + page
    en_href = ('' if lang == 'en' else 'en/') + page
    if page == 'index.html':
        sk_href = '../' if lang == 'en' else 'index.html'
        en_href = 'index.html' if lang == 'en' else 'en/'
    if page in SK_ONLY:  # Slovak-only content (local pages, blog)
        en_href = 'en/'
    h = h.replace(SWITCH_TOP, switch_top(lang, sk_href, en_href))
    # mobile: language buttons at the end of the drawer
    h = re.sub(r'(<nav aria-label="(?:Mobilná navigácia|Mobile navigation)".*?)(</nav>)',
               lambda m: m.group(1) + switch_mobile(lang, sk_href, en_href) + m.group(2), h, count=1, flags=re.S)
    # standalone pages (cookies/privacy): small switch next to "back"
    if 'class="back"' in h and 'hreflang="en"' not in h:
        h = h.replace('<a class="back"', '<span style="display:flex;gap:20px;align-items:center"><a href="%s" hreflang="%s" class="back">%s</a><a class="back"' % (
            en_href if lang == 'sk' else sk_href, 'en' if lang == 'sk' else 'sk', 'EN' if lang == 'sk' else 'SK'), 1)
        h = re.sub(r'(<a class="back"[^>]*>[^<]*</a>)', r'\1</span>', h, count=1)
    # hreflang alternates
    url_sk = seo.SITE + ('' if page == 'index.html' else page)
    url_en = seo.SITE + 'en/' + ('' if page == 'index.html' else page)
    alt = ('<link rel="alternate" hreflang="sk" href="%s">\n<link rel="alternate" hreflang="en" href="%s">\n'
           '<link rel="alternate" hreflang="x-default" href="%s">\n') % (url_sk, url_en, url_sk)
    if 'hreflang="x-default"' not in h and page not in SK_ONLY:
        h = h.replace('</head>', alt + '</head>', 1)
    return h


def listing_meta_en(L):
    facts = dict(L['facts'])
    bits = [T.get(L['price'], L['price'])]
    for k in ('Výmera', 'Výmera bytu', 'Úžitková plocha'):
        if k in facts:
            v = facts[k].split(' (')[0]
            bits.append(T.get(v, v)); break
    r = facts.get('Počet izieb')
    if r:
        bits.append(r + (' room' if r == '1' else ' rooms'))
    d0 = T.get(L['desc'][0], '')
    desc = '%s – %s. %s. %s' % (T.get(L['title'], L['title']), T.get(L['place'], L['place']), ' · '.join(bits), d0)
    if len(desc) > 290:
        desc = desc[:290].rsplit(' ', 1)[0].rstrip(',.;–') + '…'
    return desc


def fix_head_en(h, page):
    h = h.replace('<html lang="sk">', '<html lang="en">', 1)
    url_sk = seo.SITE + ('' if page == 'index.html' else page)
    url_en = seo.SITE + 'en/' + ('' if page == 'index.html' else page)
    h = h.replace('<link rel="canonical" href="%s">' % url_sk, '<link rel="canonical" href="%s">' % url_en)
    h = h.replace('<meta property="og:url" content="%s">' % url_sk, '<meta property="og:url" content="%s">' % url_en)
    h = h.replace('content="sk_SK"', 'content="en_GB"')
    # descriptions: translate whole string, or rebuild for listings
    def desc_sub(m):
        v = html.unescape(m.group(2))
        e = T.get(v)
        if e is None:
            for L in listing.LISTINGS.values():
                if seo.listing_meta(L)[0] == v:
                    e = listing_meta_en(L); break
        if e is None:
            missing.add('META:' + v[:80]); e = v
        return m.group(1) + html.escape(e, quote=True) + '"'
    h = re.sub(r'(<meta (?:name="description"|property="og:description") content=")([^"]*)"', desc_sub, h)
    # forms
    h = h.replace('https://lumera.sk/nacenenie.html?nacenenie=odoslane', 'https://lumera.sk/en/nacenenie.html?nacenenie=odoslane')
    h = re.sub(r'value="https://lumera\.sk/([a-z0-9-]+\.html)\?odoslane=1"', r'value="https://lumera.sk/en/\1?odoslane=1"', h)
    h = h.replace('"areaServed": "Trenčín a okolie"', '"areaServed": "Trenčín and surroundings"')
    # assets live one level up
    h = ASSET_RX.sub(lambda m: m.group(1) + '../' + m.group(2) + '"', h)
    h = h.replace("url('img/", "url('../img/").replace('url(img/', 'url(../img/').replace('url("img/', 'url("../img/')
    h = h.replace('<link rel="icon" href="logo.png">', '<link rel="icon" href="../logo.png">')
    return h


def main():
    os.makedirs(EN, exist_ok=True)
    pages = sorted(f for f in os.listdir(SITE) if f.endswith('.html'))
    for f in pages:
        sk = open(os.path.join(SITE, f)).read()
        sk = re.sub(r'<link rel="alternate" hreflang[^>]*>\n', '', sk)
        if f in SK_ONLY:
            open(os.path.join(SITE, f), 'w').write(add_switch(sk, 'sk', f))
            continue
        p = Rewriter(); p.feed(sk); p.close()
        en = fix_head_en(''.join(p.out), f)
        # the parser re-serialises tags; keep the doctype line intact
        # international format of phone numbers for foreign visitors
        en = re.sub(r'<!-- BLOG TEASER -->.*?<!-- /BLOG TEASER -->\n', '', en, flags=re.S)
        for sk_only in SK_ONLY:
            en = en.replace('href="%s"' % sk_only, 'href="../%s"' % sk_only)
        en = en.replace('0949 888 663', '+421 949 888 663').replace('0904 255 252', '+421 904 255 252')
        open(os.path.join(EN, f), 'w').write(add_switch(en, 'en', f))
        open(os.path.join(SITE, f), 'w').write(add_switch(sk, 'sk', f))
    # sitemap with both languages
    sm = open(os.path.join(SITE, 'sitemap.xml')).read()
    if '/en/' not in sm:
        rows = re.findall(r'<url>.*?</url>\n', sm)
        en_rows = [r.replace('<loc>https://lumera.sk/', '<loc>https://lumera.sk/en/') for r in rows
                   if not any('/' + f + '<' in r for f in SK_ONLY)]
        sm = sm.replace('</urlset>', ''.join(en_rows) + '</urlset>')
        open(os.path.join(SITE, 'sitemap.xml'), 'w').write(sm)
    if missing:
        print('UNTRANSLATED (%d):' % len(missing))
        for s in sorted(missing):
            print('  ', repr(s[:140]))
    print('en ok', len(pages), 'pages')


if __name__ == '__main__':
    main()
