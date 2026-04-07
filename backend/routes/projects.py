from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.project import Project, ProjectMember
from models.user import User

projects_bp = Blueprint('projects', __name__, url_prefix='/api/projects')


@projects_bp.route('/', methods=['GET'])
def list_projects():
    projects = Project.query.all()
    result = []
    for p in projects:
        d = p.to_dict()
        d['owner_name'] = p.owner.name if p.owner else None
        d['member_count'] = len(p.members)
        result.append(d)
    return jsonify({'projects': result}), 200


@projects_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'name is required'}), 400

    project = Project(
        name=name,
        description=data.get('description', ''),
        stack=data.get('stack', []),
        status=data.get('status', 'recruiting'),
        owner_id=user_id,
    )
    db.session.add(project)
    db.session.flush()

    member = ProjectMember(
        project_id=project.id,
        user_id=user_id,
        role='owner',
    )
    db.session.add(member)
    db.session.commit()

    return jsonify({'project': project.to_dict()}), 201


@projects_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    members_list = []
    for m in project.members:
        user = User.query.get(m.user_id)
        members_list.append({
            'user_id': m.user_id,
            'name': user.name if user else None,
            'role': m.role,
            'joined_at': m.joined_at.isoformat() if m.joined_at else None,
        })

    data = project.to_dict()
    data['owner_name'] = project.owner.name if project.owner else None
    data['members'] = members_list
    return jsonify({'project': data}), 200


@projects_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    if project.owner_id != user_id:
        return jsonify({'error': 'Forbidden: only the owner can update this project'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'name' in data:
        project.name = data['name']
    if 'description' in data:
        project.description = data['description']
    if 'stack' in data:
        project.stack = data['stack']
    if 'status' in data:
        project.status = data['status']

    db.session.commit()
    return jsonify({'project': project.to_dict()}), 200


@projects_bp.route('/<int:project_id>/join', methods=['POST'])
@jwt_required()
def join_project(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    existing = ProjectMember.query.filter_by(project_id=project_id, user_id=user_id).first()
    if existing:
        return jsonify({'error': 'Already a member of this project'}), 400

    member = ProjectMember(
        project_id=project_id,
        user_id=user_id,
        role='member',
    )
    db.session.add(member)
    db.session.commit()
    return jsonify({'message': 'Joined project successfully', 'membership': member.to_dict()}), 201


@projects_bp.route('/<int:project_id>/leave', methods=['DELETE'])
@jwt_required()
def leave_project(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    member = ProjectMember.query.filter_by(project_id=project_id, user_id=user_id).first()
    if not member:
        return jsonify({'error': 'You are not a member of this project'}), 404

    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Left project successfully'}), 200
