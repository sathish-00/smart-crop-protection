from flask import Blueprint, request, jsonify

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/api/recommend_crop", methods=["POST"])
def recommend_crop():
    data = request.get_json()

    soil = data.get("soil")
    season = data.get("season")
    water = data.get("water")
    budget = data.get("budget")
    lang = data.get("lang", "en")

    # ✅ Rule-based recommendation (Telugu states major crops)
    crops = []

    def add_crop(en, te, slug, score, reason_en, reason_te):
        crops.append({
            "crop": te if lang == "te" else en,
            "crop_slug": slug,
            "score": score,
            "reason": reason_te if lang == "te" else reason_en
        })

    # ✅ Some strong AP/TS rules (extend later)
    if season == "kharif":
        if soil in ["black", "red"] and water in ["borewell", "canal"]:
            add_crop("Cotton", "పత్తి", "cotton", 95,
                     "Good for Kharif with irrigation in black/red soils.",
                     "నల్ల/ఎర్ర నేలల్లో ఖరీఫ్‌లో సాగు నీరు ఉంటే పత్తికి అనుకూలం.")
        if water in ["canal", "rainfed"]:
            add_crop("Rice", "వరి", "rice", 90,
                     "Rice performs well in Kharif with rainfall/canal water.",
                     "ఖరీఫ్‌లో వర్షాధార/కాలువ నీటితో వరి బాగా పెరుగుతుంది.")
        add_crop("Maize", "మొక్కజొన్న", "maize", 80,
                 "Maize is suitable for many soils in Kharif season.",
                 "ఖరీఫ్‌లో చాలానేలలకు మొక్కజొన్న సరిపోతుంది.")

    if season == "rabi":
        if water in ["borewell", "drip"]:
            add_crop("Chilli", "మిరప", "chilli", 90,
                     "Chilli gives good output in Rabi with controlled irrigation.",
                     "రబీలో నియంత్రిత నీటితో మిరప బాగా వస్తుంది.")
            add_crop("Tomato", "టమాటా", "tomato", 85,
                     "Tomato suits Rabi with borewell/drip water.",
                     "రబీలో బోరుబావి/డ్రిప్‌తో టమాటా అనుకూలం.")
        add_crop("Bengal Gram", "శనగ", "bengalgram", 78,
                 "Bengal gram is common in Rabi under moderate water.",
                 "రబీలో మితమైన నీటితో శనగ పంట సాధారణం.")

    if season == "summer":
        if water in ["drip", "borewell"]:
            add_crop("Watermelon", "పుచ్చకాయ", "watermelon", 88,
                     "Summer watermelon needs reliable irrigation.",
                     "వేసవిలో పుచ్చకాయకు నమ్మకమైన నీటి వనరు అవసరం.")
            add_crop("Sunflower", "సూర్యకాంతి", "sunflower", 75,
                     "Sunflower can grow in summer with irrigation.",
                     "నీరు ఉంటే వేసవిలో సూర్యకాంతి సాగు చేయచ్చు.")

    # ✅ Budget filter (simple scoring adjust)
    if budget == "low":
        for c in crops:
            c["score"] -= 5
    elif budget == "high":
        for c in crops:
            c["score"] += 3

    # sort top first
    crops = sorted(crops, key=lambda x: x["score"], reverse=True)

    return jsonify({"recommended": crops[:6]})
