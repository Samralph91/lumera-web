# -*- coding: utf-8 -*-
"""Texts for the local pages (reality-<mesto>.html) and the blog. Slovak only."""

# listing detail pages by area (static filenames)
TN = ['dom-trencianske-mitice.html', 'byt-28-oktobra.html', 'pozemok-zamarovce.html', 'dom-trencianska-turna.html',
      'byt-odbojarov-prenajom.html', 'pozemok-svinna.html', 'byt-trencianske-teplice.html']

AREAS = [
  dict(
    file='reality-trencin.html', town='Trenčín', short='Trenčín',
    title='Realitná kancelária Trenčín – predaj a kúpa nehnuteľností | LUMERA',
    desc='Realitná kancelária v Trenčíne. Predaj, kúpa, prenájom a výkup bytov, domov a pozemkov v Trenčíne a okolí, nacenenie zdarma, právny servis a hypotéky na jednom mieste.',
    h1='Realitná kancelária Trenčín',
    lead='Predávate, kupujete alebo prenajímate byt, dom či pozemok v Trenčíne? Sme miestna realitná kancelária s kanceláriou na Legionárskej ulici a trenčiansky trh poznáme z každodennej praxe.',
    body=[
      ('Prečo predávať s miestnou kanceláriou',
       ['Trenčín má veľmi rozdielne lokality – iná cena platí na Sihoti, iná na Juhu, v Zámostí alebo v novej výstavbe pri Zlatovciach a Zamarovciach. Cenu preto nestanovujeme podľa celoslovenských priemerov, ale podľa nehnuteľností, ktoré sa naozaj predali vo vašej štvrti.',
        'Kupujúcich, ktorí hľadajú v Trenčíne, aktívne evidujeme. Časť nehnuteľností tak predáme ešte predtým, než sa dostanú na realitné portály.']),
      ('Čo pre vás v Trenčíne urobíme',
       ['Pripravíme trhové nacenenie, profesionálne fotky so zábermi z dronu, pri bytoch na rekonštrukciu aj vizualizácie a nehnuteľnosť pred obhliadkami pripravíme formou home stagingu. Obhliadky vedieme sami, preverujeme záujemcov a vyjednávame o cene.',
        'Zmluvy, preverenie listu vlastníctva aj návrh na vklad do katastra vybavíme na jednom mieste. Kupujúcemu pomôžeme s hypotékou, takže obchod nestojí na čakaní na banku.']),
    ],
    listings=TN[:6], listings_title='Aktuálne nehnuteľnosti v Trenčíne a okolí',
    faq=[
      ('Koľko stojí nacenenie nehnuteľnosti v Trenčíne?', 'Nacenenie je bezplatné a nezáväzné. Stačí vyplniť krátky formulár na stránke Nacenenie alebo nám zavolať a odhad trhovej ceny vám pošleme do 24 hodín.'),
      ('Ako dlho trvá predaj bytu v Trenčíne?', 'Závisí najmä od ceny a stavu bytu. Správne nacenený a dobre odprezentovaný byt sa v Trenčíne často predá v priebehu niekoľkých týždňov. Ak potrebujete peniaze hneď, ponúkneme aj výkup.'),
      ('Pôsobíte aj mimo mesta Trenčín?', 'Áno. Okrem Trenčína pracujeme v celom okrese a v okolí – napríklad v Trenčianskych Tepliciach, Nemšovej, Dubnici nad Váhom, Bánovciach nad Bebravou a v okolitých obciach.'),
    ]),
  dict(
    file='reality-trencianske-teplice.html', town='Trenčianske Teplice', short='Trenčianske Teplice',
    title='Reality Trenčianske Teplice – predaj bytov a domov | LUMERA',
    desc='Predaj a kúpa bytov, domov a pozemkov v Trenčianskych Tepliciach. Nacenenie zdarma, prezentácia nehnuteľnosti, právny servis a hypotéky – LUMERA Real Estate.',
    h1='Reality Trenčianske Teplice',
    lead='Kúpeľné mesto Trenčianske Teplice láka na trvalé bývanie aj na investíciu. Pomôžeme vám nehnuteľnosť v Tepliciach a okolí predať, kúpiť alebo prenajať – od nacenenia až po odovzdanie kľúčov.',
    body=[
      ('Bývanie aj investícia',
       ['Byty v Trenčianskych Tepliciach kupujú rodiny, ktoré chcú pokoj a prírodu s Trenčínom na dosah, ale aj investori, ktorí ich prenajímajú kúpeľným hosťom, turistom či dlhodobým nájomníkom. Pri predaji preto nehnuteľnosť prezentujeme tak, aby oslovila obe skupiny.',
        'Okrem samotného mesta pracujeme aj v okolitých obciach doliny – vrátane rodinných domov, chalúp a pozemkov.']),
      ('Kompletný servis na jednom mieste',
       ['Nacenenie podľa reálnych predajov, fotky a dron, home staging, obhliadky s prípravou nehnuteľnosti, zmluvy a návrh na vklad do katastra. Kupujúcemu pomôžeme s hypotékou.']),
    ],
    listings=['byt-trencianske-teplice.html', 'dom-trencianske-mitice.html', 'byt-28-oktobra.html'],
    listings_title='Ponuka v Trenčianskych Tepliciach a okolí',
    faq=[
      ('Oplatí sa kúpiť byt v Trenčianskych Tepliciach na prenájom?', 'Kúpeľné mesto má dopyt po krátkodobom aj dlhodobom prenájme. Výnos závisí od ceny, stavu a polohy bytu – radi vám pripravíme orientačný prepočet pre konkrétnu nehnuteľnosť.'),
      ('Pomôžete mi predať nehnuteľnosť v Tepliciach, ak bývam inde?', 'Áno. Obhliadky, komunikáciu so záujemcami aj väčšinu dokumentov vybavíme za vás. Zmluvy sa dajú podpísať aj na diaľku.'),
    ]),
  dict(
    file='reality-dubnica-nad-vahom.html', town='Dubnica nad Váhom', short='Dubnica nad Váhom',
    title='Reality Dubnica nad Váhom – predaj a kúpa nehnuteľností | LUMERA',
    desc='Predávate alebo kupujete byt či dom v Dubnici nad Váhom? Bezplatné nacenenie, profesionálna prezentácia, právny servis a hypotéky – LUMERA Real Estate.',
    h1='Reality Dubnica nad Váhom',
    lead='Dubnica nad Váhom je priemyselné mesto s množstvom pracovných príležitostí v okolí – a s tým aj so stálym záujmom o byty. Pomôžeme vám tu predať, kúpiť aj prenajať nehnuteľnosť.',
    body=[
      ('Pre koho je Dubnica zaujímavá',
       ['Byty v Dubnici hľadajú mladé rodiny, ľudia pracujúci v okolitých firmách aj investori, ktorí chcú byt prenajímať. Pri predaji sa zameriavame práve na týchto kupujúcich a cenu nastavujeme podľa toho, za koľko sa porovnateľné byty skutočne predali.',
        'Z Trenčína sme v Dubnici rýchlo, takže obhliadky vieme zorganizovať pružne – aj podvečer alebo cez víkend.']),
      ('Ako postupujeme',
       ['Po bezplatnom nacenení pripravíme fotky, inzerciu a obhliadky. Postaráme sa o rezervačnú a kúpnu zmluvu, preverenie listu vlastníctva aj návrh na vklad do katastra. Ak potrebujete predať rýchlo, ponúkneme výkup.']),
    ],
    listings=TN[:4], listings_title='Ponuka v okolí Dubnice nad Váhom',
    faq=[
      ('Vykupujete nehnuteľnosti aj v Dubnici nad Váhom?', 'Áno. Ak potrebujete predať rýchlo – napríklad pri dedičstve, sťahovaní alebo exekúcii – pripravíme záväznú ponuku na výkup.'),
      ('Momentálne nemáte v Dubnici ponuku. Viete mi niečo nájsť?', 'Napíšte nám, čo hľadáte. Nové nehnuteľnosti často predáme skôr, než sa dostanú na web, a záujemcom z nášho zoznamu ich ponúkame ako prvým.'),
    ]),
  dict(
    file='reality-nemsova.html', town='Nemšová', short='Nemšová',
    title='Reality Nemšová – predaj domov, bytov a pozemkov | LUMERA',
    desc='Predaj a kúpa rodinných domov, bytov a pozemkov v Nemšovej a okolí. Nacenenie zdarma, prezentácia, zmluvy aj hypotéka – LUMERA Real Estate Trenčín.',
    h1='Reality Nemšová',
    lead='Nemšová a jej okolie sú obľúbené u rodín, ktoré chcú bývať v rodinnom dome, no mať Trenčín blízko. Pomôžeme vám predať alebo kúpiť dom, byt či stavebný pozemok.',
    body=[
      ('Domy a pozemky v okolí Trenčína',
       ['Pri rodinných domoch a pozemkoch rozhoduje najmä poloha, inžinierske siete a územný plán. Pred predajom preto preveríme podklady, aby kupujúci dostal jasné odpovede a obchod sa nezasekol pri banke.',
        'Pozemky prezentujeme aj pomocou vizualizácií možnej výstavby – kupujúci tak hneď vidí, aký dom na pozemku môže stáť.']),
      ('Servis od nacenenia po kataster',
       ['Bezplatné nacenenie, fotky a dron, inzercia, obhliadky, zmluvy, návrh na vklad do katastra a hypotéka pre kupujúceho.']),
    ],
    listings=['pozemok-zamarovce.html', 'dom-trencianska-turna.html', 'pozemok-svinna.html'],
    listings_title='Domy a pozemky v okolí',
    faq=[
      ('Predávam pozemok. Čo budem potrebovať?', 'Základom je list vlastníctva, informácia o inžinierskych sieťach a ideálne aj územnoplánovacia informácia z obce. S ich zabezpečením vám pomôžeme.'),
      ('Pomôžete s predajom rodinného domu, ktorý potrebuje rekonštrukciu?', 'Áno. Pri domoch na rekonštrukciu pripravujeme vizualizácie, ktoré kupujúcim ukážu, ako by mohol dom vyzerať po úpravách.'),
    ]),
  dict(
    file='reality-banovce-nad-bebravou.html', town='Bánovce nad Bebravou', short='Bánovce nad Bebravou',
    title='Reality Bánovce nad Bebravou – domy, chalupy a pozemky | LUMERA',
    desc='Predaj a kúpa nehnuteľností v Bánovciach nad Bebravou a okolí – rodinné domy, chalupy, byty a pozemky. Nacenenie zdarma, právny servis a hypotéky.',
    h1='Reality Bánovce nad Bebravou',
    lead='V Bánovciach nad Bebravou a okolitých obciach predávame byty, rodinné domy, vidiecke chalupy aj stavebné pozemky. Dostupnejšie ceny lákajú kupujúcich z Trenčína aj zo vzdialenejších regiónov.',
    body=[
      ('Vidiecke domy a chalupy',
       ['Vidiecke domy hľadajú ľudia, ktorí chcú vlastnú chalupu na víkendy, aj rodiny, ktoré plánujú rekonštrukciu na trvalé bývanie. Pri takýchto nehnuteľnostiach pomáhajú vizualizácie a poctivý popis stavu – kupujúci vie, do čoho ide, a obchod je férový pre obe strany.']),
      ('Celý proces za vás',
       ['Postaráme sa o nacenenie, prezentáciu, obhliadky, zmluvy aj kataster. Ak chcete predať rýchlo, pripravíme ponuku na výkup.']),
    ],
    listings=['dom-trebichava.html', 'pozemok-svinna.html', 'dom-trencianske-mitice.html'],
    listings_title='Ponuka v okolí Bánoviec nad Bebravou',
    faq=[
      ('Predáte aj starší dom na dedine?', 'Áno. Staršie domy a chalupy majú svojich kupujúcich – dôležitá je správna cena a pravdivá prezentácia stavu. Pomôžeme vám s oboma.'),
      ('Je nacenenie naozaj zadarmo?', 'Áno, nacenenie je bezplatné a nezáväzné. Rozhodnutie, či nehnuteľnosť predáte, je len na vás.'),
    ]),
]

