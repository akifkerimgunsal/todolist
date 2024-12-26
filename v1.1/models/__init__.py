from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.auth.user import User
from models.project.project import Project
from models.project.task import Task
