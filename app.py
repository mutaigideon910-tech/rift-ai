import os, base64, requests, datetime, traceback
from flask import Flask, request, jsonify, render_template_string
app = Flask(__name__)

def rift_brain(msg):
    m=msg.lower()
    if "farm" in m: return "Rift Valley tip: Maize 75x30cm, DAP at planting!"
    return f"RIFT AI: You said '{msg}'. I'm live from Eldoret!"

def get_token():
    try:
        k = (os.environ.get("MPESA_CONSUMER_KEY") or "").strip()
        s = (os.environ.get("MPESA_CONSUMER_SECRET") or "").strip()
        if not k or not s: return None, "No keys set"
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        r = requests.get(url, auth=(k,s), timeout=10)
        data = r.json()
        token = data.get("access_token")
        if not token: return None, f"Daraja error: {data}"
        return token, None
    except Exception as e:
        return None, str(e)

HTML = """<html><head><meta name=viewport content="width=device-width">
<title>RIFT AI</title>
<style>body{background:#0f0f0f;color:white;font-family:sans-serif;text-align:center;padding:20px}
#chatbox{border:1px solid #333;height:200px;overflow-y:auto;text-align:left;padding:10px;margin:10px 0}
input{padding:10px;width:45%}button{padding:10px;background:#ff9800;border:none}.mpesa{border:2px solid #00ff88;padding:15px;margin-top:15px}</style>
</head><body>
<p>Made in Eldoret | RIFT AI v1.0</p>
<div id="chatbox"><div>Habari! RIFT AI with REAL M-Pesa ready!</div></div>
<input id="q" placeholder="Ask..."><button onclick="ask()">Send</button>
<div class="mpesa">
<h3>Support RIFT AI - Till: 0180974422</h3>
<p style="color:#00ff88">REAL STK PUSH ACTIVE</p>
<input id="phone" placeholder="254708374149" value="254708374149"><input id="amount" value="10" style="width:20%"><button onclick="pay()">Lipa REAL</button>
<p id="paystatus" style="color:yellow"></p>
<p style="font-size:10px">Sandbox test number must be 254708374149. After Go-Live, real money to 0180974422</p>
</div>
<script>
async function ask(){let q=document.getElementById('q').value;let b=document.getElementById('chatbox');b.innerHTML+=`<div>You: ${q}</div>`;document.getElementById('q').value='';let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q})});let d=await r.json();b.innerHTML+=`<div style="color:#ff9800">RIFT: ${d.reply}</div>`}
async function pay(){let ph=document.getElementById('phone').value;let am=document.getElementById('amount').value;let s=document.getElementById('paystatus');s.innerText='Sending...';try{let r=await fetch('/mpesa/pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:ph,amount:am})});let d=await r.json();s.innerText=d.message; s.style.color=d.ok?'#00ff88':'red';}catch(e){s.innerText='Network error: '+e}}
</script></body></html>"""

@app.route("/")
def home(): return render_template_string(HTML)
@app.route("/chat", methods=["POST"])
def chat(): return jsonify({"reply": rift_brain(request.json.get("message",""))})

@app.route("/mpesa/pay", methods=["POST"])
def mpesa_pay():
    try:
        d=request.json; phone=(d.get("phone") or "").strip(); amount=(d.get("amount") or "10").strip()
        if phone.startswith("0"): phone="254"+phone[1:]
        token, err = get_token()
        if not token: return jsonify({"message": f"TOKEN FAILED: {err} - Check your MPESA_CONSUMER_KEY/SECRET in Render Environment. Remove spaces!", "ok": False})
        ts=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        sc=(os.environ.get("MPESA_SHORTCODE") or "174379").strip()
        pk=(os.environ.get("MPESA_PASSKEY") or "").strip()
        pwd=base64.b64encode(f"{sc}{pk}{ts}".encode()).decode()
        payload={"BusinessShortCode":sc,"Password":pwd,"Timestamp":ts,"TransactionType":"CustomerPayBillOnline","Amount":amount,"PartyA":phone,"PartyB":sc,"PhoneNumber":phone,"CallBackURL":os.environ.get("MPESA_CALLBACK"),"AccountReference":"RIFT AI","TransactionDesc":"Support"}
        headers={"Authorization": f"Bearer {token}"}
        r=requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=headers, timeout=15)
        j=r.json()
        if j.get("ResponseCode")=="0":
            return jsonify({"message": f"SUCCESS! STK sent to {phone}. Check phone. CheckoutID: {j.get('CheckoutRequestID')}", "ok": True})
        else:
            return jsonify({"message": f"Daraja said: {j}", "ok": False})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": f"Server error: {e}", "ok": False})

@app.route("/mpesa/callback", methods=["POST"])
def cb(): print("CALLBACK", request.json); return jsonify({"ResultCode":0})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))


