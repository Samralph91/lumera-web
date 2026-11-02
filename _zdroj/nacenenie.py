"""Property valuation request (3-step form), rendered for the canvas (dc) and for lumera.sk (static)."""

TYPES = ['Byt', 'Rodinný dom', 'Pozemok', 'Garsónka']
ROOMS = ['1', '2', '3', '4+']
CONDS = ['Pôvodný stav', 'Po rekonštrukcii', 'Novostavba']

PILL_OFF = ('min-height: 44px; padding: 0 20px; border-radius: 4px; border: 1px solid #CFC8B8; background: #FFFFFF; '
            'color: #001939; font-size: 15px; font-weight: 700; font-family: inherit; cursor: pointer')
INPUT = ('height: 48px; padding: 0 14px; border-radius: 4px; border: 1px solid #CFC8B8; background: #FFFFFF; '
         'font-size: 16px; font-family: inherit; color: #1B2533; width: 100%; box-sizing: border-box')
LABEL = 'font-size: 15px; font-weight: 800; color: #001939'
BTN_MAIN = ('min-height: 52px; padding: 0 28px; border: none; border-radius: 4px; background: #001939; color: #F7F5F0; '
            'font-size: 16px; font-weight: 800; font-family: inherit; cursor: pointer')
BTN_BACK = ('min-height: 52px; padding: 0 22px; border: 1px solid #CFC8B8; border-radius: 4px; background: #FFFFFF; '
            'color: #001939; font-size: 16px; font-weight: 700; font-family: inherit; cursor: pointer')
ERR = 'margin: 0; font-size: 14px; font-weight: 700; color: #A3361F'

INTRO = '''<!-- NACENENIE -->
<section id="nacenenie" style="background: #EFEBE1; padding: 96px 0">
<div style="max-width: 1240px; margin: 0 auto; padding: 0 24px; display: flex; flex-wrap: wrap; gap: 48px; align-items: flex-start">
<div style="flex: 1 1 360px; min-width: 0; display: flex; flex-direction: column; gap: 20px">
<span style="font-size: 13px; font-weight: 800; letter-spacing: 0.28em; color: #8A6A2B">NACENENIE ZDARMA</span>
<h2 style="margin: 0; font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: clamp(2rem, 3.6vw, 3rem); line-height: 1.1; color: #001939">Koľko stojí vaša nehnuteľnosť?</h2>
<p style="margin: 0; font-size: 17px; line-height: 1.65; color: #4A5566">Vyplňte tri krátke kroky a do 24 hodín vám pošleme odhad trhovej ceny podľa aktuálnych predajov vo vašom okolí. Nezáväzne a zadarmo.</p>
<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 12px; font-size: 16px; color: #1B2533">
<li style="display: flex; gap: 12px; align-items: flex-start"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#8A6A2B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex: none; margin-top: 2px"><path d="M20 6 9 17l-5-5"></path></svg>Odhad podľa reálnych cien v Trenčíne a okolí</li>
<li style="display: flex; gap: 12px; align-items: flex-start"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#8A6A2B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex: none; margin-top: 2px"><path d="M20 6 9 17l-5-5"></path></svg>Bez záväzku – rozhodnutie je len na vás</li>
<li style="display: flex; gap: 12px; align-items: flex-start"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#8A6A2B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex: none; margin-top: 2px"><path d="M20 6 9 17l-5-5"></path></svg>Ak chcete predať rýchlo, ponúkneme aj výkup</li>
</ul>
</div>
'''

OUTRO = '''</div>
</section>

'''


def card_open(form_attrs):
    return ('<form %s style="flex: 1 1 560px; min-width: 0; background: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; '
            'padding: 32px; display: flex; flex-direction: column; gap: 24px">\n' % form_attrs)


def progress(step_text, bar_style_attr):
    return ('<div style="display: flex; flex-direction: column; gap: 10px">\n'
            '<span style="font-size: 13px; font-weight: 800; letter-spacing: 0.16em; color: #8A6A2B">%s</span>\n'
            '<div style="height: 6px; background: #EFEBE1; border-radius: 3px; overflow: hidden"><div %s></div></div>\n'
            '</div>\n' % (step_text, bar_style_attr))


def field_group(label, inner, extra_attr=''):
    return ('<div %s style="display: flex; flex-direction: column; gap: 10px">\n<span style="%s">%s</span>\n'
            '<div style="display: flex; flex-wrap: wrap; gap: 10px">\n%s</div>\n</div>\n' % (extra_attr, LABEL, label, inner))


