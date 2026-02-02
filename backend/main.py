from flask import Blueprint, render_template, request, jsonify
import time

main = Blueprint('main', __name__)

# ==========================================
# 1. DISEASE DATABASE
# ==========================================
DISEASE_DB = {
    "rice": {
        "blast": {
            "en": {
                "name": "Rice Blast",
                "symptoms": "Spindle-shaped spots with gray or white centers on leaves.",
                "chemical": "Spray Tricyclazole 75 WP @ 0.6 g/l.",
                "organic": "Treat seeds with Pseudomonas fluorescens."
            },
            "te": {
                "name": "అగ్గి తెగులు (Rice Blast)",
                "symptoms": "ఆకులపై బూడిద లేదా తెలుపు మధ్యలో ఉన్న మచ్చలు.",
                "chemical": "ట్రైసైక్లోజోల్ 75 WP @ 0.6 గ్రా/లీ పిచికారీ చేయాలి.",
                "organic": "విత్తన శుద్ధి సుడోమోనాస్ ఫ్లోరోసెన్స్ తో చేయాలి."
            }
        },
        "brown_spot": {
            "en": {
                "name": "Brown Spot",
                "symptoms": "Round to oval dark brown spots on leaves.",
                "chemical": "Spray Mancozeb @ 2.5g/liter.",
                "organic": "Hot water treatment of seeds."
            },
            "te": {
                "name": "గోధుమ మచ్చ తెగులు",
                "symptoms": "ఆకులపై గుండ్రని ముదురు గోధుమ రంగు మచ్చలు.",
                "chemical": "మాంకోజెబ్ @ 2.5 గ్రా/లీటర్ నీటిలో కలిపి పిచికారీ చేయాలి.",
                "organic": "విత్తనాలను వేడి నీటిలో శుద్ధి చేయాలి."
            }
        }
    },
    "cotton": {
        "bollworm": {
             "en": {
                "name": "Pink Bollworm",
                "symptoms": "Rosette flowers, holes in bolls.",
                "chemical": "Spray Profenofos 50 EC @ 2ml/liter.",
                "organic": "Install Pheromone traps @ 5/acre."
            },
            "te": {
                "name": "గులాబీ రంగు పురుగు",
                "symptoms": "పువ్వులు ముడుచుకుపోవడం, కాయలకు రంధ్రాలు.",
                "chemical": "ప్రొఫెనోఫాస్ 50 EC @ 2ml/లీటర్ పిచికారీ చేయాలి.",
                "organic": "ఎకరానికి 5 లింగాకర్షక బుట్టలను అమర్చాలి."
            }
        }
    }
}

