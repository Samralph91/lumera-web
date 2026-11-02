"""Convert the canvas design (Main.dc.html) into a standalone static site for lumera.sk."""
import re, shutil, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hypo, nacenenie, pages, listing, vyhladavac, seo

SP = os.path.dirname(os.path.abspath(__file__))
OUT = SP + '/site'
os.makedirs(OUT, exist_ok=True)

MAP_SRC = 'https://www.google.com/maps?q=Legion%C3%A1rska+6419,+911+01+Tren%C4%8D%C3%ADn&amp;hl=sk&amp;z=16&amp;output=embed'
MAP_HTML = (
    '<div style="display: flex; flex-direction: column; gap: 10px; height: 100%">'
    '<iframe title="Mapa – LUMERA Real Estate, Legionárska 6419, Trenčín" src="' + MAP_SRC + '" '
    'style="width: 100%; flex: 1; min-height: 300px; border: 0; border-radius: 6px" loading="lazy" '
    'referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>'
    '<a href="https://www.google.com/maps/search/?api=1&amp;query=Legion%C3%A1rska+6419%2C+911+01+Tren%C4%8D%C3%ADn" '
    'style="color: #D9AE52; font-weight: 700; font-size: 14px">Otvoriť v Google Mapách →</a></div>')
MAP_SCRIPT = """<script>
(function(){
  var maps=document.querySelectorAll('.lm-map'); if(!maps.length)return;
  function load(){maps.forEach(function(m){if(m.querySelector('iframe'))return;var f=document.createElement('iframe');f.src=m.dataset.src;f.title='Mapa – LUMERA Real Estate, Legionárska 6419, Trenčín';f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';f.setAttribute('allowfullscreen','');f.style.cssText='position:absolute;inset:0;width:100%;height:100%;border:0';m.appendChild(f);var p=m.querySelector('.lm-map-ph');if(p)p.style.display='none'})}
  var ok=false;try{ok=localStorage.getItem('lumera-mapy')==='1'}catch(e){}
  if(ok)load();
  document.querySelectorAll('.lm-map-on').forEach(function(b){b.addEventListener('click',function(){try{localStorage.setItem('lumera-mapy','1')}catch(e){}load()})});
})();
</script>
"""