def text_field(fid, label, typ, attrs, placeholder=''):
    ph = ' placeholder="%s"' % placeholder if placeholder else ''
    return ('<div style="display: flex; flex-direction: column; gap: 8px">\n<label for="%s" style="%s">%s</label>\n'
            '<input id="%s" type="%s"%s %s style="%s">\n</div>\n' % (fid, LABEL, label, fid, typ, ph, attrs, INPUT))


# ---------------------------------------------------------------- canvas (.dc.html)
def dc():
    def pills(lst):
        return ('<sc-for list="{{val.%s}}" as="p" hint-placeholder-count="4">'
                '<button type="button" onClick="{{p.pick}}" style="{{p.style}}">{{p.label}}</button></sc-for>\n' % lst)
    s = INTRO + card_open('aria-label="Formulár na nacenenie nehnuteľnosti"')
    s += progress('KROK {{val.step}} Z 3 · {{val.stepName}}', 'style="{{val.bar}}"')
    # step 1
    s += '<sc-if value="{{val.s1}}" hint-placeholder-val="{{ true }}">\n<div style="display: flex; flex-direction: column; gap: 24px">\n'
    s += field_group('Typ nehnuteľnosti', pills('types'))
    s += '<sc-if value="{{val.showRooms}}" hint-placeholder-val="{{ true }}">' + field_group('Počet izieb', pills('rooms')) + '</sc-if>\n'
    s += '<div style="max-width: 260px">' + text_field('n-vymera', 'Výmera (m²)', 'number', 'min="1" value="{{val.area}}" onChange="{{val.onArea}}"', 'napr. 68') + '</div>\n'
    s += field_group('Stav', pills('conds'))
    s += '</div>\n</sc-if>\n'
    # step 2
    s += '<sc-if value="{{val.s2}}" hint-placeholder-val="{{ false }}">\n<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px">\n'
    s += text_field('n-obec', 'Obec / mesto', 'text', 'value="{{val.town}}" onChange="{{val.onTown}}"', 'napr. Trenčín')
    s += text_field('n-ulica', 'Ulica alebo časť obce', 'text', 'value="{{val.street}}" onChange="{{val.onStreet}}"', 'napr. Sihoť')
    s += '</div>\n</sc-if>\n'
    # step 3
    s += '<sc-if value="{{val.s3}}" hint-placeholder-val="{{ false }}">\n<div style="display: flex; flex-direction: column; gap: 20px">\n'
    s += text_field('n-meno', 'Meno a priezvisko', 'text', 'value="{{val.name}}" onChange="{{val.onName}}"')
    s += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px">\n'
    s += text_field('n-tel', 'Telefón', 'tel', 'value="{{val.phone}}" onChange="{{val.onPhone}}"')
    s += text_field('n-mail', 'E-mail', 'email', 'value="{{val.mail}}" onChange="{{val.onMail}}"')
    s += '</div>\n<p style="margin: 0; font-size: 13px; color: #5C6472">Údaje použijeme len na pripravenie odhadu. Viac v časti <a href="ochrana-osobnych-udajov.html">Ochrana osobných údajov</a>.</p>\n</div>\n</sc-if>\n'
    # done
    s += ('<sc-if value="{{val.done}}" hint-placeholder-val="{{ false }}">\n<div style="display: flex; flex-direction: column; gap: 10px; padding: 12px 0">\n'
          '<span style="font-family: \'Cormorant Garamond\', serif; font-size: 32px; font-weight: 700; color: #001939">Ďakujeme, žiadosť sme prijali.</span>\n'
          '<span style="font-size: 16px; color: #4A5566">Odhad ceny vám pošleme do 24 hodín. Ak sa ponáhľate, zavolajte na <a href="tel:+421949888663">0949 888 663</a>.</span>\n</div>\n</sc-if>\n')
    s += '<sc-if value="{{val.err}}" hint-placeholder-val="{{ false }}"><p role="alert" style="%s">{{val.errText}}</p></sc-if>\n' % ERR
    s += ('<sc-if value="{{val.showNav}}" hint-placeholder-val="{{ true }}">\n<div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center">\n'
          '<sc-if value="{{val.showBack}}" hint-placeholder-val="{{ false }}"><button type="button" onClick="{{val.back}}" style="%s">← Späť</button></sc-if>\n'
          '<button type="button" onClick="{{val.next}}" style="%s; margin-left: auto">{{val.nextLabel}}</button>\n</div>\n</sc-if>\n' % (BTN_BACK, BTN_MAIN))
    s += '</form>\n' + OUTRO
    return s


