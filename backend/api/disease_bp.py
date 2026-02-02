# smart-crop-protection/backend/api/disease_bp.py

from flask import Blueprint, jsonify, request
from backend.extensions import db
from backend.models.disease_model import Disease
from sqlalchemy import or_, and_
import random

# Define the Blueprint object.
disease_bp = Blueprint('disease', __name__)

# Crop-specific disease mapping (this could be expanded with more data)
CROP_DISEASES = {
    'rice': ['blast', 'bacterial blight', 'brown spot', 'sheath blight'],
    'wheat': ['rust', 'powdery mildew', 'septoria', 'scab'],
    'maize': ['corn borer', 'downy mildew', 'rust', 'smut'],
    'cotton': ['bollworm', 'bacterial blight', 'fusarium wilt', 'verticillium wilt'],
    'sugarcane': ['red rot', 'smut', 'rust', 'mosaic'],
    'groundnut': ['leaf spot', 'rust', 'aflatoxin', 'bud necrosis'],
    'soybean': ['rust', 'mosaic', 'pod borer', 'anthracnose'],
    'chickpea': ['fusarium wilt', 'ascochyta blight', 'botrytis gray mold'],
    'mustard': ['alternaria blight', 'white rust', 'downy mildew'],
    'potato': ['late blight', 'early blight', 'black scurf', 'potato virus']
}

@disease_bp.route('/identify', methods=['POST'])
def identify_disease():
    """
    Enhanced AI disease identification with crop selection and multiple input types.
    Expects JSON data: {'symptom': 'symptoms', 'crop': 'crop_name', 'input_type': 'text/checklist/image'}
    """
    data = request.get_json()
    symptom_input = data.get('symptom', '').strip()
    crop = data.get('crop', '').strip().lower()
    input_type = data.get('input_type', 'text')

    if not symptom_input:
        return jsonify({
            "success": False,
            "error_te": "దయచేసి లక్షణాలను నమోదు చేయండి. (Please provide symptoms.)",
            "error_en": "Please provide symptoms for identification."
        }), 400

    # Handle image input (placeholder for future ML integration)
    if input_type == 'image':
        # For now, return a placeholder response for image analysis
        return jsonify({
            "success": True,
            "name_en": "Image Analysis Required",
            "name_te": "చిత్ర విశ్లేషణ అవసరం",
            "symptoms_en": "Image uploaded for analysis",
            "cause": "Requires expert analysis of uploaded image",
            "impact": "Cannot determine without image processing",
            "pesticide": "Consult agricultural expert",
            "dosage": "To be determined by expert",
            "safety": "Follow expert recommendations",
            "traditional_remedy": "Contact local agricultural extension service",
            "confidence": 0
        })

    # Convert input to lowercase for case-insensitive search
    search_term = symptom_input.lower()

    # Build query with crop filtering if crop is specified
    query = db.select(Disease)

    if crop and crop in CROP_DISEASES:
        # Filter by crop-specific diseases
        crop_diseases = CROP_DISEASES[crop]
        crop_conditions = []
        for disease in crop_diseases:
            crop_conditions.extend([
                Disease.disease_name_en.ilike(f"%{disease}%"),
                Disease.symptoms_en.ilike(f"%{disease}%")
            ])
        query = query.filter(or_(*crop_conditions))

    # Add symptom matching conditions
    symptom_conditions = []
    symptoms_list = search_term.split(',')

    for symptom in symptoms_list:
        symptom = symptom.strip()
        if symptom:
            symptom_conditions.extend([
                Disease.disease_name_en.ilike(f"%{symptom}%"),
                Disease.symptoms_en.ilike(f"%{symptom}%")
            ])

    if symptom_conditions:
        query = query.filter(or_(*symptom_conditions))

    # Execute query
    matches = db.session.execute(query).scalars().all()

    if matches:
        # Select the best match (first one for now, could be improved with scoring)
        match = matches[0]

        # Calculate confidence based on how well symptoms match
        confidence = calculate_confidence(symptom_input, match.symptoms_en)

        # Enhanced response with more comprehensive information
        response = {
            "name_en": match.disease_name_en,
            "name_te": match.disease_name_te or match.disease_name_en,
            "symptoms_en": match.symptoms_en,
            "cause": getattr(match, 'cause_en', 'Pathogenic infection'),
            "impact": getattr(match, 'impact_en', 'Can reduce crop yield significantly'),
            "pesticide": match.pesticide_rec_en or "Consult local agricultural expert",
            "dosage": getattr(match, 'dosage_en', 'As recommended by agricultural expert'),
            "safety": match.safety_en or "Wear protective clothing, follow label instructions",
            "traditional_remedy": getattr(match, 'traditional_remedy_en', 'Use organic pest control methods'),
            "confidence": confidence,
            "success": True
        }
        return jsonify(response)
    else:
        # No match found - provide helpful suggestions
        suggestions = []
        if crop and crop in CROP_DISEASES:
            suggestions.append(f"Common diseases for {crop.title()}: {', '.join(CROP_DISEASES[crop][:3])}")

        suggestions.extend([
            "Try describing symptoms more specifically",
            "Include multiple symptoms for better matching",
            "Consider uploading a photo of the affected plant",
            "Consult local agricultural extension services"
        ])

        return jsonify({
            "success": False,
            "error_te": f"మీరు ఇచ్చిన లక్షణాలకు సరిపోయే తెగులును కనుగొనలేకపోయాము. {crop.title() if crop else ''} పంట కోసం మరింత స్పష్టమైన సమాచారం అందించండి.",
            "error_en": f"No matching disease found for the provided symptoms{' in ' + crop if crop else ''}. Please provide more specific information.",
            "suggestions": suggestions
        }), 404

def calculate_confidence(symptom_input, disease_symptoms):
    """
    Calculate confidence score based on symptom matching.
    Returns a percentage (0-100).
    """
    if not symptom_input or not disease_symptoms:
        return 0

    input_symptoms = set(symptom_input.lower().split(','))
    disease_symptoms_set = set(disease_symptoms.lower().split(','))

    # Remove empty strings
    input_symptoms = {s.strip() for s in input_symptoms if s.strip()}
    disease_symptoms_set = {s.strip() for s in disease_symptoms_set if s.strip()}

    if not disease_symptoms_set:
        return 0

    # Calculate overlap
    matches = input_symptoms.intersection(disease_symptoms_set)
    match_ratio = len(matches) / len(disease_symptoms_set)

    # Convert to percentage with some base confidence
    confidence = min(95, max(30, match_ratio * 100))

    return round(confidence)