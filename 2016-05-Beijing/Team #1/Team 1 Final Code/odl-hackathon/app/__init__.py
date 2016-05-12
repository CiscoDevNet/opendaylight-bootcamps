import json

from flask import Flask, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def ajax_dialog_view(tmp, **context):
    return json.dumps({'type': 'dialog', 'data': {'html': render_template(tmp, **context)}})


def ajax_refresh():
    return json.dumps({'type': 'refresh', 'data': ''})


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    from .topology import topology
    app.register_blueprint(topology, url_prefix='/topology')
    from .account import account
    app.register_blueprint(account, url_prefix='/account')

    @app.route('/')
    def index():
        return redirect(url_for('topology.index'))

    return app
