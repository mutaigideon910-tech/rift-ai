from flask import Flask, render_template_string, request, jsonify
import os
import random
import string

app = Flask(__name__)

AMOUNT = 50
POCHI = "0180974422"
USED_CODES = set()

# Simple offline knowledge for Eldoret
FARMING_KB = {
    "armyworm": "Fall Armyworm in Moiben: Spray NOVA BT or Duduthrin early morning. For organic: mix ash + pepper. Plant early to escape. Call KALRO for free advice.",
    "maize": "Maize in Uasin Gishu: Use DH04 or H614. Plant with 10g DAP. Top-dress with CAN after 3 weeks. Weed at 2 weeks.",
    "potato": "Potato blight: Spray Ridomil Gold every 7 days in rainy season. Use clean seed from ADC Molo. Store in diffused light store.",
    "dairy": "Dairy feeding: 10kg silage + 2kg dairy meal per cow per day. Deworm every 3 months. Use hay in dry season Jan-Mar.",
    "coffee": "COFFEE Kahawa - Batian/Ruiru11: CBD resistant 30kg/tree. Spacing 2m x 2m. Diseases: CBD=Captafol, Rust=Copper. Fertilizer: 100g DAP planting",
    "kahawa": "COFFEE Kahawa - Batian/Ruiru11: CBD resistant 30kg/tree. Spacing 2m x 2m. Diseases: CBD=Captafol, Rust=Copper. Fertilizer: 100g DAP planting",
    "batian": "BATIAN COFFEE KENYA: CBD resistant, 30kg/tree, spacing 2x2m, KALRO approved. Price Cherry 80-110 KES/kg (KPCU). Pruning light.",
    "ruiru": "RUIRU 11 KENYA: Compact, 20-25kg/tree, needs CBD spray in cold areas like Nandi Hills. Spacing 2x2m. Good for small shamba.",
    "sl28": "SL28 KENYA: Best quality, premium price, susceptible to CBD, needs Captafol/Copper spray. Altitude 1300-1600m. 25kg/tree",
    "kenya_coffee": "KENYA: Batian CBD resistant 30kg/tree spacing 2x2m KALRO. Ruiru 11 Compact 20-25kg needs CBD spray. SL28 Best quality needs Captafol. Price Cherry 80-110 KES/kg (KPCU)",
    "kenya": "KENYA COFFEE: Batian, Ruiru 11, SL28, SL34. Price 80-110 KES/kg cherry. KPCU. CBD and Leaf Rust main diseases. Spacing 2x2m",
    "uganda": "UGANDA: Varieties Robusta main SL14 Caturra. Board UCDA. Price Kiboko 6000-8000 UGX/kg FAQ 12000 UGX/kg. Disease Coffee Wilt Disease CWD + Black Twig Borer. Spacing Robusta 3x3m",
    "ethiopia": "ETHIOPIA: Varieties Heirloom Geisha Caturra Bourbon. Price 80-150 ETB/kg cherry. Disease CBD Wilt. Note Birthplace of coffee washed process",
    "rwanda": "RWANDA TANZANIA: Varieties Bourbon Kent. Price Rwanda cherry 800-1200 RWF/kg Tanzania 3000-5000 TZS/kg. Disease Antestia Bug Rwanda CBD",
    "tanzania": "TANZANIA: Varieties Bourbon Kent. Price 3000-5000 TZS/kg. Disease CBD. Altitude 1000-1500m",
    "global_coffee": "GLOBAL Brazil Colombia Vietnam: Arabica 60% Robusta 40%. Brazil Mundo Novo Catuai 50-60 bags/ha. Colombia Castillo Caturra. Vietnam Robusta 90%. General pH 5.5-6.5 altitude 1200-2000m Arabica",
    "brazil": "BRAZIL: Mundo Novo Catuai 50-60 bags/ha. High yield. Mundo Novo tall, Catuai compact. Price 60kg bag",
    "colombia": "COLOMBIA: Castillo Caturra altitude 1500-2000m. Castillo disease resistant. Washed process famous",
    "vietnam": "VIETNAM: Robusta 90% world Robusta. High yield. Low altitude 500-800m",
    "heirloom": "ETHIOPIA Heirloom: Ancient varieties, birthplace of coffee. Price 80-150 ETB/kg cherry. Washed natural process. High quality",
    "geisha": "GEISHA: Ethiopia origin, Panama famous. Price premium 3x. Needs high altitude 1600-2000m. Floral taste. Ethiopia 80-150 ETB/kg",
    "bourbon": "BOURBON: Rwanda famous, also Ethiopia Tanzania. Sweet high quality. Price Rwanda 800-1200 RWF/kg. Altitude 1300-1800m",
    "mundo novo": "MUNDO NOVO BRAZIL: Tall, high yield 50-60 bags/ha. Disease resistant. Brazil main variety. Altitude 800-1200m. Cross Bourbon + Typica",
    "catuai": "CATUAI BRAZIL: Compact high yield 50-60 bags/ha. Needs fertilizer. Parent Mundo Novo x Caturra. Good for small shamba",
    "castillo": "CASTILLO COLOMBIA: Disease resistant, Caturra parent. 30-40 bags/ha. Altitude 1500-2000m. Colombia main variety",
    "robusta": "ROBUSTA UGANDA: Main variety Uganda. Board UCDA. Price Kiboko 6000-8000 UGX/kg FAQ 12000 UGX/kg. Spacing 3x3m. Wilt disease CWD",
    "caturra": "CATURRA: Compact high quality. Ethiopia Colombia. Price 80-150 ETB/kg. Needs high altitude. Bourbon mutation",
    "kent": "KENT TANZANIA: Disease resistant, high altitude. Price 3000-5000 TZS/kg",
    "sl14": "SL14 UGANDA: Drought resistant, Robusta cross. Uganda variety",
    "default": "RIFT AI - Eldoret Offline AI: I help with armyworm, maize, potatoes, dairy, coffee. I now support Kenya Uganda Ethiopia Rwanda Tanzania Brazil Colombia Vietnam. Ask in English, Swahili, or Sheng. Example: 'dawa ya armyworm' or 'Geisha coffee' or 'Mundo Novo' or 'price Uganda'"
}

