from flask import Flask
from .exts import db,fa
from .config import DevConfig
from .models import Task
from .api import resources
from .ui import ui

import os

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

SECRET_KEY='not a secret'
SQLALCHEMY_TRACK_MODIFICATIONS=False

SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(BASE_DIR,'tasks.db')
DEBUG=True
TESTING=True

def create_app():
    app=Flask(__name__)

    app.config.from_object(__name__)

    db.init_app(app)
    fa.init_app(app)

    app.register_blueprint(resources,url_prefix='/api')
    app.register_blueprint(ui,url_prefix='/')

    @app.shell_context_processor
    def make_shell_context():
        return {
            'app':app,
            'db':db,
            'Task':Task
        }

    return app