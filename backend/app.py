from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from config import Config
from extensions import db, jwt
from routes.auth import auth_bp
from routes.users import users_bp
from routes.projects import projects_bp
from routes.opportunities import opportunities_bp
from routes.feed import feed_bp
from routes.comments import comments_bp
from routes.notifications import notifications_bp
from routes.search import search_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)
    CORS(app, origins=["http://localhost:5173"])

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(opportunities_bp)
    app.register_blueprint(feed_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(search_bp)

    # Health check
    @app.route('/api/health')
    def health():
        return jsonify({'status': 'ok'}), 200

    return app


app = create_app()

# Create all tables on startup
with app.app_context():
    # Import models so SQLAlchemy knows about them
    from models.user import User
    from models.project import Project, ProjectMember
    from models.opportunity import Opportunity
    from models.post import Post
    from models.response import OpportunityResponse, Comment, Notification
    db.create_all()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
