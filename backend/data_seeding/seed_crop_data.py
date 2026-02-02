from backend import create_app
from backend.extensions import db
from backend.models.crop_model import Crop, FertilizerSchedule


def seed_crop(name_en, name_te, soil_type_en, sowing_season_en, crop_cycle_days, schedules):
    crop = Crop.query.filter_by(name_en=name_en).first()

    if crop is None:
        print(f"Seeding {name_en} crop and roadmap...")

        crop = Crop(
            name_en=name_en,
            name_te=name_te,
            soil_type_en=soil_type_en,
            sowing_season_en=sowing_season_en,
            crop_cycle_days=crop_cycle_days
        )
        db.session.add(crop)
        db.session.commit()

        for s in schedules:
            db.session.add(FertilizerSchedule(
                crop_id=crop.id,
                growth_stage_en=s["stage_en"],
                growth_stage_te=s["stage_te"],
                week_range=s["week_range"],
                fertilizer_dosage_en=s["fertilizer"],
                irrigation_advice_en=s["irrigation"]
            ))
        db.session.commit()

        print(f"✅ {name_en} seeded.")
    else:
        print(f"ℹ️ {name_en} already exists. Skipping.")


def seed_all_crops(app):
    with app.app_context():

        # ✅ 1) Cotton
        seed_crop(
            "Cotton", "ప్రత్తి",
            "Black cotton soil",
            "June-August",
            180,
            [
                {"week_range": "1-4", "stage_en": "Sowing & Germination", "stage_te": "విత్తనం & మొలకెత్తుట", "fertilizer": "DAP (25kg/acre)", "irrigation": "Light irrigation"},
                {"week_range": "5-8", "stage_en": "Vegetative Growth", "stage_te": "మొక్కల పెరుగుదల దశ", "fertilizer": "Urea (50kg/acre)", "irrigation": "Irrigate every 7 days"},
                {"week_range": "9-12", "stage_en": "Flowering Start", "stage_te": "పువ్వుల దశ ప్రారంభం", "fertilizer": "Potash (30kg/acre)", "irrigation": "Maintain moisture"},
            ]
        )

        # ✅ 2) Rice
        seed_crop(
            "Rice", "వరి",
            "Clay soil / Alluvial soil",
            "June-September",
            120,
            [
                {"week_range": "1-4", "stage_en": "Nursery & Transplanting", "stage_te": "నర్సరీ & నాటడం", "fertilizer": "DAP (25kg/acre)", "irrigation": "Maintain standing water"},
                {"week_range": "5-8", "stage_en": "Tillering Stage", "stage_te": "కొమ్మలు పెరుగుదల దశ", "fertilizer": "Urea (50kg/acre)", "irrigation": "Maintain water in field"},
                {"week_range": "9-12", "stage_en": "Flowering & Grain Filling", "stage_te": "పుష్పించడం & గింజలు నిండడం", "fertilizer": "Potash (25kg/acre)", "irrigation": "Reduce water before harvest"},
            ]
        )

        # ✅ 3) Maize
        seed_crop(
            "Maize", "మొక్కజొన్న",
            "Red soil / Black soil (well drained)",
            "June-August",
            110,
            [
                {"week_range": "1-3", "stage_en": "Land Preparation & Sowing", "stage_te": "భూమి సిద్ధం & విత్తనం", "fertilizer": "DAP (20kg/acre)", "irrigation": "Light irrigation if needed"},
                {"week_range": "4-6", "stage_en": "Vegetative Growth", "stage_te": "మొక్క పెరుగుదల దశ", "fertilizer": "Urea (40kg/acre)", "irrigation": "Irrigate every 7-10 days"},
                {"week_range": "7-10", "stage_en": "Cob Formation", "stage_te": "కాబ్ ఏర్పాట్లు", "fertilizer": "Potash (20kg/acre)", "irrigation": "Maintain moisture"},
            ]
        )

        # ✅ 4) Groundnut
        seed_crop(
            "Groundnut", "వేరుశెనగ",
            "Sandy soil / Red soil",
            "June-August",
            115,
            [
                {"week_range": "1-3", "stage_en": "Sowing & Germination", "stage_te": "విత్తనం & మొలకెత్తుట", "fertilizer": "Gypsum (50kg/acre)", "irrigation": "Light irrigation"},
                {"week_range": "4-7", "stage_en": "Vegetative Growth", "stage_te": "మొక్క పెరుగుదల దశ", "fertilizer": "Urea (25kg/acre)", "irrigation": "Irrigate every 10 days"},
                {"week_range": "8-12", "stage_en": "Flowering & Pod Formation", "stage_te": "పుష్పించడం & కాయ ఏర్పాట్లు", "fertilizer": "Potash (20kg/acre)", "irrigation": "Maintain moisture"},
            ]
        )

        # ✅ 5) Chilli
        seed_crop(
            "Chilli", "మిరప",
            "Red soil / Sandy loam",
            "June-September / Oct-Nov",
            150,
            [
                {"week_range": "1-4", "stage_en": "Nursery & Transplanting", "stage_te": "నర్సరీ & నాటడం", "fertilizer": "DAP (20kg/acre)", "irrigation": "Light irrigation after transplant"},
                {"week_range": "5-8", "stage_en": "Vegetative Growth", "stage_te": "మొక్క పెరుగుదల దశ", "fertilizer": "Urea (40kg/acre)", "irrigation": "Irrigate every 6-8 days"},
                {"week_range": "9-14", "stage_en": "Flowering & Fruit Set", "stage_te": "పుష్పించడం & కాయ ఏర్పాట్లు", "fertilizer": "Potash (25kg/acre)", "irrigation": "Maintain soil moisture"},
            ]
        )

        # ✅ 6) Tomato
        seed_crop(
            "Tomato", "టమాట",
            "Loamy soil (well drained)",
            "Oct-December",
            105,
            [
                {"week_range": "1-3", "stage_en": "Transplanting", "stage_te": "నాటడం", "fertilizer": "DAP (20kg/acre)", "irrigation": "Irrigate after transplant"},
                {"week_range": "4-6", "stage_en": "Vegetative Stage", "stage_te": "మొక్క పెరుగుదల దశ", "fertilizer": "Urea (35kg/acre)", "irrigation": "Irrigate every 5-7 days"},
                {"week_range": "7-10", "stage_en": "Flowering & Fruit", "stage_te": "పుష్పించడం & ఫలదశ", "fertilizer": "Potash (25kg/acre)", "irrigation": "Maintain moisture"},
            ]
        )

        # ✅ 7) Onion
        seed_crop(
            "Onion", "ఉల్లి",
            "Sandy loam soil",
            "Oct-November",
            120,
            [
                {"week_range": "1-4", "stage_en": "Nursery & Transplant", "stage_te": "నర్సరీ & నాటడం", "fertilizer": "DAP (20kg/acre)", "irrigation": "Light irrigation"},
                {"week_range": "5-8", "stage_en": "Bulb Formation", "stage_te": "గడ్డ ఏర్పాట్లు", "fertilizer": "Urea (40kg/acre)", "irrigation": "Irrigate every 7 days"},
                {"week_range": "9-12", "stage_en": "Maturity", "stage_te": "పక్వ దశ", "fertilizer": "Potash (20kg/acre)", "irrigation": "Reduce water"},
            ]
        )

        # ✅ 8) Sunflower
        seed_crop(
            "Sunflower", "సూర్యకాంతి",
            "Red soil / Black soil",
            "June-September / Jan-Feb",
            95,
            [
                {"week_range": "1-3", "stage_en": "Sowing", "stage_te": "విత్తనం", "fertilizer": "DAP (15kg/acre)", "irrigation": "Light irrigation"},
                {"week_range": "4-6", "stage_en": "Vegetative", "stage_te": "మొక్క పెరుగుదల దశ", "fertilizer": "Urea (25kg/acre)", "irrigation": "Every 10 days"},
                {"week_range": "7-9", "stage_en": "Flowering", "stage_te": "పుష్ప దశ", "fertilizer": "Potash (15kg/acre)", "irrigation": "Maintain moisture"},
            ]
        )

        # ✅ 9) Bengal Gram
        seed_crop(
            "Bengalgram", "శనగ",
            "Red soil / Black soil",
            "Oct-November",
            110,
            [
                {"week_range": "1-4", "stage_en": "Sowing & Early Growth", "stage_te": "విత్తనం & ప్రారంభ దశ", "fertilizer": "DAP (15kg/acre)", "irrigation": "Minimal irrigation"},
                {"week_range": "5-8", "stage_en": "Vegetative", "stage_te": "పెరుగుదల దశ", "fertilizer": "Urea (10kg/acre)", "irrigation": "Only if needed"},
                {"week_range": "9-12", "stage_en": "Pod Formation", "stage_te": "కాయ ఏర్పాట్లు", "fertilizer": "Potash (10kg/acre)", "irrigation": "Avoid excess water"},
            ]
        )

        # ✅ 10) Sugarcane
        seed_crop(
            "Sugarcane", "చెరకు",
            "Alluvial soil / Clay soil",
            "Jan-March / July-Aug",
            300,
            [
                {"week_range": "1-8", "stage_en": "Planting & Germination", "stage_te": "నాటడం & మొలకెత్తుట", "fertilizer": "DAP (30kg/acre)", "irrigation": "Regular irrigation"},
                {"week_range": "9-20", "stage_en": "Tillering", "stage_te": "కొమ్మలు పెరుగుదల", "fertilizer": "Urea (60kg/acre)", "irrigation": "Every 7 days"},
                {"week_range": "21-40", "stage_en": "Grand Growth", "stage_te": "తీవ్ర పెరుగుదల", "fertilizer": "Potash (40kg/acre)", "irrigation": "Maintain moisture"},
            ]
        )

        print("\n✅✅ ALL MAJOR AP & TS CROPS SEEDED SUCCESSFULLY ✅✅")


if __name__ == "__main__":
    app = create_app()
    seed_all_crops(app)
