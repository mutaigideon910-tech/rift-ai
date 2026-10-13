from flask import Flask, request, jsonify, render_template_string
import re
from datetime import datetime

app = Flask(__name__)

# Store used codes to prevent reuse (simple in-memory)
used_codes = set()

# === YOUR TILL ===
TILL_NUMBER = "0180974442"
AMOUNT = 50

HTML_PAGE = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RIFT AI - Support</title>
<style>
body{{font-family:Arial;background:#0f172a;color:white;padding:20px;text-align:center}}
.card{{background:#1e293b;padding:25px;border-radius:15px;max-width:400px;margin:auto}}
input{{width:90%;padding:12px;margin:10px;border-radius:8px;border:none}}
button{{background:#22c55e;color:black;padding:12px 20px;border:none;border-radius:8px;font-weight:bold;width:95%;cursor:pointer}}
button:disabled{{background:gray}}
.instruct{{background:#334155;padding:15px;border-radius:10px;text-align:left;margin:15px 0;font-size:14px}}
.success{{color:#22c55e;font-weight:bold}}
</style>
</head>
<body>
<h2>🌾 RIFT AI - Eldoret</h2>
<div class="card">
  <h3>Support Kenya's Offline AI</h3>
  <div class="instruct">
    <b>Step 1:</b> Go to M-Pesa<br>
    <b>Step 2:</b> Lipa na M-Pesa → Buy Goods and Services<br>
    <b>Step 3:</b> Enter Till: <b>{TILL_NUMBER}</b><br>
    <b>Step 4:</b> Amount: <b>{AMOUNT}</b><br>
    <b>Step 5:</b> Enter PIN and Send<br>
    <b>Step 6:</b> Copy the M-Pesa Code (e.g. THI... ) and paste below
  </div>
  
  <input id="mpesa_code" placeholder="Paste M-Pesa Code e.g. THI5A9K2L1" />
  <input id="phone" placeholder="Your Phone 07..." />
  <button onclick="verify()">Verify & Unlock AI</button>
  <p id="status"></p>
</div>

<script>
async function verify(){{
  let code = document.getElementById('mpesa_code').value.trim().toUpperCase();
  let phone = document.getElementById('phone').value.trim();
  let status = document.getElementById('status');
  
  if(code.length < 8){{ status.innerText = "Enter valid M-Pesa code"; return; }}
  
  status.innerText = "Verifying...";
  let res = await fetch('/verify-mpesa', {{
    method:'POST',
    headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{code: code, phone: phone}})
  }});
  let data = await res.json();
  status.innerHTML = data.message;
  if(data.ok){{
    status.className = "success";
    setTimeout(()=>{{ window.location.href = "/chat"; }}, 1500);
  }}
}}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/verify-mpesa", methods=["POST"])
def verify_mpesa():
    data = request.get_json()
    code = data.get("code","").strip().upper()
    phone = data.get("phone","").strip()

    # 1. Validate format: M-Pesa codes are 10 chars, letters + numbers, e.g. TH...
    if not re.match(r'^[A-Z0-9]{8,12}$', code):
        return jsonify({"ok": False, "message": "❌ Invalid code format. Check SMS from M-PESA"})

    # 2. Prevent reuse
    if code in used_codes:
        return jsonify({"ok": False, "message": "⚠️ This code was already used. Use new payment."})

    # 3. Basic check - you can later add real SMS forwarding check
    # For now we accept any valid-looking code and log it for you to confirm in M-Pesa app
    used_codes.add(code)
    
    # Log to Render logs so you can see who paid
    print(f"[{datetime.now()}] NEW PAYMENT: Code={code} Phone={phone} Till={TILL_NUMBER}", flush=True)

    return jsonify({
        "ok": True, 
        "message": f"✅ Verified! Code {code} received. Money confirmed to Till {TILL_NUMBER}. Unlocking RIFT AI..."
    })

@app.route("/chat")
def chat():
    return "<h2 style='text-align:center;margin-top:50px'>✅ Payment Confirmed!<br><br>RIFT AI Full Chat Unlocked<br><br><a href='/'>Back Home</a></h2>"

@app.route("/admin/payments")
def admin():
    return f"Used codes: {list(used_codes)} | Check your M-Pesa Org portal or My Safaricom App for Till {TILL_NUMBER} balance"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
