from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_simplemde import SimpleMDE
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES

from config import config_options

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
photos = UploadSet('photos', IMAGES)
mail = Mail()
simple = SimpleMDE()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # get config in instance folder
    app.config.from_pyfile('config.py')

    # initialize SQLAlchemy
    db.init_app(app)

    # initialize flask-migrate
    migrate.init_app(app, db)

    # Initialize flask-login
    login_manager.init_app(app)

    # Initialize flask-uploads
    configure_uploads(app, photos)

    # initialize flask-mail
    mail.init_app(app)

    # Initialize flask-simplemde
    simple.init_app(app)

    # Initializing flask extensions
    bootstrap.init_app(app)

    # Will add the views and forms

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    # setting config
    from .request import configure_request
    configure_request(app)

    return app
