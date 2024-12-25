from flask import Flask
from flask_migrate import Migrate
from config import Config
from models import db
from routes.project_routes import project_routes
from routes.task_routes import task_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Veritabanı ve migrate başlatma
    db.init_app(app)
    migrate = Migrate(app, db)

    # Blueprint'leri kaydet
    app.register_blueprint(project_routes, url_prefix='/project/')
    app.register_blueprint(task_routes, url_prefix='/task')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)