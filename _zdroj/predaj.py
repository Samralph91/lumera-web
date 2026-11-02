"""'Chcem predať / prenajať' page sections (canvas markup; export turns data-callback forms into real ones)."""

ICON = {
    'cena': '<path d="M3 3v18h18"></path><path d="m7 15 4-4 3 3 5-6"></path>',
    'foto': '<rect x="3" y="6" width="18" height="14" rx="2"></rect><circle cx="12" cy="13" r="3.5"></circle><path d="M8 6l1.5-2h5L16 6"></path>',
    'marketing': '<path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1Z"></path><path d="M15 9a4 4 0 0 1 0 6"></path><path d="M18 6a8 8 0 0 1 0 12"></path>',
    'obhliadka': '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"></path><circle cx="12" cy="12" r="3"></circle>',
    'pravo': '<path d="M12 3v18"></path><path d="M5 7h14"></path><path d="M5 7 2 14a3 3 0 0 0 6 0Z"></path><path d="M19 7l-3 7a3 3 0 0 0 6 0Z"></path><path d="M8 21h8"></path>',
    'staging': '<path d="M4 18v-6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v6"></path><path d="M2 18h20"></path><path d="M6 10V7a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v3"></path><path d="M5 18v2M19 18v2"></path>',
    'hypo': '<rect x="3" y="6" width="18" height="13" rx="2"></rect><path d="M3 10h18"></path><path d="M7 15h4"></path>',
}

SERVICES = [
    ('cena', 'Cena podľa reálneho trhu',
     'Cenu nastavíme podľa skutočne predaných nehnuteľností vo vašom okolí, nie podľa dojmu. Správna cena od prvého dňa skracuje predaj a chráni vás pred zbytočným zľavovaním.'),
    ('foto', 'Fotky, dron a vizualizácie',
     'Nehnuteľnosť nafotíme tak, aby vynikla, vrátane záberov z dronu. Pri bytoch na rekonštrukciu a pri pozemkoch pripravíme vizualizácie, ktoré kupujúcim ukážu, čo všetko sa z nich dá urobiť.'),
    ('marketing', 'Inzercia, ktorá predáva',
     'Ponuku zverejníme na najväčších realitných portáloch aj na našom webe – s textom, ktorý vystihne to podstatné, a s cieľom osloviť práve tých, ktorí hľadajú nehnuteľnosť ako je vaša.'),
    ('staging', 'Home staging',
     'Kupujúci sa rozhodujú očami a emóciou. Nehnuteľnosť pripravíme a zariadime tak, aby oslovila čo najširší okruh záujemcov a pôsobila ako domov, nie ako prázdny priestor. Doplnky odvezieme až po úspešnom predaji.'),
    ('obhliadka', 'Obhliadky ako zážitok',
     'Na obhliadku pripravíme nehnuteľnosť aj občerstvenie, aby sa záujemcovia cítili príjemne a mali čas všetko si v pokoji pozrieť. Záujemcov vopred preveríme, obhliadky vedieme my a vyjednáme pre vás najlepšie podmienky.'),
    ('pravo', 'Zmluvy a dokumenty za vás',
     'Rezervačná a kúpna zmluva, preverenie listu vlastníctva, podklady pre banku aj návrh na vklad do katastra. Všetko vybavíme my – bez toho, aby ste si museli brať dovolenku.'),
    ('hypo', 'Hypotéka pre kupujúceho',
     'Kupujúcemu pomôžeme s financovaním priamo u nás. Obchod tak nestojí na čakaní na banku a peniaze za nehnuteľnosť máte na účte skôr.'),
]