# ---------------------------------------------------------------- blog
AUTHOR = 'Samuel Bucha'
POSTS = [
  dict(
    file='blog-predaj-bytu-krok-za-krokom.html', date='2026-11-02',
    title='Predaj bytu krok za krokom: od nacenenia po kataster',
    desc='Ako predať byt bez stresu? Postup krok za krokom – nacenenie, príprava, inzercia, obhliadky, rezervačná a kúpna zmluva, návrh na vklad a odovzdanie bytu.',
    lead='Predaj bytu sa skladá z niekoľkých krokov, ktoré na seba nadväzujú. Keď ich poznáte vopred, vyhnete sa zbytočným chybám, zľavám aj čakaniu.',
    body=[
      ('h2', '1. Zistite reálnu cenu'),
      ('p', 'Najčastejšia chyba pri predaji je príliš vysoká cena na začiatku. Byt potom visí na portáloch, kupujúci si ho „zapamätajú“ a nakoniec sa predáva so zľavou. Cenu preto nastavujte podľa bytov, ktoré sa vo vašej lokalite naozaj predali – nie podľa toho, za koľko sú ponúkané.'),
      ('h2', '2. Pripravte dokumenty'),
      ('ul', ['list vlastníctva (overíme ho za vás),', 'kúpna alebo darovacia zmluva, prípadne osvedčenie o dedičstve,', 'potvrdenie od správcu alebo spoločenstva vlastníkov o nedoplatkoch,', 'energetický certifikát, ak ho máte,', 'pri hypotéke na byte údaje o úvere – banka vydá súhlas s predajom a vyčíslenie zostatku.']),
      ('h2', '3. Pripravte byt a urobte dobré fotky'),
      ('p', 'Upratanie, vyvetranie a odstránenie osobných vecí urobí viac, než si myslíte. Pri prázdnych bytoch pomáha home staging – byt pôsobí ako domov a kupujúci si vie predstaviť, ako by v ňom býval. Profesionálne fotky sú prvé, čo záujemca uvidí, a často rozhodnú, či vôbec príde na obhliadku.'),
      ('h2', '4. Inzercia a obhliadky'),
      ('p', 'Inzerát má vystihnúť to podstatné: dispozíciu, stav, poschodie, náklady a okolie. Na obhliadke buďte pripravení odpovedať na otázky o nákladoch, susedoch, stave domu a plánovaných opravách. Záujemcov je dobré vopred preveriť – najmä to, či majú vyriešené financovanie.'),
      ('h2', '5. Rezervačná zmluva a záloha'),
      ('p', 'Keď sa s kupujúcim dohodnete, podpíšete rezervačnú zmluvu a kupujúci zloží rezervačný poplatok. Zmluva by mala jasne určiť, čo sa so zálohou stane, ak niektorá strana od obchodu odstúpi, a do kedy sa podpíše kúpna zmluva.'),
      ('h2', '6. Kúpna zmluva a úschova peňazí'),
      ('p', 'Ak kupujúci financuje kúpu hypotékou, banka zvyčajne vyžaduje kúpnu zmluvu a záložnú zmluvu. Peniaze je bezpečné viesť cez úschovu u notára, advokáta alebo v banke – predávajúci ich dostane až po zápise vlastníctva kupujúceho do katastra.'),
      ('h2', '7. Návrh na vklad do katastra'),
      ('p', 'Návrh na vklad sa podáva na okresný úrad, katastrálny odbor. Pri bežnom konaní je správny poplatok 50 € pri elektronickom podaní a 100 € pri podaní v papierovej podobe. Ak sa ponáhľate, môžete požiadať o zrýchlené konanie do 15 dní za 150 € elektronicky alebo 300 € papierovo.'),
      ('h2', '8. Odovzdanie bytu'),
      ('p', 'Pri odovzdaní spíšte preberací protokol so stavmi meračov a odovzdajte všetky kľúče. Nezabudnite prepísať energie a oznámiť zmenu vlastníka správcovi domu.'),
      ('cta', 'Chcete to mať bez starostí? Všetky kroky – od nacenenia po kataster – vybavíme za vás.'),
    ]),
  dict(
    file='blog-dan-z-predaja-nehnutelnosti.html', date='2026-11-02',
    title='Daň pri predaji nehnuteľnosti: kedy ju platíte a kedy nie',
    desc='Kedy je predaj bytu alebo domu oslobodený od dane? Pravidlo 5 rokov, zdedená nehnuteľnosť, výdavky, ktoré si môžete odpočítať, a termín daňového priznania.',
    lead='Pri predaji nehnuteľnosti sa mnohí predávajúci obávajú dane. V mnohých prípadoch ju však neplatíte vôbec. Rozhoduje najmä to, ako dlho nehnuteľnosť vlastníte.',
    body=[
      ('h2', 'Pravidlo piatich rokov'),
      ('p', 'Ak predávate nehnuteľnosť ako fyzická osoba (nie ako podnikateľ) a od jej nadobudnutia uplynulo viac ako 5 rokov, príjem z predaja je od dane z príjmov oslobodený. Lehota sa počíta od dňa, keď bol váš vlastnícky vzťah zapísaný do katastra – teda od právoplatnosti rozhodnutia o povolení vkladu, nie od podpisu kúpnej zmluvy.'),
      ('h2', 'Zdedená nehnuteľnosť'),
      ('p', 'Ak ste nehnuteľnosť zdedili v priamom rade (napríklad od rodičov alebo starých rodičov), do lehoty piatich rokov sa započítava aj doba, počas ktorej ju vlastnil poručiteľ. Ak spolu presiahne 5 rokov, predaj je oslobodený. Pri dedení mimo priameho radu sa ráta len doba od nadobudnutia dedičstva.'),
      ('h2', 'Keď predávate skôr ako po piatich rokoch'),
      ('p', 'Zdaňuje sa len zisk, nie celá predajná cena. Od príjmu si môžete odpočítať preukázateľné výdavky, napríklad:'),
      ('ul', ['pôvodnú kúpnu cenu,', 'náklady na rekonštrukciu a technické zhodnotenie,', 'úroky a poplatky z hypotéky,', 'poplatky za znalecký posudok a províziu realitnej kancelárie.']),
      ('p', 'Zo zisku sa platí daň z príjmov a zdravotný odvod. Presná výška závisí od vašich ostatných príjmov v danom roku. Daňové priznanie typu B treba podať a daň zaplatiť do 31. marca nasledujúceho roka; lehotu je možné predĺžiť oznámením správcovi dane.'),
      ('h2', 'Praktické tipy'),
      ('ul', ['Odkladajte si doklady o kúpe aj o všetkých investíciách do nehnuteľnosti – pri predaji pred uplynutím 5 rokov znížia daň.', 'Ak sa blíži hranica piatich rokov, oplatí sa načasovať podpis kúpnej zmluvy a podanie návrhu na vklad tak, aby ste ju bezpečne prekročili.', 'Pri nehnuteľnosti zahrnutej v obchodnom majetku podnikateľa platia iné pravidlá.']),
      ('note', 'Článok má informatívny charakter a nenahrádza daňové poradenstvo. Pravidlá sa môžu meniť – v konkrétnom prípade odporúčame overiť si situáciu u daňového poradcu. Radi vám odporučíme overeného odborníka.'),
      ('cta', 'Plánujete predaj a nie ste si istí, či budete platiť daň? Prejdeme to spolu pri bezplatnej konzultácii.'),
    ]),
  dict(
    file='blog-hypoteka-2027-zmeny.html', date='2026-11-02',
    title='Hypotéky od roku 2027: mladí až 90 %, investori najviac 70 %',
    desc='Národná banka Slovenska mení od 1. januára 2027 pravidlá hypoték. Kto dostane úver až do 90 % hodnoty nehnuteľnosti, pre koho platí 80 % a kedy len 70 %.',
    lead='Národná banka Slovenska schválila zmeny pravidiel pre hypotéky, ktoré platia od 1. januára 2027. Mladým ľuďom uľahčia prvé bývanie, kupujúcim ďalších investičných bytov naopak sprísnia financovanie.',
    body=[
      ('h2', 'Čo sa mení'),
      ('ul', ['<strong>Do 90 % hodnoty nehnuteľnosti</strong> – žiadatelia do 35 rokov, ktorí kupujú alebo stavajú svoje prvé bývanie.', '<strong>Do 80 %</strong> – základný limit pre ostatných žiadateľov.', '<strong>Najviac 70 %</strong> – ak financujete tretiu alebo ďalšiu nehnuteľnosť na bývanie.']),
      ('p', 'Banky budú nové pravidlá zavádzať postupne, pretože musia upraviť svoje procesy – napríklad overovanie, koľko nehnuteľností už žiadateľ vlastní.'),
      ('h2', 'Čo to znamená v praxi'),
      ('p', 'Pri byte za 150 000 € potrebuje kupujúci s limitom 80 % vlastné zdroje aspoň 30 000 € plus poplatky. Mladý žiadateľ, ktorý splní podmienky pre 90 %, môže mať vlastných zdrojov len 15 000 €. Investor, ktorý kupuje už tretí byt, bude potrebovať najmenej 45 000 €.'),
      ('p', 'Výška úveru nie je len otázkou LTV. Banka naďalej posudzuje príjem, existujúce dlhy, vek a celkovú zadlženosť. Aj keď splníte podmienky pre 90 %, banka môže schváliť nižšiu sumu.'),
      ('h2', 'Ako sa pripraviť'),
      ('ul', ['Spočítajte si vlastné zdroje vrátane poplatkov za kataster, znalecký posudok a prípadnú províziu.', 'Splaťte alebo zrušte nevyužívané kreditné karty a povolené prečerpania – znižujú sumu, ktorú vám banka požičia.', 'Ak spĺňate podmienky pre 90 % od roku 2027, porovnajte ponuky viacerých bánk – každá ich môže zaviesť v inom čase.']),
      ('p', 'Orientačnú splátku si môžete hneď vypočítať v našej <a href="hypoteky.html">hypotekárnej kalkulačke</a>.'),
      ('note', 'Zdroj: rozhodnutie Bankovej rady NBS o úprave pravidiel pre financovanie bývania (september 2026). Článok má informatívny charakter.'),
      ('cta', 'Chcete vedieť, akú hypotéku dostanete? Porovnáme ponuky bánk a vybavíme úver od žiadosti až po čerpanie – bezplatne.'),
    ]),
  dict(
    file='blog-ako-pripravit-nehnutelnost-na-predaj.html', date='2026-11-02',
    title='Ako pripraviť nehnuteľnosť na predaj: 9 tipov, ktoré zvýšia cenu',
    desc='Prvý dojem rozhoduje. Ako pripraviť byt alebo dom na fotenie a obhliadky – upratanie, drobné opravy, home staging, svetlo a vôňa. Praktické tipy od makléra.',
    lead='Kupujúci sa rozhodujú očami a emóciou. Pár drobností pred fotením a obhliadkami môže rozhodnúť o tom, či sa nehnuteľnosť predá rýchlo a za dobrú cenu.',
    body=[
      ('h2', 'Pred fotením'),
      ('ul', ['<strong>Menej je viac.</strong> Odneste osobné veci, fotky, magnetky a väčšinu dekorácií. Kupujúci si musí vedieť predstaviť, že tu býva on.', '<strong>Svetlo.</strong> Roztiahnite závesy, umyte okná a vymeňte nefunkčné žiarovky. Svetlé priestory pôsobia väčšie.', '<strong>Drobné opravy.</strong> Kvapkajúci kohútik, uvoľnená kľučka alebo prasknutá dlaždica pôsobia ako signál, že „tu bude treba veľa robiť“.', '<strong>Kúpeľňa a kuchyňa.</strong> Tieto miestnosti predávajú. Prázdne linky, čisté škáry a nový uterák urobia veľký rozdiel.']),
      ('h2', 'Home staging'),
      ('p', 'Prázdny byt pôsobí chladne a menší, než v skutočnosti je. Pri home stagingu ho zariadime tak, aby oslovil čo najviac záujemcov – stačí niekoľko kusov nábytku, textílie a doplnky. Doplnky odvezieme až po predaji.'),
      ('h2', 'Pred obhliadkou'),
      ('ul', ['<strong>Vyvetrajte</strong> a vyhnite sa výrazným vôňam a vareniu tesne pred obhliadkou.', '<strong>Teplota.</strong> V zime prikúrte, v lete vyvetrajte ráno a zatiahnite žalúzie.', '<strong>Pripravte podklady</strong> – výšku nákladov, energetický certifikát, informácie o dome a rekonštrukciách.', '<strong>Nechajte priestor maklérovi.</strong> Záujemca sa cíti slobodnejšie, keď si nehnuteľnosť môže pozrieť bez majiteľa.', '<strong>Malé pohostenie</strong> – voda, káva, niečo malé pod zub. Na našich obhliadkach je to štandard a záujemcovia si nehnuteľnosť zapamätajú v dobrom.']),
      ('cta', 'Prípravu nehnuteľnosti, fotky, home staging aj obhliadky urobíme za vás. Pozrite si, ako pracujeme.'),
    ]),
]
