"""Mortgage calculator section, rendered two ways from one template:
   dc()     -> markup for the canvas design (holes + handlers)
   static() -> markup + script for the live site lumera.sk
"""

DEFAULTS = {'price': 150000, 'own': 20, 'rate': 3.5, 'years': 30, 'fees': 0}

TPL = '''<!-- HYPOTÉKA -->
<section id="hypoteka" style="background: #FFFFFF; border-top: 1px solid #E4DFD3; padding: 96px 0">
<div style="max-width: 1240px; margin: 0 auto; padding: 0 24px; display: flex; flex-direction: column; gap: 40px">
<div style="display: flex; flex-direction: column; gap: 14px; max-width: 720px">
<span style="font-size: 13px; font-weight: 800; letter-spacing: 0.28em; color: #8A6A2B">HYPOKALKULAČKA</span>
<h2 style="margin: 0; font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: clamp(2rem, 3.6vw, 3rem); line-height: 1.1; color: #001939">Koľko budete splácať?</h2>
<p style="margin: 0; font-size: 17px; line-height: 1.6; color: #4A5566">Vypočítajte si orientačnú mesačnú splátku. Najvýhodnejšiu ponuku z bánk vám potom nájdeme my.</p>
</div>
<div style="display: flex; flex-wrap: wrap; gap: 32px; align-items: stretch">

<form style="flex: 1 1 520px; min-width: 0; display: flex; flex-direction: column; gap: 28px" onsubmit="return false">
<div style="display: flex; flex-direction: column; gap: 10px">
<div style="display: flex; flex-wrap: wrap; gap: 8px 16px; justify-content: space-between; align-items: center">
<label for="h-price" style="font-size: 15px; font-weight: 800; color: #001939">Cena nehnuteľnosti</label>
<span style="display: flex; align-items: center; gap: 8px"><input %%NUM_price%% type="number" min="0" max="2000000" step="1000" aria-label="Cena nehnuteľnosti v eurách" style="width: 140px; height: 44px; padding: 0 12px; border-radius: 4px; border: 1px solid #CFC8B8; font-size: 16px; font-weight: 700; font-family: inherit; color: #001939; text-align: right"><span style="font-weight: 700; color: #001939">€</span></span>
</div>
<input id="h-price" %%RANGE_price%% type="range" min="10000" max="1000000" step="1000" class="hrange">
<div style="display: flex; justify-content: space-between; font-size: 13px; color: #5C6472"><span>10 000 €</span><span>1 000 000 €</span></div>
</div>

<div style="display: flex; flex-direction: column; gap: 10px">
<div style="display: flex; flex-wrap: wrap; gap: 8px 16px; justify-content: space-between; align-items: baseline">
<label for="h-own" style="font-size: 15px; font-weight: 800; color: #001939">Vlastné zdroje</label>
<span style="font-size: 16px; font-weight: 700; color: #001939">%%OWN_LABEL%%</span>
</div>
<input id="h-own" %%RANGE_own%% type="range" min="0" max="100" step="1" class="hrange">
%%OWN_NOTE%%
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 28px">
<div style="display: flex; flex-direction: column; gap: 10px">
<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px">
<label for="h-rate" style="font-size: 15px; font-weight: 800; color: #001939">Úroková sadzba</label>
<span style="font-size: 16px; font-weight: 700; color: #001939">%%RATE_LABEL%%</span>
</div>
<input id="h-rate" %%RANGE_rate%% type="range" min="0.1" max="7" step="0.05" class="hrange">
</div>
<div style="display: flex; flex-direction: column; gap: 10px">
<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px">
<label for="h-years" style="font-size: 15px; font-weight: 800; color: #001939">Splatnosť</label>
<span style="font-size: 16px; font-weight: 700; color: #001939">%%YEARS_LABEL%%</span>
</div>
<input id="h-years" %%RANGE_years%% type="range" min="1" max="30" step="1" class="hrange">
</div>
<div style="display: flex; flex-direction: column; gap: 10px">
<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px">
<label for="h-fees" style="font-size: 15px; font-weight: 800; color: #001939">Jednorazové poplatky</label>
<span style="font-size: 16px; font-weight: 700; color: #001939">%%FEES_LABEL%%</span>
</div>
<input id="h-fees" %%RANGE_fees%% type="range" min="0" max="10000" step="50" class="hrange">
</div>
</div>
</form>

<div style="flex: 1 1 360px; min-width: 0; background: #001939; color: #F7F5F0; border-radius: 6px; padding: 36px; display: flex; flex-direction: column; gap: 22px">
<div style="display: flex; flex-direction: column; gap: 6px">
<span style="font-size: 13px; font-weight: 800; letter-spacing: 0.2em; color: #D9AE52">MESAČNÁ SPLÁTKA</span>
<span aria-live="polite" style="font-family: 'Cormorant Garamond', serif; font-size: clamp(2.6rem, 5vw, 3.6rem); font-weight: 700; line-height: 1">%%MONTHLY%%</span>
</div>
<dl style="margin: 0; display: flex; flex-direction: column; gap: 12px; font-size: 15px; border-top: 1px solid #1C3D6B; padding-top: 20px">
<div style="display: flex; justify-content: space-between; gap: 16px"><dt style="color: #C7CFDB">Výška úveru</dt><dd style="margin: 0; font-weight: 700">%%LOAN%%</dd></div>
<div style="display: flex; justify-content: space-between; gap: 16px"><dt style="color: #C7CFDB">Zaplatené úroky</dt><dd style="margin: 0; font-weight: 700">%%INTEREST%%</dd></div>
<div style="display: flex; justify-content: space-between; gap: 16px"><dt style="color: #C7CFDB">Jednorazové poplatky</dt><dd style="margin: 0; font-weight: 700">%%FEES%%</dd></div>
<div style="display: flex; justify-content: space-between; gap: 16px; border-top: 1px solid #1C3D6B; padding-top: 12px"><dt style="color: #F7F5F0; font-weight: 700">Zaplatené banke celkom</dt><dd style="margin: 0; font-weight: 800; color: #D9AE52">%%TOTAL%%</dd></div>
</dl>
<a href="#kontakt" style="margin-top: auto; text-align: center; background: #D9AE52; color: #001939; text-decoration: none; padding: 16px 20px; border-radius: 4px; font-weight: 800; font-size: 16px">Chcem nezáväznú ponuku hypotéky</a>
<p style="margin: 0; font-size: 12px; line-height: 1.5; color: #A9B4C6">Výpočet má len informatívny charakter a nie je ponukou úveru. Skutočná splátka závisí od banky, fixácie a vašej bonity.</p>
</div>

</div>
</div>
</section>

'''

