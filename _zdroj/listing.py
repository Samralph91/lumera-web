"""Property detail pages (gallery + facts + description), for the canvas (dc) and lumera.sk (static)."""
import json, os

REAL, VIS, PLAN, VISB, LOT, SIT = 'real', 'vis', 'plan', 'visb', 'lot', 'sit'
BADGE = {REAL: 'Aktuálny stav', VIS: 'Vizualizácia možnej rekonštrukcie', PLAN: 'Pôdorys (orientačný)', VISB: 'Vizualizácia možnej výstavby', LOT: 'Aktuálny stav · vyznačená hranica pozemku', SIT: 'Situácia – štúdia možnej zástavby'}
BADGE_STYLE = {
    REAL: 'background: #001939; color: #F7F5F0',
    VIS: 'background: #D9AE52; color: #001939',
    PLAN: 'background: #FFFFFF; color: #001939',
    VISB: 'background: #D9AE52; color: #001939',
    LOT: 'background: #001939; color: #F7F5F0',
    SIT: 'background: #FFFFFF; color: #001939',
}

LISTINGS = {
    'byt28': {
        'marker': 'BYT 28. OKTÓBRA',
        'folder': 'byt-28-oktobra',
        'tag': 'Predaj',
        'title': '3-izbový byt s 2 balkónmi v tehlovom dome',
        'place': 'Trenčín, ulica 28. októbra',
        'price': '139 900 €',
        'per_m2': '2 088 € / m²',
        'facts': [
            ('Výmera', '67 m²'), ('Počet izieb', '3'), ('Poschodie', '2. z 6'), ('Konštrukcia', 'tehlová'),
            ('Stav', 'pôvodný, na rekonštrukciu'), ('Balkóny', '2'), ('Pivnica', 'murovaná, cca 2 m²'),
            ('Kúrenie', 'ústredné'), ('Mesačné náklady', 'cca 150 €'), ('Rok výstavby', '1970 – 1989'),
            ('Energetický certifikát', 'v príprave'),
        ],
        'desc': [
            'Na predaj ponúkame 3-izbový byt s dvoma balkónmi v tehlovom dome na ulici 28. októbra v Trenčíne. '
            'Byt má 67 m² a nachádza sa na 2. poschodí zo 6. Na poschodí sú len tri byty. Dom je obnovený, zateplený a má nový výťah.',
            'Byt je v pôvodnom stave – v izbách sú drevené parkety, pôvodné okná a umakartové jadro – a je pripravený '
            'na rekonštrukciu podľa vašich predstáv. Jeden balkón je prístupný z kuchyne, druhý z izby a smeruje do tichšej časti domu. '
            'K bytu patrí murovaná pivnica.',
            'V okolí je trh, detské ihrisko, školy, nemocnica aj poliklinika. Predávajúci ponúka aj kompletnú rekonštrukciu '
            'podľa požiadaviek kupujúceho; zmeny dispozície si vyžadujú technické posúdenie.',
        ],
        'note': 'Vizualizácie ukazujú, ako by mohol byt vyzerať po rekonštrukcii. Nie sú fotografiami súčasného stavu.',
        'inzerat': 'https://www.nehnutelnosti.sk/detail/Juy2WHflF9P/lumera--na-predaj-3-izbovy-byt-s-2-balkonmi-v-tehlovom-dome--67-m--trencinl-28-oktobra',
        # (file, kind, canvas blob)
        'photos': [
            ('01.jpg', REAL, '/_blob/d8315ec8465cc4146e0e6775269c5a86'),
            ('02.jpg', REAL, '/_blob/6b1b8665983ab794a43e47438001762d'),
            ('03.jpg', REAL, '/_blob/e29395f226d2132218fc070b352c547a'),
            ('04.jpg', REAL, '/_blob/c32d8b646151a5113fd8af4ddad6dac8'),
            ('05.jpg', REAL, '/_blob/5553df478e70da031c767c261b7f78d0'),
            ('06.jpg', VIS, '/_blob/eab3d4bf8756a41d04550b9270e29e12'),
            ('07.jpg', VIS, '/_blob/21375d7fe483d8799aff148d95106fd3'),
            ('08.jpg', VIS, '/_blob/2eed52d48df1276310545946aa23c08f'),
            ('09.jpg', VIS, '/_blob/8f22463160a96467503cda98e1281477'),
            ('10.jpg', PLAN, '/_blob/81b43654eb696338669a1179d089af8f'),
        ],
    },
    'zamarovce': {
        'marker': 'POZEMOK ZAMAROVCE',
        'folder': 'pozemok-zamarovce',
        'aspect': '16 / 9',
        'tag': 'Predaj',
        'title': 'Slnečný pozemok 770 m² v pokojnej slepej ulici',
        'place': 'Zamarovce, Pod Kopánky – Trenčín na dosah',
        'price': '143 400 €',
        'per_m2': '186 € / m²',
        'facts': [
            ('Výmera', '770 m²'), ('Typ', 'stavebný pozemok pre rodinný dom'),
            ('Šírka', 'cca 14 m (vpredu 14,5 m, vzadu 13,5 m)'), ('Terén', 'rovinatý, slnečný'),
            ('Oplotenie', 'áno, s vjazdovou bránou'), ('Voda', 'vlastná studňa, cca 16 m'), ('Elektrina', '230 V'),
            ('Plyn', 'v blízkosti pozemku'), ('Kanalizácia', 'nie – žumpa'),
            ('Územný plán', 'schválený, zastavanosť max. 35 %, max. 2 nadzemné podlažia'),
            ('Na pozemku', 'záhradný domček'),
        ],
        'desc': [
            'Na predaj ponúkame slnečný rovinatý stavebný pozemok s výmerou 770 m² v Zamarovciach, na konci pokojnej slepej ulice '
            'Pod Kopánky – mimo prejazdnej dopravy a s Trenčínom na dosah. Pozemok je oplotený, má vjazdovú bránu a pozdĺž zadnej '
            'hranice vzrastlé tuje.',
            'Pretiahnutý tvar so šírkou približne 14 m umožňuje oddeliť vstupnú časť od súkromnej obytnej zóny a záhrady. '
            'Na pozemku je vlastná studňa (cca 16 m) a elektrina 230 V, plyn je podľa podkladov v blízkosti pozemku. Kanalizácia nie je, '
            'odpadové vody sa riešia žumpou. Súčasťou predaja je aj časť príjazdovej cesty.',
            'Pozemok je podľa územného plánu určený na výstavbu rodinného domu s maximálnou zastavanosťou 35 % a najviac dvoma nadzemnými '
            'podlažiami. K dispozícii sú architektonické podklady pre rodinný dom s garážou, podľa ktorých vznikli vizualizácie. '
            'V blízkosti je materská škola.',
        ],
        'note': 'Vizualizácie sú len ilustračné. Predmetom predaja je pozemok – dom, garáž, bazén ani záhradné úpravy nie sú súčasťou ceny.',
        'inzerat': 'https://www.nehnutelnosti.sk/detail/JuC7ZA7Nc1h/lumera--slnecny-pozemok-770-m-v-zamarovciach--pokoj-slepej-ulicel-trencin-na-dosah',
        'photos': [
            ('01.jpg', VISB, '/_blob/c5f940361bd2d099ee4ba1b507187565'),
            ('02.jpg', VISB, '/_blob/ff7f41fce688c7bbccc95f74ca695ad0'),
            ('03.jpg', VISB, '/_blob/4cae63958c83adc487136b2fbe219112'),
            ('04.jpg', REAL, '/_blob/a1fc233c310823d6a97671efd26efc9a'),
            ('05.jpg', REAL, '/_blob/b919d9db6a21bf5d94d1265761a1eb74'),
            ('06.jpg', REAL, '/_blob/089ce571376eb002820b99e47971af0a'),
        ],
    },
    'trebichava': {
        'marker': 'DOM TREBICHAVA',
        'folder': 'dom-trebichava',
        'aspect': '16 / 9',
        'tag': 'Predaj',
        'title': 'Vidiecky dom v Trebichave – príležitosť na vlastnú chalupu',
        'place': 'Trebichava, okres Bánovce nad Bebravou',
        'price': '17 990 €',
        'per_m2': '360 € / m² úžitkovej plochy',
        'facts': [
            ('Typ', 'rodinný dom (na LV)'), ('Úžitková plocha', '50 m²'), ('Pozemok', '327 m² vrátane zastavanej plochy'),
            ('Stav', 'pôvodný, na rekonštrukciu'), ('Rok výstavby', '1946 – 1969'), ('Konštrukcia', 'zmiešaná'),
            ('Terén', 'mierne svahovitý'), ('Voda', 'vlastná studňa'), ('Elektrina', '230 V, zavedená v dome'),
            ('Plyn', 'nie'), ('Kanalizácia', 'nie'), ('WC', 'suché, za domom'), ('Energetický certifikát', 'nie je'),
        ],
        'desc': [
            'Na predaj ponúkame vidiecky dom v obci Trebichava v okrese Bánovce nad Bebravou. Dom je na liste vlastníctva '
            'zapísaný ako rodinný dom a spolu s pozemkom má 327 m² vrátane zastavanej plochy.',
            'Nehnuteľnosť je v pôvodnom stave a je určená na rekonštrukciu – ideálna pre toho, kto hľadá rekreačné bývanie '
            'a chce si dispozíciu aj vybavenie prispôsobiť podľa seba. Na pozemku je vlastná studňa, v dome je zavedená '
            'elektrina 230 V. Plyn ani kanalizácia nie sú, za domom je suché WC.',
            'Pokojné prostredie obklopené prírodou je ako stvorené na víkendy mimo mesta, prechádzky a oddych. '
            'Autobusová zastávka je hneď pri dome. Ak hľadáte vlastnú chalupu za rozumnú cenu, dohodnite si obhliadku.',
        ],
        'note': 'Vizualizácie ukazujú, ako by mohol dom vyzerať po rekonštrukcii. Nie sú fotografiami súčasného stavu.',
        'inzerat': 'https://www.nehnutelnosti.sk/detail/JuPG9x3kKat/lumera--vidiecky-dom-v-trebichave-za-17-990---prilezitost-na-vlastnu-chalupu',
        'photos': [
            ('01.jpg', LOT, '/_blob/be57e36b289857a11f370d99e5b71e10'),
            ('02.jpg', VIS, '/_blob/118190a0c7faf7999b41ceaec01b9c73'),
            ('03.jpg', VIS, '/_blob/71cde9ae3a9862fbb186072030696f22'),
            ('04.jpg', REAL, '/_blob/a840aa31a2a6cd1b1972427fe6d6a8c9'),
            ('05.jpg', REAL, '/_blob/ee53a8c82790b3863725654c86211732'),
            ('06.jpg', REAL, '/_blob/f11197097dceb8736b5e1d3517bca981'),
            ('07.jpg', REAL, '/_blob/2ae69f00a8906fde3daf1f2b76e74d9d'),
        ],
    },
    'myjava': {
        'marker': 'BYT MYJAVA',
        'folder': 'byt-myjava',
        'tag': 'Predaj',
        'title': '1-izbový byt v pokojnej štvrti',
        'place': 'Myjava, Dolná štvrť',
        'price': '69 900 €',
        'per_m2': '2 056 € / m²',
        'facts': [
            ('Výmera', '34 m²'), ('Počet izieb', '1'), ('Poschodie', '1. z 6'), ('Konštrukcia', 'panelová'), ('Stav', 'čiastočná rekonštrukcia'),
            ('Bytové jadro', 'murované'), ('Elektroinštalácia', 'nová'), ('Kúrenie', 'ústredné'),
            ('Energetická trieda', 'B'), ('Výťah', 'áno, bezbariérový prístup'), ('Pivnica', '2,5 m²'),
            ('Komora', 'na medzipodlaží'), ('Zariadenie', 'čiastočne zariadený'), ('Dostupnosť', 'ihneď'),
        ],
        'desc': [
            'Na predaj ponúkame 1-izbový byt s výmerou 34 m² v pokojnej Dolnej štvrti v Myjave. Je ideálny ako dostupné '
            'vlastné bývanie pre jednotlivca, mladý pár či seniora, ale aj ako investícia na prenájom.',
            'Byt má murované bytové jadro, novú elektroinštaláciu a ústredné kúrenie. Do domu je bezbariérový prístup '
            'a výťah. K bytu patrí pivnica s výmerou 2,5 m² a komora na medzipodlaží. Byt je čiastočne zariadený a voľný ihneď.',
            'V okolí sú obchody, služby, zastávky verejnej dopravy aj detské ihrisko. Základná škola je približne 400 m '
            'od domu. Dohodnite si obhliadku.',
        ],
        'note': '',
        'agent': ('Maklérka', 'Katarína Ribovičová', '0904 255 252'),
        'inzerat': 'https://www.nehnutelnosti.sk/detail/Ju6VgYo-1et/na-predaj-1-izbovy-byt--myjaval-dolna-stvrt',
        'photos': [
            ('01.jpg', REAL, '/_blob/0b501106e661c42b5f9bdc145791bb3f'),
            ('02.jpg', REAL, '/_blob/1f35197460de722bf4fb96190d8eb8ff'),
            ('03.jpg', REAL, '/_blob/ca8da058e9bf491a49cd9fbd4e48880f'),
            ('04.jpg', REAL, '/_blob/6a89850396b74b743de45fdf7d10d4c1'),
            ('05.jpg', REAL, '/_blob/e9867dc6ca47e9e320c1df0c6fad0c3e'),
            ('06.jpg', REAL, '/_blob/f24281e7a3c5187b98b4b378a90119ca'),
        ],
    },
    'mitice': {
        'marker': 'DOM MITICE',
        'folder': 'dom-mitice',
        'aspect': '16 / 9',
        'tag': 'Exkluzívne',
        'title': '5-izbový nízkoenergetický dom s dvojgarážou a fotovoltikou',
        'place': 'Trenčianske Mitice – Zemianske Mitice',
        'price': 'Info v RK',
        'per_m2': 'Cenu vám radi povieme osobne',
        'facts': [
            ('Úžitková plocha', '180 m²'), ('Zastavaná plocha', '220 m²'), ('Pozemok', '690 m²'), ('Počet izieb', '5'),
            ('Stav', 'kompletná rekonštrukcia'), ('Konštrukcia', 'tehlová'), ('Energetická trieda', 'A0'),
            ('Kúrenie', 'tepelné čerpadlo, podlahové'), ('Fotovoltika', 'áno'), ('Garáž', 'dvojgaráž, 32 m²'),
            ('Terasa', '20 m² s pergolou'), ('Pivnica', 'cca 60 m²'), ('Voda', 'verejný vodovod'),
            ('Kanalizácia', 'žumpa'), ('Nasťahovanie', 'ihneď'),
        ],
        'desc': [
            'Na predaj exkluzívne ponúkame 5-izbový nízkoenergetický rodinný dom s dvojgarážou, fotovoltikou a krásnym výhľadom '
            'do prírody v Zemianskych Miticiach, časti obce Trenčianske Mitice. Tehlový dom prešiel kompletnou rekonštrukciou, '
            'je certifikovaný v energetickej triede A0 a je pripravený na okamžité bývanie bez ďalších investícií.',
            'Rekonštrukcia zahŕňala novú strešnú krytinu, novú elektroinštaláciu a rozvody vody, podlahové kúrenie s tepelným '
            'čerpadlom, nové sadrokartóny, omietky a poter, plastové okná s trojsklom, zateplenie minerálnou vlnou a novú fasádu. '
            'Dom je pripravený na vonkajšie žalúzie.',
            'Dispozícia: vstupná chodba s prístupom do garáže, kuchyňa s ostrovčekom otvorená do obývačky s výstupom na terasu '
            's pergolou, pracovňa, hlavná kúpeľňa s vaňou aj sprchou, dve detské izby, technická miestnosť, šatník a spálňa '
            's vlastnou sprchou. K domu patrí aj pivnica s výmerou približne 60 m².',
            'Dom je vhodný na pohodlné rodinné bývanie aj na podnikanie. V obci je materská škola a obchod, v susednom Trenčianskom '
            'Jastrabí (cca 2 km) základná škola, pošta, zdravotné stredisko a ďalšie služby. K dispozícii je znalecký posudok pre hypotéku.',
        ],
        'note': '',
        'inzerat': 'https://www.nehnutelnosti.sk/detail/JuYaNZ8aLO5/exkluzivne--5-izbovy-nizkoenergeticky-rodinny-dom-s-dvojgarazoul-fotovoltikou-a-krasnym-vyhladom--trencianske-mitice',
        'photos': [
            ('01.jpg', REAL, '/_blob/c1c1ae6c4ae2152cefc6c415529cf1c8'),
            ('02.jpg', REAL, '/_blob/ee15675e96ae26ff1558fc8cf28fc9cf'),
            ('03.jpg', REAL, '/_blob/b8b211bf11ba4b8f7e42e1f3cd266f78'),
            ('04.jpg', LOT, '/_blob/644d32e9b3b8be05d423a58a0ec2602a'),
            ('05.jpg', REAL, '/_blob/be3485f0a40eb135bdb46b7b8c5dbe37'),
        ],
    },
    'malacky': {
        'marker': 'POZEMOK MALACKY',
        'folder': 'pozemok-malacky',
        'aspect': '16 / 9',
        'tag': 'Znížená cena',
        'title': 'Stavebný pozemok 13 000 m² v priemyselnom parku',
        'place': 'Malacky, Továrenská ulica',
        'price': '920 000 € bez DPH',
        'per_m2': '70,77 € / m²',
        'facts': [
            ('Výmera', '13 000 m²'), ('Typ', 'priemyselná zóna, komerčný pozemok'), ('Rozmery', 'cca 125 × 105 m'),
            ('Tvar', 'približne štvorcový'), ('Terén', 'rovinatý'), ('Územný plán', 'schválený'),
            ('Voda', 'verejný vodovod pri pozemku'), ('Elektrina', '400 V pri pozemku'), ('Plyn', 'pri pozemku'),
            ('Prístup', 'priamo z cesty'), ('Súčasný stav', 'zarastený stromami a náletovými drevinami'),
            ('Zastúpenie', 'výhradné zastúpenie majiteľa'),
        ],
        'desc': [
            'Vo výhradnom zastúpení majiteľa ponúkame na predaj stavebný pozemok s výmerou 13 000 m² v priemyselnom parku '
            'na Továrenskej ulici v Malackách – v lokalite, kde pôsobia veľké výrobné a logistické firmy.',
            'Pozemok je rovinatý, približne štvorcového tvaru s rozmermi zhruba 125 × 105 m a má bezproblémový prístup priamo z cesty. '
            'Verejný vodovod, elektrina 400 V aj plyn sú pri pozemku, ostatné inžinierske siete v blízkosti. Pozemok je schválený '
            'v územnom pláne.',
            'Momentálne je zarastený stromami a náletovými drevinami; pri vážnom záujme ho majiteľ ponúka vyčistiť. '
            'Cena je uvedená bez DPH.',
        ],
        'note': '',
        'inzerat': 'https://www.nehnutelnosti.sk/detail/Ju1egIiVOxs/lumera--na-predaj-stavebny-pozemok-malacky-tovarenska-ulica',
        'photos': [
            ('01.jpg', LOT, '/_blob/307df7bd32ca46d9e9901c8c7e295074'),
            ('02.jpg', LOT, '/_blob/fc23fcf7e180c525d12a7be51042a595'),
            ('03.jpg', LOT, '/_blob/abac2e2d7ba44383fb69be5277b3a766'),
        ],
    },
    'svinna': {
        'marker': 'POZEMOK SVINNA',
        'folder': 'pozemok-svinna',
        'aspect': '16 / 9',
        'tag': 'Predaj',
        'title': 'Stavebný pozemok 10 833 m² pre viacero rodinných domov',
        'place': 'Svinná, okres Trenčín',
        'price': 'Cena dohodou',
        'per_m2': 'Cenu vám radi povieme osobne',
        'facts': [
            ('Výmera', '10 833 m² vrátane vlastnej prístupovej cesty'), ('Typ', 'stavebný pozemok pre rodinné domy'),
            ('Územný plán', 'schválený, pre viacero rodinných domov'), ('Dokumentácia', 'kompletná vrátane ÚPI'),
            ('Terén', 'rovinatý'), ('Voda', 'verejný vodovod pri pozemku'), ('Elektrina', '230 V pri pozemku'),
            ('Plyn', 'pri pozemku'), ('Prístup', 'vlastná prístupová cesta'),
            ('Súčasný stav', 'zarastený, pred predajom bude vyčistený'), ('Vzdialenosť', 'Trenčín 18 km, Bánovce n. B. 11 km'),
        ],
        'desc': [
            'Na predaj ponúkame rovinatý stavebný pozemok s výmerou 10 833 m² v obci Svinná, iba 18 km od Trenčína '
            'a 11 km od Bánoviec nad Bebravou. Pozemok je schválený v územnom pláne na výstavbu viacerých rodinných domov '
            'a k dispozícii je kompletná dokumentácia vrátane územnoplánovacej informácie.',
            'Súčasťou pozemku je vlastná prístupová cesta. Verejný vodovod, elektrina 230 V aj plyn sú pri pozemku. '
            'Pozemok je momentálne zarastený, pred predajom bude kompletne vyčistený.',
            'Obec má obchod, základnú a materskú školu, zdravotné stredisko aj poštu, autobusová zastávka je približne 180 m '
            'od pozemku. Ideálna príležitosť pre developera alebo na výstavbu vlastnej rodinnej lokality. Cena dohodou.',
        ],
        'note': 'Vizualizácia ukazuje jednu z možností zástavby pozemku rodinnými domami. Predmetom predaja je pozemok.',
        'inzerat': 'https://www.nehnutelnosti.sk/detail/JueTT223oaW/lumera--na-predaj-stavebny-pozemok-10-833-m--svinna',
        'photos': [
            ('02.jpg', VISB, '/_blob/59d63a137a912015af4e2e1771bda0c6'),
            ('01.jpg', LOT, '/_blob/4987e652d46d4a54a6794b1489f360be'),
        ],
    },
    'odbojarov': {
        'marker': 'BYT ODBOJAROV',
        'folder': 'byt-odbojarov',
        'tag': 'Prenájom',
        'title': 'Štýlový 2-izbový byt s loggiou a parkovaním',
        'place': 'Trenčín, Odbojárov',
        'price': '650 € / mesiac',
        'per_m2': 'Parkovacie miesto +50 € / mesiac',
        'facts': [
            ('Výmera', '45 m²'), ('Počet izieb', '2'), ('Poschodie', '1. z 2 (zvýšené)'), ('Konštrukcia', 'panelová'),
            ('Stav', 'novostavba'), ('Rok výstavby', '2010 – 2019'), ('Zariadenie', 'kompletne zariadený'),
            ('Loggia', 'áno'), ('Parkovanie', 'vyhradené miesto, 50 € / mesiac'), ('Dostupnosť', 'ihneď'),
        ],
        'desc': [
            'Na prenájom ponúkame svetlý 2-izbový byt s výmerou 45 m² na zvýšenom prízemí v tichej a vyhľadávanej lokalite '
            'na ulici Odbojárov v Trenčíne. Byt je kompletne zariadený a pripravený na okamžité nasťahovanie.',
            'Dispozícia: priestranná vstupná chodba, obývacia izba, samostatná spálňa, kuchynský kút, špajza, kúpeľňa s vaňou, '
            'samostatné WC a loggia.',
            'K bytu si môžete prenajať aj vyhradené parkovacie miesto priamo pri dome za 50 € mesačne. V okolí sú materské '
            'školy, jasle aj základná škola. Dohodnite si obhliadku.',
        ],
        'note': '',
        'agent': ('Maklérka', 'Katarína Ribovičová', '0904 255 252'),
        'inzerat': 'https://www.nehnutelnosti.sk/detail/JuFskpCe2Xm/na-prenajom-stylovy-2-izbovy-byt-s-loggiou-a-parkovacim-miestom--45-ml-k-dispozicii-ihned',
        'photos': [
            ('01.jpg', REAL, '/_blob/2abf3b0d4c4949a00184eca430164f48'),
            ('02.jpg', REAL, '/_blob/e3a9f5a0832d725e20854175b9741cac'),
            ('03.jpg', REAL, '/_blob/bf2da81d4693330a59377a18f1629ba7'),
            ('04.jpg', REAL, '/_blob/370a51d83a118f856a868353d49639cd'),
            ('05.jpg', REAL, '/_blob/74c41ef4b1eda6bf680bd645a30e0764'),
            ('06.jpg', REAL, '/_blob/fb58636348eac709d1a0f2ad2a191670'),
            ('07.jpg', REAL, '/_blob/63255ed35ae16e3465238072d0885d74'),
        ],
    },
    'teplice': {
        'marker': 'BYT TEPLICE',
        'folder': 'byt-teplice',
        'tag': 'Predaj',
        'title': 'Priestranný 3-izbový byt s dvoma balkónmi',
        'place': 'Trenčianske Teplice, Štvrť SNP',
        'price': 'Cena dohodou',
        'per_m2': 'Cenu vám rada povie maklérka',
        'facts': [
            ('Výmera', '94 m²'), ('Počet izieb', '3'), ('Poschodie', '3. z 6'), ('Výťah', 'áno'),
            ('Konštrukcia', 'panelová'), ('Stav', 'kompletná rekonštrukcia (cca pred 10 rokmi)'), ('Balkóny', '2'),
            ('Pivnica', 'murovaná + spoločná pre 3 byty'), ('Rok výstavby', '1990 – 2009'),
        ],
        'desc': [
            'Na predaj ponúkame priestranný 3-izbový byt s výmerou 94 m² a dvoma balkónmi v srdci kúpeľného mesta '
            'Trenčianske Teplice. Byt je na 3. poschodí zo 6 v dome s výťahom.',
            'Dispozícia: veľká vstupná chodba, obývacia izba, dve samostatné spálne, kuchyňa so špajzou, komora, kúpeľňa '
            'a samostatné WC. Byt prešiel približne pred 10 rokmi kompletnou rekonštrukciou, takže nevyžaduje väčšie investície. '
            'K bytu patrí murovaná pivnica a spoločná pivnica pre tri byty.',
            'Byt je vhodný na rodinné bývanie aj ako investícia – na prenájom turistom, kúpeľným hosťom či dlhodobým nájomníkom. '
            'Zastávky verejnej dopravy sú do 350 m. Dohodnite si obhliadku.',
        ],
        'note': '',
        'agent': ('Maklérka', 'Katarína Ribovičová', '0904 255 252'),
        'inzerat': 'https://www.nehnutelnosti.sk/detail/Juv70iO-ike/priestranny-3-izbovy-byt-s-dvoma-balkonmi-v-srdci-kupelneho-mesta-trencianske-teplice',
        'photos': [
            ('01.jpg', REAL, '/_blob/412de8fe5c4819bdba72b16d2432ea3a'),
            ('02.jpg', REAL, '/_blob/2a467b967fc9b3953f44478407ee99dc'),
            ('03.jpg', REAL, '/_blob/e93cc177ce24c390bfa6cb72542f1813'),
            ('04.jpg', REAL, '/_blob/35956a50e20637f1c25015cb2a588da5'),
            ('05.jpg', REAL, '/_blob/9f86e3b849e921159cd2bb5644568637'),
            ('06.jpg', REAL, '/_blob/e2aeb5645d8c646cb4545963cbb974eb'),
            ('07.jpg', REAL, '/_blob/751edf77627121d9d856248942c32d12'),
            ('08.jpg', REAL, '/_blob/a6907c4ecaf11af065418c202745cd5b'),
        ],
    },
    'vlckovce': {
        'marker': 'BYT VLCKOVCE',
        'folder': 'byt-vlckovce',
        'tag': 'Predaj',
        'title': 'Priestranný 3-izbový byt s balkónom a loggiou',
        'place': 'Vlčkovce, okres Trnava',
        'price': '199 900 €',
        'per_m2': '2 596 € / m²',
        'facts': [
            ('Výmera bytu', '77,64 m²'), ('Pivnica', '27,86 m²'), ('Spolu', '105,50 m²'), ('Počet izieb', '3'),
            ('Poschodie', '2. nadzemné podlažie'), ('Dom', 'malý bytový dom so 4 bytmi'), ('Konštrukcia', 'panelová'),
            ('Rekonštrukcia', 'byt 2016, bytový dom 2024'), ('Balkón a loggia', 'áno'), ('Bezpečnosť', 'kamerový systém'),
            ('Doprava', 'R1 a D1 cca 5 min, Trnava 10 km'),
        ],
        'desc': [
            'Na predaj ponúkame priestranný 3-izbový byt s výmerou 77,64 m² v obci Vlčkovce pri Trnave. Byt je na 2. nadzemnom '
            'podlaží v malom, pokojnom bytovom dome iba so štyrmi bytmi, ktorý má vlastný kamerový systém. K bytu patrí aj '
            'pivnica s výmerou 27,86 m², spolu teda 105,50 m².',
            'Dispozícia: chodba, tri samostatné izby, kuchyňa, kúpeľňa, samostatné WC, špajza, balkón a loggia. Byt prešiel '
            'kompletnou rekonštrukciou v roku 2016 a bytový dom v roku 2024. Má plastové okná, laminátové a keramické podlahy, '
            'modernú kuchynskú linku so vstavanou varnou doskou, elektrickou rúrou a digestorom, granitový drez a kúpeľňu '
            's vaňou aj sprchovým kútom.',
            'V obci je potraviny, základná škola s materskou školou, pošta, ihrisko aj ambulancie lekárov. Na rýchlostnú cestu R1 '
            'a diaľnicu D1 je to autom približne 5 minút, do Trnavy 10 km a do Bratislavy 50 km.',
        ],
        'note': '',
        'agent': ('Maklérka', 'Katarína Ribovičová', '0904 255 252'),
        'inzerat': 'https://www.nehnutelnosti.sk/detail/JugqcjiaalN/na-predaj-priestranny-3-izbovy-byt-vo-vlckovciach',
        'photos': [
            ('01.jpg', REAL, '/_blob/402f6ef8b728f79c8b11c32722d3b466'),
            ('02.jpg', REAL, '/_blob/d7bea819ae5dd8d6ca31fdce59f69a44'),
            ('03.jpg', REAL, '/_blob/db03f70c13a650009a9cb9bb220031dc'),
            ('04.jpg', REAL, '/_blob/f335149296a3f10e3a39a6219fe2792b'),
            ('05.jpg', REAL, '/_blob/04564dfe5eecf9fac0c4db4993a7f4c3'),
            ('06.jpg', REAL, '/_blob/09fd4aa0a9afa38338587709c685503b'),
            ('07.jpg', REAL, '/_blob/d3335b83f10649ecae4fc547eca33497'),
            ('08.jpg', REAL, '/_blob/e99fd8a922489159e968b2fe87a6dbd0'),
        ],
    },
    'nitra': {
        'marker': 'POZEMOK NITRA',
        'folder': 'pozemok-nitra',
        'aspect': '16 / 9',
        'tag': 'Predaj',
        'title': 'Priemyselný pozemok 15 843 m² pri hlavnom ťahu Nitra – Zlaté Moravce',
        'place': 'Nitrianske Hrnčiarovce, časť Malanta – okres Nitra',
        'price': '550 000 € bez DPH',
        'per_m2': '35 € / m² bez DPH',
        'facts': [
            ('Výmera', '15 843 m²'), ('Typ', 'komerčný / priemyselný pozemok'),
            ('Územný plán', 'schválený – výroba a podnikanie'), ('Prístup', 'priamo z cesty I/65 Nitra – Zlaté Moravce'),
            ('Viditeľnosť', 'výborná, z oboch smerov'), ('Dopravná štúdia', 'kapacitné posúdenie vjazdu schválené v roku 2021'),
            ('Voda', 'verejný vodovod pri pozemku'), ('Elektrina', 'pri pozemku'), ('Plyn', 'pri pozemku'),
            ('Tvar', 'nepravidelný'), ('Jaguar Land Rover', 'cca 9 km'),
        ],
        'desc': [
            'Na predaj ponúkame priemyselný pozemok s výmerou 15 843 m² v katastrálnom území Nitrianske Hrnčiarovce (časť Malanta), '
            'priamo pri hlavnom ťahu Nitra – Zlaté Moravce (cesta I/65). Pozemok je z hlavnej komunikácie výborne viditeľný z oboch '
            'smerov a nachádza sa iba 9 km od priemyselného parku Jaguar Land Rover.',
            'Podľa územného plánu je určený na výrobu a podnikanie. Kapacitné posúdenie dopravného napojenia vjazdu bolo vypracované '
            'a schválené v roku 2021. Verejný vodovod, elektrina aj plyn sú v dosahu pozemku.',
            'Pozemok je vhodný na výrobnú halu, logistické alebo skladové centrum, čerpaciu stanicu, autoservis či showroom, '
            'ubytovňu pre zamestnancov alebo iné komerčné využitie. V okolí je ubytovacie zariadenie, autoservis, potraviny '
            'aj zastávka prímestskej dopravy.',
        ],
        'note': 'Vizualizácia a situácia ukazujú jednu z možností zástavby (logistický areál). Predmetom predaja je pozemok.',
        'inzerat': 'https://www.nehnutelnosti.sk/detail/Ju5iHXyx7z7/priemyselny-pozemok-15-843-m--9-km-jaguar-land-rover--hlavny-tah-nitra--zlate-moravce',
        'photos': [
            ('01.jpg', VISB, '/_blob/6cb462ebc0f511c099b9e5d083dc6c36'),
            ('02.jpg', LOT, '/_blob/5474447d2eef700e3fd04fe6b1d9b9db'),
            ('03.jpg', REAL, '/_blob/8fe5c28cce7b049175bf996e874f9ec6'),
            ('04.jpg', SIT, '/_blob/4fd305a8c9077f68f102abeb8c679035'),
        ],
    },
    'turna': {
        'marker': 'DOM TURNA',
        'folder': 'dom-turna',
        'tag': 'Predaj',
        'title': 'Moderný 6-ročný rodinný dom s garážou',
        'place': 'Trenčianska Turná, okres Trenčín',
        'price': '459 900 €',
        'per_m2': 'Pomôžeme aj s hypotékou',
        'facts': [
            ('Úžitková plocha', 'cca 110 m² (s garážou cca 130 m²)'), ('Zastavaná plocha', '147 m²'), ('Pozemok', '574 m²'),
            ('Rok výstavby', '2020'), ('Konštrukcia', 'pórobetón (Ytong)'), ('Energetická trieda', 'A'),
            ('Kúrenie', 'tepelné čerpadlo, podlahové'), ('Okná', 'plastové s trojsklom'), ('Garáž', 'áno, vstup priamo z chodby'),
            ('Voda', 'verejný vodovod + vlastná studňa'), ('Záhrada', 'automatické zavlažovanie, záhradný domček'),
            ('Mesačné náklady', 'cca 150 €'),
        ],
        'desc': [
            'Na predaj ponúkame moderný nízkoenergetický rodinný dom z roku 2020 v Trenčianskej Turnej, s dobrou dostupnosťou '
            'do Trenčína. Dom stojí na rovinatom pozemku s výmerou 574 m² a ponúka súkromie aj pokojné bývanie.',
            'Dispozícia: vstupná chodba s priamym vstupom do garáže, obývacia izba spojená s kuchyňou na mieru, dve spálne, '
            'pracovňa, šatník, kúpeľňa s WC, samostatné WC, špajza a práčovňa. Bezbariérový prístup a vyššie stropy.',
            'Dom je postavený z pórobetónu (Ytong) v energetickej triede A. Kúrenie zabezpečuje tepelné čerpadlo s podlahovým '
            'kúrením v celom dome, okná sú plastové s trojsklom. K vybaveniu patria vonkajšie elektrické žalúzie, elektrická '
            'hliníková brána, predpríprava na alarm, vlastná studňa a automatické zavlažovanie záhrady so záhradným domčekom '
            'a posedením. Mesačné náklady sú približne 150 €. Dom nevyžaduje žiadne ďalšie investície.',
        ],
        'note': '',
        'inzerat': 'https://www.nehnutelnosti.sk/detail/JuwhwM9a1WD/lumera--na-predaj-moderny-6-rocny-rodinny-dom-s-garazoul-trencianska-turna',
        'photos': [
            ('01.jpg', REAL, '/_blob/ec152ee0e7f0095ed0948399e4e9ca36'),
            ('02.jpg', REAL, '/_blob/0e216c525d0b058e5d339facf893f97b'),
            ('03.jpg', REAL, '/_blob/2d7ec2ea3695b6ef856b030fd935af2e'),
            ('04.jpg', REAL, '/_blob/bd25709bbf508fb4b955701891067ba0'),
            ('05.jpg', REAL, '/_blob/b68fd63fc78871c76dd2695db4cc198c'),
            ('06.jpg', REAL, '/_blob/f4f87bfc2591a8fbd66dd8c749c3dc76'),
            ('07.jpg', REAL, '/_blob/09c68839abcc2b19dfca1d83020894b5'),
            ('08.jpg', REAL, '/_blob/ef1c12f76bdc9034c8feed58ad3036fb'),
            ('09.jpg', REAL, '/_blob/82d1a7bf722163bdce6c79e0fe7b3e88'),
            ('10.jpg', REAL, '/_blob/3aa20156a7359943ed9a69923a5cf56a'),
            ('11.jpg', REAL, '/_blob/ea3f96ec6ca2a4b618990504268907a1'),
            ('12.jpg', REAL, '/_blob/c66d2f801d73118b0f61057d1be3dd46'),
            ('13.jpg', REAL, '/_blob/c4c71703b9569e99bd2c63485dfcb40e'),
            ('14.jpg', REAL, '/_blob/cb4b13f287ae67625ab0c3c1260cf9c5'),
            ('15.jpg', REAL, '/_blob/106e628e01a36a5b85a22ca711892a07'),
            ('16.jpg', REAL, '/_blob/b26512c908c50d63844fcc42b4ed63d6'),
            ('17.jpg', REAL, '/_blob/67e3766ffee1dd8b0a4ae46876d3a513'),
            ('18.jpg', REAL, '/_blob/4f3fc8991ed2abc73e10e4eb26bb49dc'),
            ('19.jpg', REAL, '/_blob/9f2721f7fc675d1ce05a4fb2d79cc6cf'),
            ('20.jpg', REAL, '/_blob/95c6237a94e04d97510b18fe940e6ef9'),
        ],
    },
}


