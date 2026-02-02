# smart-crop-protection/backend/models/disease_model.py
from backend.extensions import db
from sqlalchemy.orm import Mapped

class Disease(db.Model):
    """
    Stores data about crop diseases, symptoms, and pesticide recommendations.
    This data is the knowledge base for the AI diagnosis module.
    """
    __tablename__ = 'disease'
    
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    disease_name_en: Mapped[str] = db.Column(db.String(120), unique=True, nullable=False)
    disease_name_te: Mapped[str] = db.Column(db.String(120))
    
    # Foreign Key linking to the Crop table (to know which crop this disease affects)
    host_crop_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('crop.id'), nullable=False)
    
    symptoms_en: Mapped[str] = db.Column(db.Text, nullable=False)
    pesticide_rec_en: Mapped[str] = db.Column(db.Text, nullable=False)
    dosage_en: Mapped[str] = db.Column(db.String(120))
    safety_en: Mapped[str] = db.Column(db.Text)

    def __repr__(self):
        return f'<Disease {self.disease_name_en}>'