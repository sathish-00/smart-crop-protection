# smart-crop-protection/backend/__init__.py

from flask import Flask
from .config import DevelopmentConfig
from .extensions import db

from .models import crop_model
from .models import disease_model
from .models import shop_model

from backend.api.recommend_crop import recommend_bp

from .api.crop_bp import crop_bp
from .api.disease_bp import disease_bp
from .api.shop_bp import shop_bp
from .main import main

def create_app(config_object=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)

    # Web pages
    app.register_blueprint(main)

    # APIs
    app.register_blueprint(crop_bp, url_prefix='/api/crop')
    app.register_blueprint(disease_bp, url_prefix='/api/disease')
    app.register_blueprint(shop_bp, url_prefix='/api/shops')

    # ✅ NEW: Recommendation API
    app.register_blueprint(recommend_bp)

    # Seed data on first run
    with app.app_context():
        db.create_all()
        from .data_seeding.seed_crop_data import seed_all_crops
        from .data_seeding.seed_shop_data import seed_shops
        seed_all_crops(app)
        seed_shops(app)

    return app
