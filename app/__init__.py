import os
from flask import Flask, redirect, Blueprint
from pymongo import MongoClient
from pymongo.server_api import ServerApi


class AppVariable():
    def __init__(self):
        self._app = Flask(__name__, instance_relative_config=True)
        self._uri = "mongodb+srv://datlemindast:Minhdat060501@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority"
        self._client = MongoClient(self._uri, server_api=ServerApi('1'))
    
application = AppVariable()

def create_app(test_config=None):
    from .auth.routes import my_blueprint
    # create and configure the app
    application._app.register_blueprint(my_blueprint)
    application._app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(application._app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        application._app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        application._app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(application._app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @application._app.route('/')
    def main():
        return redirect('/login/')

    return application._app