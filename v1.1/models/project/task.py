from models import db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default="Başlanmadı")
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
