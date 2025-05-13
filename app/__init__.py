from flask import Flask
from flask_cors import CORS
from app.extensions import db, jwt, migrate
from app.config import config_by_name

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.api import auth_bp, content_bp, publication_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(content_bp, url_prefix='/api/content')
    app.register_blueprint(publication_bp, url_prefix='/api/publication')

    @app.route('/')
    def health_check():
        return {"code": 200, "message": "healthy", "status": "success"}

    return app