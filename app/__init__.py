import os
from flask import Flask, Blueprint, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import g, session


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # create and configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config.from_pyfile("config.py")
    from .auth.routes import auth_blueprint
    from .blog.routes import home_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(home_blueprint)
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




