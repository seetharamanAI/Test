from flask import Flask

from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes import main_bp
    from app.quiz import quiz_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(quiz_bp)

    return app
