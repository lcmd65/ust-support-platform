import os
from flask import Flask, redirect, Blueprint, render_template

class AppVariable():
    def __init__(self):
        self._app = Flask(__name__, instance_relative_config=True)
        self._uri = "mongodb+srv://datlemindast:Minhdat060501@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority"
        self._client = None
        self._user = None
        
application = AppVariable()

def create_app(test_config=None):
    from .auth.routes import auth_blueprint
    from .blog.routes import home_blueprint
    # create and configure the app
    application._app.register_blueprint(auth_blueprint)
    application._app.register_blueprint(home_blueprint)
    application._app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(application._app.instance_path, 'flaskr.sqlite'),
    )
    application._app.config.from_pyfile("config.py")
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

    # a base page
    @application._app.route('/')
    def main():
        return render_template("base.html")
    
    @application._app.route('/nohcel')
    def nohcel():
        return render_template("base.html")

    return application._app