NOTE_STYLE = 'margin: 0; font-size: 13px; color: #6B5220; font-weight: 600'
NOTE_TEXT = 'Banky na Slovensku zvyčajne požičajú najviac 90 % hodnoty nehnuteľnosti.'


def dc():
    s = TPL
    for k in DEFAULTS:
        s = s.replace('%%RANGE_' + k + '%%', 'value="{{hypo.%s}}" onChange="{{hypo.on_%s}}"' % (k, k))
    s = s.replace('%%NUM_price%%', 'value="{{hypo.price}}" onChange="{{hypo.on_price}}"')
    s = s.replace(' onsubmit="return false"', '')
    for k, v in [('OWN_LABEL', 'ownLabel'), ('RATE_LABEL', 'rateLabel'), ('YEARS_LABEL', 'yearsLabel'),
                 ('FEES_LABEL', 'feesLabel'), ('MONTHLY', 'monthly'), ('LOAN', 'loan'),
                 ('INTEREST', 'interest'), ('FEES', 'fees2'), ('TOTAL', 'total')]:
        s = s.replace('%%' + k + '%%', '{{hypo.%s}}' % v)
    s = s.replace('%%OWN_NOTE%%', '<sc-if value="{{hypo.lowOwn}}" hint-placeholder-val="{{ false }}"><p style="%s">%s</p></sc-if>' % (NOTE_STYLE, NOTE_TEXT))
    return s


