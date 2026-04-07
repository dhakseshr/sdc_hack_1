from datetime import datetime
import bcrypt
from extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.JSON, default=list)
    github = db.Column(db.String(255), nullable=True)
    linkedin = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    projects_owned = db.relationship('Project', backref='owner', lazy=True)
    project_memberships = db.relationship('ProjectMember', backref='user', lazy=True)
    opportunities_posted = db.relationship('Opportunity', backref='author', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'bio': self.bio,
            'skills': self.skills or [],
            'github': self.github,
            'linkedin': self.linkedin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
