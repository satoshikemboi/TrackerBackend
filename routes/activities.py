# routes/activities.py

from flask import Blueprint, request, jsonify
from models import db, Activity

activities_bp = Blueprint('activities', __name__, url_prefix='/api/activities')

# Read all activities
@activities_bp.route('/', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([
        {
            "id": a.id,
            "type": a.type,
            "description": a.description,
            "co2": a.co2_amount,
            "date": a.date,
            "user_id": a.user_id
        }
        for a in activities
    ]), 200

# Create activity
@activities_bp.route('/', methods=['POST'])
def create_activity():
    data = request.get_json()
    if not data or 'user_id' not in data or 'type' not in data:
        return jsonify({"message": "Missing required fields: user_id, type"}), 400

    new_activity = Activity(
        type=data['type'],
        description=data.get('description', ''),
        co2_amount=data.get('co2_amount', 0.0),
        date=data.get('date'),
        user_id=data['user_id']
    )
    db.session.add(new_activity)
    db.session.commit()
    return jsonify({
        "id": new_activity.id,
        "type": new_activity.type,
        "description": new_activity.description,
        "co2": new_activity.co2_amount,
        "date": new_activity.date,
        "user_id": new_activity.user_id
    }), 201

# Read single activity
@activities_bp.route('/<int:activity_id>', methods=['GET'])
def get_single_activity(activity_id):
    a = Activity.query.get(activity_id)
    if not a:
        return jsonify({"message": "Activity not found"}), 404

    return jsonify({
        "id": a.id,
        "type": a.type,
        "description": a.description,
        "co2": a.co2_amount,
        "date": a.date,
        "user_id": a.user_id
    }), 200

# Update activity
@activities_bp.route('/<int:activity_id>', methods=['PUT'])
def update_activity(activity_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    a = Activity.query.get(activity_id)
    if not a:
        return jsonify({"message": "Activity not found"}), 404

    # Update allowed fields
    if 'type' in data:
        a.type = data['type']
    if 'description' in data:
        a.description = data['description']
    if 'co2_amount' in data:
        a.co2_amount = data['co2_amount']
    if 'date' in data:
        a.date = data['date']
    if 'user_id' in data:
        a.user_id = data['user_id']

    db.session.commit()
    return jsonify({
        "id": a.id,
        "type": a.type,
        "description": a.description,
        "co2": a.co2_amount,
        "date": a.date,
        "user_id": a.user_id
    }), 200

# Delete activity
@activities_bp.route('/<int:activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    a = Activity.query.get(activity_id)
    if not a:
        return jsonify({"message": "Activity not found"}), 404

    db.session.delete(a)
    db.session.commit()
    return jsonify({"message": f"Activity {activity_id} deleted"}), 200
