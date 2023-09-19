import os
from flask import Flask, redirect, Blueprint
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def create_app(test_config=None):
    from .auth.routes import my_blueprint
    # create and configure the app
    uri = "mongodb+srv://datlemindast:Minhdat060501@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(my_blueprint)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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

    # a simple page that says hello
    @app.route('/')
    def main():
        return redirect('/login/')

    return app