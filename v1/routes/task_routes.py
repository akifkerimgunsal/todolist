from flask import request, jsonify
from models.task import Task
from models.project import Project
from models import db
from routes import task_routes

@task_routes.route('/<int:project_id>/', methods=['POST'])
def add_task_to_project(project_id):
    project = Project.query.get(project_id)

    if not project:
        return jsonify({"error": "Project not found!"}), 404

    data = request.get_json()
    task_name = data.get('task')
    status = data.get('status', 'Başlanmadı')

    if not task_name:
        return jsonify({"error": "Task name is required!"}), 400

    if status not in ["Başlanmadı", "Yapılmakta", "Tamamlandı"]:
        return jsonify({"error": "Invalid status value!"}), 400

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
def get_tasks_by_project(project_id):
    project = Project.query.get(project_id)

    if not project:
        return jsonify({"error": "Task not found!"}), 404

    tasks = [{
        "id": task.id,
        "task": task.task,
        "status": task.status
    } for task in project.tasks]

    return jsonify(tasks), 200

@task_routes.route('/<int:task_id>/', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found!"}), 404

    data = request.get_json()
    task.task = data.get('task', task.task)
    status = data.get('status', task.status)

    if status not in ["Başlanmadı", "Yapılmakta", "Tamamlandı"]:
        return jsonify({"error": "Invalid status value!"}), 400

    task.status = status
    db.session.commit()

    return jsonify({"message": "Task updated successfully!", "task": {
        "id": task.id,
        "task": task.task,
        "status": task.status
    }}), 200

@task_routes.route('/<int:task_id>/', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found!"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully!"}), 200