def get_answer(q):
    q = q.lower()
    for key in FARMING_KB:
        if key in q:
            return FARMING_KB[key]
    if "jeshi" in q or "army" in q:
        return FARMING_KB["armyworm"]
    if "viazi" in q:
        return FARMING_KB["potato"]
    if "maziwa" in q or "ng'ombe" in q or "milk" in q:
        return FARMING_KB["dairy"]
    if "mahindi" in q or "maize" in q:
        return FARMING_KB["maize"]
    return FARMING_KB["default"]

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>RIFT AI - Eldoret</title>
<title>RIFT AI - Eldoret</title>
<link rel="icon" type="image/png" href="/static/rift-ai-logo-light.png">
<meta name="viewport"...
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial; max-width:500px; margin:auto; padding:20px; background:#f5f5f0;}
.card{background:white; padding:20px; border-radius:15px; box-shadow:0 4px 10px rgba(0,0,0,0.1); text-align:center;}
.logo{font-size:60px;}
h1{color:#2e7d32; margin:5px;}
.green-btn{width:100%; padding:14px; background:#2e7d32; color:white; font-size:18px; border:none; border-radius:8px; cursor:pointer; font-weight:bold;}
.m-pesa{background:#e8f5e9; padding:12px; border-radius:8px; margin:15px 0; text-align:left;}
input{width:100%; padding:12px; border:1px solid #ccc; border-radius:8px; margin:5px 0;}
#chatBox{height:300px; overflow-y:auto; border:1px solid #ddd; padding:10px; border-radius:8px; text-align:left; background:#fafafa; display:none;}
.user{color:blue; margin:5px 0;}.bot{color:#2e7d32; margin:5px 0; background:#e8f5e9; padding:8px; border-radius:8px;}
</style>
</head>
<body>
<div class="card">

<img src="/static/rift-ai-logo-light.png" alt="RIFT AI" style="height:65px; display:block; margin:0 auto 8px;">
<h2 style="margin:5px 0;">RIFT AI</h2>
<p><b>ELDORET • OFFLINE AI</b></p>

<div id="paySection">
<div class="m-pesa">
<b>🔓 Unlock Instructions:</b><br>
1. Lipa <b>Ksh 50</b> to Pochi <b>0180974422</b> (RIFT AI)<br>
2. Tumia code utapewa WhatsApp au hapa<br>
3. <b style="color:green;">✅ Pay once, use forever! No weekly payment - LIFETIME access!</b>
</div>
<button class="green-btn" onclick="generateCode()">🔓 Unlock RIFT AI - Ksh 50 - LIFETIME ✅ Pay once, use forever!</button>
<p style="margin-top:10px;"><input id="codeInput" placeholder="Enter code e.g. UJD9Z9YO3D"><button class="green-btn" style="background:#4caf50; margin-top:5px;" onclick="unlock()">Unlock Chat</button></p>
<p id="status"></p>
</div>

<div id="chatBox"></div>
<div id="chatInput" style="display:none; margin-top:10px;">
<input id="q" placeholder="Ask: dawa ya armyworm?"><button class="green-btn" onclick="ask()">Ask RIFT AI</button>
</div>

<p style="font-size:12px; color:gray; margin-top:20px;">Tested for Moiben, Turbo, Soy • KALRO methods</p>
</div>

<script>
function generateCode(){
  let code = Math.random().toString(36).substring(2,12).toUpperCase();
  document.getElementById('status').innerHTML = "Your code: <b>"+code+"</b><br>Copy it and paste below! (Demo - in real use you verify M-Pesa)";
  document.getElementById('codeInput').value = code;
}
function unlock(){
  let c = document.getElementById('codeInput').value;
  if(c.length < 5){ alert("Enter valid code"); return;}
  fetch('/unlock',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({code:c})})
 .then(r=>r.json()).then(d=>{
    if(d.ok){
      document.getElementById('paySection').style.display='none';
      document.getElementById('chatBox').style.display='block';
      document.getElementById('chatInput').style.display='block';
      document.getElementById('chatBox').innerHTML = "<div class='bot'><b>RIFT AI:</b> Chat Unlocked ✅ - LIFETIME access! Ask me anything about farming!</div>";
    } else {
      alert(d.msg);
    }
  });
}
function ask(){
  let q = document.getElementById('q').value;
  if(!q) return;
  let box = document.getElementById('chatBox');
  box.innerHTML += "<div class='user'><b>You:</b> "+q+"</div>";
  document.getElementById('q').value="";
  fetch('/ask',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({q:q})})
 .then(r=>r.json()).then(d=>{
    box.innerHTML += "<div class='bot'><b>RIFT AI:</b> "+d.a+"</div>";
    box.scrollTop = box.scrollHeight;
  });
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/chat')
def chat_page():
    return render_template_string(HTML_PAGE)

@app.route('/unlock', methods=['POST'])
def unlock_code():
    data = request.json
    code = data.get('code','').strip().upper()
    if code in USED_CODES:
        return jsonify({"ok": False, "msg": "Code already used!"})
    USED_CODES.add(code)
    return jsonify({"ok": True})

@app.route('/ask', methods=['POST'])
def ask_q():
    data = request.json
    q = data.get('q','')
    ans = get_answer(q)
    return jsonify({"a": ans})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
