
from flask import Flask
from flask_cors import CORS
from database import db
from routes.users import users_bp
from routes.activities import activities_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize DB
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(activities_bp, url_prefix='/api/activities')

    @app.route('/')
    def home():
        return {"message": "Welcome to TrackerBackend API!"}

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