def _form(suffix, dark):
    lab = '#F7F5F0' if dark else '#001939'
    note = '#C7CFDB' if dark else '#4A5566'
    border = '#2A4C7E' if dark else '#CFC8B8'
    return '''<form data-callback="1" style="display: flex; flex-direction: column; gap: 14px; max-width: 560px">
<div style="display: flex; flex-wrap: wrap; gap: 12px">
<label for="cb-tel-%(s)s" style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0)">Vaše telefónne číslo</label>
<input id="cb-tel-%(s)s" name="Telefón" type="tel" required placeholder="Vaše telefónne číslo" autocomplete="tel" style="flex: 1 1 240px; min-width: 0; height: 56px; padding: 0 16px; border-radius: 4px; border: 1px solid %(b)s; background: #FFFFFF; color: #1B2533; font-size: 17px; font-family: inherit">
<button type="button" data-cb-submit="1" class="cb-btn" style="flex: 0 0 auto; height: 56px; padding: 0 28px; border: none; border-radius: 4px; background: #D9AE52; color: #001939; font-size: 16px; font-weight: 800; font-family: inherit; cursor: pointer">Zavolajte mi</button>
</div>
<label style="display: flex; gap: 10px; align-items: flex-start; font-size: 13px; line-height: 1.5; color: %(n)s; cursor: pointer">
<input type="checkbox" name="Súhlas" value="áno" required style="width: 20px; height: 20px; margin: 0; flex: none; accent-color: #B8860B">
<span>Súhlasím so spracovaním telefónneho čísla na účel spätného kontaktu. Viac v časti <a href="ochrana-osobnych-udajov.html" style="color: %(l)s">Ochrana osobných údajov</a>.</span>
</label>
</form>''' % dict(s=suffix, b=border, n=note, l=lab if dark else '#8A6A2B')