DC_STATE = "nstep: 1, ntype: '', nrooms: '', ncond: '', narea: '', ntown: '', nstreet: '', nname: '', nphone: '', nmail: '', nerr: ''"

DC_METHOD = '''  val() {
    const st = this.state;
    const pill = (on) => this.pill(on);
    const mk = (labels, key) => labels.map((l) => ({ label: l, style: pill(st[key] === l), pick: () => this.setState({ [key]: l, nerr: '' }) }));
    const set = (key) => (e) => this.setState({ [key]: e.target.value, nerr: '' });
    const names = ['', 'NEHNUTEĽNOSŤ', 'LOKALITA', 'KONTAKT', 'HOTOVO'];
    const step = st.nstep;
    const next = () => {
      if (step === 1 && (!st.ntype || !(Number(st.narea) > 0))) return this.setState({ nerr: 'Vyberte typ nehnuteľnosti a zadajte výmeru.' });
      if (step === 2 && !st.ntown.trim()) return this.setState({ nerr: 'Zadajte obec alebo mesto.' });
      if (step === 3 && (!st.nname.trim() || (!st.nphone.trim() && !st.nmail.trim()))) return this.setState({ nerr: 'Zadajte meno a telefón alebo e-mail.' });
      this.setState({ nstep: step + 1, nerr: '' });
    };
    return {
      step: Math.min(step, 3), stepName: names[step],
      bar: 'height: 100%; background: #D9AE52; border-radius: 3px; width: ' + Math.round(Math.min(step, 3) / 3 * 100) + '%',
      s1: step === 1, s2: step === 2, s3: step === 3, done: step === 4,
      types: mk(['Byt', 'Rodinný dom', 'Pozemok', 'Garsónka'], 'ntype'),
      rooms: mk(['1', '2', '3', '4+'], 'nrooms'),
      conds: mk(['Pôvodný stav', 'Po rekonštrukcii', 'Novostavba'], 'ncond'),
      showRooms: st.ntype !== 'Pozemok' && st.ntype !== 'Garsónka',
      area: st.narea, onArea: set('narea'), town: st.ntown, onTown: set('ntown'), street: st.nstreet, onStreet: set('nstreet'),
      name: st.nname, onName: set('nname'), phone: st.nphone, onPhone: set('nphone'), mail: st.nmail, onMail: set('nmail'),
      err: !!st.nerr, errText: st.nerr,
      showNav: step < 4, showBack: step > 1 && step < 4,
      back: () => this.setState({ nstep: step - 1, nerr: '' }), next: next,
      nextLabel: step === 3 ? 'Odoslať žiadosť' : 'Pokračovať →'
    };
  }
'''


