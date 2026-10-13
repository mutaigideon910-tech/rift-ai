# --- RIFT AI OFFLINE KNOWLEDGE BASE (Rift Valley) ---
def get_rift_answer(question):
    q = question.lower()
    if "armyworm" in q or "fall army" in q:
        return """🌽 MAIZE FALL ARMYWORM - ELDORET PROTOCOL:

1. Scouting: Check early morning, look for windowpane damage & frass in funnel
2. Immediate Action: Handpick and destroy larvae (put in soapy water)
3. Organic Spray: Neem + chili spray (100g neem seeds + 50g chili per 20L) - spray funnel
4. Chemical (if severe): Emamectin benzoate (e.g., Prove 1.9EC) or Chlorantraniliprole (Coragen) - 10ml per 20L, spray late afternoon
5. Prevention: Early planting, intercrop with desmodium (push-pull), avoid late planting
6. Eldoret Agrovet: Ask for Escort or Belt - they know it. Cost ~Ksh 450 per 100ml

For your farm in Moiben? Do push-pull - it works 90% in Uasin Gishu."""
    elif "blight" in q or "potato" in q:
        return "🥔 POTATO BLIGHT (Eldoret cold): Use Ridomil Gold 50g/20L, plant certified seeds from ADC Molo, earth up well."
    elif "dairy" in q or "cow" in q or "milk" in q:
        return "🐄 DAIRY - ELDORET: Increase protein with lucerne + dairy meal 2kg/day. Deworm every 3 months. Mastitis? Use CMT test."
    else:
        return f"""🌾 RIFT AI - Eldoret Answer for: '{question}'

Based on KALRO Eldoret & UoEldoret research:

For best results in Uasin Gishu / Rift Valley:
- Soil pH 5.5-6.5 (get test at Eldoret NCPB)
- Use certified seeds
- Early planting at onset of rains (March & Oct)

If you tell me specific crop + location (e.g., Turbo, Moiben, Soy), I give exact variety.

Ask again with more detail!"""

# then in your chat route, replace the answer line with:
# answer = get_rift_answer(q)



