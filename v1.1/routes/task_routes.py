from flask import Blueprint, request, jsonify
from models.project.task import Task
from models.project.project import Project
from models import db
from flask_jwt_extended import jwt_required, get_jwt_identity

task_routes = Blueprint('task_routes', __name__)

@task_routes.route('/<int:project_id>/', methods=['POST'])
@jwt_required()
def add_task_to_project(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()

    if not project:
        return jsonify({"error": "Project not found or you do not have access!"}), 404

    data = request.get_json()
    task_name = data.get('task')
    status = data.get('status', 'Başlanmadı')

    if not task_name:
        return jsonify({"error": "Task name is required!"}), 400

    new_task = Task(task=task_name, status=status, project_id=project.id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task added successfully!", "task": {
        "id": new_task.id,
        "task": new_task.task,
        "status": new_task.status,
        "project_id": new_task.project_id
    }}), 201

@task_routes.route('/<int:project_id>/', methods=['GET'])
@jwt_required()
def get_tasks_by_project(project_id):
    user_id = int(get_jwt_identity()) 
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()

    if not project:
        return jsonify({"error": "Project not found or you do not have access!"}), 404

    tasks = [{
        "id": task.id,
        "task": task.task,
        "status": task.status
    } for task in project.tasks]

    return jsonify(tasks), 200

@task_routes.route('/<int:task_id>/', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())
    task = Task.query.join(Project).filter(Task.id == task_id, Project.user_id == user_id).first()

    if not task:
        return jsonify({"error": "Task not found or you do not have access!"}), 404

    data = request.get_json()
    task.task = data.get('task', task.task)
    task.status = data.get('status', task.status)

    db.session.commit()

    return jsonify({"message": "Task updated successfully!", "task": {
        "id": task.id,
        "task": task.task,
        "status": task.status
    }}), 200

@task_routes.route('/<int:task_id>/', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())
    task = Task.query.join(Project).filter(Task.id == task_id, Project.user_id == user_id).first()

    if not task:
        return jsonify({"error": "Task not found or you do not have access!"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully!"}), 200
