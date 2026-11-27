# -*- coding: utf-8 -*-
"""Cookie consent for lumera.sk (SK + EN).

The site itself sets no cookies. Only Google Maps (iframe) can store Google's cookies, so the map is loaded
only after consent. The banner asks once; the choice is kept in localStorage 'lumera-cookies' = 'all' | 'necessary'.
Run last in the build (after en_build), it adds the banner + script to every page in ./site and ./site/en.
"""
import glob, os

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
MARK = '<!-- COOKIE CONSENT -->'

TXT = {
    'sk': dict(
        label='Súhlas s cookies',
        title='Cookies na webe lumera.sk',
        text='Náš web nepoužíva analytické ani reklamné cookies. Cookies môže uložiť iba služba Google Mapy, '
             'ktorú zobrazujeme na stránkach s mapou. Mapu načítame len s vaším súhlasom.',
        more='Viac o cookies', more_href='cookies.html',
        accept='Prijať všetky', reject='Len nevyhnutné',
    ),
    'en': dict(
        label='Cookie consent',
        title='Cookies on lumera.sk',
        text='Our website uses no analytics or advertising cookies. Cookies can only be stored by Google Maps, '
             'which we show on pages with a map. We load the map only with your consent.',
        more='More about cookies', more_href='cookies.html',
        accept='Accept all', reject='Necessary only',
    ),
}

BTN = ('min-height: 48px; padding: 0 22px; border-radius: 4px; font: inherit; font-size: 15px; font-weight: 800; cursor: pointer; '
       'flex: 1 1 160px')

BANNER = '''<!-- COOKIE CONSENT -->
<div id="lm-cc" role="dialog" aria-live="polite" aria-label="%(label)s" hidden style="position: fixed; left: 16px; right: 16px; bottom: 16px; z-index: 200; max-width: 720px; margin: 0 auto; box-sizing: border-box; background: #001939; color: #F7F5F0; border: 1px solid #1C3D6B; border-radius: 8px; box-shadow: 0 18px 40px rgba(0,17,42,0.45); padding: 22px 24px; font-family: 'Manrope', system-ui, sans-serif; display: flex; flex-direction: column; gap: 14px">
<strong style="font-size: 17px; color: #D9AE52">%(title)s</strong>
<p style="margin: 0; font-size: 15px; line-height: 1.6; color: #E3E8F0">%(text)s <a href="%(more_href)s" style="color: #D9AE52; font-weight: 700">%(more)s</a></p>
<div style="display: flex; flex-wrap: wrap; gap: 10px">
<button type="button" id="lm-cc-reject" style="%(btn)s; border: 1px solid #F7F5F0; background: transparent; color: #F7F5F0">%(reject)s</button>
<button type="button" id="lm-cc-accept" style="%(btn)s; border: 1px solid #D9AE52; background: #D9AE52; color: #001939">%(accept)s</button>
</div>
</div>
<script>
(function(){
  var K='lumera-cookies', v=null;
  try{v=localStorage.getItem(K)}catch(e){}
  var box=document.getElementById('lm-cc');
  function maps(){document.querySelectorAll('.lm-map').forEach(function(m){if(m.querySelector('iframe'))return;var f=document.createElement('iframe');f.src=m.dataset.src;f.title=m.dataset.title||'Mapa';f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';f.setAttribute('allowfullscreen','');f.style.cssText='position:absolute;inset:0;width:100%%;height:100%%;border:0';m.appendChild(f);var p=m.querySelector('.lm-map-ph');if(p)p.style.display='none'})}
  function set(x){try{localStorage.setItem(K,x)}catch(e){}v=x;box.hidden=true;if(x==='all')maps()}
  if(v==='all')maps(); else if(v!=='necessary')box.hidden=false;
  document.getElementById('lm-cc-accept').addEventListener('click',function(){set('all')});
  document.getElementById('lm-cc-reject').addEventListener('click',function(){set('necessary')});
  document.querySelectorAll('.lm-map-on').forEach(function(b){b.addEventListener('click',function(){set('all')})});
  document.querySelectorAll('.lm-cc-open').forEach(function(b){b.addEventListener('click',function(){try{localStorage.removeItem(K)}catch(e){}v=null;box.hidden=false;document.getElementById('lm-cc-accept').focus()})});
})();
</script>
'''


def main():
    n = 0
    for path in glob.glob(SITE + '/*.html') + glob.glob(SITE + '/en/*.html'):
        h = open(path).read()
        if MARK in h or '</body>' not in h:
            continue
        lang = 'en' if os.sep + 'en' + os.sep in path else 'sk'
        b = BANNER % dict(TXT[lang], btn=BTN)
        i = h.rindex('</body>')
        open(path, 'w').write(h[:i] + b + h[i:])
        n += 1
    print('cookie consent on %d pages' % n)


if __name__ == '__main__':
    main()
