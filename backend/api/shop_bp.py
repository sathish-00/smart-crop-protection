from flask import Blueprint, request, jsonify
from backend.models.shop_model import FertilizerShop
import math

shop_bp = Blueprint("shop_bp", __name__)

def haversine(lat1, lon1, lat2, lon2):
    # Distance in KM
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


@shop_bp.route("/nearby", methods=["GET"])
def nearby_shops():
    """
    GET /api/shops/nearby?lat=15.80&lng=77.49&radius=25
    """
    try:
        lat = float(request.args.get("lat"))
        lng = float(request.args.get("lng"))
        radius = float(request.args.get("radius", 25))  # default 25km
    except:
        return jsonify({"error": "Invalid lat/lng values"}), 400

    shops = FertilizerShop.query.all()
    results = []

    for s in shops:
        dist = haversine(lat, lng, s.latitude, s.longitude)
        if dist <= radius:
            results.append({
                "name": s.name,
                "address": s.address,
                "phone": s.phone,
                "latitude": s.latitude,
                "longitude": s.longitude,
                "distance_km": round(dist, 2)
            })

    results.sort(key=lambda x: x["distance_km"])
    return jsonify({"shops": results})
