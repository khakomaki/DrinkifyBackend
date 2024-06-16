from flask import Blueprint, request, jsonify, current_app
from firebase_admin import firestore

api = Blueprint("api", __name__)

@api.route("/register", methods=["POST"])
def register_user():
    data = request.json
    database = current_app.config["FIRESTORE"]
    user_ref = database.collection("users").document(data["username"])
    user_ref.set({
        "username": data["username"],
        "weight": data["weight"],
        "gender": data["gender"]
    })
    return jsonify({
        "status": "User registered successfully"
    }), 201

@api.route("/record_drink", methods=["POST"])
def record_drink():
    data = request.json
    database = current_app.config["FIREBASE"]
    user_ref = database.collection["users"].document(data["username"])
    drink_ref = user_ref.collection("drinks").document()
    drink_ref.set({
        "type": data["type"],
        "amount": data["amount"],
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return jsonify({
        "status": "Drink recorded successfully"
    }), 201

@api.route('/calculate_BAC', methods=['GET'])
def get_BAC():
    username = request.args.get("username")
    database = current_app.config["FIREBASE"]
    user_ref = database.collection("users").document(username)
    user = user_ref.get().to_dict()
    drinks_ref = user_ref.collection("drinks")
    drinks = [drink.to_dict() for drink in drinks_ref.stream()]
    bac = _calculate_BAC(user["weight"], user.get("gender"), "male", drinks)

    return jsonify({
        "bac": bac
    }), 201

def _calculate_BAC(weight, gender, drinks):
    alcohol_elim_rates = {
        "male": 0.68, 
        "female": 0.55
    }

    # Get alcohol elimination rate from gender or calculate average
    if gender in alcohol_elim_rates:
        alcohol_elim_rate = alcohol_elim_rates[gender]
    else:
        alcohol_elim_rate = sum(alcohol_elim_rates.values) / len(alcohol_elim_rates)

    total_alcohol = sum(drink['amount'] * drink['type']['alcohol_content'] for drink in drinks)
    bac = (total_alcohol / (weight * alcohol_elim_rate)) * 100
    return bac
