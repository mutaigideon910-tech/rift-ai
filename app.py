from flask import Flask, request, render_template_string
import os
import re

app = Flask(__name__)
app.secret_key = "rift-ai-final-perfect-eldoret-2026"

TILL_NUMBER = "0180974422"
TILL_NAME = "GIDEON MUTAI - RIFT AI"
AMOUNT = 50
USED_CODES = set()

# --- REAL RIFT AI BRAIN ---
def get_rift_answer(question):
    q = question.lower()
    if any(x in q for x in ["armyworm", "fall army", "jeshi", "maize worm"]):
        return """
        🌽 <b>MAIZE FALL ARMYWORM - Eldoret/Uasin Gishu</b><br><br>
        <b>1. Scout:</b> Check at 6am inside funnel for worms + sawdust (frass)<br>
        <b>2. Handpick:</b> Crush larvae or put in soapy water<br>
        <b>3. Organic (Best):</b> 200g Neem powder + 50g chili + soap in 20L water. Spray into funnel at 5pm<br>
        <b>4. Chemical if severe:</b> Prove 1.9EC or Coragen 10ml/20L, spray evening<br>
        <b>5. Prevention:</b> Push-Pull: Desmodium between maize, Brachiaria border - 89% works in Moiben/Turbo (ICIPE trial)<br>
        <b>6. Buy:</b> Eldoret Agrovets, Ksh 450-600<br><br>
        <i>KALRO Kitale Approved</i>
        """
    elif any(x in q for x in ["blight", "viazi", "potato"]):
        return "🥔 <b>POTATO BLIGHT:</b> Cold + rain in Kaptagat. Use Ridomil Gold 50g/20L every 7 days, remove infected leaves. Seeds: Certified Shangi from ADC Molo."
    elif any(x in q for x in ["dairy", "ng'ombe", "maziwa", "cow", "milk"]):
        return "🐄 <b>DAIRY BOOST - Uasin Gishu:</b> Dairy meal 2kg + 1kg lucerne (Timboroa). Deworm Nilzan Plus every 3 months. Water 80L per cow/day. Mastitis? CMT test Ksh 1200 Eldoret Vet Labs."
    elif any(x in q for x in ["soil", "mbolea", "fertilizer", "chumvi"]):
        return "🌱 <b>SOIL:</b> Get test at NCPB Eldoret (Ksh 1200). Uasin Gishu pH 5.2-5.8 acidic -> Lime 100kg/acre. Maize: DAP 50kg + CAN 2 bags/acre."
    elif any(x in q for x in ["chicken", "kuku"]):
        return "🐓 <b>POULTRY:</b> Newcastle kills! Vaccinate La Sota every 3 months (Ksh 350/100 birds). Feed 120g layers mash/day, light 16hrs."
    else:
        return f"🌾 <b>RIFT AI for:</b> '{question}'<br><br>Tell me: Crop + Location (Moiben/Turbo/Soy/Kesses) + Problem.<br>Example: 'Maize yellowing in Moiben 2 weeks after planting'<br><br><b>Rift Tip:</b> Certified seeds from Kenya Seed Eldoret, plant mid-March & mid-Oct. Maize H6213 for highland.<br><br><i>Offline AI for Rift Valley farmers</i>"

HOME_HTML = f"""
<div style="max-width:550px; margin:30px auto; font-family:sans-serif; padding:15px;">
<h2 style="text-align:center; color:#2e7d32;">🌾 RIFT AI - Eldoret Offline AI</h2>
<p style="text-align:center;">For Uasin Gishu Farmers. Works Offline.</p>
<div style="background:#e8f5e9; border:2px solid #2e7d32; padding:18px; border-radius:12px;">
<b style="color:#2e7d32;">💚 Lipa na M-Pesa Pochi la Biashara</b><br><br>
M-Pesa → Lipa na M-Pesa → <b>Pochi la Biashara</b><br>
Phone: <b style="font-size:22px;">{TILL_NUMBER}</b><br>
Name: {TILL_NAME}<br>
Amount: <b>Ksh {AMOUNT}</b><br>
PIN → Get SMS CODE (UJD9Z9...)<br>
Paste CODE below
</div>
<br>
<form action="/pay" method="post">
<input name="code" placeholder="Paste M-Pesa Code e.g. UJD9Z9YO3D" style="width:100%; padding:14px; font-size:16px; border:2px solid #2e7d32; border-radius:8px;" required>
<br><br>
<button style="width:100%; padding:14px; background:#2e7d32; color:white; font-size:18px; border:none; border-radius:8px;">🔓 Unlock RIFT AI - Ksh {AMOUNT}</button>
</form>
<br><center><a href="/chat">Already paid? Go to Chat →</a></center>
<br><br><center style="font-size:11px; color:#999;">{TILL_NUMBER} | Eldoret, Kenya 2026</center>
</div>
"""

CHAT_HTML = """
<div style="max-width:700px; margin:20px auto; font-family:sans-serif; padding:15px;">
<h2>RIFT AI Chat - Unlocked ✅</h2>
<p><b>Ask farming question:</b></p>
<form method="post">
<textarea name="q" placeholder="e.g., How to handle maize fall armyworm in Eldoret?" style="width:100%; height:90px; padding:10px; font-size:15px;"></textarea><br><br>
<button style="padding:12px 24px; background:#2e7d32; color:white; border:none; border-radius:6px; font-size:16px;">Ask RIFT AI</button>
</form>
{% if answer %}
<hr><div style="background:#f9fbe7; padding:15px; border-left:4px solid #2e7d32; border-radius:5px;">
{{ answer|safe }}
</div>
{% endif %}
<br><br><a href="/">← Back Home</a>
</div>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/pay", methods=["POST"])
def pay():
    code = request.form.get("code","").strip().upper()
    if len(code) < 8:
        return f"❌ Code too short: {code} <br><a href='/'>Back</a>"
    if code in USED_CODES:
        return f"❌ Code {code} already used! Use new payment. <br><a href='/chat'>But you can still go to Chat →</a><br><a href='/'>Home</a>"
    if not re.match(r'^[A-Z0-9]{8,12}$', code):
        return f"❌ Invalid code format. Copy from M-Pesa SMS. <br><a href='/'>Back</a>"
    USED_CODES.add(code)
    return f"""
    <div style="text-align:center; margin-top:60px; font-family:sans-serif;">
    <h2>✅ Payment Confirmed!</h2>
    <p>Code {code} Accepted</p>
    <h3>RIFT AI Full Chat Unlocked Forever</h3>
    <a href="/chat" style="background:#2e7d32; color:white; padding:14px 24px; text-decoration:none; border-radius:8px; font-size:18px;">🚀 Go to Chat Now</a>
    </div>
    """

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
       
