
from flask import Blueprint, jsonify, request
from models import db, Activity

activities_bp = Blueprint('activities', __name__)

@activities_bp.route('/', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([
        {"id": a.id, "type": a.type, "description": a.description, "co2": a.co2_amount}
        for a in activities
    ])

@activities_bp.route('/', methods=['POST'])
def create_activity():
    data = request.json
    new_activity = Activity(
        type=data['type'],
        description=data.get('description', ''),
        co2_amount=data.get('co2_amount', 0.0),
        date=data.get('date', ''),
        user_id=data['user_id']
    )
    db.session.add(new_activity)
    db.session.commit()
    return jsonify({"message": "Activity logged successfully"}), 201
