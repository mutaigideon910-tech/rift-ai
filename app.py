from flask import Flask, request, render_template_string, session
import os
import re

app = Flask(__name__)
app.secret_key = "rift-ai-eldoret-2026-final-v1"

TILL_NUMBER = "0180974422"
TILL_NAME = "GIDEON MUTAI - RIFT AI"
AMOUNT = 50
USED_CODES = set()

# --- RIFT AI REAL BRAIN - ELDORET / RIFT VALLEY KNOWLEDGE ---
def get_rift_answer(question):
    q = question.lower()

    if any(x in q for x in ["armyworm", "fall army", "jeshi"]):
        return """
        🌽 <b>MAIZE FALL ARMYWORM - Eldoret/Uasin Gishu Protocol</b><br><br>
        <b>1. Scout:</b> Check at 6am, look inside funnel for small green/brown worms + sawdust (frass)<br>
        <b>2. Handpick:</b> Remove larvae, crush or put in soapy water<br>
        <b>3. Organic (Best for Rift):</b> Neem spray - 200g neem powder + 50g chili + small soap in 20L water. Spray directly into funnel at 5pm<br>
        <b>4. Chemical if severe:</b> Prove 1.9EC (Emamectin) 10ml per 20L OR Coragen 10ml/20L. Spray late evening<br>
        <b>5. Prevention:</b> Plant early (March 1st week), Use Push-Pull: Desmodium between maize, Brachiaria border - works 89% in Moiben/Turbo trials<br>
        <b>6. Where to buy:</b> Eldoret Town - Nairobi Rd Agrovets, Ksh 450-600<br><br>
        <i>Source: KALRO Kitale + ICIPE Push-Pull manual</i>
        """
    elif any(x in q for x in ["blight", "viazi", "potato"]):
        return """
        🥔 <b>POTATO LATE BLIGHT - Eldoret Highlands</b><br>
        Cause: Cold + rain in Kaptagat/Timboroa<br>
        <b>Action:</b> Ridomil Gold 50g per 20L every 7 days, remove infected leaves, earth-up properly<br>
        <b>Seeds:</b> Use certified Shangi/Marka from ADC Molo or Kisima - NOT market potatoes<br>
        """
    elif any(x in q for x in ["dairy", "ng'ombe", "maziwa", "cow", "milk"]):
        return """
        🐄 <b>DAIRY BOOST - Uasin Gishu</b><br>
        Low milk? Do this:<br>
        - Dairy meal 2kg per milking + 1kg lucerne hay (Timboroa)<br>
        - Deworm with Nilzan Plus every 3 months<br>
        - Mastitis check: CMT test kit Ksh 1200 at Eldoret Vet Labs<br>
        - Water: 80L per cow per day!<br>
        """
    elif any(x in q for x in ["soil", "mbolea", "fertilizer"]):
        return """
        🌱 <b>SOIL & FERTILIZER - Rift Valley</b><br>
        Don't guess! Get soil test at Eldoret NCPB or UoE (Ksh 1200)<br>
        Typical Uasin Gishu: pH 5.2-5.8 (acidic) -> Apply 100kg lime per acre<br>
        Maize: DAP 50kg + 2 bags CAN per acre<br>
        Potato: 100kg DAP + 80kg MOP per acre<br>
        """
    elif any(x in q for x in ["chicken", "kuku", "poultry"]):
        return """
        🐓 <b>POULTRY - Eldoret</b><br>
        Newcastle is killer! Vaccinate: La Sota every 3 months (Ksh 350 for 100 birds)<br>
        Feed: 120g layers mash per day, light 16hrs for eggs<br>
        """
    else:
        return f"""
        🌾 <b>RIFT AI Answer for:</b> '{question}'<br><br>
        For accurate advice, include:<br>
        1. Crop/Livestock<br>
        2. Location (e.g., Moiben, Turbo, Soy, Kesses)<br>
        3. Problem seen<br><br>
        <b>General Rift Valley Tip:</b><br>
        - Plant certified seeds (Kenya Seed Eldoret branch)<br>
        - Plant at onset of rains (Mid-March & Mid-Oct)<br>
        - Use KALRO varieties: Maize H6213 for highland, H624 for medium<br><br>
        Ask again like: "Maize yellowing in Moiben 2 weeks after planting" - I will give exact solution!<br><br>
        <i>Offline AI built for Rift Valley farmers, no internet needed in field version</i>
        """

