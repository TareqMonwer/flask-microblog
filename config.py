import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'bgsasfd$@adsfasf')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(BASE_DIR, 'mirco_blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
