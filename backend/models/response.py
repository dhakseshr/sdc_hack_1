from datetime import datetime
from extensions import db


class OpportunityResponse(db.Model):
    __tablename__ = 'opportunity_responses'

    id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    opportunity = db.relationship('Opportunity', backref='responses')
    user = db.relationship('User', backref='opportunity_responses')

    def to_dict(self):
        return {
            'id': self.id,
            'opportunity_id': self.opportunity_id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = db.relationship('User', backref='comments')
    project = db.relationship('Project', backref='comments')
    post = db.relationship('Post', backref='comments')

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'author_id': self.author_id,
            'author_name': self.author.name if self.author else None,
            'project_id': self.project_id,
            'post_id': self.post_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50))  # 'project_invite', 'joined_project', 'new_comment', 'opp_response'
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text)
    related_id = db.Column(db.Integer, nullable=True)  # project/opportunity id
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='notifications')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'related_id': self.related_id,
            'read': self.read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
