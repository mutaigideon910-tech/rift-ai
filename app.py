import os
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# --- FREE RIFT AI BRAIN - NO API KEY NEEDED ---
def rift_brain(user_msg):
    msg = user_msg.lower()
    if "hello" in msg or "habari" in msg:
        return "Habari! 👋 I am RIFT AI, built in Eldoret by Riftai. I run 100% free, no OpenAI needed. How can I help you today?"
    if "farm" in msg or "shamba" in msg:
        return "For Rift Valley farming: Maize does best with early planting March-April. Use DAP fertilizer, consider crop rotation with beans. Want a full farming calendar for Eldoret?"
    if "mpesa" in msg or "pay" in msg or "lipa" in msg:
        return "RIFT AI supports M-Pesa! Use the green Lipa na M-Pesa box below. We use Safaricom Daraja Sandbox - it's free to test, and when you go live you earn real KES."
    if "code" in msg or "python" in msg or "chromebook" in msg:
        return "You are coding on an ASUS Chromebook with Python 3.13.5 and Flask - just like you did! Want me to teach you to add a new feature?"
    if "who are you" in msg:
        return "I am RIFT AI, Version 1.0, Made in Eldoret, Kenya. Built on ASUS Chromebook that said 'not compatible'. Creator: Riftai. Mission: Make AI accessible for all Kenyans."
    if "business" in msg:
        return "Business idea for Eldoret: 1. AI cyber cafe for students 2. M-Pesa + AI shop assistant 3. Farm advice SMS bot. RIFT AI can power all 3. Want a business plan?"
    # default smart reply
    return f"You said: '{user_msg}'. As RIFT AI (Eldoret's AI), I'm thinking... In Rift Valley context, this is interesting! I'm still learning, but I can help with farming, coding, business, schoolwork. What exactly do you need? Built locally with no paid API - so you own it 100%."

HTML = """
<!DOCTYPE html>
<html><head>
<title>RIFT AI - Kenya's Free AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;background:#0a0a0a;color:white;margin:0}
.header{background:linear-gradient(90deg,#ff0000,#000,#00ff00);padding:25px;text-align:center}
.container{max-width:800px;margin:auto;padding:20px}
#chatbox{height:350px;background:#141414;border-radius:12px;padding:15px;overflow-y:auto;border:1px solid #333}
.msg{margin:10px 0;padding:12px;border-radius:10px;max-width:80%}
.user{background:#0066ff;margin-left:auto;text-align:right}
.ai{background:#222}
input,button{padding:13px;border-radius:10px;border:none;font-size:16px}
input{width:68%;background:#222;color:white;border:1px solid #444}
button{background:#00ff88;color:black;font-weight:bold;cursor:pointer}
.mpesa{background:linear-gradient(135deg,#0a2e0a,#001a00);padding:18px;border-radius:12px;margin-top:25px;border:1px solid #00ff88}
.badge{display:inline-block;background:#00ff88;color:black;padding:3px 10px;border-radius:20px;font-size:12px;font-weight:bold}
</style>
</head><body>
<div class="header">
<h1>RIFT AI 🚀 <span class="badge">100% FREE</span></h1>
<p>Made in Eldoret, Rift Valley | No API Key Needed | Runs Offline</p>
</div>
<div class="container">
<div id="chatbox"><div class="msg ai">Habari! I am RIFT AI v1.0 — Kenya's FREE AI built by Riftai in Eldoret. No OpenAI $ needed. Ask me about farming, business, coding, schoolwork!</div></div>
<div style="margin-top:15px">
<input id="q" placeholder="Ask RIFT AI anything..." onkeypress="if(event.key=='Enter')ask()">
<button onclick="ask()">Send 🚀</button>
</div>
<div class="mpesa">
<h3>💚 Support RIFT AI — Lipa na M-Pesa</h3>0180974422
<p>Your support helps us buy OpenAI credits and keep servers running. Every 10 KES helps!</p>
<input id="phone" placeholder="07XX XXX XXX" style="width:45%"><input id="amount" placeholder="KES 10" style="width:20%"><button onclick="pay()">Lipa</button>
<p id="paystatus" style="color:#00ff88"></p>
<p style="font-size:12px;color:#888">Powered by Safaricom Daraja Sandbox • Demo mode until you add Daraja keys • Money goes to your M-Pesa when live</p>
</div>
<div style="text-align:center;margin-top:30px;color:#666;font-size:13px">
<p>Made by Riftai | ASUS Chromebook | Python 3.13.5 | Eldoret, Kenya | 2026</p>
<p>Free AI • No Dollars Needed • Kenyan Built</p>
</div>
</div>
<script>
async function ask(){
 let q=document.getElementById('q').value; if(!q) return;
 let box=document.getElementById('chatbox'); box.innerHTML+=`<div class='msg user'>${q}</div>`; document.getElementById('q').value='';
 let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q})});
 let data=await res.json(); box.innerHTML+=`<div class='msg ai'>${data.reply}</div>`; box.scrollTop=box.scrollHeight;
}
async function pay(){
 let phone=document.getElementById('phone').value; let amount=document.getElementById('amount').value||'10';
 document.getElementById('paystatus').innerText='Simulating STK Push to '+phone+'...';
 let res=await fetch('/mpesa/pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({0180974422})});
 let data=await res.json(); document.getElementById('paystatus').innerText=data.message;
}
</script>
</body></html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message","")
    reply = rift_brain(user_msg)
    return jsonify({"reply": reply})

@app.route("/mpesa/pay", methods=["POST"])
def mpesa_pay():
    data = request.json
    phone = data.get("phone","")
    amount = data.get("amount","10")
    return jsonify({"message": f"✅ DEMO: STK Push would be sent to {0180974422} for KES {10}. To make it REAL: Get FREE Daraja keys at developer.safaricom.co.ke (no payment needed). Then people can pay you and you earn! RIFT AI is ready to monetize."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
