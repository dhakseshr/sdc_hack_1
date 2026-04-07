from datetime import datetime
from extensions import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    post_type = db.Column(db.String(50))  # 'project', 'opportunity', 'update'
    ref_id = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'post_type': self.post_type,
            'ref_id': self.ref_id,
            'author_id': self.author_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
