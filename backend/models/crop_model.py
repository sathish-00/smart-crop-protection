# smart-crop-protection/backend/models/crop_model.py
from backend.extensions import db
from sqlalchemy.orm import relationship, Mapped

class Crop(db.Model):
    __tablename__ = 'crop'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name_en: Mapped[str] = db.Column(db.String(80), unique=True, nullable=False)
    name_te: Mapped[str] = db.Column(db.String(80), unique=True, nullable=False)
    soil_type_en: Mapped[str] = db.Column(db.String(120))
    sowing_season_en: Mapped[str] = db.Column(db.String(120))
    crop_cycle_days: Mapped[int] = db.Column(db.Integer)

    schedule = relationship("FertilizerSchedule", back_populates="crop")

class FertilizerSchedule(db.Model):
    __tablename__ = 'fertilizer_schedule'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    crop_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('crop.id'), nullable=False)

    growth_stage_en: Mapped[str] = db.Column(db.String(120), nullable=False)
    growth_stage_te: Mapped[str] = db.Column(db.String(120), nullable=False)
    week_range: Mapped[str] = db.Column(db.String(50))
    fertilizer_dosage_en: Mapped[str] = db.Column(db.Text, nullable=False)
    irrigation_advice_en: Mapped[str] = db.Column(db.Text)

    crop = relationship("Crop", back_populates="schedule")