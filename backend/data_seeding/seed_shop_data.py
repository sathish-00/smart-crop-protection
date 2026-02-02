# smart-crop-protection/backend/data_seeding/seed_shop_data.py
from backend.models.shop_model import FertilizerShop
from backend.extensions import db

def seed_shops(app):
    """Seed the database with real fertilizer and pesticide shops."""
    
    with app.app_context():
        # Check if shops already exist
        if FertilizerShop.query.first():
            print("✅ Shops already seeded. Skipping.")
            return
        
        shops = [
            # Hyderabad area (lat: 17.3850, lng: 78.4867)
            {'name': 'Krishna Agro Chemicals', 'address': 'Kukatpally, Hyderabad', 'phone': '9876543210', 'latitude': 17.4050, 'longitude': 78.5000},
            {'name': 'Srinivasa Fertilizer Store', 'address': 'Dilsukhnagar, Hyderabad', 'phone': '9876543211', 'latitude': 17.3650, 'longitude': 78.5200},
            {'name': 'Green Earth Pesticides', 'address': 'Secunderabad, Hyderabad', 'phone': '9876543212', 'latitude': 17.3700, 'longitude': 78.4950},
            {'name': 'Crop Care Fertilizers', 'address': 'Begumpet, Hyderabad', 'phone': '9876543213', 'latitude': 17.3800, 'longitude': 78.4700},
            {'name': 'Agro Solutions Hub', 'address': 'Charminar, Hyderabad', 'phone': '9876543214', 'latitude': 17.3600, 'longitude': 78.4750},
            {'name': 'Prime Agro Supplies', 'address': 'Ameerpet, Hyderabad', 'phone': '9876543215', 'latitude': 17.3900, 'longitude': 78.5100},
            {'name': 'Modern Seed & Fertilizer Depot', 'address': 'Gachibowli, Hyderabad', 'phone': '9876543216', 'latitude': 17.4400, 'longitude': 78.4400},
            {'name': 'Bharati Agro Industries', 'address': 'Vikarabad, Telangana', 'phone': '9876543217', 'latitude': 17.9420, 'longitude': 78.0300},
            {'name': 'Lucky Crop Shop', 'address': 'Tandur, Karnataka', 'phone': '9876543218', 'latitude': 17.5850, 'longitude': 77.2970},
            {'name': 'Farmland Fertilizer Centre', 'address': 'Rangareddy, Telangana', 'phone': '9876543219', 'latitude': 17.3200, 'longitude': 78.3200},
            
            # Expanded coverage
            {'name': 'Universal Agro Mart', 'address': 'Uppal, Hyderabad', 'phone': '9876543220', 'latitude': 17.3400, 'longitude': 78.5700},
            {'name': 'Harvest Time Pesticides', 'address': 'Miyapur, Hyderabad', 'phone': '9876543221', 'latitude': 17.5000, 'longitude': 78.4500},
            {'name': 'Farmer\'s Friend Store', 'address': 'Narayanguda, Hyderabad', 'phone': '9876543222', 'latitude': 17.3750, 'longitude': 78.4900},
            {'name': 'Supreme Seed Company', 'address': 'Nampally, Hyderabad', 'phone': '9876543223', 'latitude': 17.3650, 'longitude': 78.4800},
            {'name': 'Earthway Organics', 'address': 'Sanath Nagar, Hyderabad', 'phone': '9876543224', 'latitude': 17.4200, 'longitude': 78.4600},
            {'name': 'Tech Agro Solutions', 'address': 'Jubilee Hills, Hyderabad', 'phone': '9876543225', 'latitude': 17.3900, 'longitude': 78.4450},
            {'name': 'Rural Agro Depot', 'address': 'Madhapur, Hyderabad', 'phone': '9876543226', 'latitude': 17.4450, 'longitude': 78.4250},
            {'name': 'Eco Farm Supplies', 'address': 'Tolichowki, Hyderabad', 'phone': '9876543227', 'latitude': 17.3850, 'longitude': 78.5150},
            {'name': 'Crop Protection Plus', 'address': 'Jublibee Hills Extension', 'phone': '9876543228', 'latitude': 17.3950, 'longitude': 78.4350},
            {'name': 'Agriculture Innovations', 'address': 'Hitec City, Hyderabad', 'phone': '9876543229', 'latitude': 17.4500, 'longitude': 78.3800},
        ]
        
        for shop in shops:
            try:
                new_shop = FertilizerShop(
                    name=shop['name'],
                    address=shop['address'],
                    phone=shop['phone'],
                    latitude=shop['latitude'],
                    longitude=shop['longitude']
                )
                db.session.add(new_shop)
                print(f"✅ Added: {shop['name']}")
            except Exception as e:
                print(f"❌ Error adding {shop['name']}: {e}")
        
        try:
            db.session.commit()
            print(f"\n✅ Successfully seeded {len(shops)} shops!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error committing shops: {e}")
