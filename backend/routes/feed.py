from flask import Blueprint, jsonify
from models.post import Post

feed_bp = Blueprint('feed', __name__, url_prefix='/api/feed')


@feed_bp.route('/', methods=['GET'])
def get_feed():
    posts = Post.query.order_by(Post.created_at.desc()).limit(50).all()
    result = []
    for p in posts:
        result.append({
            'id': p.id,
            'content': p.content,
            'post_type': p.post_type,
            'ref_id': p.ref_id,
            'author_id': p.author_id,
            'author_name': p.author.name if p.author else None,
            'created_at': p.created_at.isoformat() if p.created_at else None,
        })
    return jsonify({'posts': result}), 200