# ---------------------------------------------------------------- live site (static)
def static():
    def pills(group, labels):
        return ''.join('<button type="button" class="pill" data-group="%s" data-value="%s" aria-pressed="false">%s</button>\n'
                       % (group, l, l) for l in labels)
    s = INTRO + card_open('id="nac-form" action="https://formsubmit.co/info@lumera.sk" method="POST" novalidate '
                          'aria-label="Formulár na nacenenie nehnuteľnosti"')
    s += ('<input type="hidden" name="_subject" value="Žiadosť o nacenenie nehnuteľnosti – lumera.sk">'
          '<input type="hidden" name="_template" value="table">'
          '<input type="hidden" name="_next" value="https://lumera.sk/nacenenie.html?nacenenie=odoslane">'
          '<input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">'
          '<input type="hidden" name="Typ nehnuteľnosti" id="nf-typ"><input type="hidden" name="Počet izieb" id="nf-izby">'
          '<input type="hidden" name="Stav" id="nf-stav">\n')
    s += progress('<span id="n-steptext">KROK 1 Z 3 · NEHNUTEĽNOSŤ</span>',
                  'id="n-bar" style="height: 100%; background: #D9AE52; border-radius: 3px; width: 33%"')
    s += '<div class="n-step" data-step="1" style="display: flex; flex-direction: column; gap: 24px">\n'
    s += field_group('Typ nehnuteľnosti', pills('nf-typ', TYPES), 'role="group" aria-label="Typ nehnuteľnosti"')
    s += field_group('Počet izieb', pills('nf-izby', ROOMS), 'id="n-rooms" role="group" aria-label="Počet izieb"')
    s += '<div style="max-width: 260px">' + text_field('n-vymera', 'Výmera (m²)', 'number', 'name="Výmera m2" min="1"', 'napr. 68') + '</div>\n'
    s += field_group('Stav', pills('nf-stav', CONDS), 'role="group" aria-label="Stav"')
    s += '</div>\n'
    s += '<div class="n-step" data-step="2" hidden style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px">\n'
    s += text_field('n-obec', 'Obec / mesto', 'text', 'name="Obec"', 'napr. Trenčín')
    s += text_field('n-ulica', 'Ulica alebo časť obce', 'text', 'name="Ulica"', 'napr. Sihoť')
    s += '</div>\n'
    s += '<div class="n-step" data-step="3" hidden style="display: flex; flex-direction: column; gap: 20px">\n'
    s += text_field('n-meno', 'Meno a priezvisko', 'text', 'name="Meno"')
    s += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px">\n'
    s += text_field('n-tel', 'Telefón', 'tel', 'name="Telefón"')
    s += text_field('n-mail', 'E-mail', 'email', 'name="E-mail"')
    s += '</div>\n<p style="margin: 0; font-size: 13px; color: #5C6472">Údaje použijeme len na pripravenie odhadu. Viac v časti <a href="ochrana-osobnych-udajov.html">Ochrana osobných údajov</a>.</p>\n</div>\n'
    s += ('<div id="n-done" hidden style="display: flex; flex-direction: column; gap: 10px; padding: 12px 0">\n'
          '<span style="font-family: \'Cormorant Garamond\', serif; font-size: 32px; font-weight: 700; color: #001939">Ďakujeme, žiadosť sme prijali.</span>\n'
          '<span style="font-size: 16px; color: #4A5566">Odhad ceny vám pošleme do 24 hodín. Ak sa ponáhľate, zavolajte na <a href="tel:+421949888663">0949 888 663</a>.</span>\n</div>\n')
    s += '<p id="n-err" role="alert" hidden style="%s"></p>\n' % ERR
    s += ('<div id="n-nav" style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center">\n'
          '<button type="button" id="n-back" hidden style="%s">← Späť</button>\n'
          '<button type="button" id="n-next" style="%s; margin-left: auto">Pokračovať →</button>\n</div>\n' % (BTN_BACK, BTN_MAIN))
    s += '</form>\n' + OUTRO
    return s


STATIC_SCRIPT = '''<script>
(function(){
  var f=document.getElementById('nac-form'); if(!f)return;
  var $=function(id){return document.getElementById(id)}, step=1,
      names=['','NEHNUTEĽNOSŤ','LOKALITA','KONTAKT'];
  f.querySelectorAll('.pill').forEach(function(b){b.addEventListener('click',function(){
    $(b.dataset.group).value=b.dataset.value; err('');
    if(b.dataset.group==='nf-typ'){var hide=b.dataset.value==='Pozemok'||b.dataset.value==='Garsónka';$('n-rooms').hidden=hide;if(hide)$('nf-izby').value='';}
  })});
  function err(t){$('n-err').textContent=t;$('n-err').hidden=!t}
  function show(){
    f.querySelectorAll('.n-step').forEach(function(d){d.hidden=Number(d.dataset.step)!==step});
    $('n-steptext').textContent='KROK '+step+' Z 3 · '+names[step];
    $('n-bar').style.width=Math.round(step/3*100)+'%';
    $('n-back').hidden=step===1;
    $('n-next').textContent=step===3?'Odoslať žiadosť':'Pokračovať →';
  }
  $('n-back').addEventListener('click',function(){step--;err('');show()});
  $('n-next').addEventListener('click',function(){
    if(step===1&&(!$('nf-typ').value||!(Number($('n-vymera').value)>0)))return err('Vyberte typ nehnuteľnosti a zadajte výmeru.');
    if(step===2&&!$('n-obec').value.trim())return err('Zadajte obec alebo mesto.');
    if(step===3){
      if(!$('n-meno').value.trim()||(!$('n-tel').value.trim()&&!$('n-mail').value.trim()))return err('Zadajte meno a telefón alebo e-mail.');
      if($('n-mail').value.trim()&&!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test($('n-mail').value.trim()))return err('Skontrolujte e-mailovú adresu.');
      $('n-next').disabled=true;$('n-next').textContent='Odosielam…';return f.submit();
    }
    step++;err('');show();
  });
  if(/[?&]nacenenie=odoslane/.test(location.search)){
    f.querySelectorAll('.n-step').forEach(function(d){d.hidden=true});
    $('n-nav').hidden=true;$('n-done').hidden=false;$('n-steptext').textContent='HOTOVO';$('n-bar').style.width='100%';
  }
})();
</script>
'''
