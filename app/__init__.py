import os
import cache
import json
import pickle
import ssl
from flask import Flask, Blueprint, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import g, session
from flask_caching import Cache
from .db import DB


class AppVariable():
    def __init__(self):
        self._uri = "mongodb+srv://datlemindast:Minhdat060501@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority"
        self._client = None
        self._user = None

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # create and configure the app
    app.config.from_mapping(
        SECRET_KEY='dev1911007',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        CACHE_TYPE = 'FileSystemCache',
        CACHE_DIR = 'cache',
        CACHE_THRESHOLD = 100000,
    )
    app.config.from_pyfile("config.py")
    from .auth.routes import auth_blueprint
    from .blog.routes import home_blueprint
    from .api.user_api import api_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(api_blueprint)
    cache.cache.init_app(app)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a base page
    @app.route('/')
    def main():
        return render_template("base.html")
    @app.route('/nohcel')
    def nohcel():
        return render_template("base.html")
    
    return app




