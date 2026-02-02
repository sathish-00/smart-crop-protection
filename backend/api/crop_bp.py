# smart-crop-protection/backend/api/crop_bp.py

from flask import Blueprint, jsonify
from backend.extensions import db
from backend.models.crop_model import Crop, FertilizerSchedule 
from sqlalchemy import exc
from sqlalchemy.orm import joinedload # <--- CRITICAL IMPORT ADDED

# Define the Blueprint object.
crop_bp = Blueprint('crop', __name__)

# --- Simple Test Route (for status check) ---
@crop_bp.route('/test', methods=['GET'])
def crop_test():
    """Confirms the API Blueprint is active."""
    return jsonify({"status": "Crop API Blueprint is active!"})

# --- Main Functional Route: Get Crop Roadmap ---
@crop_bp.route('/<string:crop_name>', methods=['GET'])
def get_crop_roadmap(crop_name):
    """ Fetches the detailed crop roadmap and schedule from the database. """
    
    name = crop_name.capitalize()
    
    try:
        # 1. Query the Crop table and eagerly load the associated schedule
        crop_data = db.session.execute(
            db.select(Crop)
            .filter_by(name_en=name)
            .options(joinedload(Crop.schedule)) 
        ).scalars().first()

        if not crop_data:
            return jsonify({"error": f"Crop '{name}' not found. Please check spelling."}), 404

        # 2. Build the detailed schedule list
        schedule_list = []
        sorted_schedule = sorted(crop_data.schedule, key=lambda s: s.week_range)
        
        for item in sorted_schedule:
            schedule_list.append({
                "week_range": item.week_range,
                "stage_en": item.growth_stage_en,
                "stage_te": item.growth_stage_te,
                "fertilizer_en": item.fertilizer_dosage_en,
                "fertilizer_te": item.fertilizer_dosage_en,  # Using English for Telugu as well for now
                "irrigation_en": item.irrigation_advice_en,
                "irrigation_te": item.irrigation_advice_en,  # Using English for Telugu as well for now
            })

        # 3. Compile the final JSON response
        response = {
            "name_en": crop_data.name_en,
            "name_te": crop_data.name_te,
            "soil_type_en": crop_data.soil_type_en,
            "soil_type_te": crop_data.soil_type_en,  # Using English for Telugu as well for now
            "sowing_season_en": crop_data.sowing_season_en,
            "sowing_season_te": crop_data.sowing_season_en,  # Using English for Telugu as well for now
            "crop_cycle_days": crop_data.crop_cycle_days,
            "roadmap": schedule_list
        }
        
        return jsonify(response)
        
    except exc.SQLAlchemyError as e:
        return jsonify({"error": "Database query failed", "details": str(e)}), 500