import os
import flask
from flask import current_app,Flask
# from flask import flask, current_app
import arhamcollection_app.config as Config


from .common import constants as COMMON_CONSTANTS

from .main_app.views import main_app as ma
from .user_management.views import user_management as um
from .user_management.models import User

from .main_app.errorhandling import *
from arhamcollection_app.extensions import db,principal,login_manager,mail,csrf


__all__ = ['create_app']


DEFAULT_BLUEPRINTS = [
    ma,um
]

def create_app(config=None, app_name=None,blueprints=None):
    if app_name is None:
        app_name=Config.DevelopmentConfig.PROJECT
    if blueprints is None:
        blueprints=DEFAULT_BLUEPRINTS
    app = Flask(app_name, instance_path=COMMON_CONSTANTS.INSTANCE_FOLDER_PATH, instance_relative_config=True)
    configure_app(app, config=None)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    app.register_error_handler(404,page_not_found_404)
    app.register_error_handler(403,page_not_found_403)
    app.register_error_handler(500,page_not_found_500)
    return app


def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)



def configure_extensions(app):
    #   pass
    print('INITIALIZING APP DATABASE')
    db.init_app(app)

    mail.init_app(app)
    principal.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    # celery.init_app(app)
    login_manager.login_view = "user_management.login"


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def configure_app(app, config=None):

    app.config.from_object(Config.DevelopmentConfig)
    
    if config:
        app.config.from_object(config)
    return

    # application_mode = os.getenv('APPLICATION_MODE', 'LOCAL')
    # app.config.from_object(Config.get_config(application_mode))