def render(dc_path):
    s = open(dc_path).read()
    global logic
    body = s[s.index('<div style="font-family'):s.index('</x-dc>')]
    logic = s[s.index('class Component'):]

    body = body.replace('{{accent}}', '#D9AE52')
    body = body.replace('/_blob/f5d4ae16313d223686d3f437daaac616', 'logo.png')
    body = body.replace('/_blob/4b911459f3fdefed4a64d12dd4650db6', 'trencin.jpg')
    body = body.replace('/_blob/68f511317b0f65d99927f8bd4c191e66', 'samuel.jpg')
    body = body.replace('/_blob/42578aedd5d3f6d7da371c0d33b6e465', 'img/obhliadka.jpg')


    def js_objects(name):
        """Pull a list of {key: 'value'} objects out of renderVals()."""
        block = re.search(name + r': \[(.*?)\]\s*,?\s*\n', logic, re.S).group(1)
        items = []
        for obj in re.findall(r'\{(.*?)\}', block, re.S):
            items.append(dict(re.findall(r"(\w+): '((?:[^'\\]|\\.)*)'", obj)))
        return items


    def expand(body, name, var, items):
        m = re.search(r'<sc-for list="\{\{' + name + r'\}\}"[^>]*>(.*?)</sc-for>', body, re.S)
        out = ''
        for it in items:
            t = m.group(1)
            for k, v in it.items():
                t = t.replace('{{' + var + '.' + k + '}}', v)
            out += t
        return body[:m.start()] + out + body[m.end():]


    m = re.search(r'<!-- HYPOTÉKA -->.*?</section>\n\n', body, re.S)
    if m:
        body = body[:m.start()] + hypo.static() + body[m.end():]
    m = re.search(r'<!-- NACENENIE -->.*?</section>\n\n', body, re.S)
    if m:
        body = body[:m.start()] + nacenenie.static() + body[m.end():]

    extra_scripts = ''
    for key, L in listing.LISTINGS.items():
        m = re.search(r'<!-- ' + re.escape(L['marker']) + r' -->.*?</section>\n\n', body, re.S)
        if m:
            sec, scr = listing.static(key)
            body = body[:m.start()] + sec + body[m.end():]
            extra_scripts += scr
    m = re.search(r'<sc-for list="\{\{flt\.top\}\}".*?</sc-for>', body, re.S)
    if m:
        body = body[:m.start()] + vyhladavac.top_static(vyhladavac.listings(s)) + body[m.end():]
    m = re.search(r'<!-- PONUKA VYHLADAVAC -->.*?</section>\n\n', body, re.S)
    if m:
        body = body[:m.start()] + vyhladavac.section('static', vyhladavac.listings(s)) + body[m.end():]
        extra_scripts += '<style>' + vyhladavac.STATIC_CSS + '</style>\n' + vyhladavac.STATIC_SCRIPT
    if 'id="home-search"' in body:
        extra_scripts += vyhladavac.HOME_SCRIPT
    if '{{listings}}' in body:
        body = expand(body, 'listings', 'item', js_objects('listings'))
    if '{{allListings}}' in body:
        body = expand(body, 'allListings', 'item', js_objects('allListings'))
    if '{{reviews}}' in body:
        body = expand(body, 'reviews', 'r', js_objects('reviews'))


    def pills(body, name, group, labels):
        m = re.search(r'<sc-for list="\{\{' + name + r'\}\}"[^>]*>(.*?)</sc-for>', body, re.S)
        out = ''.join(
            '<button type="button" class="pill%s" data-group="%s" aria-pressed="%s">%s</button>\n'
            % (' on' if i == 0 else '', group, 'true' if i == 0 else 'false', l)
            for i, l in enumerate(labels))
        return body[:m.start()] + out + body[m.end():]


    if '{{deals}}' in body:
        body = pills(body, 'deals', 'deal', ['Kúpa', 'Prenájom'])
        body = pills(body, 'types', 'type', ['Byt', 'Rodinný dom', 'Pozemok', 'Komerčné / priemyselné', 'Nebytový priestor'])

    # Live Google map instead of the canvas link box
    m = re.search(r'<a id="mapa".*?</a>', body, re.S)
    if m:
        body = body[:m.start()] + MAP_HTML + body[m.end():]

    # ---- Public-site cleanup: nothing unfinished or non-working goes live ----
    # Listing photo placeholders -> neutral brand tile pointing to the listing photos
    body = body.replace('\n[FOTO]\n', '\n<span style="font-weight: 700; color: #001939">Fotografie v inzeráte →</span>\n')
    body = body.replace("url('')", 'none')
    for b, f in listing.blob_map().items():
        body = body.replace(b, f)
    # About: team photo placeholder -> Trenčín photo; drop the unfinished paragraph
    body = re.sub(r'<div style="flex: 1 1 380px; min-width: 0; height: 380px;[^>]*>\[FOTO TÍMU / KANCELÁRIE\]</div>',
                  '<img src="trencin.jpg" alt="Trenčín – sídlo realitnej kancelárie LUMERA" style="flex: 1 1 380px; min-width: 0; height: 380px; object-fit: cover; border-radius: 6px">', body)
    body = re.sub(r'<p[^>]*>\[Krátky príbeh kancelárie, oblasť pôsobenia, tím\.\]</p>\n?', '', body)
    # Newsletter has no mailing service behind it yet -> leave it out
    body = re.sub(r'<!-- NEWSLETTER -->.*?</section>\n', '', body, flags=re.S)
    # Footer links without a destination yet -> leave them out
    body = body.replace('<nav aria-label="Päta" style="display: flex; flex-wrap: wrap; gap: 8px 24px">\n</nav>',
                        '<div style="display: flex; flex-direction: column; gap: 6px"><a href="tel:+421949888663" style="color: #C7CFDB">0949 888 663</a><a href="mailto:info@lumera.sk" style="color: #C7CFDB">info@lumera.sk</a></div>')
    # Contact form: real sending via FormSubmit to info@lumera.sk
    body = body.replace('<form style="flex: 1 1 460px;',
                        '<form action="https://formsubmit.co/info@lumera.sk" method="POST" style="flex: 1 1 460px;')
    for fid, nm in [('meno', 'Meno'), ('telefon', 'Telefón'), ('email', 'E-mail'), ('zaujem', 'Záujem'), ('sprava', 'Správa')]:
        body = body.replace('id="%s"' % fid, 'id="%s" name="%s"' % (fid, nm), 1)
    body = body.replace('<input id="meno" name="Meno"', '<input id="meno" name="Meno" required')
    body = body.replace('<input id="email" name="E-mail"', '<input id="email" name="E-mail" required')
    body = body.replace('<button type="button" style="height: 52px; border: none; border-radius: 4px; background: #D9AE52',
                        '<input type="hidden" name="_subject" value="Nový dopyt z webu lumera.sk">'
                        '<input type="hidden" name="_next" value="%%NEXT%%">'
                        '<input type="hidden" name="_template" value="table">'
                        '<input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">'
                        '<button type="submit" style="height: 52px; border: none; border-radius: 4px; background: #D9AE52')

    # Callback forms (Chcem predať) -> FormSubmit
    body = body.replace('<form data-callback="1" ', '<form action="https://formsubmit.co/info@lumera.sk" method="POST" ')
    body = body.replace('<button type="button" data-cb-submit="1" ', '<input type="hidden" name="_subject" value="Chcem predať / prenajať – zavolajte mi (lumera.sk)"><input type="hidden" name="_next" value="%%NEXT%%"><input type="hidden" name="_template" value="table"><input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true"><button type="submit" ')
    for bad in ['[FOTO', '[Krátky', '[XX', '[CENA', '[Mesto', '[Meno', '[info@', '[Ulica']:
        assert bad not in body, bad

    leftover = re.findall(r'\{\{[^}]*\}\}', body)
    assert not leftover, leftover


    return body, extra_scripts


