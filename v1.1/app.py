from flask import Flask
from flask_migrate import Migrate
from config import Config
from models import db
from routes import register_blueprints
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt = JWTManager(app)

    db.init_app(app)
    migrate = Migrate(app, db)

    register_blueprints(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
