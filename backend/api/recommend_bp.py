from flask import Blueprint, request, jsonify

recommend_bp = Blueprint("recommend_bp", __name__)

@recommend_bp.route("/api/recommend_crop", methods=["POST"])
def recommend_crop():
    """
    Input JSON:
    {
      "soil": "black/red/sandy/alluvial/clay",
      "season": "kharif/rabi/summer",
      "water": "rainfed/borewell/canal/drip",
      "budget": "low/medium/high",
      "lang": "en/te"
    }
    """

    data = request.get_json() or {}

    soil = data.get("soil", "")
    season = data.get("season", "")
    water = data.get("water", "")
    budget = data.get("budget", "")
    lang = data.get("lang", "en")  # en default

    recommended = []

    # ✅ helper function
    def add_crop(en_name, te_name, slug, score, reason_en, reason_te):
        recommended.append({
            "crop": te_name if lang == "te" else en_name,
            "crop_slug": slug.lower(),  # ✅ always lowercase slug
            "score": score,
            "reason": reason_te if lang == "te" else reason_en
        })

    # ✅ Telugu states major crops rules (AP + TS)
    # =========================================================

    # 🌧️ KHARIF
    if season == "kharif":
        # Paddy
        if water in ["canal", "rainfed"]:
            add_crop(
                "Rice (Paddy)", "వరి", "rice",
                92,
                "Best crop for Kharif with rainfall or canal water.",
                "ఖరీఫ్‌లో వర్షం లేదా కాలువ నీరు ఉంటే వరి ఉత్తమం."
            )

        # Cotton
        if soil in ["black", "red"] and water in ["borewell", "canal"]:
            add_crop(
                "Cotton", "పత్తి", "cotton",
                95,
                "Cotton suits Kharif season in black/red soils with irrigation.",
                "నల్ల/ఎర్ర నేలల్లో ఖరీఫ్‌లో సాగునీరు ఉంటే పత్తి బాగా వస్తుంది."
            )

        # Maize
        add_crop(
            "Maize", "మొక్కజొన్న", "maize",
            85,
            "Maize works in Kharif for many soils with moderate water.",
            "ఖరీఫ్‌లో మితమైన నీటితో చాలానేలల్లో మొక్కజొన్న సరిపోతుంది."
        )

        # Groundnut
        if soil in ["sandy", "red"] and water in ["rainfed", "borewell"]:
            add_crop(
                "Groundnut", "వేరుశెనగ", "groundnut",
                83,
                "Groundnut fits sandy/red soils with rainfed or borewell support.",
                "ఇసుక/ఎర్ర నేలల్లో వర్షాధార లేదా బోరుబావి నీటితో వేరుశెనగ సరిపోతుంది."
            )

    # 🌾 RABI
    if season == "rabi":
        # Bengal gram
        add_crop(
            "Bengal Gram (Chana)", "శనగ", "bengalgram",
            80,
            "Chana is common in Rabi with low to medium water use.",
            "రబీలో తక్కువ/మధ్యస్థ నీటితో శనగ సాగు సాధారణం."
        )

        # Chilli
        if water in ["borewell", "drip"]:
            add_crop(
                "Chilli", "మిరప", "chilli",
                90,
                "Chilli gives good results in Rabi with drip/borewell irrigation.",
                "రబీలో డ్రిప్/బోరుబావి నీటితో మిరప బాగా వస్తుంది."
            )

        # Tomato
        if water in ["borewell", "drip"]:
            add_crop(
                "Tomato", "టమాట", "tomato",
                86,
                "Tomato suits Rabi season with controlled irrigation.",
                "రబీలో నియంత్రిత నీటితో టమాట సాగుకు అనుకూలం."
            )

        # Sunflower
        add_crop(
            "Sunflower", "సూర్యకాంతి", "sunflower",
            78,
            "Sunflower is suitable in Rabi for many regions of AP & TS.",
            "ఏపీ & తెలంగాణలో రబీలో సూర్యకాంతి సాగు చేయవచ్చు."
        )

        # Onion
        if water in ["borewell", "drip"]:
            add_crop(
                "Onion", "ఉల్లి", "onion",
                82,
                "Onion performs better in Rabi with good irrigation.",
                "రబీలో మంచి నీటితో ఉల్లి పంట బాగా వస్తుంది."
            )

    # ☀️ SUMMER
    if season == "summer":
        if water in ["drip", "borewell"]:
            add_crop(
                "Watermelon", "పుచ్చకాయ", "watermelon",
                88,
                "Watermelon grows well in summer with reliable irrigation.",
                "వేసవిలో నమ్మకమైన నీటి వనరు ఉంటే పుచ్చకాయ బాగా వస్తుంది."
            )

            add_crop(
                "Muskmelon", "ఖర్బుజా", "muskmelon",
                84,
                "Muskmelon suits summer with drip/borewell support.",
                "డ్రిప్/బోరుబావి నీటితో వేసవిలో ఖర్బుజా సాగుకు అనుకూలం."
            )

            add_crop(
                "Okra (Lady Finger)", "బెండకాయ", "okra",
                75,
                "Okra can be grown in summer with irrigation support.",
                "నీరు ఉంటే వేసవిలో బెండకాయ సాగు చేయవచ్చు."
            )

    # ✅ Budget adjustment (simple)
    if budget == "low":
        for c in recommended:
            c["score"] -= 5
    elif budget == "high":
        for c in recommended:
            c["score"] += 3

    # ✅ Remove duplicates by slug (keep best score)
    unique = {}
    for item in recommended:
        slug = item["crop_slug"]
        if slug not in unique or item["score"] > unique[slug]["score"]:
            unique[slug] = item

    final_list = list(unique.values())
    final_list = sorted(final_list, key=lambda x: x["score"], reverse=True)

    return jsonify({"recommended": final_list[:8]})