# ==========================================
# 2. CROP ROADMAP DATABASE
# ==========================================
CROP_ROADMAP_DB = {
    "rice": {
        "name_en": "Rice", "name_te": "వరి",
        "soil_type_en": "Clayey / Loamy", "soil_type_te": "బంకమట్టి / ఒండ్రు మట్టి",
        "sowing_season_en": "June - July (Kharif)", "sowing_season_te": "జూన్ - జులై (ఖరీఫ్)",
        "crop_cycle_days": "120-150",
        "roadmap": [
            {"week_range": "0-2", "stage_en": "Sowing & Nursery", "stage_te": "నారుమడి దశ", "fertilizer_en": "FYM + DAP", "fertilizer_te": "పశువుల ఎరువు + డి.ఎ.పి", "irrigation_en": "Light irrigation", "irrigation_te": "తేలికపాటి తడి"},
            {"week_range": "3-5", "stage_en": "Transplanting", "stage_te": "నాట్లు వేయుట", "fertilizer_en": "Urea + Zinc", "fertilizer_te": "యూరియా + జింక్", "irrigation_en": "Maintain 2-3cm water", "irrigation_te": "2-3 సెం.మీ నీరు ఉంచాలి"},
            {"week_range": "6-9", "stage_en": "Tillering Stage", "stage_te": "పిలక దశ", "fertilizer_en": "Urea (Top Dressing)", "fertilizer_te": "యూరియా (పైపాటు)", "irrigation_en": "Continuous flow", "irrigation_te": "నిరంతర ప్రవాహం"},
            {"week_range": "10-12", "stage_en": "Panicle Initiation", "stage_te": "అంకుర దశ", "fertilizer_en": "Potash + Urea", "fertilizer_te": "పొటాష్ + యూరియా", "irrigation_en": "Critical stage", "irrigation_te": "కీలక దశ - నీరు అవసరం"},
            {"week_range": "13-16", "stage_en": "Harvesting", "stage_te": "కోత దశ", "fertilizer_en": "None", "fertilizer_te": "అవసరం లేదు", "irrigation_en": "Drain water 10 days before", "irrigation_te": "10 రోజుల ముందు నీరు తీసివేయాలి"}
        ]
    },
    "cotton": {
        "name_en": "Cotton", "name_te": "పత్తి",
        "soil_type_en": "Black Soil", "soil_type_te": "నల్లరేగడి నేల",
        "sowing_season_en": "May - June", "sowing_season_te": "మే - జూన్",
        "crop_cycle_days": "150-180",
        "roadmap": [
            {"week_range": "0-2", "stage_en": "Sowing", "stage_te": "విత్తడం", "fertilizer_en": "DAP + Potash", "fertilizer_te": "డి.ఎ.పి + పొటాష్", "irrigation_en": "Pre-sowing irrigation", "irrigation_te": "విత్తే ముందు తడి"},
            {"week_range": "3-5", "stage_en": "Vegetative Growth", "stage_te": "ఏపుగా పెరిగే దశ", "fertilizer_en": "Urea", "fertilizer_te": "యూరియా", "irrigation_en": "If needed", "irrigation_te": "అవసరమైతే"},
            {"week_range": "6-9", "stage_en": "Square Formation", "stage_te": "మొగ్గ తొడిగే దశ", "fertilizer_en": "Magnesium Sulphate", "fertilizer_te": "మెగ్నీషియం సల్ఫేట్", "irrigation_en": "Light irrigation", "irrigation_te": "తేలికపాటి తడి"},
            {"week_range": "10-14", "stage_en": "Flowering & Boll", "stage_te": "పూత & కాయ దశ", "fertilizer_en": "Urea + Potash", "fertilizer_te": "యూరియా + పొటాష్", "irrigation_en": "Critical - Moderate", "irrigation_te": "కీలక దశ - తగు మోతాదులో"},
            {"week_range": "15-20", "stage_en": "Boll Bursting", "stage_te": "కాయ పగిలే దశ", "fertilizer_en": "None", "fertilizer_te": "అవసరం లేదు", "irrigation_en": "Stop irrigation", "irrigation_te": "నీరు ఆపివేయాలి"}
        ]
    },
    "maize": {
        "name_en": "Maize", "name_te": "మొక్కజొన్న",
        "soil_type_en": "Red Loamy / Sandy Loam", "soil_type_te": "ఎర్ర నేలలు / ఇసుక కలిసిన ఒండ్రు",
        "sowing_season_en": "June - July", "sowing_season_te": "జూన్ - జులై",
        "crop_cycle_days": "90-110",
        "roadmap": [
            {"week_range": "0-1", "stage_en": "Sowing", "stage_te": "విత్తడం", "fertilizer_en": "DAP + Zinc", "fertilizer_te": "డి.ఎ.పి + జింక్", "irrigation_en": "Immediate", "irrigation_te": "వెంటనే"},
            {"week_range": "3-4", "stage_en": "Knee High Stage", "stage_te": "మోకాలి ఎత్తు దశ", "fertilizer_en": "Urea", "fertilizer_te": "యూరియా", "irrigation_en": "Light", "irrigation_te": "తేలికపాటి"},
            {"week_range": "5-7", "stage_en": "Tasseling (Flowering)", "stage_te": "పూత దశ", "fertilizer_en": "Urea + Potash", "fertilizer_te": "యూరియా + పొటాష్", "irrigation_en": "Critical", "irrigation_te": "అత్యవసరం"},
            {"week_range": "8-10", "stage_en": "Grain Filling (Silking)", "stage_te": "గింజ పాలుపోసుకునే దశ", "fertilizer_en": "None", "fertilizer_te": "అవసరం లేదు", "irrigation_en": "Essential", "irrigation_te": "తప్పనిసరి"},
            {"week_range": "12-14", "stage_en": "Harvesting", "stage_te": "కోత దశ", "fertilizer_en": "None", "fertilizer_te": "అవసరం లేదు", "irrigation_en": "Stop 1 week before", "irrigation_te": "వారం ముందు ఆపాలి"}
        ]
    },
    "groundnut": {
        "name_en": "Groundnut", "name_te": "వేరుశనగ",
        "soil_type_en": "Sandy Loam", "soil_type_te": "ఇసుక నేలలు",
        "sowing_season_en": "May - June", "sowing_season_te": "మే - జూన్",
        "crop_cycle_days": "100-120",
        "roadmap": [
            {"week_range": "0-1", "stage_en": "Sowing", "stage_te": "విత్తడం", "fertilizer_en": "Gypsum + DAP", "fertilizer_te": "జిప్సం + డి.ఎ.పి", "irrigation_en": "Pre-sowing", "irrigation_te": "విత్తే ముందు"},
            {"week_range": "3-4", "stage_en": "Vegetative", "stage_te": "పెరుగుదల దశ", "fertilizer_en": "None", "fertilizer_te": "అవసరం లేదు", "irrigation_en": "Avoid water stress", "irrigation_te": "నీటి ఎద్దడి లేకుండా చూడాలి"},
            {"week_range": "5-7", "stage_en": "Flowering & Pegging", "stage_te": "పూత & ఊడ దిగే దశ", "fertilizer_en": "Gypsum (Earthing up)", "fertilizer_te": "జిప్సం (మట్టి ఎగదోయాలి)", "irrigation_en": "Critical", "irrigation_te": "అత్యవసరం"},
            {"week_range": "8-11", "stage_en": "Pod Formation", "stage_te": "కాయ ఊరే దశ", "fertilizer_en": "Potash", "fertilizer_te": "పొటాష్", "irrigation_en": "Moist soil", "irrigation_te": "తేమ ఉండాలి"},
            {"week_range": "13-15", "stage_en": "Harvesting", "stage_te": "త్రవ్వకం", "fertilizer_en": "None", "fertilizer_te": "అవసరం లేదు", "irrigation_en": "Light irrigation before harvest", "irrigation_te": "త్రవ్వే ముందు తేలికపాటి తడి"}
        ]
    },
    "tomato": {
        "name_en": "Tomato", "name_te": "టమాటా",
        "soil_type_en": "Red Loam / Black Soil", "soil_type_te": "ఎర్ర గరప / నల్లరేగడి",
        "sowing_season_en": "August - September", "sowing_season_te": "ఆగస్టు - సెప్టెంబర్",
        "crop_cycle_days": "110-140",
        "roadmap": [
            {"week_range": "0-3", "stage_en": "Nursery", "stage_te": "నారుమడి", "fertilizer_en": "Cocopeat/FYM", "fertilizer_te": "కొబ్బరి పొట్టు/ఎరువు", "irrigation_en": "Daily Sprinkling", "irrigation_te": "రోజువారీ పిచికారీ"},
            {"week_range": "4-5", "stage_en": "Transplanting", "stage_te": "నాట్లు", "fertilizer_en": "DAP + Neem Cake", "fertilizer_te": "డి.ఎ.పి + వేప పిండి", "irrigation_en": "Immediate", "irrigation_te": "వెంటనే"},
            {"week_range": "6-8", "stage_en": "Flowering", "stage_te": "పూత దశ", "fertilizer_en": "NPK 19:19:19", "fertilizer_te": "ఎన్.పి.కె 19:19:19", "irrigation_en": "Regular interval", "irrigation_te": "క్రమం తప్పకుండా"},
            {"week_range": "9-12", "stage_en": "Fruiting", "stage_te": "కాయ దశ", "fertilizer_en": "Calcium Nitrate", "fertilizer_te": "కాల్షియం నైట్రేట్", "irrigation_en": "Avoid excess", "irrigation_te": "అధిక నీరు వద్దు"},
            {"week_range": "13-16", "stage_en": "Harvesting", "stage_te": "కోత", "fertilizer_en": "None", "fertilizer_te": "అవసరం లేదు", "irrigation_en": "As needed", "irrigation_te": "అవసరాన్ని బట్టి"}
        ]
    },
    "sugarcane": {
        "name_en": "Sugarcane", "name_te": "చెరకు",
        "soil_type_en": "Deep Loamy", "soil_type_te": "లోతైన ఒండ్రు నేల",
        "sowing_season_en": "Jan - March", "sowing_season_te": "జనవరి - మార్చి",
        "crop_cycle_days": "300-360 (1 Year)",
        "roadmap": [
            {"week_range": "0-4", "stage_en": "Planting & Germination", "stage_te": "నాటడం & మొలకెత్తడం", "fertilizer_en": "DAP + Zinc", "fertilizer_te": "డి.ఎ.పి + జింక్", "irrigation_en": "Frequent", "irrigation_te": "తరచుగా"},
            {"week_range": "5-12", "stage_en": "Tillering (Formative)", "stage_te": "పిలక దశ", "fertilizer_en": "Urea (Split doses)", "fertilizer_te": "యూరియా (విడతలవారీగా)", "irrigation_en": "Every 10 days", "irrigation_te": "10 రోజులకు ఒకసారి"},
            {"week_range": "13-24", "stage_en": "Grand Growth", "stage_te": "ఏపుగా పెరిగే దశ", "fertilizer_en": "Urea + Potash", "fertilizer_te": "యూరియా + పొటాష్", "irrigation_en": "Heavy irrigation", "irrigation_te": "ఎక్కువ నీరు అవసరం"},
            {"week_range": "25-36", "stage_en": "Maturity", "stage_te": "పక్వ దశ", "fertilizer_en": "Stop Nitrogen", "fertilizer_te": "నత్రజని ఆపాలి", "irrigation_en": "Reduce frequency", "irrigation_te": "తగ్గించాలి"},
            {"week_range": "40+", "stage_en": "Harvesting", "stage_te": "గానుగ కోత", "fertilizer_en": "None", "fertilizer_te": "అవసరం లేదు", "irrigation_en": "Stop 1 month before", "irrigation_te": "నెల ముందు ఆపాలి"}
        ]
    },
    "chilli": {
        "name_en": "Chilli", "name_te": "మిరప",
        "soil_type_en": "Black / Loamy", "soil_type_te": "నల్లరేగడి / ఒండ్రు",
        "sowing_season_en": "July - August", "sowing_season_te": "జూలై - ఆగస్టు",
        "crop_cycle_days": "150-180",
        "roadmap": [
            {"week_range": "0-4", "stage_en": "Nursery", "stage_te": "నారుమడి", "fertilizer_en": "FYM", "fertilizer_te": "పశువుల ఎరువు", "irrigation_en": "Regular sprinkling", "irrigation_te": "క్రమం తప్పకుండా"},
            {"week_range": "5-6", "stage_en": "Transplanting", "stage_te": "నాట్లు", "fertilizer_en": "DAP", "fertilizer_te": "డి.ఎ.పి", "irrigation_en": "Immediate", "irrigation_te": "వెంటనే"},
            {"week_range": "8-12", "stage_en": "Flowering", "stage_te": "పూత దశ", "fertilizer_en": "NPK + Micronutrients", "fertilizer_te": "సూక్ష్మ పోషకాలు", "irrigation_en": "Maintain moisture", "irrigation_te": "తేమ ఉంచాలి"},
            {"week_range": "13-20", "stage_en": "Fruiting & Picking", "stage_te": "కాయ & కోత", "fertilizer_en": "Potash (for color)", "fertilizer_te": "పొటాష్ (రంగు కోసం)", "irrigation_en": "Regular", "irrigation_te": "క్రమం తప్పకుండా"}
        ]
    }
}


