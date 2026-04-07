from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from extensions import db
from models.user import User
from models.project import Project
from models.opportunity import Opportunity

search_bp = Blueprint('search', __name__, url_prefix='/api/search')


@search_bp.route('/', methods=['GET'])
@jwt_required()
def global_search():
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'all')  # all, users, projects, opportunities

    if not query or len(query) < 2:
        return jsonify({'error': 'Query must be at least 2 characters'}), 400

    results = {}

    # Search users
    if search_type in ('all', 'users'):
        users = User.query.filter(
            or_(
                User.name.ilike(f'%{query}%'),
                User.bio.ilike(f'%{query}%'),
            )
        ).limit(10).all()
        results['users'] = [
            {
                'id': u.id,
                'name': u.name,
                'bio': u.bio,
                'skills': u.skills or [],
            }
            for u in users
        ]

    # Search projects
    if search_type in ('all', 'projects'):
        projects = Project.query.filter(
            or_(
                Project.name.ilike(f'%{query}%'),
                Project.description.ilike(f'%{query}%'),
            )
        ).limit(10).all()
        results['projects'] = [
            {
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'stack': p.stack or [],
                'owner_name': p.owner.name if p.owner else None,
            }
            for p in projects
        ]

    # Search opportunities
    if search_type in ('all', 'opportunities'):
        opportunities = Opportunity.query.filter(
            or_(
                Opportunity.title.ilike(f'%{query}%'),
                Opportunity.description.ilike(f'%{query}%'),
            )
        ).limit(10).all()
        results['opportunities'] = [
            {
                'id': o.id,
                'title': o.title,
                'description': o.description,
                'category': o.category,
                'author_name': o.author.name if o.author else None,
            }
            for o in opportunities
        ]

    return jsonify({'results': results, 'query': query}), 200


@search_bp.route('/users', methods=['GET'])
@jwt_required()
def search_users():
    query = request.args.get('q', '').strip()
    skill = request.args.get('skill', '').strip()

    q = User.query

    if query:
        q = q.filter(or_(
            User.name.ilike(f'%{query}%'),
            User.bio.ilike(f'%{query}%'),
        ))

    if skill:
        # This is a simple check; for production, use full-text search
        q = q.filter(User.skills.contains([skill]))

    users = q.limit(20).all()
    return jsonify({
        'users': [
            {
                'id': u.id,
                'name': u.name,
                'bio': u.bio,
                'skills': u.skills or [],
                'github': u.github,
            }
            for u in users
        ]
    }), 200


@search_bp.route('/projects/by-tech', methods=['GET'])
@jwt_required()
def search_projects_by_tech():
    tech = request.args.get('tech', '').strip()

    if not tech:
        return jsonify({'error': 'tech parameter is required'}), 400

    projects = Project.query.all()
    # Filter by tech stack (since JSON filtering varies by DB)
    filtered = [p for p in projects if tech.lower() in [t.lower() for t in (p.stack or [])]]

    return jsonify({
        'projects': [
            {
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'stack': p.stack or [],
                'owner_name': p.owner.name if p.owner else None,
            }
            for p in filtered[:20]
        ]
    }), 200