head = '''<!doctype html>
<html lang="sk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
%%META%%<meta name="theme-color" content="#001939">
<link rel="icon" href="logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
html{scroll-behavior:smooth}
body{margin:0;background:#F7F5F0}
[hidden]{display:none!important}
a{color:#8A6A2B}a:hover{color:#5E4719}
.pill{min-height:44px;padding:0 20px;border-radius:4px;border:1px solid #CFC8B8;background:#FFFFFF;color:#001939;font-size:15px;font-weight:700;font-family:inherit;cursor:pointer}
.pill.on{border-color:#001939;background:#001939;color:#F7F5F0}
'''+hypo.RANGE_CSS+'''
</style>
</head>
<body>
'''
tail = '''<script>
document.querySelectorAll('.pill').forEach(function(b){b.addEventListener('click',function(){
document.querySelectorAll('.pill[data-group="'+b.dataset.group+'"]').forEach(function(o){o.classList.remove('on');o.setAttribute('aria-pressed','false')});
b.classList.add('on');b.setAttribute('aria-pressed','true');});});
(function(){
  if(!/[?&]odoslane=1/.test(location.search))return;
  var d=document.createElement('div');d.setAttribute('role','status');
  d.style.cssText='position:fixed;left:50%;top:max(16px,env(safe-area-inset-top,0px));transform:translateX(-50%);z-index:100;width:min(560px,calc(100% - 32px));box-sizing:border-box;background:#001939;color:#F7F5F0;border:1px solid #D9AE52;border-radius:6px;padding:18px 52px 18px 20px;box-shadow:0 18px 30px rgba(0,17,42,0.45);font-family:Manrope,system-ui,sans-serif;font-size:16px;line-height:1.5';
  var t=document.createElement('strong');t.style.cssText='display:block;color:#D9AE52;font-size:17px;margin-bottom:4px';t.textContent='Ďakujeme, správu sme dostali.';
  var p=document.createElement('span');p.textContent='Ozveme sa vám čo najskôr, zvyčajne ešte v ten istý pracovný deň.';
  var x=document.createElement('button');x.type='button';x.setAttribute('aria-label','Zavrieť');x.textContent='×';
  x.style.cssText='position:absolute;top:8px;right:8px;width:40px;height:40px;border:0;background:transparent;color:#F7F5F0;font-size:26px;cursor:pointer';
  x.onclick=function(){d.remove()};
  d.appendChild(t);d.appendChild(p);d.appendChild(x);document.body.appendChild(d);
  if(history.replaceState)history.replaceState(null,'',location.pathname+location.hash);
})();
</script>
</body>
</html>
'''
for dc_name, static_name, title, *_ in pages.PAGES:
    body, extra = render(os.path.join(SP, 'lumera/project', dc_name))
    for d, st in pages.STATIC_NAME.items():
        body = body.replace('href="%s"' % d, 'href="%s"' % st)
    assert '.dc.html' not in body, static_name
    scripts = extra + (hypo.STATIC_SCRIPT if 'id="h-price"' in body else '') + (nacenenie.STATIC_SCRIPT if 'id="nac-form"' in body else '')
    helmet_css = re.search(r'<helmet>.*?<style>(.*?)</style>', open(os.path.join(SP, 'lumera/project', dc_name)).read(), re.S).group(1)
    lkey = dc_name[:-8].lower()
    if lkey in listing.LISTINGS:
        desc, img = seo.listing_meta(listing.LISTINGS[lkey])
    else:
        desc, img = seo.DESC[static_name], seo.SITE + 'trencin.jpg'
    page_head = head.replace('%%TITLE%%', title).replace('%%META%%', seo.head_tags(static_name, title, desc, img)).replace('</style>', helmet_css + '\n</style>', 1)
    body = body.replace('%%NEXT%%', seo.SITE + static_name + '?odoslane=1')
    open(os.path.join(OUT, static_name), 'w').write(page_head + body + scripts + tail)
