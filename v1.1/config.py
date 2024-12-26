import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:akg@localhost:5432/todolist_deneme3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'akg')