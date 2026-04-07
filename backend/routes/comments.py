from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.response import Comment, Notification
from models.project import Project
from models.post import Post

comments_bp = Blueprint('comments', __name__, url_prefix='/api/comments')


@comments_bp.route('/project/<int:project_id>', methods=['GET'])
def get_project_comments(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    comments = Comment.query.filter_by(project_id=project_id).order_by(Comment.created_at.desc()).all()
    return jsonify({'comments': [c.to_dict() for c in comments]}), 200


@comments_bp.route('/project/<int:project_id>', methods=['POST'])
@jwt_required()
def create_project_comment(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    data = request.get_json() or {}
    content = data.get('content', '').strip()
    if not content:
        return jsonify({'error': 'content is required'}), 400

    comment = Comment(
        content=content,
        author_id=user_id,
        project_id=project_id,
    )
    db.session.add(comment)

    # Notify project owner if commenter is not owner
    if project.owner_id != user_id:
        notification = Notification(
            user_id=project.owner_id,
            type='new_comment',
            title=f'New comment on {project.name}',
            message=f'Someone commented on your project',
            related_id=project_id,
        )
        db.session.add(notification)

    db.session.commit()
    return jsonify({'comment': comment.to_dict()}), 201


@comments_bp.route('/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    user_id = int(get_jwt_identity())
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    if comment.author_id != user_id:
        return jsonify({'error': 'Forbidden: only author can edit'}), 403

    data = request.get_json() or {}
    content = data.get('content', '').strip()
    if not content:
        return jsonify({'error': 'content is required'}), 400

    comment.content = content
    db.session.commit()
    return jsonify({'comment': comment.to_dict()}), 200


@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = int(get_jwt_identity())
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    if comment.author_id != user_id:
        return jsonify({'error': 'Forbidden: only author can delete'}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'}), 200
