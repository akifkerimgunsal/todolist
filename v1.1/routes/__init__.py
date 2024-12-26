from flask import Blueprint
from routes.auth_routes import auth_routes
from routes.project_routes import project_routes
from routes.task_routes import task_routes

def register_blueprints(app):
    app.register_blueprint(auth_routes, url_prefix='/api/auth')
    app.register_blueprint(project_routes, url_prefix='/api/projects')
    app.register_blueprint(task_routes, url_prefix='/api/tasks')
