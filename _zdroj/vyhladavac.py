"""On-site property search for the Ponuka page – canvas (dc) and lumera.sk (static) versions.

Card texts/images come from allListings in source.dc.html; filter facts live in FACTS below (keyed by detail page).
"""
import json, re

# href (canvas artboard) -> filter facts
FACTS = {
    'Byt28.dc.html':      dict(deal='kupa', type='byt', okres='Trenčín', price=139900, area=67, rooms=3, nov=False, park=False, order=1, kom=False),
    'Zamarovce.dc.html':  dict(deal='kupa', type='pozemok', okres='Trenčín', price=143400, area=770, rooms=0, nov=False, park=False, order=2, kom=False),
    'Trebichava.dc.html': dict(deal='kupa', type='dom', okres='Bánovce nad Bebravou', price=17990, area=50, rooms=0, nov=False, park=False, order=3, kom=False),
    'Myjava.dc.html':     dict(deal='kupa', type='byt', okres='Myjava', price=69900, area=34, rooms=1, nov=False, park=False, order=4, kom=False),
    'Mitice.dc.html':     dict(deal='kupa', type='dom', okres='Trenčín', price=None, area=180, rooms=5, nov=False, park=True, order=5, kom=False),
    'Malacky.dc.html':    dict(deal='kupa', type='pozemok', okres='Malacky', price=920000, area=13000, rooms=0, nov=False, park=False, order=6, kom=True),
    'Svinna.dc.html':     dict(deal='kupa', type='pozemok', okres='Trenčín', price=None, area=10833, rooms=0, nov=False, park=False, order=7, kom=False),
    'Teplice.dc.html':    dict(deal='kupa', type='byt', okres='Trenčín', price=None, area=94, rooms=3, nov=False, park=False, order=8, kom=False),
    'Vlckovce.dc.html':   dict(deal='kupa', type='byt', okres='Trnava', price=199900, area=78, rooms=3, nov=False, park=False, order=9, kom=False),
    'Nitra.dc.html':      dict(deal='kupa', type='pozemok', okres='Nitra', price=550000, area=15843, rooms=0, nov=False, park=False, order=10, kom=True),
    'Turna.dc.html':      dict(deal='kupa', type='dom', okres='Trenčín', price=459900, area=110, rooms=4, nov=True, park=True, order=11, kom=False),
    'Odbojarov.dc.html':  dict(deal='prenajom', type='byt', okres='Trenčín', price=650, area=45, rooms=2, nov=True, park=True, order=12, kom=False),
}
OKRESY = ['Trenčín', 'Bánovce nad Bebravou', 'Myjava', 'Malacky', 'Nitra', 'Trnava']
DEALS = [('kupa', 'Kúpa'), ('prenajom', 'Prenájom'), ('', 'Všetko')]
TYPES = [('', 'Všetky typy'), ('byt', 'Byt'), ('dom', 'Rodinný dom'), ('pozemok', 'Pozemok'), ('komercne', 'Komerčné / priemyselné'), ('nebyt', 'Nebytový priestor')]
ROOMS = [('', 'Všetky'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5+')]
SORTS = [('odp', 'Odporúčané'), ('lac', 'Najlacnejšie'), ('dra', 'Najdrahšie'), ('vym', 'Najväčšia výmera')]

LABEL = 'font-size: 14px; font-weight: 800; color: #001939'
INPUT = ('height: 48px; padding: 0 12px; border-radius: 4px; border: 1px solid #CFC8B8; background: #FFFFFF; '
         'font-size: 16px; font-family: inherit; color: #1B2533; width: 100%; box-sizing: border-box; min-width: 0')
PILL_ON = ('min-height: 44px; padding: 0 18px; border-radius: 4px; border: 1px solid #001939; background: #001939; '
           'color: #F7F5F0; font-size: 15px; font-weight: 700; font-family: inherit; cursor: pointer')
PILL_OFF = ('min-height: 44px; padding: 0 18px; border-radius: 4px; border: 1px solid #CFC8B8; background: #FFFFFF; '
            'color: #001939; font-size: 15px; font-weight: 700; font-family: inherit; cursor: pointer')
CHECK = 'display: flex; gap: 10px; align-items: center; font-size: 15px; font-weight: 600; color: #001939; cursor: pointer; min-height: 44px'

DC_FIELDS = ('href', 'title', 'img', 'imgnote', 'tag', 'place', 'price', 'kind', 'areaT', 'roomsT', 'sub')

CARD = '''<article %(attrs)s style="background: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; overflow: hidden; display: flex; flex-direction: column">
<a href="%(href)s" aria-label="%(title)s" style="position: relative; height: 220px; background: #DCD6C8 url('%(img)s') center / cover no-repeat; display: block; text-decoration: none">
<span class="card-note" style="position: absolute; bottom: 12px; right: 14px; background: rgba(0,17,42,0.82); color: #F7F5F0; font-size: 12px; font-weight: 700; padding: 5px 9px; border-radius: 3px">%(imgnote)s</span>
<span style="position: absolute; top: 14px; left: 14px; background: #001939; color: #F7F5F0; font-size: 12px; font-weight: 700; padding: 6px 10px; border-radius: 3px">%(tag)s</span>
</a>
<div style="padding: 20px; display: flex; flex-direction: column; gap: 8px; flex: 1">
<span style="font-size: 12px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: #8A6A2B">%(kind)s</span>
<h3 style="margin: 0; font-size: 18px; font-weight: 800; color: #001939; line-height: 1.3">%(title)s</h3>
<ul style="margin: 2px 0 0; padding: 0; list-style: none; display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: 14px; color: #2A3444">
<li style="display: flex; align-items: center; gap: 6px"><svg role="img" aria-label="Výmera" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8A6A2B" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="flex: none"><path d="M4 4h16v16H4z"></path><path d="M4 9h3M4 14h3M9 4v3M14 4v3"></path></svg>%(areaT)s</li>
<li class="c-r" data-v="%(roomsT)s" style="display: flex; align-items: center; gap: 6px"><svg role="img" aria-label="Dispozícia" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8A6A2B" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="flex: none"><path d="M3 19v-7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v7"></path><path d="M3 15h18"></path><path d="M6 10V7a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v3"></path></svg>%(roomsT)s</li>
<li style="display: flex; align-items: center; gap: 6px; flex-basis: 100%%"><svg role="img" aria-label="Lokalita" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8A6A2B" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="flex: none"><path d="M12 22s7-6.3 7-12a7 7 0 0 0-14 0c0 5.7 7 12 7 12Z"></path><circle cx="12" cy="10" r="2.5"></circle></svg>%(place)s</li>
</ul>
<div style="margin-top: auto; padding-top: 12px; border-top: 1px solid #EFEBE1; display: flex; flex-direction: column; gap: 2px">
<span style="font-family: 'Cormorant Garamond', serif; font-size: 28px; font-weight: 700; color: #001939">%(price)s</span>
<span style="font-size: 13px; color: #6B5220; font-weight: 700">%(sub)s</span>
</div>
<a href="%(href)s" style="margin-top: 10px; text-align: center; text-decoration: none; background: #001939; color: #F7F5F0; padding: 13px; border-radius: 4px; font-weight: 700; font-size: 15px">Zobraziť ponuku</a>
</div>
</article>
'''


HYPO_RATE, HYPO_YEARS, HYPO_LTV = 3.5, 30, 0.8
HYPO_NOTE = ('* Orientačná mesačná splátka pri financovaní 80 % ceny, splatnosti 30 rokov a úroku 3,5 % p. a. '
             'Presnú ponuku z bánk vám pripravíme bezplatne.')
AREA_TXT = {'Vlckovce.dc.html': '77,64 m²'}
ROOMS_TXT = {'Trebichava.dc.html': 'pozemok 327 m²'}


def _num(n):
    return '{:,}'.format(int(round(n))).replace(',', '\u00a0')


def hypo_monthly(price):
    r, n = HYPO_RATE / 100 / 12, HYPO_YEARS * 12
    loan = price * HYPO_LTV
    return loan * r / (1 - (1 + r) ** -n)


def _enrich(d):
    t, r = d['type'], d['rooms']
    d['kind'] = ('%d-izbový byt' % r if r else 'Byt') if t == 'byt' else 'Rodinný dom' if t == 'dom' else (
        'Priemyselný pozemok' if d['kom'] else 'Stavebný pozemok' if t == 'pozemok' else 'Nebytový priestor')
    if d['deal'] == 'prenajom':
        d['kind'] += ' · prenájom'
    d['areaT'] = AREA_TXT.get(d['href'], _num(d['area']) + ' m²')
    if t in ('byt', 'dom') and r:
        d['roomsT'] = '1 izba' if r == 1 else '%d izby' % r if r < 5 else '%d izieb' % r
    else:
        d['roomsT'] = ROOMS_TXT.get(d['href'], '')
    if d['deal'] == 'kupa' and d['pnum'] and not d['kom']:
        d['sub'] = 'Hypotéka od %s € / mes.*' % _num(hypo_monthly(d['pnum']))
    else:
        d['sub'] = d['note']


DC_CARD = None  # set below


def _sold(href):
    import listing
    return listing.is_sold(href[:-len('.dc.html')].lower())


def listings(source_text):
    block = re.search(r'allListings: \[(.*?)\]\s*,?\s*\n', source_text, re.S).group(1)
    out = []
    for obj in re.findall(r'\{(.*?)\}', block, re.S):
        d = dict(re.findall(r"(\w+): '((?:[^'\\]|\\.)*)'", obj))
        if _sold(d['href']):
            continue
        f = dict(FACTS[d['href']]); f['pnum'] = f.pop('price'); d.update(f); _enrich(d)
        out.append(d)
    return out


def _pills(group, opts, mode, active):
    if mode == 'dc':
        return ('<sc-for list="{{flt.%s}}" as="p" hint-placeholder-count="%d"><button type="button" onClick="{{p.pick}}" '
                'aria-pressed="{{p.on}}" style="{{p.style}}">{{p.label}}</button></sc-for>\n' % (group, len(opts)))
    return ''.join('<button type="button" class="pill%s" data-group="f-%s" data-value="%s" aria-pressed="%s">%s</button>\n'
                   % (' on' if v == active else '', group, v, 'true' if v == active else 'false', l) for v, l in opts)


def _field(fid, label, inner):
    return ('<div class="%s-w" style="display: flex; flex-direction: column; gap: 8px; min-width: 0">\n<label for="%s" style="%s">%s</label>\n%s</div>\n'
            % (fid, fid, LABEL, label, inner))


def section(mode, items):
    dc = mode == 'dc'

    def ev(name, kind='onChange'):
        return ' %s="{{flt.%s}}"' % (kind, name) if dc else ''

    def val(name):
        return ' value="{{flt.%s}}"' % name if dc else ''

    okres_opts = '<option value="">Všetky lokality</option>' + ''.join('<option value="%s">%s</option>' % (o, o) for o in OKRESY)
    sort_opts = ''.join('<option value="%s">%s</option>' % s for s in SORTS)
    num = lambda fid, ph, nm: '<input id="%s" type="number" inputmode="numeric" min="0" placeholder="%s"%s%s style="%s">\n' % (fid, ph, val(nm), ev('on_' + nm), INPUT)

    form = '''<form id="vyhladavac-form" onsubmit="return false" style="background: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 28px; display: flex; flex-direction: column; gap: 22px">
<div style="display: flex; flex-wrap: wrap; gap: 18px 40px">
<div role="group" aria-label="Typ obchodu" style="display: flex; flex-direction: column; gap: 10px">
<span style="%(L)s">Mám záujem o</span>
<div style="display: flex; flex-wrap: wrap; gap: 8px">
%(deal)s</div>
</div>
<div role="group" aria-label="Typ nehnuteľnosti" style="display: flex; flex-direction: column; gap: 10px">
<span style="%(L)s">Typ nehnuteľnosti</span>
<div style="display: flex; flex-wrap: wrap; gap: 8px">
%(type)s</div>
</div>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px">
%(okres)s%(pod)s%(pdo)s%(aod)s%(ado)s</div>
<div style="display: flex; flex-wrap: wrap; gap: 14px 40px; align-items: flex-end">
<div role="group" aria-label="Počet izieb" style="display: flex; flex-direction: column; gap: 10px">
<span style="%(L)s">Počet izieb</span>
<div style="display: flex; flex-wrap: wrap; gap: 8px">
%(rooms)s</div>
</div>
<div style="display: flex; flex-wrap: wrap; gap: 4px 24px">
<label style="%(C)s"><input id="f-nov" type="checkbox"%(nov_ch)s%(nov_ev)s style="width: 22px; height: 22px; margin: 0; accent-color: #B8860B">Len novostavby</label>
<label style="%(C)s"><input id="f-park" type="checkbox"%(park_ch)s%(park_ev)s style="width: 22px; height: 22px; margin: 0; accent-color: #B8860B">Garáž / vlastné parkovanie</label>
</div>
</div>
</form>
''' % dict(L=LABEL, C=CHECK,
           deal=_pills('deals', DEALS, mode, 'kupa'), type=_pills('types', TYPES, mode, ''), rooms=_pills('rooms', ROOMS, mode, ''),
           okres=_field('f-okres', 'Lokalita (okres)', '<select id="f-okres"%s%s style="%s">%s</select>\n' % (val('okres'), ev('on_okres'), INPUT, okres_opts)),
           pod=_field('f-cod', 'Cena od (€)', num('f-cod', '0', 'cod')),
           pdo=_field('f-cdo', 'Cena do (€)', num('f-cdo', 'bez limitu', 'cdo')),
           aod=_field('f-vod', 'Výmera od (m²)', num('f-vod', '0', 'vod')),
           ado=_field('f-vdo', 'Výmera do (m²)', num('f-vdo', 'bez limitu', 'vdo')),
           nov_ch=' checked="{{flt.nov}}"' if dc else '', nov_ev=ev('on_nov'),
           park_ch=' checked="{{flt.park}}"' if dc else '', park_ev=ev('on_park'))

    toggle = ('' if dc else '<button type="button" id="f-toggle" class="f-toggle" aria-expanded="false" aria-controls="vyhladavac-form" '
              'style="display: none; min-height: 52px; align-items: center; justify-content: center; gap: 10px; border: 1px solid #001939; border-radius: 4px; '
              'background: #FFFFFF; color: #001939; font-size: 16px; font-weight: 800; font-family: inherit; cursor: pointer">'
              '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#001939" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M7 12h10M10 18h4"></path></svg>'
              '<span id="f-toggle-t">Zobraziť filter</span></button>\n')
    toolbar = '''<div style="display: flex; flex-wrap: wrap; gap: 12px 24px; align-items: center; justify-content: space-between">
<p id="f-count" aria-live="polite" style="margin: 0; font-size: 17px; font-weight: 700; color: #001939">%s</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; align-items: center">
<button type="button" id="f-reset"%s style="min-height: 44px; padding: 0 16px; border: none; background: none; color: #8A6A2B; font-size: 15px; font-weight: 700; font-family: inherit; cursor: pointer; text-decoration: underline">Zrušiť filtre</button>
<label for="f-sort" style="font-size: 14px; font-weight: 700; color: #4A5566">Zoradiť</label>
<select id="f-sort"%s%s style="height: 44px; padding: 0 12px; border-radius: 4px; border: 1px solid #CFC8B8; background: #FFFFFF; font-size: 15px; font-family: inherit; color: #1B2533">%s</select>
</div>
</div>
''' % ('{{flt.count}}' if dc else 'Nájdené ponuky', ev('reset', 'onClick'), val('sort'), ev('on_sort'), sort_opts)

    if dc:
        grid = ('<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px">\n'
                '<sc-for list="{{flt.results}}" as="item" hint-placeholder-count="6">\n'
                + DC_CARD
                + '</sc-for>\n</div>\n')
        more = ''
    else:
        cards = ''
        for d in items:
            attrs = ('data-deal="%s" data-type="%s" data-okres="%s" data-price="%s" data-area="%s" data-rooms="%s" data-nov="%d" data-park="%d" data-kom="%d" data-order="%d"'
                     % (d['deal'], d['type'], d['okres'], '' if d['pnum'] is None else d['pnum'], d['area'], d['rooms'], d['nov'], d['park'], d['kom'], d['order']))
            cards += CARD % dict(d, attrs='class="f-card" ' + attrs)
        grid = '<div id="f-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px">\n' + cards + '</div>\n'
        more = ('<button type="button" id="f-more" hidden style="align-self: center; min-height: 52px; padding: 0 32px; border: 1px solid #001939; '
                'border-radius: 4px; background: #FFFFFF; color: #001939; font-size: 16px; font-weight: 800; font-family: inherit; cursor: pointer">Načítať ďalšie ponuky</button>\n')

    empty = '''<div %s style="background: #FFFFFF; border: 1px dashed #CFC8B8; border-radius: 6px; padding: 40px 28px; text-align: center; display: flex; flex-direction: column; gap: 12px; align-items: center">
<strong style="font-size: 20px; color: #001939">Takúto nehnuteľnosť momentálne v ponuke nemáme</strong>
<span style="font-size: 16px; color: #4A5566; max-width: 520px">Napíšte nám, čo hľadáte. Nové ponuky často predáme skôr, než sa dostanú na web – ozveme sa vám ako prvým.</span>
<a href="#kontakt" style="background: #D9AE52; color: #001939; text-decoration: none; padding: 14px 24px; border-radius: 4px; font-weight: 800">Chcem byť informovaný</a>
</div>
''' % ('' if dc else 'id="f-empty" hidden')
    if dc:
        empty = '<sc-if value="{{flt.none}}" hint-placeholder-val="{{ false }}">' + empty + '</sc-if>\n'

    return '''<!-- PONUKA VYHLADAVAC -->
<section id="vyhladavac" style="padding: 64px 0 96px">
<div style="max-width: 1240px; margin: 0 auto; padding: 0 24px; display: flex; flex-direction: column; gap: 28px">
<div style="display: flex; flex-direction: column; gap: 14px">
<span style="font-size: 13px; font-weight: 800; letter-spacing: 0.28em; color: #8A6A2B">PONUKA NEHNUTEĽNOSTÍ</span>
<h1 style="margin: 0; font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: clamp(2.2rem, 4vw, 3.2rem); line-height: 1.1; color: #001939">Vyberte si z celej ponuky</h1>
</div>
%s%s%s%s%s%s</div>
</section>

''' % (toggle, form, toolbar, grid, empty, more + FOOT)


DC_STATE = "f_deal: 'kupa', f_type: '', f_rooms: '', f_okres: '', f_cod: '', f_cdo: '', f_vod: '', f_vdo: '', f_nov: false, f_park: false, f_sort: 'odp'"


def dc_logic(items):
    data = [{k: d[k] for k in DC_FIELDS} for d in items]
    for o, d in zip(data, items):
        o.update(fd=d['deal'], ft=d['type'], fo=d['okres'], fp=d['pnum'], fa=d['area'], fr=d['rooms'], fn=d['nov'], fk=d['park'], fc=d['kom'], ord=d['order'])
    return '''  flt() {
    const L = %s;
    const st = this.state, P_ON = '%s', P_OFF = '%s';
    const set = (k) => (e) => this.setState({ [k]: e.target.value });
    const pills = (opts, key) => opts.map(([v, l]) => ({ label: l, on: String(st[key] === v), style: st[key] === v ? P_ON : P_OFF, pick: () => this.setState({ [key]: v }) }));
    const n = (v) => (v === '' || v === null || v === undefined ? null : Number(v));
    const cod = n(st.f_cod), cdo = n(st.f_cdo), vod = n(st.f_vod), vdo = n(st.f_vdo);
    let r = L.filter((x) => (!st.f_deal || x.fd === st.f_deal) && (!st.f_type || (st.f_type === 'komercne' ? x.fc : x.ft === st.f_type)) && (!st.f_okres || x.fo === st.f_okres)
      && (!st.f_rooms || (st.f_rooms === '5' ? x.fr >= 5 : x.fr === Number(st.f_rooms)))
      && (cod === null || (x.fp !== null && x.fp >= cod)) && (cdo === null || (x.fp !== null && x.fp <= cdo))
      && (vod === null || x.fa >= vod) && (vdo === null || x.fa <= vdo) && (!st.f_nov || x.fn) && (!st.f_park || x.fk));
    const pk = (x, hi) => (x.fp === null ? (hi ? -1 : Infinity) : x.fp);
    if (st.f_sort === 'lac') r = r.slice().sort((a, b) => pk(a, false) - pk(b, false));
    else if (st.f_sort === 'dra') r = r.slice().sort((a, b) => pk(b, true) - pk(a, true));
    else if (st.f_sort === 'vym') r = r.slice().sort((a, b) => b.fa - a.fa);
    else r = r.slice().sort((a, b) => a.ord - b.ord);
    const c = r.length;
    return {
      deals: pills(%s, 'f_deal'), types: pills(%s, 'f_type'), rooms: pills(%s, 'f_rooms'),
      okres: st.f_okres, cod: st.f_cod, cdo: st.f_cdo, vod: st.f_vod, vdo: st.f_vdo, sort: st.f_sort, nov: st.f_nov, park: st.f_park,
      on_okres: set('f_okres'), on_cod: set('f_cod'), on_cdo: set('f_cdo'), on_vod: set('f_vod'), on_vdo: set('f_vdo'), on_sort: set('f_sort'),
      on_nov: (e) => this.setState({ f_nov: e.target.checked }), on_park: (e) => this.setState({ f_park: e.target.checked }),
      reset: () => this.setState({ %s }),
      results: r, none: c === 0, top: %s.map((h) => L.find((x) => x.href === h)),
      count: c === 1 ? 'Nájdená 1 nehnuteľnosť' : (c >= 2 && c <= 4 ? 'Nájdené ' + c + ' nehnuteľnosti' : 'Nájdených ' + c + ' nehnuteľností')
    };
  }
''' % (json.dumps(data, ensure_ascii=False), PILL_ON, PILL_OFF, json.dumps(DEALS, ensure_ascii=False),
       json.dumps(TYPES, ensure_ascii=False), json.dumps(ROOMS, ensure_ascii=False), DC_STATE, json.dumps(TOP))


STATIC_CSS = '@media (max-width: 640px){.f-toggle{display:flex!important}.f-okres-w{grid-column:1/-1}#vyhladavac-form:not(.f-open){display:none!important}}'

STATIC_SCRIPT = '''<script>
(function(){
  var grid=document.getElementById('f-grid'); if(!grid)return;
  var $=function(id){return document.getElementById(id)}, cards=[].slice.call(grid.querySelectorAll('.f-card')), PAGE=9, shown=PAGE;
  var pick=function(g){var b=document.querySelector('.pill.on[data-group="f-'+g+'"]');return b?b.dataset.value:''};
  var setPill=function(g,v){document.querySelectorAll('.pill[data-group="f-'+g+'"]').forEach(function(b){var on=b.dataset.value===v;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on?'true':'false')})};
  var num=function(id){var v=$(id).value;return v===''?null:Number(v)};
  function apply(keep){
    if(!keep)shown=PAGE;
    var deal=pick('deals'),type=pick('types'),rooms=pick('rooms'),ok=$('f-okres').value,cod=num('f-cod'),cdo=num('f-cdo'),vod=num('f-vod'),vdo=num('f-vdo'),nov=$('f-nov').checked,park=$('f-park').checked,s=$('f-sort').value;
    var hits=cards.filter(function(c){var d=c.dataset,p=d.price===''?null:Number(d.price),a=Number(d.area),r=Number(d.rooms);
      return (!deal||d.deal===deal)&&(!type||(type==='komercne'?d.kom==='1':d.type===type))&&(!ok||d.okres===ok)&&(!rooms||(rooms==='5'?r>=5:r===Number(rooms)))
        &&(cod===null||(p!==null&&p>=cod))&&(cdo===null||(p!==null&&p<=cdo))&&(vod===null||a>=vod)&&(vdo===null||a<=vdo)&&(!nov||d.nov==='1')&&(!park||d.park==='1')});
    var pr=function(c,hi){return c.dataset.price===''?(hi?-1:Infinity):Number(c.dataset.price)};
    hits.sort(function(a,b){if(s==='lac')return pr(a,0)-pr(b,0);if(s==='dra')return pr(b,1)-pr(a,1);if(s==='vym')return b.dataset.area-a.dataset.area;return a.dataset.order-b.dataset.order});
    cards.forEach(function(c){c.hidden=true});
    hits.forEach(function(c,i){grid.appendChild(c);c.hidden=i>=shown});
    var n=hits.length;
    $('f-count').textContent=n===1?'Nájdená 1 nehnuteľnosť':(n>=2&&n<=4?'Nájdené '+n+' nehnuteľnosti':'Nájdených '+n+' nehnuteľností');
    $('f-empty').hidden=n>0; $('f-more').hidden=n<=shown;
  }
  document.querySelectorAll('.pill[data-group^="f-"]').forEach(function(b){b.addEventListener('click',function(){setTimeout(function(){apply()},0)})});
  ['f-okres','f-cod','f-cdo','f-vod','f-vdo','f-nov','f-park','f-sort'].forEach(function(id){$(id).addEventListener('input',function(){apply()});$(id).addEventListener('change',function(){apply()})});
  $('f-more').addEventListener('click',function(){shown+=PAGE;apply(true)});
  $('f-reset').addEventListener('click',function(){setPill('deals','kupa');setPill('types','');setPill('rooms','');['f-okres','f-cod','f-cdo','f-vod','f-vdo'].forEach(function(id){$(id).value=''});$('f-nov').checked=false;$('f-park').checked=false;$('f-sort').value='odp';apply()});
  var tg=$('f-toggle'),fm=$('vyhladavac-form');
  tg.addEventListener('click',function(){var o=fm.classList.toggle('f-open');tg.setAttribute('aria-expanded',o?'true':'false');$('f-toggle-t').textContent=o?'Skryť filter':'Zobraziť filter'});
  var q=new URLSearchParams(location.search);
  if(q.has('deal'))setPill('deals',q.get('deal'));
  if(q.has('type'))setPill('types',q.get('type'));
  if(q.get('okres'))$('f-okres').value=q.get('okres');
  if(q.get('cod'))$('f-cod').value=q.get('cod');
  if(q.get('cdo'))$('f-cdo').value=q.get('cdo');
  apply();
})();
</script>
'''

HOME_SCRIPT = '''<script>
(function(){
  var go=document.getElementById('home-search'); if(!go)return;
  var map={'Kúpa':'kupa','Prenájom':'prenajom','Byt':'byt','Rodinný dom':'dom','Pozemok':'pozemok','Nebytový priestor':'nebyt','Komerčné / priemyselné':'komercne'};
  go.addEventListener('click',function(e){
    e.preventDefault();
    var p=new URLSearchParams(), d=document.querySelector('.pill.on[data-group="deal"]'), t=document.querySelector('.pill.on[data-group="type"]');
    if(d)p.set('deal',map[d.textContent.trim()]||''); if(t)p.set('type',map[t.textContent.trim()]||'');
    var o=document.getElementById('lokalita').value; if(o&&o!=='Všetky lokality')p.set('okres',o);
    var a=document.getElementById('cena-od').value, b=document.getElementById('cena-do').value; if(a)p.set('cod',a); if(b)p.set('cdo',b);
    location.href='ponuka.html?'+p.toString()+'#vyhladavac';
  });
})();
</script>
'''


FOOT = '<p style="margin: 0; font-size: 13px; color: #4A5566">' + HYPO_NOTE + ' <a href="#hypoteka">Vypočítať vlastnú splátku →</a></p>\n'
DC_CARD = CARD % dict({k: '{{item.%s}}' % k for k in DC_FIELDS}, attrs='')
TOP = ['Mitice.dc.html', 'Byt28.dc.html', 'Zamarovce.dc.html', 'Odbojarov.dc.html']


def top_dc():
    return '<sc-for list="{{flt.top}}" as="item" hint-placeholder-count="4">\n' + DC_CARD + '</sc-for>'


def top_static(items):
    by = {d['href']: d for d in items}
    picks = [h for h in TOP if h in by] + [d['href'] for d in items if d['href'] not in TOP]
    return ''.join(CARD % dict(by[h], attrs='') for h in picks[:len(TOP)])
