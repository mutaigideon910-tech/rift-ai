
import os, base64, requests, datetime
from flask import Flask, request, jsonify, render_template_string
app = Flask(__name__)

def rift_brain(msg):
    m=msg.lower()
    if "farm" in m: return "Rift Valley tip: Plant maize 75x30cm, use DAP!"
    if "hello" in m or "habari" in m: return "Habari! RIFT AI from Eldoret - now with REAL M-Pesa!"
    return f"You said: {msg}. RIFT AI ready!"

def get_token():
    k=os.environ.get("MPESA_CONSUMER_KEY")
    s=os.environ.get("MPESA_CONSUMER_SECRET")
    if not k: return None
    r=requests.get("https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials", auth=(k,s))
    return r.json().get("access_token")

HTML = """
<html><head><meta name="viewport" content="width=device-width">
<title>RIFT AI - Real M-Pesa</title>
<style>body{background:#0f0f0f;color:white;font-family:sans-serif;text-align:center;padding:20px}
#chatbox{border:1px solid #333;height:250px;overflow-y:scroll;text-align:left;padding:10px;margin:15px 0}
input{padding:10px;width:50%}button{padding:10px;background:#ff9800;border:none}.mpesa{border:2px solid #00ff88;padding:15px;margin-top:20px}</style>
</head><body>
<p>Made in Eldoret, Rift Valley | No API Key Needed | Runs Offline</p>
<div id="chatbox"><div>Habari! I am RIFT AI - Kenya's FREE AI. Ask me about farming. Now with REAL M-Pesa!</div></div>
<input id="q" placeholder="Ask RIFT AI..."><button onclick="ask()">Send</button>
<div class="mpesa">
<h3>Support RIFT AI - Lipa na M-Pesa: 0180974422</h3>
<p style="color:#00ff88">REAL STK PUSH ACTIVE - Enter phone!</p>
<input id="phone" placeholder="07XXXXXXXX"><input id="amount" placeholder="10" style="width:20%"><button onclick="pay()">Lipa REAL</button>
<p id="paystatus" style="color:#00ff88;font-weight:bold"></p>
<p style="font-size:11px">Sandbox: Use 254708374149 for test. After Go-Live, money goes to Till 0180974422</p>
</div>
<script>
async function ask(){
 let q=document.getElementById('q').value; if(!q)return;
 let b=document.getElementById('chatbox'); b.innerHTML+=`<div>You: ${q}</div>`; document.getElementById('q').value='';
 let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q})});
 let d=await res.json(); b.innerHTML+=`<div style="color:#ff9800">RIFT: ${d.reply}</div>`;
}
async function pay(){
 let ph=document.getElementById('phone').value; let am=document.getElementById('amount').value||'10';
 document.getElementById('paystatus').innerText='Sending REAL STK to '+ph+'...';
 let res=await fetch('/mpesa/pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:ph,amount:am})});
 let d=await res.json(); document.getElementById('paystatus').innerText=d.message;
}
</script>
</body></html>
"""
@app.route("/")
def home(): return render_template_string(HTML)
@app.route("/chat", methods=["POST"])
def chat(): return jsonify({"reply": rift_brain(request.json.get("message",""))})
@app.route("/mpesa/pay", methods=["POST"])
def mpesa_pay():
    d=request.json; phone=d.get("phone",""); amount=d.get("amount","10")
    if phone.startswith("0"): phone="254"+phone[1:]
    token=get_token()
    if not token: return jsonify({"message": "Keys missing! Check Render Environment Variables"})
    ts=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    sc=os.environ.get("MPESA_SHORTCODE","174379"); pk=os.environ.get("MPESA_PASSKEY")
    pwd=base64.b64encode(f"{sc}{pk}{ts}".encode()).decode()
    payload={"BusinessShortCode":sc,"Password":pwd,"Timestamp":ts,"TransactionType":"CustomerPayBillOnline","Amount":amount,"PartyA":phone,"PartyB":sc,"PhoneNumber":phone,"CallBackURL":os.environ.get("MPESA_CALLBACK"),"AccountReference":"RIFT AI","TransactionDesc":"Support RIFT"}
    h={"Authorization": f"Bearer {token}"}
    r=requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=h)
    return jsonify({"message": f"STK Sent to {phone}! Response: {r.json().get('ResponseDescription','Check phone')}"})
@app.route("/mpesa/callback", methods=["POST"])
def cb(): print(request.json); return jsonify({"ResultCode":0})
if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000)); app.run(host="0.0.0.0", port=port)
