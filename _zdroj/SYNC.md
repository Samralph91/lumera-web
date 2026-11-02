# Synchronizácia lumera.sk s nehnutelnosti.sk

Zdroj webu je v tomto priečinku (`_zdroj/`, GitHub Pages ho nezverejňuje – priečinky s `_` Jekyll vynecháva).

## Postup kontroly
1. Stiahni zoznam inzerátov RK (Composio workbench – tento kontajner na nehnutelnosti.sk nedosiahne):
   `agency_url` zo `sync_state.json` → všetky odkazy `/detail/<ID>/<slug>` (ak je stránkovanie, prejdi všetky strany).
2. Pre každý inzerát načítaj detail a cenu: prvý `"priceSpecification": {... "price": N}` v JSON-LD. `0` = cena skrytá („Cena dohodou“ / „Info v RK“).
3. Porovnaj so `snapshot` v `sync_state.json`:
   - **zmena ceny** inzerátu, ktorý je na webe (`python3 sync.py map` ukáže kľúč a súčasnú cenu) → `python3 sync.py set-price <kľúč> <cena>`; robí sa automaticky.
   - **inzerát zmizol** a je na webe → `python3 sync.py sold <kľúč>` (zostane ako referencia so štítkom PREDANÉ); automaticky.
   - **nový inzerát** (ID nie je v snapshot ani v `not_on_site`) → priprav novú stránku (pozri nižšie), ukáž náhľad Samuelovi a nahraj až po jeho „nahraj to“.
   - ID v `not_on_site` sú známe, zatiaľ nepridané – neopakuj upozornenie každý deň (najviac raz týždenne pripomeň).
4. `python3 sync.py build` → `python3 sync.py publish ..` (z `_zdroj/`), skontroluj `git diff --stat`, commit + push na `main`.
5. Aktualizuj `snapshot` + `snapshot_date` v `sync_state.json`, commitni.

## Nový inzerát – kde všetko doplniť
- `listing.py` → nový záznam v `LISTINGS` (marker, folder, aspect, tag, title, place, price, per_m2, facts, desc, note, agent, inzerat, photos). Fotky do `lumera/img/<folder>/NN.jpg`; tretí prvok v `photos` je pôvodný blob z canvasu – pre nové fotky použi `''` a over, že `blob_map` a export prejde.
- `vyhladavac.py` → `FACTS['<Nazov>.dc.html']`.
- `source.dc.html` → sekcia `<!-- MARKER -->` a položka v `allListings` (a v `const L = [...]`).
- `pages.py` → `PAGES` (+ `TITLES`), `seo_content.py` → prípadne zaradiť do stránky lokality.
- Preklad: nové texty doplň do `tr_en3.py` (inak ostanú v anglickej verzii po slovensky – `en_build` ich vypíše ako UNTRANSLATED).
- Poradie fotiek: Samuel chce najprv reálne fotky, vizualizácie označené; pri pozemkoch najprv fotky s vyznačenou hranicou.
- Maklérka Katarína Ribovičová (0904 255 252) – `agent: ('Maklérka', 'Katarína Ribovičová', '0904 255 252')`.
