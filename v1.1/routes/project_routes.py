from flask import Blueprint, request, jsonify
from models.project.project import Project
from models.auth.user import User
from models import db
from flask_jwt_extended import jwt_required, get_jwt_identity

project_routes = Blueprint('project_routes', __name__)

@project_routes.route('/', methods=['POST'])
@jwt_required()
def add_project():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    user_id = int(get_jwt_identity()) 

    if not name:
        return jsonify({"error": "Project name is required!"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found!"}), 404

    new_project = Project(name=name, description=description, user_id=user_id)
    db.session.add(new_project)
    db.session.commit()

    return jsonify({"message": "Project added successfully!", "project": {
        "id": new_project.id,
        "name": new_project.name,
        "description": new_project.description,
        "user_id": new_project.user_id
    }}), 201

@project_routes.route('/', methods=['GET'])
@jwt_required()
def get_projects():
    user_id = int(get_jwt_identity())
    projects = Project.query.filter_by(user_id=user_id).all()
    result = [{
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "user_id": project.user_id,
        "tasks": [{"id": task.id, "task": task.task, "status": task.status} for task in project.tasks]
    } for project in projects]

    return jsonify(result), 200

@project_routes.route('/<int:project_id>/', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()

    if not project:
        return jsonify({"error": "Project not found!"}), 404

    data = request.get_json()
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)

    db.session.commit()

    return jsonify({"message": "Project updated successfully!", "project": {
        "id": project.id,
        "name": project.name,
        "description": project.description
    }}), 200

@project_routes.route('/<int:project_id>/', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    user_id = int(get_jwt_identity()) 
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()

    if not project:
        return jsonify({"error": "Project not found!"}), 404

    db.session.delete(project)
    db.session.commit()

    return jsonify({"message": "Project and its tasks deleted successfully!"}), 200