def static():
    s = TPL
    for k, v in DEFAULTS.items():
        s = s.replace('%%RANGE_' + k + '%%', 'value="%s"' % v)
    s = s.replace('%%NUM_price%%', 'id="h-price-num" value="%s"' % DEFAULTS['price'])
    for k, i in [('OWN_LABEL', 'h-own-l'), ('RATE_LABEL', 'h-rate-l'), ('YEARS_LABEL', 'h-years-l'),
                 ('FEES_LABEL', 'h-fees-l'), ('MONTHLY', 'h-monthly'), ('LOAN', 'h-loan'),
                 ('INTEREST', 'h-interest'), ('FEES', 'h-fees-o'), ('TOTAL', 'h-total')]:
        s = s.replace('%%' + k + '%%', '<span id="%s"></span>' % i)
    s = s.replace('%%OWN_NOTE%%', '<p id="h-own-note" style="%s" hidden>%s</p>' % (NOTE_STYLE, NOTE_TEXT))
    return s


STATIC_SCRIPT = '''<script>
(function(){
  var $=function(id){return document.getElementById(id)};
  if(!$('h-price'))return;
  var eur=function(v,d){return v.toLocaleString('sk-SK',{minimumFractionDigits:d,maximumFractionDigits:d})+' €'};
  function calc(){
    var price=Math.max(0,Number($('h-price-num').value)||0), own=Number($('h-own').value),
        rate=Number($('h-rate').value), years=Number($('h-years').value), fees=Number($('h-fees').value);
    var loan=Math.max(0,price*(1-own/100)), n=years*12, r=rate/100/12;
    var m=loan<=0?0:(r===0?loan/n:loan*r/(1-Math.pow(1+r,-n)));
    $('h-own-l').textContent=own+' % · '+eur(price*own/100,0);
    $('h-rate-l').textContent=rate.toLocaleString('sk-SK',{minimumFractionDigits:2,maximumFractionDigits:2})+' %';
    $('h-years-l').textContent=years+(years===1?' rok':years<5?' roky':' rokov');
    $('h-fees-l').textContent=eur(fees,0);
    $('h-monthly').textContent=eur(m,2);
    $('h-loan').textContent=eur(loan,0);
    $('h-interest').textContent=eur(Math.max(0,m*n-loan),2);
    $('h-fees-o').textContent=eur(fees,2);
    $('h-total').textContent=eur(m*n+fees,2);
    $('h-own-note').hidden=!(own<10&&loan>0);
  }
  $('h-price').addEventListener('input',function(){$('h-price-num').value=this.value;calc()});
  $('h-price-num').addEventListener('input',function(){var v=Number(this.value)||0;$('h-price').value=Math.min(1000000,Math.max(10000,v));calc()});
  ['h-own','h-rate','h-years','h-fees'].forEach(function(id){$(id).addEventListener('input',calc)});
  calc();
})();
</script>
'''

RANGE_CSS = 'input[type=range].hrange{width:100%;height:28px;margin:0;accent-color:#B8860B;cursor:pointer}'

DC_LOGIC_STATE = "hprice: 150000, hown: 20, hrate: 3.5, hyears: 30, hfees: 0"

DC_LOGIC_METHOD = '''  hypo() {
    const st = this.state;
    const eur = (v, d) => v.toLocaleString('sk-SK', { minimumFractionDigits: d, maximumFractionDigits: d }) + ' €';
    const price = Math.max(0, Number(st.hprice) || 0), own = Number(st.hown), rate = Number(st.hrate), years = Number(st.hyears), fees = Number(st.hfees);
    const loan = Math.max(0, price * (1 - own / 100)), n = years * 12, r = rate / 100 / 12;
    const m = loan <= 0 ? 0 : (r === 0 ? loan / n : loan * r / (1 - Math.pow(1 + r, -n)));
    const set = (key) => (e) => this.setState({ [key]: e.target.value });
    return {
      price: st.hprice, own: st.hown, rate: st.hrate, years: st.hyears, fees: st.hfees,
      on_price: set('hprice'), on_own: set('hown'), on_rate: set('hrate'), on_years: set('hyears'), on_fees: set('hfees'),
      ownLabel: own + ' % · ' + eur(price * own / 100, 0),
      rateLabel: rate.toLocaleString('sk-SK', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' %',
      yearsLabel: years + (years === 1 ? ' rok' : years < 5 ? ' roky' : ' rokov'),
      feesLabel: eur(fees, 0),
      monthly: eur(m, 2), loan: eur(loan, 0), interest: eur(Math.max(0, m * n - loan), 2),
      fees2: eur(fees, 2), total: eur(m * n + fees, 2),
      lowOwn: own < 10 && loan > 0
    };
  }
'''
