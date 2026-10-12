



import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

def rift_brain(msg):
    msg = msg.lower()
    if "farm" in msg: return "For farming in Rift Valley: Use certified seeds, plant at onset of rains. Eldoret soils love maize & potatoes!"
    if "hello" in msg or "habari" in msg: return "Habari! I am RIFT AI v1.0 - Kenya's FREE AI built by Riftai in Eldoret. No OpenAI needed. How can I help?"
    return f"You said: {msg}. I am RIFT AI running offline in Eldoret, ready to help with farming, business, and knowledge!"

HTML = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width">
<title>RIFT AI - Kenya's Free AI</title>
<style>
body{background:#0f0f0f;color:white;font-family:sans-serif;text-align:center;padding:20px}
#chatbox{border:1px solid #333;height:300px;overflow-y:scroll;text-align:left;padding:10px;margin:20px 0}
.msg{margin:8px 0}.user{color:#4caf50}.ai{color:#ff9800}
input{padding:10px;width:60%}button{padding:10px;background:#ff9800;border:none}
.mpesa{border:1px dashed #ff9800;padding:15px;margin-top:20px}
</style>
</head>
<body>
<p>Made in Eldoret, Rift Valley | No API Key Needed | Runs Offline</p>
<div class="container">
<div id="chatbox"><div class="msg ai">Habari! I am RIFT AI v1.0 - Kenya's FREE AI built by Riftai in Eldoret. No OpenAI $ needed. Ask me about farming.</div></div>
<div style="margin-top:15px">
<input id="q" placeholder="Ask RIFT AI anything..." onkeypress="if(event.key==='Enter')ask()">
<button onclick="ask()">Send</button>
</div>
<div class="mpesa">
<h3> Support RIFT AI - Lipa na M-Pesa: 0180974422 </h3>
<p>Your support helps us buy OpenAI credits... Send to 0180974422 - Every 10 KES helps!</p>
<input id="phone" placeholder="07XXXXXXXX" style="width:45%"><input id="amount" placeholder="KES 10" style="width:20%"><button onclick="pay()">Lipa</button>
<p id="paystatus" style="color:#00ff88"></p>
<p style="font-size:12px;color:#888">Powered by Safaricom Daraja Sandbox - Demo mode until you add Daraja keys - Money goes to your M-Pesa when live</p>
</div>
<div style="text-align:center;margin-top:30px;color:#666;font-size:11px">
<p>Made by RiftAI | ASUS Chromebook | Python 3.13.6 | Eldoret, Kenya | 2026</p>
<p>Free AI - No Dollars Needed - Kenyan Built</p>
</div>
</div>
<script>
async function ask(){
 let q=document.getElementById('q').value; if(!q) return;
 let box=document.getElementById('chatbox'); box.innerHTML+=`<div class="msg user">${q}</div>`; document.getElementById('q').value='';
 let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q})});
 let data=await res.json(); box.innerHTML+=`<div class="msg ai">${data.reply}</div>`; box.scrollTop=box.scrollHeight;
}
async function pay(){
 let phone=document.getElementById('phone').value; let amount=document.getElementById('amount').value||'10';
 document.getElementById('paystatus').innerText='Simulating STK Push to '+phone+'...';
 let res=await fetch('/mpesa/pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:phone, amount:amount})});
 let data=await res.json(); document.getElementById('paystatus').innerText=data.message;
}
</script>
</body>
</html>
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
    return jsonify({"message": f"DEMO: STK Push would be sent to {phone} for KES {amount}. To make it REAL: Get FREE Daraja keys at developer.safaricom.co.ke - Till 0180974422"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
