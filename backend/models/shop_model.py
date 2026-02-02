# smart-crop-protection/backend/models/shop_model.py
from backend.extensions import db
from sqlalchemy.orm import relationship, Mapped

class FertilizerShop(db.Model):
    """Stores static shop details including geographical coordinates."""
    __tablename__ = 'fertilizer_shop'
    
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    address: Mapped[str] = db.Column(db.String(255))
    latitude: Mapped[float] = db.Column(db.Float, nullable=False)
    longitude: Mapped[float] = db.Column(db.Float, nullable=False)
    phone: Mapped[str] = db.Column(db.String(20))
    
    # Relationship: One shop has many inventory items
    inventory = relationship("PesticideInventory", back_populates="shop")

    def __repr__(self):
        return f'<Shop {self.name}>'

class PesticideInventory(db.Model):
    """Stores dynamic price and stock status for products at a specific shop."""
    __tablename__ = 'pesticide_inventory'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    # Foreign Key linking back to the FertilizerShop table
    shop_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('fertilizer_shop.id'), nullable=False)
    
    pesticide_name: Mapped[str] = db.Column(db.String(150), nullable=False)
    stock_status: Mapped[str] = db.Column(db.String(50)) # e.g., 'In Stock', 'Low Stock'
    price: Mapped[float] = db.Column(db.Float) # Current selling price
    
    # Relationship back to Shop
    shop = relationship("FertilizerShop", back_populates="inventory")

    def __repr__(self):
        return f'<Inventory {self.pesticide_name} at Shop {self.shop_id}>'