shutil.copy(SP + '/lumera/logo3.png', OUT + '/logo.png')
shutil.copy(SP + '/lumera/trencin.jpg', OUT + '/trencin.jpg')
shutil.copy(SP + '/lumera/samuel.jpg', OUT + '/samuel.jpg')
shutil.copy(SP + '/cookies-page.html', OUT + '/cookies.html')
shutil.copy(SP + '/privacy-page.html', OUT + '/ochrana-osobnych-udajov.html')
open(OUT + '/sitemap.xml', 'w').write(seo.sitemap([p[1] for p in pages.PAGES] + ['cookies.html', 'ochrana-osobnych-udajov.html']))
open(OUT + '/robots.txt', 'w').write(seo.ROBOTS)
for L in listing.LISTINGS.values():
    shutil.copytree(SP + '/lumera/img/' + L['folder'], OUT + '/img/' + L['folder'], dirs_exist_ok=True)
open(OUT + '/CNAME', 'w').write('lumera.sk\n')
print('ok', sorted(os.listdir(OUT)))

shutil.copy(SP + '/lumera/obhliadka.jpg', OUT + '/img/obhliadka.jpg')
import seo_pages  # local landing pages, blog, footer area links
seo_pages.build()
import ai  # llms.txt, robots.txt for AI crawlers, IndexNow key
ai.write(OUT)
import optimize  # lighter images
optimize.main()
import en_build  # English version + SK/EN switch
en_build.main()
