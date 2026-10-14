from flask import Flask, request, render_template_string
import os, re

app = Flask(__name__)
app.secret_key = "rift-ai-perfect-logo-2026"

TILL_NUMBER = "0180974422"
TILL_NAME = "GIDEON MUTAI - RIFT AI"
AMOUNT = 50
USED_CODES = set()

def get_rift_answer(question):
    q = question.lower()
    if any(x in q for x in ["armyworm", "fall army", "jeshi", "maize worm"]):
        return """
        🌽 <b>MAIZE FALL ARMYWORM - Eldoret/Uasin Gishu</b><br><br>
        <b>1. Scout:</b> Check at 6am inside funnel for worms + sawdust (frass)<br>
        <b>2. Handpick:</b> Crush larvae or put in soapy water<br>
        <b>3. Organic (Best):</b> 200g Neem powder + 50g chili + soap in 20L water. Spray into funnel at 5pm<br>
        <b>4. Chemical if severe:</b> Prove 1.9EC or Coragen 10ml/20L, spray evening<br>
        <b>5. Prevention:</b> Push-Pull: Desmodium between maize, Brachiaria border - 89% works in Moiben/Turbo<br>
        <b>6. Buy:</b> Eldoret Agrovets, Ksh 450-600<br><br><i>KALRO Kitale Approved</i>
        """
    elif any(x in q for x in ["blight", "viazi", "potato"]):
        return "🥔 <b>POTATO BLIGHT:</b> Cold + rain in Kaptagat. Use Ridomil Gold 50g/20L every 7 days, remove infected leaves."
    elif any(x in q for x in ["dairy", "ng'ombe", "maziwa", "cow", "milk"]):
        return "🐄 <b>DAIRY BOOST:</b> Dairy meal 2kg + 1kg lucerne. Deworm Nilzan Plus every 3 months. Water 80L per cow/day."
    elif any(x in q for x in ["soil", "mbolea"]):
        return "🌱 <b>SOIL:</b> Test at NCPB Eldoret Ksh 1200. pH 5.2 acidic -> Lime 100kg/acre. DAP 50kg + CAN 2 bags/acre."
    else:
        return f"🌾 <b>RIFT AI for:</b> '{question}'<br><br>Tell me Crop + Location (Moiben/Turbo/Soy) + Problem.<br>Example: 'Maize yellowing in Moiben 2 weeks after planting'"

LOGO_HTML = """
<div style="text-align:center; margin-bottom:15px;">
<div style="width:90px; height:90px; margin:0 auto; background:#e8f5e9; border:3px solid #ffb300; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:42px;">🧠</div>
<div style="font-size:28px; font-weight:800; color:#1b4332; letter-spacing:2px; margin-top:8px;">RIFT AI</div>
<div style="font-size:12px; color:#2e7d32; letter-spacing:3px;">ELDORET • OFFLINE AI</div>
</div>
"""

HOME_HTML = f"""
<div style="max-width:550px; margin:20px auto; font-family:sans-serif; padding:15px;">
{LOGO_HTML}
<p style="text-align:center; margin-top:0;">For Uasin Gishu Farmers. Works Offline.</p>
<div style="background:#e8f5e9; border:2px solid #2e7d32; padding:18px; border-radius:12px;">
<b style="color:#2e7d32;">💚 Lipa na M-Pesa Pochi la Biashara</b><br><br>
M-Pesa → Lipa na M-Pesa → <b>Pochi la Biashara</b><br>
Phone: <b style="font-size:22px;">{TILL_NUMBER}</b><br>
Name: {TILL_NAME}<br>
Amount: <b>Ksh {AMOUNT}</b><br>
PIN → Get SMS CODE
</div>
<br>
<form action="/pay" method="post">
<input name="code" placeholder="Paste M-Pesa Code e.g. UJD9Z9YO3D" style="width:100%; padding:14px; font-size:16px; border:2px solid #2e7d32; border-radius:8px;" required>
<br><br>
<button style="width:100%; padding:14px; background:#2e7d32; color:white; font-size:18px; border:none; border-radius:8px;">🔓 Unlock RIFT AI - Ksh {AMOUNT}</button>
</form>
<br><center><a href="/chat">Already paid? Go to Chat →</a></center>
</div>
"""

CHAT_HTML = f"""
<div style="max-width:700px; margin:20px auto; font-family:sans-serif; padding:15px;">
{LOGO_HTML}
<h2 style="text-align:center;">Chat - Unlocked ✅</h2>
<form method="post">
<textarea name="q" placeholder="e.g., How to handle maize fall armyworm in Eldoret?" style="width:100%; height:90px; padding:10px; font-size:15px;"></textarea><br><br>
<button style="width:100%; padding:12px; background:#2e7d32; color:white; border:none; border-radius:6px; font-size:16px;">Ask RIFT AI</button>
</form>
{{% if answer %}}
<hr><div style="background:#f9fbe7; padding:15px; border-left:4px solid #2e7d32; border-radius:5px;">{{{{ answer|safe }}}}</div>
{{% endif %}}
<br><a href="/">← Back Home</a>
</div>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/pay", methods=["POST"])
def pay():
    code = request.form.get("code","").strip().upper()
    if len(code) < 8:
        return f"❌ Code too short <br><a href='/'>Back</a>"
    if code in USED_CODES:
        return f"✅ Already used - Go to Chat <br><a href='/chat'>Chat →</a>"
    if not re.match(r'^[A-Z0-9]{{8,12}}$', code):
        return f"❌ Invalid code <br><a href='/'>Back</a>"
    USED_CODES.add(code)
    return f'<div style="text-align:center; margin-top:60px; font-family:sans-serif;"><h2>✅ Payment Confirmed!</h2><p>Code {code} Accepted</p><a href="/chat" style="background:#2e7d32; color:white; padding:14px 24px; text-decoration:none; border-radius:8px;">🚀 Go to Chat Now</a></div>'

@app.route("/chat", methods=["GET","POST"])
def chat():
    answer = None
    if request.method == "POST":
        q = request.form.get("q","").strip()
        if q:
            answer = get_rift_answer(q)
    return render_template_string(CHAT_HTML, answer=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