# ==========================================
# 3. PAGE ROUTES
# ==========================================
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/disease/input')
def disease_input_page():
    return render_template('disease_input.html')

@main.route('/shops/finder')
def shop_finder_page():
    return render_template('shop_finder.html')

@main.route("/crop/recommend")
def crop_recommend():
    return render_template("crop_recommend.html")

@main.route('/crop/<string:crop_name>')
def crop_roadmap_page(crop_name):
    # Sends the crop name (e.g. "rice") to the HTML template
    return render_template('crop_roadmap.html', crop=crop_name.lower())

@main.route('/contact')
def contact_support():
    return render_template('contact.html')


# ==========================================
# 4. API ROUTES
# ==========================================

# 4.1. Disease Identification API
@main.route('/api/disease/identify', methods=['POST'])
def identify_disease():
    try:
        time.sleep(1.5)
        crop = request.form.get('crop')
        input_type = request.form.get('type')
        input_data = request.form.get('data', '').lower()
        file = request.files.get('file')
        result_key = None
        confidence = 0

        # MOCK LOGIC for Disease
        if input_type == 'image' and file:
            if crop == 'rice':
                result_key = 'blast'; confidence = 88
            elif crop == 'cotton':
                result_key = 'bollworm'; confidence = 92
            else:
                return jsonify({
                    "success": True, "confidence": 75,
                    "en": {"name": f"Potential {crop.title()} Disease", "symptoms": "Visual abnormalities.", "chemical": "Consult expert.", "organic": "Neem oil."},
                    "te": {"name": f"సాధ్యమయ్యే {crop} తెగులు", "symptoms": "దృశ్య లోపాలు.", "chemical": "నిపుణుడిని సంప్రదించండి.", "organic": "వేప నూనె."}
                })
        else:
            if crop == 'rice':
                result_key = 'brown_spot' if 'brown' in input_data else 'blast'
                confidence = 80
            elif crop == 'cotton':
                result_key = 'bollworm'
                confidence = 90
            else:
                return jsonify({
                    "success": True, "confidence": 70,
                    "en": {"name": "General Deficiency", "symptoms": "Nutrient deficiency.", "chemical": "NPK.", "organic": "Compost."},
                    "te": {"name": "పోషక లోపం", "symptoms": "పోషకాల లోపం.", "chemical": "NPK.", "organic": "కంపోస్ట్."}
                })

        if result_key and result_key in DISEASE_DB.get(crop, {}):
            data = DISEASE_DB[crop][result_key]
            return jsonify({"success": True, "confidence": confidence, "en": data['en'], "te": data['te']})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

    return jsonify({"success": False, "error": "Unknown error"})


# 4.2. Crop Roadmap API
@main.route('/api/crop/<string:crop_name>', methods=['GET'])
def get_crop_roadmap(crop_name):
    crop_name = crop_name.lower()
    
    # Check if we have data for this crop
    if crop_name in CROP_ROADMAP_DB:
        return jsonify(CROP_ROADMAP_DB[crop_name])
    
    # Fallback if crop not found (e.g. Onion, Sunflower which are in dropdown but not in DB)
    return jsonify({
        "error": "Crop not found",
        "name_en": crop_name.title(),
        "name_te": crop_name.title(),
        "soil_type_en": "General Soil", "soil_type_te": "సాధారణ నేల",
        "sowing_season_en": "Any Season", "sowing_season_te": "ఏ సీజన్ అయినా",
        "crop_cycle_days": "N/A",
        "roadmap": []
    })