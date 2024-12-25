from flask import Blueprint, request, jsonify
from models.project import Project
from models import db

project_routes = Blueprint('project_routes', __name__)

@project_routes.route('/', methods=['POST'])
def add_project():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')

    if not name:
        return jsonify({"error": "Project name is required!"}), 400

    new_project = Project(name=name, description=description)
    db.session.add(new_project)
    db.session.commit()

    return jsonify({"message": "Project added successfully!", "project": {
        "id": new_project.id,
        "name": new_project.name,
        "description": new_project.description
    }}), 201

# Diğer rotalar değişmeden kalabilir


@project_routes.route('/', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    result = [{
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "tasks": [{"id": task.id, "task": task.task, "status": task.status} for task in project.tasks]
    } for project in projects]

    return jsonify(result), 200

@project_routes.route('/<int:project_id>/', methods=['PUT'])
def update_project(project_id):
    project = Project.query.get(project_id)

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
def delete_project(project_id):
    project = Project.query.get(project_id)

    if not project:
        return jsonify({"error": "Project not found!"}), 404

    # İlgili görevleri de sil
    for task in project.tasks:
        db.session.delete(task)

    db.session.delete(project)
    db.session.commit()

    return jsonify({"message": "Project deleted successfully!"}), 200
