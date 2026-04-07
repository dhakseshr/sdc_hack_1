from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.response import Notification

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')


@notifications_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = int(get_jwt_identity())
    unread_only = request.args.get('unread', 'false').lower() == 'true'

    query = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc())
    if unread_only:
        query = query.filter_by(read=False)

    notifications = query.limit(50).all()
    unread_count = Notification.query.filter_by(user_id=user_id, read=False).count()

    return jsonify({
        'notifications': [n.to_dict() for n in notifications],
        'unread_count': unread_count
    }), 200


@notifications_bp.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notification_id):
    user_id = int(get_jwt_identity())
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404

    if notification.user_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403

    notification.read = True
    db.session.commit()
    return jsonify({'notification': notification.to_dict()}), 200


@notifications_bp.route('/read-all', methods=['PUT'])
@jwt_required()
def mark_all_read():
    user_id = int(get_jwt_identity())
    Notification.query.filter_by(user_id=user_id, read=False).update({'read': True})
    db.session.commit()
    return jsonify({'message': 'All notifications marked as read'}), 200


@notifications_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    user_id = int(get_jwt_identity())
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404

    if notification.user_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403

    db.session.delete(notification)
    db.session.commit()
    return jsonify({'message': 'Notification deleted'}), 200
