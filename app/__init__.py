from flask import Flask

from app.helpers import send_log_in_mail, save_log_in_file
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

if not app.debug:
    if app.config['MAIL_SERVER']:
        # send_log_in_mail()    # make sure mail server is functioning (dummy or real one).
        save_log_in_file()

from app import routes, models, errors