def sections():
    cards = ''.join('''<article style="%s background: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 32px; display: flex; flex-direction: column; gap: 14px">
<div style="display: flex; align-items: center; justify-content: space-between">
<svg aria-hidden="true" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#8A6A2B" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">%s</svg>
<span style="font-family: 'Cormorant Garamond', serif; font-size: 36px; font-weight: 700; color: #E4DFD3; line-height: 1">%02d</span>
</div>
<h3 style="margin: 0; font-size: 21px; font-weight: 800; color: #001939">%s</h3>
<p style="margin: 0; font-size: 16px; line-height: 1.65; color: #4A5566">%s</p>
</article>
''' % ('grid-column: 1 / -1;' if i == len(SERVICES) - 1 else '', ICON[k], i + 1, t, d) for i, (k, t, d) in enumerate(SERVICES))

    return '''<!-- PREDAJ HERO -->
<section id="predat" style="position: relative; background: #001939; color: #F7F5F0; overflow: hidden">
<img src="/_blob/4b911459f3fdefed4a64d12dd4650db6" alt="" aria-hidden="true" style="position: absolute; inset: 0; width: 100%%; height: 100%%; object-fit: cover; object-position: 60%% 50%%">
<div aria-hidden="true" class="lm-hero-shade" style="position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,25,57,0.96) 0%%, rgba(0,25,57,0.86) 50%%, rgba(0,25,57,0.55) 100%%)"></div>
<div class="lm-hero" style="position: relative; max-width: 1240px; margin: 0 auto; padding: 112px 24px 120px; display: flex; flex-direction: column; gap: 24px">
<span style="font-size: 13px; font-weight: 700; letter-spacing: 0.3em; color: #D9AE52">CHCEM PREDAŤ / PRENAJAŤ</span>
<h1 style="margin: 0; font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: clamp(2.4rem, 5vw, 4.2rem); line-height: 1.05; max-width: 860px">Sedem dôvodov, prečo s nami predáte rýchlejšie a za lepšiu cenu.</h1>
<p style="margin: 0; font-size: 19px; line-height: 1.6; color: #D3DAE4; max-width: 620px">Nechajte nám svoje číslo a ozveme sa vám ešte v ten istý pracovný deň. Prvá konzultácia aj ocenenie sú nezáväzné a zadarmo.</p>
%(form1)s
<p style="margin: 0; font-size: 15px; color: #C7CFDB">Alebo nám rovno zavolajte: <a href="tel:+421949888663" style="color: #D9AE52; font-weight: 800; text-decoration: none">0949 888 663</a></p>
</div>
</section>

<!-- PREDAJ SLUZBY -->
<section style="padding: 96px 0">
<div style="max-width: 1240px; margin: 0 auto; padding: 0 24px; display: flex; flex-direction: column; gap: 44px">
<div style="display: flex; flex-direction: column; gap: 14px; max-width: 720px">
<span style="font-size: 13px; font-weight: 800; letter-spacing: 0.28em; color: #8A6A2B">ČO PRE VÁS UROBÍME</span>
<h2 style="margin: 0; font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: clamp(2rem, 3.6vw, 3rem); line-height: 1.1; color: #001939">Kompletný servis – od ceny až po odovzdanie kľúčov</h2>
<p style="margin: 0; font-size: 17px; line-height: 1.65; color: #4A5566">Predaj alebo prenájom nehnuteľnosti zaberie veľa času aj nervov. My sa postaráme o všetko a vy budete mať prehľad v každom kroku.</p>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px">
%(cards)s</div>
<div style="display: flex; flex-wrap: wrap; gap: 32px 56px; align-items: center; background: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; overflow: hidden">
<img src="/_blob/42578aedd5d3f6d7da371c0d33b6e465" alt="Pripravená obhliadka nehnuteľnosti s občerstvením pri vchode" loading="lazy" style="flex: 1 1 340px; min-width: 0; max-width: 520px; aspect-ratio: 3 / 4; max-height: 560px; object-fit: cover; display: block">
<div style="flex: 1 1 380px; min-width: 0; padding: 32px; display: flex; flex-direction: column; gap: 16px">
<span style="font-size: 13px; font-weight: 800; letter-spacing: 0.28em; color: #8A6A2B">OBHLIADKA S LUMEROU</span>
<h3 style="margin: 0; font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: clamp(1.8rem, 3vw, 2.4rem); line-height: 1.1; color: #001939">Prvý dojem rozhoduje</h3>
<p style="margin: 0; font-size: 17px; line-height: 1.7; color: #4A5566">Takto vítame záujemcov na našich obhliadkach: pripravený vstup, osviežujúce nápoje, niečo malé pod zub a podklady k nehnuteľnosti na stole. Záujemca sa cíti vítaný, zdrží sa dlhšie a nehnuteľnosť si zapamätá v dobrom.</p>
<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 10px; font-size: 16px; color: #1B2533">
<li style="display: flex; gap: 12px"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#8A6A2B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex: none"><path d="M20 6 9 17l-5-5"></path></svg>Nehnuteľnosť pripravená a vyvetraná pred každou obhliadkou</li>
<li style="display: flex; gap: 12px"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#8A6A2B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex: none"><path d="M20 6 9 17l-5-5"></path></svg>Občerstvenie a podklady pre záujemcov</li>
<li style="display: flex; gap: 12px"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#8A6A2B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex: none"><path d="M20 6 9 17l-5-5"></path></svg>Maklér, ktorý pozná každý detail a odpovie na všetky otázky</li>
</ul>
</div>
</div>
<a href="#vykup" style="display: flex; flex-wrap: wrap; gap: 12px 24px; align-items: center; justify-content: space-between; background: #001939; color: #F7F5F0; text-decoration: none; border-radius: 6px; padding: 28px 32px">
<span style="display: flex; flex-direction: column; gap: 4px"><strong style="font-size: 20px; font-weight: 800">Potrebujete predať rýchlo?</strong><span style="font-size: 15px; color: #C7CFDB">Nehnuteľnosť od vás vykúpime – bez čakania na kupca.</span></span>
<span style="font-weight: 800; color: #D9AE52; font-size: 16px">Výkup nehnuteľností →</span>
</a>
</div>
</section>

<!-- PREDAJ CTA -->
<section style="background: #001939; color: #F7F5F0; padding: 88px 0">
<div style="max-width: 1240px; margin: 0 auto; padding: 0 24px; display: flex; flex-wrap: wrap; gap: 32px 56px; align-items: center; justify-content: space-between">
<div style="flex: 1 1 420px; min-width: 0; display: flex; flex-direction: column; gap: 14px">
<h2 style="margin: 0; font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: clamp(2rem, 3.6vw, 3rem); line-height: 1.1">Začnime vaším predajom ešte dnes</h2>
<p style="margin: 0; font-size: 17px; line-height: 1.6; color: #C7CFDB">Zanechajte nám telefónne číslo. Ozveme sa, prejdeme vaše predstavy a navrhneme ďalší postup – nezáväzne.</p>
</div>
<div style="flex: 1 1 420px; min-width: 0">
%(form2)s
</div>
</div>
</section>

''' % dict(form1=_form('1', True), form2=_form('2', True), cards=cards)
