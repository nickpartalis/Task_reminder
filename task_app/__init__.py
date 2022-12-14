from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from task_app.config import Config
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from task_app.users.routes import users
    from task_app.tasks.routes import tasks
    from task_app.main.routes import main
    from task_app.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(tasks)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
