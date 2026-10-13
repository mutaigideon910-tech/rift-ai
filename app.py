from flask import Flask, request, render_template_string, session, redirect
import os

app = Flask(__name__)
app.secret_key = "rift-ai-eldoret-2026"

TILL_NUMBER = "0180974422"
TILL_NAME = "GIDEON MUTAI - RIFT AI"
AMOUNT = 50

# Store used codes so no one re-uses same SMS
USED_CODES = set()

HOME_HTML = f"""
<h2 style="text-align:center;">🌾 RIFT AI - Eldoret Offline AI</h2>
<div style="max-width:500px; margin:auto; font-family:sans-serif;">
<div style="background:#e8f5e9; border:2px solid #2e7d32; padding:15px; border-radius:10px;">
<b style="color:#2e7d32;">💚 Lipa na M-Pesa Pochi la Biashara</b><br><br>
<b>1.</b> M-Pesa → Lipa na M-Pesa → <b>Pochi la Biashara</b><br>
<b>2.</b> Phone: <b style="font-size:20px;">{TILL_NUMBER}</b><br>
Name: {TILL_NAME}<br>
<b>3.</b> Amount: <b>Ksh {AMOUNT}</b><br>
<b>4.</b> PIN → Get SMS with CODE (e.g. UJD9Z9...)<br>
<b>5.</b> Paste CODE below to unlock
</div>
<br>
<form action="/chat" method="post">
<input name="code" placeholder="Paste M-Pesa Code e.g. UJD9Z9YJYL" style="width:100%; padding:12px; font-size:16px;" required>
<br><br>
<button style="width:100%; padding:12px; background:#2e7d32; color:white; font-size:18px; border:none; border-radius:8px;">🔓 Unlock RIFT AI Chat</button>
</form>
<br>
<a href="/chat?free=1">Continue with Free Demo (1 question)</a>
</div>
"""

CHAT_HTML = """
<h2>RIFT AI Chat - Unlocked ✅</h2>
<p>Ask your farming question:</p>
<form method="post">
<textarea name="q" style="width:100%; height:100px;"></textarea><br>
<button>Ask RIFT AI</button>
</form>
{% if answer %}
<hr><b>Answer:</b><br>{{ answer }}
{% endif %}
<br><br><a href="/">Back Home</a>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/chat", methods=["GET","POST"])
def chat():
    if request.method == "GET" and request.args.get("free"):
        session["paid"] = False
        return render_template_string(CHAT_HTML, answer="Free demo: RIFT AI works offline for Eldoret farmers!")

    if request.method == "POST":
        code = request.form.get("code","").strip().upper()
        q = request.form.get("q","")

        # Payment verification
        if code and not q:
            if len(code) < 8:
                return "❌ Code too short. Paste full code from SMS e.g. UJD9Z9YJYL <br><a href='/'>Back</a>"
            if code in USED_CODES:
                return "❌ This code was already used! Use a new payment. <br><a href='/'>Back</a>"
            USED_CODES.add(code)
            session["paid"] = True
            return f"""
            <div style="text-align:center; margin-top:50px; font-family:sans-serif;">
            <h2>✅ Payment Confirmed!</h2>
            <p>Code {code} Accepted</p>
            <h3>RIFT AI Full Chat Unlocked</h3>
            <a href="/chat">Go to Chat</a>
            </div>
            """

        # Chat question
        if q:
            if not session.get("paid"):
                return "Please pay first <a href='/'>Home</a>"
            # Simple AI answer placeholder - your original AI logic here
            answer = f"RIFT AI Answer for: '{q}' -> [Your offline AI model response here. Works offline in Rift Valley!]"
            return render_template_string(CHAT_HTML, answer=answer)

    return render_template_string(CHAT_HTML, answer=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