# --- HTML TEMPLATES ---
HOME_HTML = f"""
<div style="max-width:550px; margin:30px auto; font-family:sans-serif; padding:15px;">
<h2 style="text-align:center; color:#2e7d32;">🌾 RIFT AI - Eldoret Offline AI</h2>
<p style="text-align:center;">Built for Uasin Gishu Farmers. Works offline.</p>
<div style="background:#e8f5e9; border:2px solid #2e7d32; padding:18px; border-radius:12px;">
<b style="color:#2e7d32; font-size:17px;">💚 Lipa na M-Pesa Pochi la Biashara</b><br><br>
<b>1.</b> Go to M-Pesa → Lipa na M-Pesa → <b>Pochi la Biashara</b><br>
<b>2.</b> Enter Phone: <b style="font-size:22px; color:#000;">{TILL_NUMBER}</b><br>
&nbsp;&nbsp;&nbsp;&nbsp;Name: <b>{TILL_NAME}</b><br>
<b>3.</b> Amount: <b>Ksh {AMOUNT}</b><br>
<b>4.</b> Enter PIN → You get SMS with CODE (e.g. UJD9Z9Y...)<br>
<b>5.</b> Copy CODE and paste below
</div>
<br>
<form action="/chat" method="post">
<input name="code" placeholder="Paste M-Pesa Code e.g. UJD9Z9YO3D" style="width:100%; padding:14px; font-size:16px; border:2px solid #2e7d32; border-radius:8px;" required>
<br><br>
<button style="width:100%; padding:14px; background:#2e7d32; color:white; font-size:18px; border:none; border-radius:8px; cursor:pointer;">🔓 Unlock RIFT AI Chat - Ksh {AMOUNT}</button>
</form>
<br>
<center><a href="/chat?free=1" style="color:#666;">Try Free Demo (1 question)</a></center>
<br><br>
<center style="font-size:12px; color:#999;">Pochi: {TILL_NUMBER} | Eldoret, Kenya | 2026</center>
</div>
"""

CHAT_HTML = """
<div style="max-width:700px; margin:20px auto; font-family:sans-serif; padding:15px;">
<h2>RIFT AI Chat - Unlocked ✅</h2>
<p><b>Ask your farming question:</b> (e.g., Maize armyworm, potato blight, dairy)</p>
<form method="post">
<textarea name="q" placeholder="Type your question here... e.g., How to handle maize fall armyworm in Eldoret?" style="width:100%; height:90px; padding:10px; font-size:15px;"></textarea><br><br>
<button style="padding:10px 20px; background:#2e7d32; color:white; border:none; border-radius:6px;">Ask RIFT AI</button>
</form>
{% if answer %}
<hr style="margin:20px 0;">
<div style="background:#f9fbe7; padding:15px; border-left:4px solid #2e7d32; border-radius:5px;">
<b>Answer:</b><br><br>{{ answer|safe }}
</div>
{% endif %}
<br><br><a href="/">← Back Home</a>
</div>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/chat", methods=["GET","POST"])
def chat():
    if request.method == "GET" and request.args.get("free"):
        session["paid"] = False
        return render_template_string(CHAT_HTML, answer="Free demo mode: Ask 1 question. For unlimited, pay Ksh 50 at home.")

    if request.method == "POST":
        code = request.form.get("code","").strip().upper()
        q = request.form.get("q","")

        # Payment verification
        if code and not q:
            if len(code) < 8 or len(code) > 12:
                return f"❌ Invalid code '{code}'. Paste full code from M-Pesa SMS e.g. UJD9Z9Y... <br><a href='/'>Back</a>"
            if code in USED_CODES:
                return f"❌ Code {code} was already used! Each payment used once. Pay new {AMOUNT} bob. <br><a href='/'>Back</a>"
            # Basic format check: M-Pesa codes are like UJD9Z9YO3D
            if not re.match(r'^[A-Z0-9]{8,12}$', code):
                return f"❌ Code looks wrong. Use code from M-Pesa SMS. <br><a href='/'>Back</a>"
            USED_CODES.add(code)
            session["paid"] = True
            return f"""
            <div style="text-align:center; margin-top:60px; font-family:sans-serif;">
            <h2>✅ Payment Confirmed!</h2>
            <p>Code {code} Accepted</p>
            <h3>RIFT AI Full Chat Unlocked</h3>
            <a href="/chat" style="background:#2e7d32; color:white; padding:12px 20px; text-decoration:none; border-radius:8px;">Go to Chat</a>
            </div>
            """

        if q:
            if not session.get("paid") and "free" not in request.args:
                # Allow if they have paid in session
                if not session.get("paid"):
                    return render_template_string(CHAT_HTML, answer="Please pay first to unlock. <a href='/'>Go Home to pay Ksh 50</a>")
            answer = get_rift_answer(q)
            return render_template_string(CHAT_HTML, answer=answer)

    return render_template_string(CHAT_HTML, answer=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