DEFAULT_AGENT = ('Maklér', 'Samuel Bucha', '0949 888 663')

# listings marked as sold (sync with nehnutelnosti.sk) – they stay as a reference page with a PREDANÉ badge
try:
    SOLD = set(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_state.json'))).get('sold', []))
except (OSError, ValueError):
    SOLD = set()


def is_sold(key):
    return key in SOLD


def _agent(L):
    role, name, phone = L.get('agent', DEFAULT_AGENT)
    return dict(agent_role=role, agent_name=name, agent_phone=phone, agent_tel='+421' + phone.replace(' ', '')[1:])


def blob_map():
    """canvas blob url -> path on lumera.sk"""
    return {b: 'img/%s/%s' % (L['folder'], f) for L in LISTINGS.values() for f, _k, b in L['photos']}


ARROW_L = '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#001939" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"></path></svg>'
ARROW_R = '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#001939" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"></path></svg>'
NAV_BTN = ('position: absolute; top: 50%; transform: translateY(-50%); width: 48px; height: 48px; border-radius: 50%; '
           'border: none; background: rgba(247,245,240,0.92); display: flex; align-items: center; justify-content: center; cursor: pointer')
THUMB = ('flex: none; width: 76px; height: 100px; padding: 0; border-radius: 4px; overflow: hidden; cursor: pointer; '
         'background: #DCD6C8; border: 2px solid %s')


def _state(key, L):
    """Fields that change when a listing is sold."""
    if is_sold(key):
        return dict(tag='PREDANÉ', tag_bg='#D9AE52', tag_fg='#001939', price='Predané',
                    per_m2='Podobnú nehnuteľnosť vám radi nájdeme.', cta='Chcem podobnú nehnuteľnosť', extra_links='')
    return dict(tag=L['tag'], tag_bg='#001939', tag_fg='#F7F5F0', price=L['price'], per_m2=L['per_m2'], cta='Dohodnúť obhliadku',
                extra_links='<a href="#hypoteka" style="text-align: center; font-weight: 700; font-size: 15px; padding: 6px">Vypočítať hypotéku →</a>\n'
                            '<a href="%s" style="text-align: center; font-size: 14px; color: #4A5566">Inzerát na nehnutelnosti.sk ↗</a>' % L['inzerat'])


def _section(key, L, g):
    """g: dict of fragments that differ between canvas and static."""
    facts = ''.join('<div style="display: flex; justify-content: space-between; gap: 16px; padding: 10px 0; border-bottom: 1px solid #EFEBE1">'
                    '<dt style="color: #4A5566">%s</dt><dd style="margin: 0; font-weight: 700; color: #001939; text-align: right">%s</dd></div>\n' % f
                    for f in L['facts'])
    desc = ''.join('<p style="margin: 0; font-size: 17px; line-height: 1.75; color: #2A3444">%s</p>\n' % p for p in L['desc'])
    return '''<!-- %(marker)s -->
<section id="detail-%(key)s" style="padding: 40px 0 96px">
<div style="max-width: 1240px; margin: 0 auto; padding: 0 24px; display: flex; flex-direction: column; gap: 28px">
<nav aria-label="Navigácia" style="font-size: 14px; color: #4A5566"><a href="#ponuka">Ponuka nehnuteľností</a> <span aria-hidden="true">›</span> %(title)s</nav>
<div style="display: flex; flex-direction: column; gap: 10px">
<span style="align-self: flex-start; background: %(tag_bg)s; color: %(tag_fg)s; font-size: 12px; font-weight: 800; letter-spacing: 0.1em; padding: 6px 10px; border-radius: 3px">%(tag)s</span>
<h1 style="margin: 0; font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: clamp(2rem, 4vw, 3.2rem); line-height: 1.1; color: #001939">%(title)s</h1>
<span style="font-size: 17px; color: #4A5566">%(place)s</span>
</div>
<div style="display: flex; flex-wrap: wrap; gap: 32px; align-items: flex-start">

<div style="flex: 1 1 600px; min-width: 0; display: flex; flex-direction: column; gap: 12px">
<figure style="margin: 0; position: relative; width: 100%%; aspect-ratio: %(aspect)s; max-height: 760px; background: #00112A; border-radius: 6px; overflow: hidden">
%(bg_img)s
%(main_img)s
%(badge)s
%(counter)s
<button type="button" %(prev)s aria-label="Predchádzajúca fotka" style="%(nav)s; left: 14px">%(al)s</button>
<button type="button" %(next)s aria-label="Ďalšia fotka" style="%(nav)s; right: 14px">%(ar)s</button>
</figure>
<div %(thumbs_attr)s style="display: flex; gap: 8px; overflow-x: auto; padding-bottom: 4px">
%(thumbs)s
</div>
</div>

<aside style="flex: 1 1 340px; min-width: 0; background: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 28px; display: flex; flex-direction: column; gap: 18px">
<div style="display: flex; flex-direction: column; gap: 4px">
<span style="font-family: 'Cormorant Garamond', serif; font-size: 40px; font-weight: 700; color: #001939; line-height: 1">%(price)s</span>
<span style="font-size: 14px; color: #4A5566">%(per_m2)s</span>
</div>
<dl style="margin: 0; font-size: 15px">
%(facts)s</dl>
<div style="display: flex; flex-direction: column; gap: 2px; padding-top: 4px">
<span style="font-size: 13px; color: #4A5566">%(agent_role)s</span>
<span style="font-size: 17px; font-weight: 800; color: #001939">%(agent_name)s</span>
</div>
<a href="#kontakt" style="text-align: center; background: #D9AE52; color: #001939; text-decoration: none; padding: 16px; border-radius: 4px; font-weight: 800; font-size: 16px">%(cta)s</a>
<a href="tel:%(agent_tel)s" style="text-align: center; background: #001939; color: #F7F5F0; text-decoration: none; padding: 15px; border-radius: 4px; font-weight: 800; font-size: 16px">Zavolať %(agent_phone)s</a>
%(extra_links)s
</aside>
</div>

<div style="max-width: 780px; display: flex; flex-direction: column; gap: 16px; margin-top: 12px">
<h2 style="margin: 0; font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: 34px; color: #001939">Popis nehnuteľnosti</h2>
%(desc)s%(note_p)s
</div>
</div>
</section>

''' % dict(marker=L['marker'], key=key, title=L['title'], place=L['place'], **_state(key, L),
           aspect=L.get('aspect', '1 / 1'), **_agent(L), facts=facts, desc=desc, note_p=('<p style="margin: 0; font-size: 14px; color: #6B5220; font-weight: 600">%s</p>' % L['note']) if L['note'] else '', nav=NAV_BTN, al=ARROW_L, ar=ARROW_R, **g)


def dc(key):
    L = LISTINGS[key]
    v = 'gal_' + key
    g = dict(
        bg_img='<img src="{{%s.src}}" alt="" aria-hidden="true" style="position: absolute; inset: -40px; width: calc(100%% + 80px); height: calc(100%% + 80px); object-fit: cover; filter: blur(28px) brightness(0.75); transform: scale(1.05)">' % v,
        main_img='<img src="{{%s.src}}" alt="{{%s.alt}}" style="position: absolute; inset: 0; width: 100%%; height: 100%%; object-fit: contain">' % (v, v),
        badge='<span style="position: absolute; top: 14px; left: 14px; font-size: 13px; font-weight: 800; padding: 7px 12px; border-radius: 3px; {{%s.badgeStyle}}">{{%s.badge}}</span>' % (v, v),
        counter='<span style="position: absolute; bottom: 14px; right: 14px; background: rgba(0,17,42,0.8); color: #F7F5F0; font-size: 13px; font-weight: 700; padding: 6px 10px; border-radius: 3px">{{%s.count}}</span>' % v,
        prev='onClick="{{%s.prev}}"' % v, next='onClick="{{%s.next}}"' % v,
        thumbs_attr='',
        thumbs='<sc-for list="{{%s.thumbs}}" as="t" hint-placeholder-count="6"><button type="button" onClick="{{t.pick}}" aria-label="{{t.label}}" style="{{t.style}}"><img src="{{t.src}}" alt="" style="width: 100%%; height: 100%%; object-fit: cover; display: block"></button></sc-for>' % v,
    )
    return _section(key, L, g)


def dc_logic():
    data = {k: [{'src': b, 'kind': kind} for _f, kind, b in L['photos']] for k, L in LISTINGS.items()}
    return '''  gal(key) {
    const G = %s;
    const B = %s, S = %s;
    const list = G[key], n = list.length, i = ((this.state['g_' + key] || 0) %% n + n) %% n;
    const go = (j) => () => this.setState({ ['g_' + key]: (j + n) %% n });
    return {
      src: list[i].src, badge: B[list[i].kind], badgeStyle: S[list[i].kind], alt: B[list[i].kind] + ' – fotka ' + (i + 1),
      count: (i + 1) + ' / ' + n, prev: go(i - 1), next: go(i + 1),
      thumbs: list.map((p, j) => ({ src: p.src, label: 'Fotka ' + (j + 1), pick: go(j),
        style: '%s'.replace('%%s', j === i ? '#D9AE52' : 'transparent') }))
    };
  }
''' % (json.dumps(data, ensure_ascii=False), json.dumps(BADGE, ensure_ascii=False), json.dumps(BADGE_STYLE), THUMB)


def static(key):
    L = LISTINGS[key]
    files = ['img/%s/%s' % (L['folder'], f) for f, _k, _b in L['photos']]
    kinds = [k for _f, k, _b in L['photos']]
    thumbs = ''.join('<button type="button" class="g-th" data-i="%d" aria-label="Fotka %d" style="%s"><img src="%s" alt="" loading="lazy" style="width: 100%%; height: 100%%; object-fit: cover; display: block"></button>\n'
                     % (j, j + 1, THUMB % ('#D9AE52' if j == 0 else 'transparent'), f) for j, f in enumerate(files))
    g = dict(
        bg_img='<img id="g-bg" src="%s" alt="" aria-hidden="true" style="position: absolute; inset: -40px; width: calc(100%% + 80px); height: calc(100%% + 80px); object-fit: cover; filter: blur(28px) brightness(0.75); transform: scale(1.05)">' % files[0],
        main_img='<img id="g-img" src="%s" alt="%s – fotka 1" style="position: absolute; inset: 0; width: 100%%; height: 100%%; object-fit: contain">' % (files[0], BADGE[kinds[0]]),
        badge='<span id="g-badge" style="position: absolute; top: 14px; left: 14px; font-size: 13px; font-weight: 800; padding: 7px 12px; border-radius: 3px; %s">%s</span>' % (BADGE_STYLE[kinds[0]], BADGE[kinds[0]]),
        counter='<span id="g-count" style="position: absolute; bottom: 14px; right: 14px; background: rgba(0,17,42,0.8); color: #F7F5F0; font-size: 13px; font-weight: 700; padding: 6px 10px; border-radius: 3px">1 / %d</span>' % len(files),
        prev='id="g-prev"', next='id="g-next"', thumbs_attr='id="g-thumbs"', thumbs=thumbs,
    )
    script = '''<script>
(function(){
  var F=%s, K=%s, B=%s, S=%s, i=0, $=function(id){return document.getElementById(id)};
  if(!$('g-img'))return;
  var th=document.querySelectorAll('.g-th');
  function show(j){
    i=(j+F.length)%%F.length; var k=K[i];
    $('g-img').src=F[i]; $('g-bg').src=F[i]; $('g-img').alt=B[k]+' – fotka '+(i+1);
    $('g-badge').textContent=B[k]; $('g-badge').setAttribute('style','position: absolute; top: 14px; left: 14px; font-size: 13px; font-weight: 800; padding: 7px 12px; border-radius: 3px; '+S[k]);
    $('g-count').textContent=(i+1)+' / '+F.length;
    th.forEach(function(t,n){t.style.borderColor=n===i?'#D9AE52':'transparent'});
    th[i].scrollIntoView({block:'nearest',inline:'nearest'});
  }
  $('g-prev').addEventListener('click',function(){show(i-1)});
  $('g-next').addEventListener('click',function(){show(i+1)});
  th.forEach(function(t){t.addEventListener('click',function(){show(Number(t.dataset.i))})});
  document.addEventListener('keydown',function(e){if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
  var x0=null,fig=$('g-img').parentNode;
  fig.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
  fig.addEventListener('touchend',function(e){if(x0===null)return;var d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>40)show(i+(d<0?1:-1));x0=null});
  F.slice(1,3).forEach(function(s){var im=new Image();im.src=s});
})();
</script>
''' % (json.dumps(files), json.dumps(kinds), json.dumps(BADGE, ensure_ascii=False), json.dumps(BADGE_STYLE))
    return _section(key, L, g), script
