from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.opportunity import Opportunity
from models.post import Post
from models.response import OpportunityResponse, Notification

opportunities_bp = Blueprint('opportunities', __name__, url_prefix='/api/opportunities')

VALID_CATEGORIES = {'Looking for Teammates', 'Project Roles', 'Hackathons'}


@opportunities_bp.route('/', methods=['GET'])
def list_opportunities():
    opportunities = Opportunity.query.order_by(Opportunity.created_at.desc()).all()
    result = []
    for o in opportunities:
        d = o.to_dict()
        d['author_name'] = o.author.name if o.author else None
        result.append(d)
    return jsonify({'opportunities': result}), 200


@opportunities_bp.route('/', methods=['POST'])
@jwt_required()
def create_opportunity():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    category = data.get('category', '').strip()

    if not title:
        return jsonify({'error': 'title is required'}), 400
    if category and category not in VALID_CATEGORIES:
        return jsonify({'error': f'category must be one of: {", ".join(VALID_CATEGORIES)}'}), 400

    opportunity = Opportunity(
        title=title,
        description=description,
        category=category or None,
        author_id=user_id,
    )
    db.session.add(opportunity)
    db.session.flush()

    post = Post(
        content=f"{title}: {description}" if description else title,
        post_type='opportunity',
        ref_id=opportunity.id,
        author_id=user_id,
    )
    db.session.add(post)
    db.session.commit()

    return jsonify({'opportunity': opportunity.to_dict()}), 201


@opportunities_bp.route('/<int:opportunity_id>', methods=['DELETE'])
@jwt_required()
def delete_opportunity(opportunity_id):
    user_id = int(get_jwt_identity())
    opportunity = Opportunity.query.get(opportunity_id)
    if not opportunity:
        return jsonify({'error': 'Opportunity not found'}), 404
    if opportunity.author_id != user_id:
        return jsonify({'error': 'Forbidden: only the author can delete this opportunity'}), 403

    db.session.delete(opportunity)
    db.session.commit()
    return jsonify({'message': 'Opportunity deleted successfully'}), 200


@opportunities_bp.route('/<int:opportunity_id>/respond', methods=['POST'])
@jwt_required()
def respond_to_opportunity(opportunity_id):
    user_id = int(get_jwt_identity())
    opportunity = Opportunity.query.get(opportunity_id)
    if not opportunity:
        return jsonify({'error': 'Opportunity not found'}), 404

    data = request.get_json() or {}
    message = data.get('message', '').strip()

    existing = OpportunityResponse.query.filter_by(
        opportunity_id=opportunity_id,
        user_id=user_id
    ).first()
    if existing:
        return jsonify({'error': 'You have already responded to this opportunity'}), 400

    response = OpportunityResponse(
        opportunity_id=opportunity_id,
        user_id=user_id,
        message=message or None,
    )
    db.session.add(response)

    # Create notification for opportunity author
    notification = Notification(
        user_id=opportunity.author_id,
        type='opp_response',
        title=f'New response to your opportunity: {opportunity.title}',
        message=f'Someone is interested in your opportunity',
        related_id=opportunity_id,
    )
    db.session.add(notification)
    db.session.commit()

    return jsonify({'message': 'Response submitted successfully', 'response': response.to_dict()}), 201


@opportunities_bp.route('/<int:opportunity_id>/responses', methods=['GET'])
@jwt_required()
def get_opportunity_responses(opportunity_id):
    user_id = int(get_jwt_identity())
    opportunity = Opportunity.query.get(opportunity_id)
    if not opportunity:
        return jsonify({'error': 'Opportunity not found'}), 404

    # Only author can view responses
    if opportunity.author_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403

    responses = OpportunityResponse.query.filter_by(opportunity_id=opportunity_id).all()
    return jsonify({'responses': [r.to_dict() for r in responses]}), 200


@opportunities_bp.route('/<int:opportunity_id>/responses/<int:response_id>', methods=['DELETE'])
@jwt_required()
def delete_opportunity_response(opportunity_id, response_id):
    user_id = int(get_jwt_identity())
    opportunity = Opportunity.query.get(opportunity_id)
    if not opportunity:
        return jsonify({'error': 'Opportunity not found'}), 404

    if opportunity.author_id != user_id:
        return jsonify({'error': 'Forbidden: only author can delete responses'}), 403

    response = OpportunityResponse.query.get(response_id)
    if not response:
        return jsonify({'error': 'Response not found'}), 404

    db.session.delete(response)
    db.session.commit()
    return jsonify({'message': 'Response deleted'}), 200
