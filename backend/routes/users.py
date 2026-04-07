from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/', methods=['GET'])
def list_users():
    users = User.query.all()
    result = [
        {
            'id': u.id,
            'name': u.name,
            'bio': u.bio,
            'skills': u.skills or [],
            'github': u.github,
        }
        for u in users
    ]
    return jsonify({'users': result}), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    projects = [p.to_dict() for p in user.projects_owned]
    opportunities = [o.to_dict() for o in user.opportunities_posted]

    data = user.to_dict()
    data['projects'] = projects
    data['opportunities'] = opportunities
    return jsonify({'user': data}), 200


@users_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'name' in data:
        user.name = data['name']
    if 'bio' in data:
        user.bio = data['bio']
    if 'skills' in data:
        user.skills = data['skills']
    if 'github' in data:
        user.github = data['github']
    if 'linkedin' in data:
        user.linkedin = data['linkedin']

    db.session.commit()
    return jsonify({'user': user.to_dict()}), 200
